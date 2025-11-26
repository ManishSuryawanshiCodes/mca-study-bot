"""
Main application interface
"""
from src.llm_groq import GroqLLM

import streamlit as st
from ui.components.theming import apply_auto_theme, load_css
from ui.pages.home import home_page
from ui.pages.chat import chat_page
from ui.pages.admin import admin_page
from ui.pages.settings import settings_page


def show_main_app():
    apply_auto_theme()
    load_css()

    # Enhanced sidebar styling
    st.markdown("""
    <style>
    /* Sidebar enhancements */
    .stSidebar {
        background: linear-gradient(180deg, rgba(20,20,25,0.9) 0%, rgba(15,17,19,0.95) 100%);
    }

    .sidebar-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        padding: 24px 16px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 24px;
    }

    .sidebar-logo {
        font-size: 36px;
        animation: fadeIn 0.6s ease-out;
    }

    .sidebar-title {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
    }

    .sidebar-subtitle {
        font-size: 12px;
        color: #a8acb4;
        text-align: center;
    }

    .sidebar-divider {
        height: 1px;
        background: rgba(255,255,255,0.08);
        margin: 16px 0;
    }

    .sidebar-footer {
        position: relative;
        padding: 12px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(124, 77, 255, 0.2);
        border-radius: 10px;
        font-size: 12px;
        color: #8b8e94;
        text-align: center;
    }

    .sidebar-footer strong {
        color: #7C4DFF;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar header
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <div class="sidebar-logo">📚</div>
            <div>
                <div class="sidebar-title">MCA Study</div>
                <div class="sidebar-subtitle">Groq</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

        # Navigation
        st.markdown(
            "<p style='color: #a8acb4; font-size: 12px; margin-left: 16px; margin-bottom: 12px;'>NAVIGATION</p>",
            unsafe_allow_html=True
        )

        pages = {
            "🏠 Home": "home",
            "💬 Chat": "chat",
            "📁 Upload Materials": "admin",
            "⚙️ Settings": "settings",
            "🧪 LLM Test": "llm_test"
        }

        # FIXED INDENTATION + FIXED BUTTON PARAMETER
        for title, key in pages.items():
            if st.button(title, use_container_width=True, key=f"nav_{key}"):
                st.session_state.current_page = key

        if "current_page" not in st.session_state:
            st.session_state.current_page = "home"

        selected_page = st.session_state.current_page

        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

        # Quick stats
        st.markdown("""
        <p style='color: #a8acb4; font-size: 12px; margin-left: 16px; margin-bottom: 12px;'>QUICK STATS</p>
        """, unsafe_allow_html=True)

        # Real-time LLM status
        try:
            llm = GroqLLM()
            status = "🟢 Online" if llm.connection_status else "🔴 Offline"
        except:
            status = "🔴 Error"

        col1, col2 = st.columns(2)
        with col1:
            st.metric("LLM", status, label_visibility="collapsed")
        with col2:
            st.metric("Version", "1.0.0", label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)

        # Footer in sidebar
        st.markdown("""
        <div class="sidebar-footer">
            Created by<br>
            <strong>Manish Suryawanshi</strong><br>
            © 2025 MCA Study Assistant
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Page routing
    if selected_page == "home":
        home_page()
    elif selected_page == "chat":
        chat_page()
    elif selected_page == "admin":
        admin_page()
    elif selected_page == "settings":
        settings_page()
    elif selected_page == "llm_test":
        from ui.pages.llm_test_page import llm_test_page
        llm_test_page()

    # Footer
    st.markdown("""
    <div class="custom-footer">
        Created by <strong>Manish Suryawanshi</strong> © 2025 MCA Study Assistant | v1.0.0
    </div>
    """, unsafe_allow_html=True)
