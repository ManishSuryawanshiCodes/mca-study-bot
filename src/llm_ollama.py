"""
Ollama LLM Interface - Free unlimited LLM
For production: https://ollama.ai
"""
import requests
from typing import List, Dict, Optional
import json

class OllamaLLM:
    """Interface for Ollama LLM (Self-hosted or Remote)"""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral"):
        """
        Initialize Ollama LLM
        
        Args:
            base_url: Ollama server URL
            model: Model name (mistral, llama2, neural-chat, etc.)
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.connection_status = self._verify_connection()

    def _verify_connection(self) -> bool:
        """Verify connection to Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Ollama connection error: {str(e)}")
            return False

    def generate_answer(
        self,
        query: str,
        documents: Optional[List[Dict]] = None,
        history: Optional[List[Dict]] = None
    ) -> Dict:
        """Generate answer using Ollama"""
        try:
            if not self.connection_status:
                return self._fallback_answer(query, documents)

            # Build context
            context = ""
            sources = []
            
            if documents:
                for idx, doc in enumerate(documents[:3]):
                    if isinstance(doc, dict):
                        text = doc.get('text', '')[:300]
                        metadata = doc.get('metadata', {})
                        context += f"\n[Ref {idx+1}] {text}"
                        sources.append({
                            "document": metadata.get('source', 'Unknown'),
                            "subject": metadata.get('subject', 'General')
                        })

            # Build prompt
            prompt = f"""Answer the question based on context.
Keep it under 200 words.

Context:
{context if context else 'General knowledge'}

Question: {query}

Answer:"""

            # Call Ollama
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=60
            )

            if response.status_code == 200:
                answer = response.json().get('response', 'No response')
                return {
                    "answer": answer,
                    "sources": sources,
                    "model": f"Ollama/{self.model}",
                    "status": "success"
                }
            else:
                return self._fallback_answer(query, documents)

        except Exception as e:
            return self._fallback_answer(query, documents)

    def _fallback_answer(self, query: str, documents: Optional[List[Dict]]) -> Dict:
        """Fallback when Ollama is unavailable"""
        if documents:
            text = documents[0].get('text', '')[:400]
            return {
                "answer": f"📚 From documents:\n\n{text}...",
                "sources": [{"document": "Uploaded material"}],
                "model": "Fallback",
                "status": "offline"
            }
        return {
            "answer": "⚠️ LLM unavailable. Upload materials to search.",
            "sources": [],
            "model": "Fallback",
            "status": "offline"
        }

    def get_status(self) -> Dict:
        """Get Ollama status"""
        return {
            "connected": self.connection_status,
            "model": self.model,
            "status": "🟢 Connected" if self.connection_status else "⚠️ Offline"
        }