"""
Admin Panel - Upload and manage documents
"""
import streamlit as st
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from src.config import Config
import os
from datetime import datetime

def admin_page():
    """Admin panel with document categorization"""
    
    st.markdown("""
    <div class="chat-header">
        <div class="chat-header-title">📁 Upload Materials</div>
        <div class="chat-header-subtitle">Organize and manage your course documents</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Authentication
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        st.markdown("""
        <div class="glass-surface" style='padding: 40px; text-align: center;'>
            <div style='color: #ff6b6b; font-weight: 600; margin-bottom: 20px; font-size: 18px;'>
                🔒 Authentication Required
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            password = st.text_input(
                "Enter Admin Password:",
                type="password",
                label_visibility="collapsed",
                placeholder="Admin Password"
            )
            
            if st.button("🔓 Login", use_container_width=True):
                if password == Config.ADMIN_PASSWORD:
                    st.session_state.admin_authenticated = True
                    st.success("✅ Authenticated!")
                    st.rerun()
                else:
                    st.error("❌ Invalid password!")
        return
    
    # Logout button
    col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
    with col3:
        if st.button("🔐 Logout", use_container_width=True, key="logout"):
            st.session_state.admin_authenticated = False
            st.rerun()
    
    st.divider()
    
    # Upload form
    st.markdown("<h3 style='color: #ffffff; margin-bottom: 20px;'>📤 Upload Documents</h3>", unsafe_allow_html=True)
    
    # Create tabs for different upload types
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Class Notes",
        "✏️ Assignments",
        "📋 Question Papers",
        "🏦 Question Bank",
        "📚 Textbooks"
    ])
    
    with tab1:
        _upload_section("notes", "Class Notes")
    
    with tab2:
        _upload_section("assignments", "Assignments")
    
    with tab3:
        _upload_section("question_paper", "Question Papers")
    
    with tab4:
        _upload_section("question_bank", "Question Bank")
    
    with tab5:
        _upload_section("textbook", "Textbooks")
    
    st.divider()
    
    # Statistics
    st.markdown("<h3 style='color: #ffffff; margin-bottom: 20px;'>📊 Document Statistics</h3>", unsafe_allow_html=True)
    
    try:
        vector_store = VectorStore(use_qdrant=Config.USE_QDRANT)
        stats = vector_store.get_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Documents", stats.get("document_count", 0), "📄")
        
        with col2:
            st.metric("Total Chunks", stats.get("chunk_count", 0), "🔀")
        
        with col3:
            st.metric("Embeddings", stats.get("embedding_count", 0), "🧠")
        
        with col4:
            st.metric("Status", "✅ Active", "Online")
        
    except Exception as e:
        st.warning(f"⚠️ Could not load stats: {str(e)}")

def _upload_section(doc_type: str, section_title: str):
    """Create upload section for document type"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject = st.selectbox(
            "Select Subject",
            Config.SUBJECTS,
            key=f"subject_{doc_type}"
        )
    
    with col2:
        year = st.selectbox(
            "Select Year",
            Config.YEARS,
            key=f"year_{doc_type}"
        )
    
    # Additional metadata
    col1, col2 = st.columns(2)
    
    with col1:
        semester = st.number_input(
            "Semester (optional)",
            min_value=1,
            max_value=4,
            key=f"semester_{doc_type}",
            help="Leave as 1 if not applicable"
        )
    
    with col2:
        chapter = st.text_input(
            "Chapter/Unit (optional)",
            placeholder="e.g., Chapter 1: Introduction",
            key=f"chapter_{doc_type}"
        )
    
    # File upload
    uploaded_files = st.file_uploader(
        f"Select PDF files for {section_title}",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more PDF files",
        key=f"files_{doc_type}"
    )
    
    if uploaded_files:
        st.info(f"📌 {len(uploaded_files)} file(s) selected for upload")
        
        if st.button(f"📤 Upload & Process {section_title}", use_container_width=True, key=f"upload_{doc_type}"):
            progress_bar = st.progress(0)
            status_container = st.container()
            
            try:
                doc_processor = DocumentProcessor()
                vector_store = VectorStore(use_qdrant=Config.USE_QDRANT)
                
                total_files = len(uploaded_files)
                total_chunks = 0
                
                for file_idx, uploaded_file in enumerate(uploaded_files):
                    # Save temporarily
                    temp_path = f"./temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    with status_container.status(f"📄 Processing: {uploaded_file.name}", expanded=True) as status:
                        st.write(f"⏳ Extracting text...")
                        
                        # Process PDF
                        chunks = doc_processor.process_pdf(temp_path)
                        
                        st.write(f"✂️ Created {len(chunks)} chunks")
                        
                        # Add metadata
                        for chunk in chunks:
                            chunk["metadata"] = {
                                "source": uploaded_file.name,
                                "type": doc_type,
                                "subject": subject,
                                "year": year,
                                "semester": int(semester),
                                "chapter": chapter or "General",
                                "upload_date": datetime.now().isoformat()
                            }
                        
                        st.write(f"🧠 Generating embeddings...")
                        
                        # Add to vector store
                        vector_store.add_documents(chunks)
                        
                        st.write(f"✅ Successfully added to database!")
                        
                        total_chunks += len(chunks)
                        
                        # Clean up
                        os.remove(temp_path)
                    
                    # Update progress
                    progress = (file_idx + 1) / total_files
                    progress_bar.progress(progress)
                
                st.success(f"""
                ✅ **Upload Complete!**
                
                📊 Summary:
                - Files uploaded: {total_files}
                - Total chunks created: {total_chunks}
                - Subject: {subject}
                - Year: {year}
                - Document Type: {section_title}
                """)
                
            except Exception as e:
                st.error(f"❌ Error during upload: {str(e)}")
                progress_bar.empty()