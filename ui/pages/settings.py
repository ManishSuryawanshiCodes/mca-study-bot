"""
Settings Page - Clean and Functional
"""
import streamlit as st
from ui.components.theming import load_css

def settings_page():
    """Settings page with streamlined interface"""
    
    load_css()
    
    # Header
    st.markdown("""
    <div class="chat-header">
        <div class="chat-header-title">⚙️ Settings</div>
        <div class="chat-header-subtitle">Customize your study experience</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    # ============================================================
    # LEFT PANEL - Settings
    # ============================================================
    with col1:
        
        # Appearance Settings
        st.markdown("### 🎨 Appearance")
        
        theme = st.radio(
            "Theme",
            ["Dark (Current)", "Light", "Auto"],
            help="Choose your preferred color theme"
        )
        st.session_state["theme"] = theme
        
        auto_scroll = st.checkbox(
            "Auto-scroll to latest messages",
            value=True,
            help="Automatically scroll to new messages in chat"
        )
        st.session_state["auto_scroll"] = auto_scroll
        
        st.divider()
        
        # Chat Settings
        st.markdown("### 💬 Chat Settings")
        
        show_timestamps = st.checkbox(
            "Show message timestamps",
            value=True,
            help="Display time for each message"
        )
        
        show_sources = st.checkbox(
            "Show source documents",
            value=True,
            help="Display document references in answers"
        )
        
        show_avatars = st.checkbox(
            "Show avatars",
            value=True,
            help="Display user and AI avatars"
        )
        
        st.session_state["show_timestamps"] = show_timestamps
        st.session_state["show_sources"] = show_sources
        st.session_state["show_avatars"] = show_avatars
        
        st.divider()
        
        # Search Settings
        st.markdown("### 🔍 Search Settings")
        
        st.markdown("**Number of relevant documents to retrieve**")
        top_k = st.slider(
            "Documents",
            min_value=3,
            max_value=10,
            value=st.session_state.get("top_k", 5),
            help="More documents = more context but slower response",
            label_visibility="collapsed"
        )
        st.session_state["top_k"] = top_k
        st.caption(f"Currently retrieving top {top_k} documents")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("**Minimum similarity threshold**")
        min_similarity = st.slider(
            "Similarity",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.get("min_similarity", 0.7),
            step=0.05,
            help="Higher = more relevant but fewer results",
            label_visibility="collapsed"
        )
        st.session_state["min_similarity"] = min_similarity
        st.caption(f"Similarity threshold: {min_similarity:.2f}")
    
    # ============================================================
    # RIGHT PANEL - About & Info
    # ============================================================
    with col2:
        st.markdown("### 🎓 About")
        
        st.info("""
        **MCA Study Assistant**
        
        Version 1.0.0
        
        **Technology Stack:**
        • Python + Streamlit
        • Groq LLM API
        • Qdrant Vector Search
        
        **Created by:**
        Manish P Suryawanshi
        
        ✓ 100% FREE
        ✓ No Rate Limits
        """)
    
    # ============================================================
    # DATA MANAGEMENT
    # ============================================================
    st.divider()
    st.markdown("### 🗄️ Data Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True, help="Delete all chat messages"):
            if "messages" in st.session_state:
                st.session_state["messages"] = []
            if "history" in st.session_state:
                st.session_state["history"] = []
            st.success("✓ Chat history cleared!")
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset Settings", use_container_width=True, help="Restore default settings"):
            # Keep messages but reset other settings
            messages_backup = st.session_state.get("messages", [])
            history_backup = st.session_state.get("history", [])
            
            # Clear all settings
            keys_to_remove = [k for k in st.session_state.keys() if k not in ["messages", "history"]]
            for key in keys_to_remove:
                del st.session_state[key]
            
            # Restore messages
            st.session_state["messages"] = messages_backup
            st.session_state["history"] = history_backup
            
            st.success("✓ Settings reset to defaults!")
            st.rerun()
    
    with col3:
        if st.button("🔄 Refresh Page", use_container_width=True, help="Reload the page"):
            st.rerun()
    
    st.divider()
    
    # ============================================================
    # SYSTEM INFORMATION
    # ============================================================
    st.markdown("### 💻 System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔧 Technology Stack**")
        st.markdown("""
        • Python + Streamlit
        • Qdrant Vector DB
        • Groq LLM API
        • Sentence Transformers
        """)
    
    with col2:
        st.markdown("**🔒 Privacy & Security**")
        st.markdown("""
        ✓ Private database
        ✓ No tracking
        ✓ Secure processing
        ✓ Local encryption
        """)
    
    st.divider()
    
    # ============================================================
    # ADDITIONAL INFO
    # ============================================================
    st.markdown("### ℹ️ Important Notes")
    
    st.markdown("""
    **📌 Document Upload:**
    Use the Upload Materials section to add study materials. 
    Password protected for admin access only.
    
    **🔍 Search Tips:**
    Use specific keywords and phrases for better results. 
    Try different phrasings if you don't find what you're looking for.
    
    **💬 Chat Best Practices:**
    Ask clear, specific questions. Include subject names or topics 
    for more accurate responses from your study materials.
    """)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    ---
    MCA Study Assistant v1.0.0 • Created with ❤️ by Manish P Suryawanshi
    """)
