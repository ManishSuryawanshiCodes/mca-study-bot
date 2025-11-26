import streamlit as st
from src.llm_groq import GroqLLM
from src.config import Config
from qdrant_client import QdrantClient

def llm_status_page():

    st.markdown("""
        <div class="chat-header">
            <div class="chat-header-title">🧠 LLM & System Status</div>
            <div class="chat-header-subtitle">Check if everything is running correctly</div>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("🔍 Groq LLM Status")

    llm = GroqLLM()
    status = llm.get_status()

    if status["connected"]:
        st.success(f"🟢 Connected to Groq — Model: {status['model']}")
    else:
        st.error("🔴 Groq LLM Not Connected")

    st.markdown("### 🔑 API Keys")
    st.code(f"""
GROQ_API_KEY: {"✔ Loaded" if Config.GROQ_API_KEY else "❌ Missing"}
QDRANT_API_KEY: {"✔ Loaded" if Config.QDRANT_API_KEY else "❌ Missing"}
GOOGLE_API_KEY: {"✔ Loaded" if Config.GOOGLE_API_KEY else "❌ Missing"}
""")

    st.markdown("### 🗂 Qdrant Status")
    if Config.USE_QDRANT:
        try:
            client = QdrantClient(url=Config.QDRANT_URL, api_key=Config.QDRANT_API_KEY)
            collections = client.get_collections()
            st.success(f"🟢 Connected to Qdrant ({len(collections.collections)} collections)")
        except Exception as e:
            st.error(f"🔴 Qdrant Error: {str(e)}")
    else:
        st.info("ℹ Qdrant disabled. Using ChromaDB.")

    st.markdown("### 🧪 Test Groq LLM")

    query = st.text_input("Enter test prompt:", "Define polymorphism in Java.")
    if st.button("Run Test"):
        response = llm.generate_answer(query, [], [])
        st.write("### Output:")
        st.success(response["answer"])

    st.markdown("### ⚙ System Info")
    st.code(f"""
Model Selected: {Config.LLM_MODEL}
Embedding Model: {Config.EMBEDDING_MODEL}
Chunk Size: {Config.CHUNK_SIZE}
Top K Results: {Config.TOP_K_RESULTS}
""")
