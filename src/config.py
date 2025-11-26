"""
Configuration Module
Centralized configuration for the MCA Study Assistant
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""

    # ----------------------------
    # API Keys
    # ----------------------------
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

    # ----------------------------
    # Qdrant Vector DB
    # ----------------------------
    USE_QDRANT = os.getenv("USE_QDRANT", "True").lower() == "true"
    QDRANT_URL = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "mca_documents")

    # ----------------------------
    # ChromaDB (fallback)
    # ----------------------------
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")

    # ----------------------------
    # Document Processing
    # ----------------------------
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))

    # ----------------------------
    # LLM Settings (Groq)
    # ----------------------------
    # The ONLY working Groq model based on TEST_LLM.py
    VALID_MODEL = "llama-3.1-8b-instant"

    # Default model — MUST be the working one
    LLM_MODEL = os.getenv("LLM_MODEL", VALID_MODEL)

    # Embeddings
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    # ----------------------------
    # Search Settings
    # ----------------------------
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))

    # ----------------------------
    # Rate Limiting
    # ----------------------------
    ENABLE_RATE_LIMITING = os.getenv("ENABLE_RATE_LIMITING", "True").lower() == "true"
    RATE_LIMIT_DELAY = int(os.getenv("RATE_LIMIT_DELAY", "1"))

    # -----------------
    # Document categories
    DOCUMENT_TYPES = {
        "notes": "📝 Class Notes",
        "assignments": "✏️ Assignments",
        "question_paper": "📋 Question Paper",
        "question_bank": "🏦 Question Bank",
        "textbook": "📚 Textbook",
        "syllabus": "📄 Syllabus"
    }

    # FIXED — you must add these back
    SUBJECTS = [
        "Programming Concepts",
        "Mathematical FOundation",
        "Database Management Systems",
        "Programming Paradigms",
        "Research Methodology",
        "Software Engineering",
        "Data Structures and Algorithms",
        "Core java",
        "Python for Data Science",
        "Web Development",
        "Software Testing",
        "Field Project"
        "Software Project Management",
        "Networking Concepts",
        "Advanced Java",
        "Data Mining",
        "MERN Stack",
        "Operating Systems",
        "Machine Learning",
        "User experience",
        "Syllabus"
    ]

    YEARS = ["Year 1", "Year 2"]

    # Admin login password
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "ADMin@manish")

