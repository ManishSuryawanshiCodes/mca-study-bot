"""
Groq LLM Interface (Final Working Version for 2025)
Supports ONLY the working Groq model:
➡ llama-3.1-8b-instant
"""

import time
import streamlit as st
from typing import List, Dict, Optional
from groq import Groq
from src.config import Config


class GroqLLM:
    """Production-grade interface for Groq's Llama 3.1 8B Instant model."""

    VALID_MODEL = "llama-3.1-8b-instant"   # Only working model confirmed by TEST_LLM.py

    def __init__(self, model: str = None):
        """Initialize Groq LLM"""

        if not Config.GROQ_API_KEY:
            self.connection_status = False
            raise RuntimeError("❌ GROQ_API_KEY is missing in .env")

        # Create Groq Client
        self.client = Groq(api_key=Config.GROQ_API_KEY)

        # Determine selected model
        ui_model = st.session_state.get("selected_model")
        env_model = Config.LLM_MODEL

        self.model = model or ui_model or env_model or self.VALID_MODEL

        # Validate: force to working model
        if self.model != self.VALID_MODEL:
            print(f"⚠️ Invalid or unsupported model: {self.model}. Using: {self.VALID_MODEL}")
            self.model = self.VALID_MODEL

        # Connection test
        self.connection_status = self._verify_connection()

        if self.connection_status:
            print(f"🟢 Groq connected (model: {self.model})")
        else:
            print(f"🔴 Groq connection failed (model: {self.model})")

    def _verify_connection(self) -> bool:
        """Verify connection with a cheap ping test."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=3,
            )
            # Corrected for new Groq API
            _ = response.choices[0].message.content
            return True

        except Exception as e:
            print(f"Groq connection error: {str(e)[:120]}")
            return False

    def generate_answer(
        self,
        query: str,
        documents: Optional[List[Dict]] = None,
        history: Optional[List[Dict]] = None
    ) -> Dict:
        """Generate answer from Groq model."""

        # Build context
        context = ""
        sources = []

        if documents:
            for i, doc in enumerate(documents[:3], 1):
                text = doc.get("text", "")[:600]
                meta = doc.get("metadata", {})
                context += f"\n[Document {i}]\n{text}\n"
                sources.append({
                    "document": meta.get("source", "Unknown"),
                    "subject": meta.get("subject", "General"),
                    "page": meta.get("page", "N/A")
                })

        # Prepare conversation history
        chat_history = []
        if history:
            for h in history[-2:]:
                chat_history.append({"role": "user", "content": h.get("user", "")})
                chat_history.append({"role": "assistant", "content": h.get("assistant", "")})

        # System instructions
        system_prompt = """
You are an MCA Study Assistant.
- Use provided context FIRST.
- If context does not contain the answer, say:
  "Not found in notes, here is general guidance:"
- Keep answers under 250 words.
- Use simple Indian-English explanations.
- For technical content, use examples.
"""

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]

        if context:
            messages.append({"role": "user", "content": f"Context:\n{context}"})
            messages.append({
                "role": "assistant",
                "content": "Context received. I will use it to answer your question."
            })

        messages.extend(chat_history)
        messages.append({"role": "user", "content": query})

        # Retry logic
        for attempt in range(2):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=500,
                    temperature=0.3,
                )

                # FINAL FIX: Correct attribute access for Groq SDK ≥ v0.36.0
                answer = response.choices[0].message.content

                return {
                    "answer": answer,
                    "sources": sources,
                    "model": self.model,
                    "status": "success",
                }

            except Exception as e:
                print(f"Attempt {attempt+1}: {str(e)}")
                time.sleep(1)

        # Final failure
        return {
            "answer": "⚠️ LLM Error — Try again later.",
            "sources": [],
            "model": self.model,
            "status": "error",
        }

    def get_status(self) -> Dict:
        """LLM connection status for Settings + Status Page."""
        return {
            "connected": self.connection_status,
            "model": self.model,
            "provider": "Groq",
            "status": "🟢 Connected" if self.connection_status else "🔴 Disconnected",
        }
