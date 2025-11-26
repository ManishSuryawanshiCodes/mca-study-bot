import streamlit as st
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from src.config import Config
from src.stats_manager import StatsManager
import os

def upload_page():
    """Upload materials with password protection, stats, doc table, and delete"""

    st.markdown("""
    <div class="chat-header">
        <div class="chat-header-title">📁 Upload Study Materials</div>
        <div class="chat-header-subtitle">Add notes, assignments, and question papers</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Password authentication
    if "upload_auth" not in st.session_state:
        st.session_state["upload_auth"] = False

    if not st.session_state["upload_auth"]:
        st.markdown("""
        <div style='background: rgba(99,102,241,0.1); border: 2px solid rgba(99,102,241,0.3); 
                    border-radius: 12px; padding: 24px; text-align: center;'>
            <div style='font-size: 32px; margin-bottom: 12px;'>🔐</div>
            <h2 style='color: #e6edf3; margin: 0 0 8px 0;'>Admin Access Required</h2>
            <p style='color: #8b949e; margin: 0 0 24px 0;'>Upload Study Materials</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            password = st.text_input(
                "Enter Admin Password",
                type="password",
                placeholder="••••••••",
                help="Enter the admin password to access this feature"
            )
            
            if st.button("🔓 Unlock", use_container_width=True, type="primary"):
                if password == Config.ADMIN_PASSWORD:
                    st.session_state["upload_auth"] = True
                    st.success("✅ Access granted!")
                    st.rerun()
                else:
                    st.error("❌ Incorrect password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.info("""
            💡 **Note:** This section is password-protected.
            Only admins with the correct password can upload materials.
            """)
        return

    st.success("✅ Admin access granted!")
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        st.session_state["upload_auth"] = False
        st.success("✅ Logged out!")
        st.rerun()

    st.divider()

    # --- Uploaded Document Table with Delete ---
        # --- Uploaded Document Table with Delete (pretty table style) ---
    try:
        vs = VectorStore(use_qdrant=Config.USE_QDRANT)
        doc_rows = vs.get_uploaded_documents(limit=1000)
        st.markdown("## 📚 Uploaded Documents Overview")
        deleted = False

        if doc_rows:
            st.write(
                """
                <style>
                .doc-table th, .doc-table td {padding: 8px 16px;}
                </style>
                """,
                unsafe_allow_html=True
            )
            # Show header row
            cols = st.columns([3, 2, 2, 2, 1])
            cols[0].markdown("**File Name**")
            cols[1].markdown("**Subject**")
            cols[2].markdown("**Year**")
            cols[3].markdown("**Type**")
            cols[4].markdown("**Delete**")
            for idx, row in enumerate(doc_rows):
                cols = st.columns([3, 2, 2, 2, 1])
                cols[0].write(row['source'])
                cols[1].write(row['subject'])
                cols[2].write(row['year'])
                cols[3].write(row['type'])
                with cols[4]:
                    if st.button("🗑️", key=f"delete_{idx}"):
                        success = vs.delete_document_by_metadata(
                            row['source'], row['subject'], row['year'], row['type']
                        )
                        if success:
                            st.success(f"Deleted: {row['source']} ({row['subject']})", icon="🗑️")
                            deleted = True
                        else:
                            st.error(f"Failed to delete: {row['source']}", icon="⚠️")
            if deleted:
                st.rerun()
            st.caption(f"{len(doc_rows)} documents listed.")
        else:
            st.info("No documents uploaded yet.")
    except Exception as e:
        st.error(f"Unable to show uploaded documents: {e}")


    # === STATS + UPLOAD LOGIC ===
    try:
        dp = DocumentProcessor()
        current_stats = vs.get_document_stats_by_type()
    except Exception as e:
        st.error(f"❌ System initialization error: {str(e)}")
        return

    st.markdown("### 📊 Current Database Statistics")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📝 Notes", current_stats.get('notes', 0))
    with col2:
        st.metric("📋 Assignments", current_stats.get('assignments', 0))
    with col3:
        st.metric("📄 Question Papers", current_stats.get('question_papers', 0))
    with col4:
        st.metric("📖 Textbooks", current_stats.get('textbooks', 0))
    with col5:
        st.metric("📑 Syllabus", current_stats.get('syllabus', 0))

    st.divider()

    st.markdown("### 📤 Upload New Documents")
    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload one or more PDF files"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        doc_type = st.selectbox(
            "Document Type",
            ["notes", "assignments", "question_papers", "textbooks", "syllabus"],
            format_func=lambda x: {
                "notes": "📝 Notes",
                "assignments": "📋 Assignments",
                "question_papers": "📄 Question Papers",
                "textbooks": "📖 Textbooks",
                "syllabus": "📑 Syllabus"
            }[x]
        )
        subject = st.selectbox("Subject", Config.SUBJECTS)
        year = st.selectbox("Year", Config.YEARS)

    st.markdown("<br>", unsafe_allow_html=True)

    if uploaded_files:
        st.info(f"📁 {len(uploaded_files)} file(s) selected")

        if st.button("🚀 Process & Upload Documents", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            total_files = len(uploaded_files)
            successful_uploads = 0
            total_chunks = 0

            for idx, uploaded_file in enumerate(uploaded_files):
                try:
                    progress = (idx / total_files)
                    progress_bar.progress(progress)
                    status_text.text(f"Processing {uploaded_file.name}... ({idx + 1}/{total_files})")
                    file_path = f"temp_{uploaded_file.name}"
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    chunks = dp.process_pdf(
                        file_path,
                        doc_type=doc_type,
                        subject=subject,
                        year=year
                    )
                    if chunks:
                        result = vs.add_documents(chunks)
                        if result['status'] == 'success':
                            successful_uploads += 1
                            total_chunks += len(chunks)
                            st.success(f"✅ {uploaded_file.name}: {len(chunks)} chunks added")
                        else:
                            st.error(f"❌ {uploaded_file.name}: {result['message']}")
                    else:
                        st.warning(f"⚠️ {uploaded_file.name}: No content extracted")
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")

            progress_bar.progress(1.0)
            status_text.text("✓ Upload complete!")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📈 Upload Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Files Uploaded", f"{successful_uploads}/{total_files}")
            with col2:
                st.metric("Total Chunks", total_chunks)
            with col3:
                st.metric("Status", "✓ Complete" if successful_uploads == total_files else "⚠️ Partial")

            StatsManager.update_documents(successful_uploads, total_chunks)
            st.success("🎉 Documents processed successfully! Students can now ask questions about these materials.")

            st.rerun()
    else:
        st.info("👆 Select PDF files to upload")

    st.divider()

    st.markdown("""
    <div class="glass-surface" style='padding: 20px;'>
        <h4 style='color: #ffffff; margin: 0 0 16px 0;'>📋 Upload Guidelines</h4>
        <div style='font-size: 13px; color: #8b949e; line-height: 1.8;'>
            <div style='margin-bottom: 8px;'>✓ Upload PDF files only</div>
            <div style='margin-bottom: 8px;'>✓ Select correct document type for better organization</div>
            <div style='margin-bottom: 8px;'>✓ Choose appropriate subject and year</div>
            <div style='margin-bottom: 8px;'>✓ Files are automatically processed and indexed</div>
            <div style='margin-bottom: 8px;'>✓ Maximum file size: 200 MB per file</div>
            <div>✓ Students can search uploaded materials in Chat section</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
