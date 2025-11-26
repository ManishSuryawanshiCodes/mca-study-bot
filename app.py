import streamlit as st

st.set_page_config(
    page_title="MCA Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
""", unsafe_allow_html=True)

from ui.pages.home import home_page
from ui.pages.chat import chat_page
from ui.pages.upload import upload_page
from ui.pages.settings import settings_page
from ui.pages.llmtest import llm_test_page
from ui.components.theming import load_css

# Load CSS
load_css()

# Sidebar header
st.sidebar.markdown("""
<div style='padding: 16px 0;'>
    <div style='font-size: 20px; font-weight: 600; color: #e6edf3; margin-bottom: 4px;'>🎓 MCA Study</div>
    <div style='font-size: 12px; color: #8b949e; margin-bottom: 16px;'>Groq Powered</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Pages
PAGES = {
    "🏠 Home": home_page,
    "💬 Chat": chat_page,
    "📁 Upload Materials": upload_page,
    "⚙️ Settings": settings_page,
    "⚡ LLM Test": llm_test_page
}

# Navigation
page = st.sidebar.radio("Navigation", list(PAGES.keys()), index=0)

st.sidebar.markdown("---")

# ============================================================
# ADMIN STATUS & LOGOUT SECTION
# ============================================================

# Check admin access status
upload_admin = st.session_state.get("upload_auth", False)
llm_admin = st.session_state.get("llm_test_auth", False)

if upload_admin or llm_admin:
    st.sidebar.markdown("""
    <div style='background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.2); 
                border-radius: 8px; padding: 12px; margin-bottom: 12px;'>
        <div style='font-size: 11px; color: #8b949e; margin-bottom: 6px;'>🔐 Admin Access</div>
        <div style='font-size: 12px; font-weight: 600; color: #6366f1;'>Enabled</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button
    if st.sidebar.button("🚪 Logout Admin", use_container_width=True, type="secondary"):
        st.session_state["upload_auth"] = False
        st.session_state["llm_test_auth"] = False
        st.success("✅ Logged out successfully!")
        st.rerun()
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Footer
st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style='text-align: center; font-size: 11px; color: #6e7681;'>
    <div>MCA Study Assistant v1.0.0</div>
    <div>Powered by Groq • FREE</div>
</div>
""", unsafe_allow_html=True)

# Run selected page
PAGES[page]()
