import streamlit as st
from src.config import Config
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore

def admin_view():
    """Admin panel - requires password authentication"""
    
    # Check if admin is logged in
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        st.warning("⚠️ Admin Area - Authentication Required")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            password = st.text_input("Enter Admin Password:", type="password")
            if st.button("Login"):
                if password == Config.ADMIN_PASSWORD:
                    st.session_state.admin_authenticated = True
                    st.success("✅ Authenticated!")
                    st.rerun()
                else:
                    st.error("❌ Wrong password!")
        return
    
    # Admin authenticated - show upload interface
    st.header("📁 Upload Course Materials")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.admin_authenticated = False
        st.rerun()
    
    dp = DocumentProcessor()
    vs = VectorStore(use_qdrant=Config.USE_QDRANT)

    col1, col2 = st.columns(2)
    with col1:
        doc_type = st.selectbox("Document Type", ["Note","Textbook","Syllabus","Assignment","Question Paper"])
        subject = st.selectbox("Subject", ["Data Structures","Algorithms","Java","Database","Mathematics","Discrete Math","Operating Systems","General"])
        year = st.selectbox("Year", ["Year 1","Year 2"])
    with col2:
        files = st.file_uploader("Upload PDFs", type=['pdf'], accept_multiple_files=True)

    if st.button("Process Documents"):
        if not files:
            st.warning("Upload at least one PDF.")
        else:
            for f in files:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                    tmp.write(f.getbuffer())
                    path = tmp.name
                try:
                    chunks = dp.process_pdf(path, doc_type.lower(), subject, year)
                    vs.add_documents(chunks)
                    st.success(f"Processed {f.name}")
                except Exception as e:
                    st.error(str(e))
                finally:
                    try:
                        os.remove(path)
                    except Exception:
                        pass

    st.markdown("---")
    stats = vs.get_stats()
    st.metric("Total Documents", stats.get('total_documents', 0))
    st.write("Database:", stats.get('database'))