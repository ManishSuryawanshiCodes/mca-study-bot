"""
LLM Test Page - Test Groq LLM directly (Password Protected)
"""
import streamlit as st
from src.llm_groq import GroqLLM
from src.config import Config
from ui.components.theming import load_css

def llm_test_page():
    """Test LLM functionality"""
    
    load_css()
    
    st.markdown("""
    <div class="chat-header">
        <div class="chat-header-title">⚡ LLM Test</div>
        <div class="chat-header-subtitle">Test Groq AI directly</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Password authentication
    if "llm_test_auth" not in st.session_state:
        st.session_state["llm_test_auth"] = False
    
    if not st.session_state["llm_test_auth"]:
        st.markdown("""
        <div style='background: rgba(99,102,241,0.1); border: 2px solid rgba(99,102,241,0.3); 
                    border-radius: 12px; padding: 24px; text-align: center;'>
            <div style='font-size: 32px; margin-bottom: 12px;'>🔐</div>
            <h2 style='color: #e6edf3; margin: 0 0 8px 0;'>Admin Access Required</h2>
            <p style='color: #8b949e; margin: 0 0 24px 0;'>LLM Testing</p>
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
                    st.session_state["llm_test_auth"] = True
                    st.success("✅ Access granted!")
                    st.rerun()
                else:
                    st.error("❌ Incorrect password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.info("""
            💡 **Note:** This section is password-protected.
            Only admins with the correct password can test LLM features.
            """)
        
        return
    
    # After password verification, show LLM test interface
    st.success("✅ Admin access granted!")
    st.markdown("<br>", unsafe_allow_html=True)
    

    col1, col2 = st.columns([2, 1])

    with col2:
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state["llm_test_auth"] = False
            st.success("✅ Logged out!")
            st.rerun()

    st.divider()


    try:
        llm = GroqLLM()
        status = llm.get_status()
        
        if not status["connected"]:
            st.error(f"❌ LLM Connection Failed: {status['status']}")
            return
        
        # Display LLM Status
        st.markdown("### 🟢 LLM Status")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Status", "Online", delta="Connected")
        with col2:
            st.metric("Model", "Llama 3.1 8B")
        with col3:
            st.metric("Provider", "Groq", delta="Free")
        
        st.divider()
        
        # Test Input
        st.markdown("### 🧪 Test Query")
        
        test_prompt = st.text_area(
            "Enter a test prompt",
            value="Explain what is machine learning in 2 sentences",
            height=100,
            help="Type a question to test the LLM"
        )
        
        if st.button("🚀 Test LLM Response", use_container_width=True, type="primary"):
            with st.spinner("⏳ Testing LLM..."):
                try:
                    response = llm.generate_answer(test_prompt, [], [])
                    answer = response.get("answer", "No response generated")
                    
                    st.success("✅ LLM Response Generated!")
                    
                    st.markdown("### 📝 Response")
                    st.write(answer)
                    
                    st.markdown("### 📊 Response Metadata")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Status", "✓ Success")
                    with col2:
                        st.metric("Model", status["model"])
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        st.divider()
        
        # Information Section
        st.markdown("### ℹ️ About This Test")
        st.markdown("""
        **What is this?**
        
        This page tests your Groq LLM connection directly without vector search.
        
        **How to use:**
        
        1. Enter a test prompt
        2. Click "Test LLM Response"
        3. See the AI-generated answer
        
        **🔗 Provider:** Groq Cloud • Free • Unlimited • Instant
        """)
        
    except Exception as e:
        st.error(f"❌ System Error: {str(e)}")
        st.info("💡 Make sure your GROQ_API_KEY is set in .env file")
