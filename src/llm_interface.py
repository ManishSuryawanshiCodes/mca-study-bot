"""
LLM Interface Module
Handles interaction with Google Gemini API
"""

import google.generativeai as genai
from src.config import Config
from typing import List, Dict, Optional
import time
import streamlit as st


class LLMInterface:
    """Interface for Google Gemini LLM"""

    def __init__(self):
        """Initialize Gemini API"""
        try:
            if not Config.GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY not set in .env file")

            genai.configure(api_key=Config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(Config.LLM_MODEL)
            self.connection_status = self._verify_connection()
            self.rate_limit_reset_time = 0

            if not self.connection_status:
                print(f"⚠️ Warning: LLM connection verification failed")
                # Don't raise error, allow fallback
                self.connection_status = False

        except Exception as e:
            self.connection_status = False
            print(f"Error initializing LLM: {str(e)}")
            raise RuntimeError(f"Failed to initialize LLM: {str(e)}")

    def _verify_connection(self) -> bool:
        """Verify connection to Gemini API"""
        try:
            test_response = self.model.generate_content("Hello")
            return test_response is not None and test_response.text
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                print(f"⚠️ Rate limit hit: {str(e)}")
                return False
            print(f"Connection verification failed: {str(e)}")
            return False

    def _wait_for_rate_limit(self):
        """Wait if rate limited"""
        if time.time() < self.rate_limit_reset_time:
            wait_time = self.rate_limit_reset_time - time.time()
            if wait_time > 0:
                print(f"Rate limit: waiting {wait_time:.1f}s...")
                time.sleep(min(wait_time + 1, 30))  # Cap at 30s
                self.rate_limit_reset_time = 0

    def generate_answer(
        self,
        query: str,
        documents: Optional[List[Dict]] = None,
        history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Generate answer using Gemini with RAG

        Args:
            query: User query
            documents: Retrieved documents from vector store
            history: Conversation history

        Returns:
            Dict with 'answer' and 'sources' keys
        """
        try:
            # Check rate limit
            self._wait_for_rate_limit()

            # Build context from documents
            context = ""
            sources = []

            if documents:
                for idx, doc in enumerate(documents[:3]):  # Limit to top 3
                    if isinstance(doc, dict):
                        text = doc.get('text', '')[:500]  # Limit text size
                        metadata = doc.get('metadata', {})
                        context += f"\n[Document {idx+1}]\n{text}\n"
                        sources.append({
                            "document": metadata.get('source', 'Unknown'),
                            "pages": metadata.get('page', 'N/A'),
                            "subject": metadata.get('subject', 'General'),
                            "type": metadata.get('type', 'General')
                        })

            # Build conversation history (limit to last 2 exchanges)
            chat_history = ""
            if history:
                for h in history[-2:]:
                    user_q = h.get('user', '')[:200]
                    asst_a = h.get('assistant', '')[:200]
                    chat_history += f"\nQ: {user_q}\nA: {asst_a}\n"

            # Create optimized prompt
            prompt = f"""Answer this question based on the provided context.
Keep your answer concise and clear. Maximum 150 words.

CONTEXT:
{context if context else 'No specific documents. Use your knowledge.'}

PREVIOUS:
{chat_history if chat_history else 'First question'}

QUESTION:
{query}

ANSWER:"""

            # Generate response with timeout
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=200,
                        temperature=0.7
                    )
                )

                if not response or not response.text:
                    raise ValueError("Empty response from Gemini API")

                return {
                    "answer": response.text,
                    "sources": sources,
                    "model": Config.LLM_MODEL,
                    "status": "success"
                }

            except Exception as e:
                error_str = str(e)

                # Handle rate limiting
                if "429" in error_str or "quota" in error_str.lower():
                    self.rate_limit_reset_time = time.time() + 30
                    return {
                        "answer": "⏱️ Rate limit reached. Please wait a moment and try again. You've used the free tier limit for this model.",
                        "sources": [],
                        "model": Config.LLM_MODEL,
                        "status": "rate_limited"
                    }

                raise e

        except Exception as e:
            return {
                "answer": f"Error generating answer: {str(e)}",
                "sources": [],
                "model": Config.LLM_MODEL,
                "status": "error"
            }

    def get_status(self) -> Dict:
        """Get LLM connection status"""
        status_text = "🟢 Connected" if self.connection_status else "⚠️ Limited"

        return {
            "connected": self.connection_status,
            "model": Config.LLM_MODEL,
            "api_key_set": bool(Config.GOOGLE_API_KEY),
            "status": status_text
        }
