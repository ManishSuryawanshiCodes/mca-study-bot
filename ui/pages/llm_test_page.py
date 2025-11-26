import streamlit as st
from src.llm_groq import GroqLLM
from qdrant_client import QdrantClient

# FIXED — missing import
from src.config import Config

def llm_test_page():

    st.header("🧪 LLM Test (Admin Only)")

    if "llm_test_auth" not in st.session_state:
        st.session_state["llm_test_auth"] = False

    if not st.session_state["llm_test_auth"]:
        pwd = st.text_input("Enter Admin Password:", type="password")
        if st.button("Login"):
            if pwd == Config.ADMIN_PASSWORD:
                st.session_state["llm_test_auth"] = True
                st.success("Access granted!")
                st.rerun()
            else:
                st.error("Wrong password")
        return


    st.markdown("""
        <div class="chat-header">
            <div class="chat-header-title">🧪 LLM Test Console</div>
            <div class="chat-header-subtitle">
                Verify Groq LLM connectivity, speed & output quality.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.info("This page helps you test the LLM independent of chat history or vector DB.")

    st.subheader("🔍 Connection Status")
    llm = GroqLLM()
    status = llm.get_status()

    if status["connected"]:
        st.success(f"🟢 Connected to Groq ({status['model']})")
    else:
        st.error("🔴 NOT Connected")

    st.divider()
    st.subheader("🧠 Run a Test Prompt")

    test_input = st.text_input("Enter prompt", "Explain polymorphism in Java with an example.")

    if st.button("Run Test", use_container_width=True):
        with st.spinner("Generating response..."):
            response = llm.generate_answer(test_input, [], [])

        if response["status"] == "success":
            st.success("Response received!")
            st.markdown("---")
            st.markdown("### 🧠 Output")
            st.write(response["answer"])
        else:
            st.error("LLM Error")
            st.write(response["answer"])

    st.divider()
    st.markdown("### ⚙ Model Info")
    st.code(f"""
Model: {status['model']}
Provider: Groq
Connected: {status['connected']}
    """)
