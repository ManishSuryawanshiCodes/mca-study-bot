"""
Authentication Module - Simple Login System
"""
import streamlit as st
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional, Dict

class AuthManager:
    """Simple authentication manager"""
    
    # Hardcoded credentials (replace with database in production)
    VALID_USERS = {
        "admin": "admin123",  # username: password
        "student": "student123",
        "teacher": "teacher123"
    }
    
    ROLES = {
        "admin": ["chat", "upload", "settings", "llmtest", "home"],
        "teacher": ["chat", "upload", "settings", "home"],
        "student": ["chat", "settings", "home"]
    }
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password"""
        return AuthManager.hash_password(password) == hashed
    
    @staticmethod
    def authenticate(username: str, password: str) -> bool:
        """Authenticate user"""
        if username not in AuthManager.VALID_USERS:
            return False
        
        valid_password = AuthManager.VALID_USERS[username]
        return password == valid_password
    
    @staticmethod
    def get_user_role(username: str) -> str:
        """Get user role"""
        if username == "admin":
            return "admin"
        elif username == "teacher":
            return "teacher"
        else:
            return "student"
    
    @staticmethod
    def get_available_pages(username: str) -> list:
        """Get pages available for user"""
        role = AuthManager.get_user_role(username)
        return AuthManager.ROLES.get(role, [])


def login_page():
    """Login page"""
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 40px 0;'>
            <div style='font-size: 48px; margin-bottom: 10px;'>🎓</div>
            <h1 style='color: #e6edf3; margin: 0 0 5px 0;'>MCA Study Assistant</h1>
            <p style='color: #8b949e; margin: 0 0 30px 0;'>Powered by Groq • 100% FREE</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login form
        st.markdown("### 🔐 Login")
        
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            help="Try: admin, teacher, or student"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )
        
        if st.button("🚀 Login", use_container_width=True, type="primary"):
            if not username or not password:
                st.error("❌ Please enter both username and password")
            elif AuthManager.authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_role = AuthManager.get_user_role(username)
                st.success(f"✅ Welcome, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        
        # Demo credentials info
        st.markdown("""
        <div style='background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.2); 
                    border-radius: 10px; padding: 16px; margin-top: 30px;'>
            <h4 style='color: #6366f1; margin-top: 0;'>📝 Demo Credentials</h4>
            <div style='font-size: 13px; color: #8b949e; line-height: 1.8;'>
                <div><strong style='color: #e6edf3;'>Admin:</strong> admin / admin123</div>
                <div><strong style='color: #e6edf3;'>Teacher:</strong> teacher / teacher123</div>
                <div><strong style='color: #e6edf3;'>Student:</strong> student / student123</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.info("""
        🔒 **Security Note:**
        - This is a demo login system
        - In production, use proper authentication with database
        - Never hardcode credentials
        - Use OAuth or JWT tokens for real apps
        """)


def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get("logged_in", False)


def get_current_user() -> Optional[str]:
    """Get current logged-in user"""
    return st.session_state.get("username", None)


def get_current_role() -> Optional[str]:
    """Get current user role"""
    return st.session_state.get("user_role", None)


def require_role(*roles):
    """Decorator to require specific roles"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_role = get_current_role()
            if current_role not in roles:
                st.error(f"❌ Access Denied. Required role: {', '.join(roles)}")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator
