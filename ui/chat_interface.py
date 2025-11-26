import streamlit as st
from src.vector_store import VectorStore
from src.document_processor import DocumentProcessor
from src.llm_interface import LLMInterface
from src.config import Config
from ui.components.message_bubble import render_message
import tempfile, os


@st.cache_resource
def init_system():
    return DocumentProcessor(), VectorStore(use_qdrant=Config.USE_QDRANT), LLMInterface()


def chat_view():
    st.header("Ask Your MCA Questions")
    doc_processor, vector_store, llm = init_system()


    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'history' not in st.session_state:
        st.session_state.history = []


    col1, col2, _ = st.columns([1,1,2])
    with col1:
        subj = st.selectbox("Subject", ["All","Data Structures","Algorithms","Java","Mathematics","Discrete Math","Database","General"])
    with col2:
        year = st.selectbox("Year", ["All","Year 1","Year 2"])


    for m in st.session_state.messages:
        render_message(m['role'], m['content'])
        if m.get('sources'):
            with st.expander("Sources"):
                for s in m['sources']:
                    st.markdown(f"**{s['document']}** pages: {s['pages']}")


    user_input = st.chat_input("Ask a question about your MCA materials...")
    if user_input:
        st.session_state.messages.append({'role':'user','content':user_input})


    filters = {}
    if subj != "All": filters['subject'] = subj
    if year != "All": filters['year'] = year


    with st.spinner("Retrieving context..."):
        st.experimental_rerun()