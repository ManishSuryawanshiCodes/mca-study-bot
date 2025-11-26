"""
Modern message bubble component using Streamlit native chat components
"""
import streamlit as st
from datetime import datetime

def render_message(role: str, content: str, sources: list = None, name: str = None, timestamp: str = None):
    """Render a single message using Streamlit's native chat message"""
    
    if not timestamp:
        timestamp = datetime.now().strftime("%I:%M %p")
    
    # Use Streamlit's native chat message component
    with st.chat_message(role, avatar="👤" if role == "user" else "🤖"):
        # Render message content
        st.markdown(content)
        
        # Render metadata
        st.caption(f"{name or ('You' if role == 'user' else 'Assistant')} • {timestamp}")
        
        # Render sources if available
        if sources and len(sources) > 0:
            with st.expander("📚 View Sources", expanded=False):
                for source in sources:
                    if isinstance(source, dict):
                        doc_name = source.get('document', source.get('source', 'Unknown'))
                        pages = source.get('pages', 'N/A')
                        subject = source.get('subject', '')
                        
                        st.markdown(f"""
                        <div style='
                            background: rgba(99, 102, 241, 0.1);
                            border-left: 3px solid #6366f1;
                            padding: 8px 12px;
                            border-radius: 6px;
                            margin-bottom: 6px;
                            font-size: 13px;
                        '>
                            <strong style='color: #6366f1;'>{doc_name}</strong><br>
                            {f"<span style='color: #8b949e;'>Pages: {pages}</span>" if pages != "N/A" else ""}
                            {f"<span style='color: #8b949e;'> • {subject}</span>" if subject else ""}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"- {source}")

def render_typing_indicator():
    """Render animated typing indicator using Streamlit spinner"""
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            pass
