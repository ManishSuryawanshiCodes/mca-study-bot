"""
Modern Chat Interface with Groq Model
Clean implementation using Streamlit native components
"""
import streamlit as st
from src.vector_store import VectorStore
from src.document_processor import DocumentProcessor
from src.llm_groq import GroqLLM
from src.config import Config
from src.stats_manager import StatsManager
from datetime import datetime
import time
import re

@st.cache_resource
def init_system():
    """Initialize all system components once"""
    try:
        dp = DocumentProcessor()
        vs = VectorStore(use_qdrant=Config.USE_QDRANT)
        llm = GroqLLM()
        return dp, vs, llm
    except Exception as e:
        st.error(f"❌ System initialization error: {str(e)}")
        return None, None, None

def strip_html_tags(text):
    """Remove HTML tags from text"""
    if isinstance(text, str):
        return re.sub(r'<[^>]+>', '', text)
    return text

def render_message(role, content, sources=None, name=None, timestamp=None):
    """Render a message bubble with optional sources"""
    
    # Message bubble styling
    if role == "user":
        bubble_color = "#6366f1"
        text_color = "#ffffff"
        avatar = "🧑‍🎓"
        border_radius = "18px 18px 4px 18px"
    else:
        bubble_color = "#26283a"
        text_color = "#e6edf3"
        avatar = "🤖"
        border_radius = "18px 18px 18px 4px"
    
    sender_time = f"{name or 'Assistant'} • {timestamp}" if timestamp else (name or "Assistant")
    
    # Render message bubble
    st.markdown(
        f"""
        <div style='margin-bottom: 16px;'>
            <div style='display: flex; gap: 10px; margin-bottom: 6px;'>
                <div style='font-size: 12px; color: #8b949e;'>{sender_time}</div>
            </div>
            <div style='background: {bubble_color}; padding: 12px 16px; border-radius: {border_radius}; color: {text_color}; word-wrap: break-word;'>
                {content}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Show sources if available
    if sources and len(sources) > 0:
        # Filter out empty sources and deduplicate
        valid_sources = []
        seen_sources = set()
        
        for source in sources:
            if isinstance(source, dict) and source.get('content'):
                source_name = strip_html_tags(str(source.get('source', 'Document')))
                if source_name not in seen_sources:
                    seen_sources.add(source_name)
                    valid_sources.append({
                        'source': source_name,
                        'subject': strip_html_tags(str(source.get('subject', 'N/A'))),
                        'year': strip_html_tags(str(source.get('year', 'N/A'))),
                        'type': strip_html_tags(str(source.get('type', 'N/A'))),
                        'page': source.get('page', 'N/A')
                    })
        
        if valid_sources:
            with st.expander("📑 View Sources"):
                for src in valid_sources:
                    st.markdown(
                        f"""
                        **📄 {src['source']}**
                        
                        - **Subject:** {src['subject']}
                        - **Year:** {src['year']}
                        - **Type:** {src['type']}
                        - **Page:** {src['page']}
                        """,
                        unsafe_allow_html=False
                    )

def chat_page():
    """Main chat interface with modern design"""
    
    # Initialize stats
    StatsManager.initialize_stats()
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "history" not in st.session_state:
        st.session_state.history = []
    
    # ==========================================
    # HEADER SECTION
    # ==========================================
    st.markdown("""
    <div class="chat-header">
        <div class="chat-header-title">💬 MCA Chat</div>
        <div class="chat-header-subtitle">Ask questions about your study materials</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ==========================================
    # LLM STATUS
    # ==========================================
    try:
        _, vs, llm = init_system()
        llm_status = llm.get_status()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🟢 Status", "Online", delta="Connected")
        
        with col2:
            st.metric("⚡ Model", "Llama 3.1 8B", delta="Fast")
        
        with col3:
            st.metric("💰 Cost", "FREE", delta="Unlimited")
        
    except Exception as e:
        st.error(f"❌ LLM Connection Error: {str(e)}")
        return
    
    st.divider()
    
    # ==========================================
    # SEARCH FILTERS
    # ==========================================
    with st.expander("🔍 Filter Search Results", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            subject_filter = st.selectbox(
                "Subject",
                ["All"] + Config.SUBJECTS,
                key="subject_filter"
            )
        with col2:
            year_filter = st.selectbox(
                "Year",
                ["All"] + Config.YEARS,
                key="year_filter"
            )
    
    st.divider()
    
    # ==========================================
    # MESSAGES DISPLAY SECTION
    # ==========================================
    
    # Display welcome message if no messages
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "👋 Hello! I'm your MCA Study Assistant.\n\nI can help you with:\n- 📚 Course materials and notes\n- 💡 Concept explanations\n- 📝 Assignment guidance\n- 🔍 Quick information lookup\n\nUpload your materials and ask me anything!",
            "sources": [],
            "name": "MCA Assistant",
            "timestamp": datetime.now().strftime("%I:%M %p")
        })
    
    # Render all messages
    for msg in st.session_state.messages:
        render_message(
            msg["role"],
            msg["content"],
            msg.get("sources", []),
            msg.get("name"),
            msg.get("timestamp")
        )
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # ==========================================
    # CHAT INPUT
    # ==========================================
    
    user_input = st.chat_input("💬 Type your question here...", key="chat_input")
    
    if user_input:
        user_text = user_input.strip()
        
        if not user_text:
            return
        
        # Add user message
        user_msg = {
            "role": "user",
            "content": user_text,
            "name": "You",
            "timestamp": datetime.now().strftime("%I:%M %p")
        }
        st.session_state.messages.append(user_msg)
        
        # Handle greetings
        greetings = {"hi", "hello", "hey", "hii", "hiya", "yo", "howdy", "greetings", "namaste"}
        if user_text.lower() in greetings:
            response_text = "Hello! 👋 How can I assist you today?"
            assistant_msg = {
                "role": "assistant",
                "content": response_text,
                "sources": [],
                "name": "MCA Assistant",
                "timestamp": datetime.now().strftime("%I:%M %p")
            }
            st.session_state.messages.append(assistant_msg)
            st.rerun()
            return
        
        # Build search filters
        filters = {}
        if subject_filter != "All":
            filters["subject"] = subject_filter
        if year_filter != "All":
            filters["year"] = year_filter
        
        # Search documents
        with st.spinner("🔍 Searching your materials..."):
            try:
                docs = vs.search(user_text, Config.TOP_K_RESULTS, filters or None)
            except Exception as e:
                docs = []
                st.warning(f"⚠️ Search error: {str(e)}")
        
        # Generate answer
        with st.spinner("✨ Generating answer..."):
            try:
                response = llm.generate_answer(
                    user_text,
                    docs,
                    st.session_state.history
                )
                answer = response.get("answer", "I apologize, but I encountered an error generating the answer.")
                sources = response.get("sources", [])
            except Exception as e:
                answer = f"❌ Error: {str(e)}"
                sources = []
        
        # Add assistant response
        assistant_msg = {
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "name": "MCA Assistant",
            "timestamp": datetime.now().strftime("%I:%M %p")
        }
        st.session_state.messages.append(assistant_msg)
        
        # Update conversation history
        st.session_state.history.append({
            "user": user_text,
            "assistant": answer
        })
        
        # Rerun to display new messages
        st.rerun()
    
    # ==========================================
    # SIDEBAR
    # ==========================================
    with st.sidebar:
        st.markdown("---")
        
        st.markdown("""
        <div style='text-align: center; padding: 16px; background: rgba(99,102,241,0.1); border-radius: 10px; border: 1px solid rgba(99,102,241,0.2);'>
            <div style='font-size: 14px; font-weight: 600; color: #e6edf3; margin-bottom: 8px;'>⚡ AI Model</div>
            <div style='font-size: 12px; color: #8b949e; margin-bottom: 4px;'>Llama 3.1 8B</div>
            <div style='font-size: 11px; color: #10b981;'>✓ Free • Instant • Unlimited</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear", use_container_width=True, key="clear_chat"):
                st.session_state.messages = []
                st.session_state.history = []
                st.rerun()
        
        with col2:
            if st.button("🔄 Refresh", use_container_width=True, key="refresh"):
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Stats
        st.markdown("""
        <div style='background: rgba(22,27,34,0.6); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 12px;'>
            <div style='font-size: 12px; font-weight: 600; color: #e6edf3; margin-bottom: 8px;'>📊 Session</div>
            <div style='font-size: 11px; color: #8b949e; line-height: 1.8;'>
                <div>💬 Messages: <strong style='color: #6366f1;'>{}</strong></div>
                <div>🔁 Exchanges: <strong style='color: #6366f1;'>{}</strong></div>
            </div>
        </div>
        """.format(len(st.session_state.messages), len(st.session_state.history)), unsafe_allow_html=True)
