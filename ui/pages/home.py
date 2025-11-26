"""
Enhanced Home/Dashboard page with detailed statistics
"""
import streamlit as st
from src.vector_store import VectorStore
from src.llm_groq import GroqLLM
from src.config import Config
from src.stats_manager import StatsManager
from datetime import datetime

def home_page():
    """Enhanced home page with dynamic features and detailed stats"""
    
    st.markdown("""
    <div class="chat-header">
        <div class="chat-header-title">🎓 MCA Study Assistant</div>
        <div class="chat-header-subtitle">Your AI-Powered Study Companion • 100% FREE</div>
    </div>
    """, unsafe_allow_html=True)
    
    StatsManager.initialize_stats()
    
    # Get system status
    try:
        vs = VectorStore(use_qdrant=Config.USE_QDRANT)
        vs_stats = vs.get_stats()
        
        # Get detailed document statistics by type
        doc_stats = vs.get_document_stats_by_type()  # We'll create this method
        
        StatsManager.update_documents(
            vs_stats.get('document_count', 0),
            vs_stats.get('chunk_count', 0)
        )
    except Exception as e:
        st.error(f"Error loading stats: {e}")
        vs_stats = {"document_count": 0, "chunk_count": 0, "embedding_count": 0}
        doc_stats = {"notes": 0, "assignments": 0, "question_papers": 0, "textbooks": 0, "syllabus": 0}
    
    app_stats = StatsManager.get_stats()
    session_duration = StatsManager.get_session_duration()
    
    # ==========================================
    # HERO SECTION
    # ==========================================
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="glass-surface">
            <h2 style='color: #ffffff; margin-top: 0;'>👋 Welcome Back!</h2>
            <p style='color: #a8acb4; font-size: 15px; line-height: 1.6;'>
                Your intelligent study companion is ready to help. Upload materials, 
                ask questions, and get instant AI-powered answers from your course content.
            </p>
            <div style='display: flex; gap: 12px; margin-top: 20px; flex-wrap: wrap;'>
                <a href="#" style='text-decoration: none;'>
                    <div style='padding: 10px 18px; background: linear-gradient(135deg, #6366f1, #8b5cf6); 
                                border-radius: 10px; color: white; font-weight: 600; font-size: 14px;
                                box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
                                transition: transform 0.2s ease;'>
                        💬 Start Chatting
                    </div>
                </a>
                <a href="#" style='text-decoration: none;'>
                    <div style='padding: 10px 18px; background: rgba(255,255,255,0.08); 
                                border: 1px solid rgba(255,255,255,0.15);
                                border-radius: 10px; color: white; font-weight: 600; font-size: 14px;
                                transition: all 0.2s ease;'>
                        📁 Upload Materials
                    </div>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        current_time = datetime.now().strftime("%I:%M %p")
        current_date = datetime.now().strftime("%B %d, %Y")
        
        st.markdown(f"""
        <div class="glass-surface">
            <h3 style='color: #ffffff; margin-top: 0;'>📊 Session Info</h3>
            <div style='color: #a8acb4; font-size: 13px; line-height: 2;'>
                <div>📅 {current_date}</div>
                <div>🕐 {current_time}</div>
                <div>⏱️ Duration: <strong style='color: #6366f1;'>{session_duration}</strong></div>
                <div>💬 Questions: <strong style='color: #6366f1;'>{app_stats['total_questions']}</strong></div>
                <div>✅ Status: <strong style='color: #10b981;'>● Online</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # UPLOADED MATERIALS STATISTICS
    # ==========================================
    st.markdown("<h2 style='color: #ffffff; margin-bottom: 16px;'>📚 Your Study Materials</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        notes_count = doc_stats.get('notes', 0)
        st.markdown(f"""
        <div class="glass-surface" style='text-align: center; padding: 20px; 
                    border: 2px solid {'rgba(99, 102, 241, 0.3)' if notes_count > 0 else 'rgba(255,255,255,0.1)'};
                    transition: all 0.3s ease;'>
            <div style='font-size: 36px; margin-bottom: 8px;'>📝</div>
            <div style='color: #ffffff; font-weight: 600; font-size: 14px; margin-bottom: 8px;'>Notes</div>
            <div style='color: #6366f1; font-size: 28px; font-weight: 700;'>{notes_count}</div>
            <div style='color: #8b949e; font-size: 11px; margin-top: 6px;'>Documents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        assignments_count = doc_stats.get('assignments', 0)
        st.markdown(f"""
        <div class="glass-surface" style='text-align: center; padding: 20px;
                    border: 2px solid {'rgba(168, 85, 247, 0.3)' if assignments_count > 0 else 'rgba(255,255,255,0.1)'};
                    transition: all 0.3s ease;'>
            <div style='font-size: 36px; margin-bottom: 8px;'>📋</div>
            <div style='color: #ffffff; font-weight: 600; font-size: 14px; margin-bottom: 8px;'>Assignments</div>
            <div style='color: #a855f7; font-size: 28px; font-weight: 700;'>{assignments_count}</div>
            <div style='color: #8b949e; font-size: 11px; margin-top: 6px;'>Documents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        qp_count = doc_stats.get('question_papers', 0)
        st.markdown(f"""
        <div class="glass-surface" style='text-align: center; padding: 20px;
                    border: 2px solid {'rgba(16, 185, 129, 0.3)' if qp_count > 0 else 'rgba(255,255,255,0.1)'};
                    transition: all 0.3s ease;'>
            <div style='font-size: 36px; margin-bottom: 8px;'>📄</div>
            <div style='color: #ffffff; font-weight: 600; font-size: 14px; margin-bottom: 8px;'>Question Papers</div>
            <div style='color: #10b981; font-size: 28px; font-weight: 700;'>{qp_count}</div>
            <div style='color: #8b949e; font-size: 11px; margin-top: 6px;'>Documents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        textbooks_count = doc_stats.get('textbooks', 0)
        st.markdown(f"""
        <div class="glass-surface" style='text-align: center; padding: 20px;
                    border: 2px solid {'rgba(251, 146, 60, 0.3)' if textbooks_count > 0 else 'rgba(255,255,255,0.1)'};
                    transition: all 0.3s ease;'>
            <div style='font-size: 36px; margin-bottom: 8px;'>📖</div>
            <div style='color: #ffffff; font-weight: 600; font-size: 14px; margin-bottom: 8px;'>Textbooks</div>
            <div style='color: #fb923c; font-size: 28px; font-weight: 700;'>{textbooks_count}</div>
            <div style='color: #8b949e; font-size: 11px; margin-top: 6px;'>Documents</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        syllabus_count = doc_stats.get('syllabus', 0)
        st.markdown(f"""
        <div class="glass-surface" style='text-align: center; padding: 20px;
                    border: 2px solid {'rgba(59, 130, 246, 0.3)' if syllabus_count > 0 else 'rgba(255,255,255,0.1)'};
                    transition: all 0.3s ease;'>
            <div style='font-size: 36px; margin-bottom: 8px;'>📑</div>
            <div style='color: #ffffff; font-weight: 600; font-size: 14px; margin-bottom: 8px;'>Syllabus</div>
            <div style='color: #3b82f6; font-size: 28px; font-weight: 700;'>{syllabus_count}</div>
            <div style='color: #8b949e; font-size: 11px; margin-top: 6px;'>Documents</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # SYSTEM STATUS SECTION
    # ==========================================
    st.markdown("<h2 style='color: #ffffff; margin-bottom: 16px;'>🔧 System Status</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="glass-surface" style='text-align: center; padding: 20px;'>
            <div style='font-size: 32px; margin-bottom: 8px;'>🟢</div>
            <div style='color: #ffffff; font-weight: 600; font-size: 14px;'>AI Status</div>
            <div style='color: #10b981; font-size: 16px; margin-top: 8px; font-weight: 600;'>Online</div>
            <div style='color: #8b949e; font-size: 11px; margin-top: 4px;'>Ready to Answer</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_docs = vs_stats.get('document_count', 0)
        st.markdown(f"""
        <div class="glass-surface" style='text-align: center; padding: 20px;'>
            <div style='font-size: 32px; margin-bottom: 8px;'>📚</div>
            <div style='color: #ffffff; font-weight: 600; font-size: 14px;'>Total Documents</div>
            <div style='color: #6366f1; font-size: 24px; font-weight: 700; margin-top: 8px;'>{total_docs}</div>
            <div style='color: #8b949e; font-size: 11px; margin-top: 4px;'>Indexed & Ready</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_chunks = vs_stats.get('chunk_count', 0)
        st.markdown(f"""
        <div class="glass-surface" style='text-align: center; padding: 20px;'>
            <div style='font-size: 32px; margin-bottom: 8px;'>🔀</div>
            <div style='color: #ffffff; font-weight: 600; font-size: 14px;'>Content Chunks</div>
            <div style='color: #8b5cf6; font-size: 24px; font-weight: 700; margin-top: 8px;'>{total_chunks}</div>
            <div style='color: #8b949e; font-size: 11px; margin-top: 4px;'>Searchable Pieces</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="glass-surface" style='text-align: center; padding: 20px;'>
            <div style='font-size: 32px; margin-bottom: 8px;'>⚡</div>
            <div style='color: #ffffff; font-weight: 600; font-size: 14px;'>Performance</div>
            <div style='color: #10b981; font-size: 16px; margin-top: 8px; font-weight: 600;'>Instant</div>
            <div style='color: #8b949e; font-size: 11px; margin-top: 4px;'>< 3s Response</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # FEATURES GRID
    # ==========================================
    st.markdown("<h2 style='color: #ffffff; margin-bottom: 16px;'>✨ Key Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glass-surface" style='text-align: center; padding: 24px;'>
            <div style='font-size: 48px; margin-bottom: 12px;'>🚀</div>
            <h3 style='color: #ffffff; margin: 0 0 8px 0; font-size: 18px;'>Lightning Fast</h3>
            <p style='color: #8b949e; font-size: 13px; line-height: 1.6;'>
                Get instant answers to your questions with our optimized AI infrastructure
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-surface" style='text-align: center; padding: 24px;'>
            <div style='font-size: 48px; margin-bottom: 12px;'>💰</div>
            <h3 style='color: #ffffff; margin: 0 0 8px 0; font-size: 18px;'>100% FREE</h3>
            <p style='color: #8b949e; font-size: 13px; line-height: 1.6;'>
                No credit card required. Unlimited questions and document uploads
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-surface" style='text-align: center; padding: 24px;'>
            <div style='font-size: 48px; margin-bottom: 12px;'>🔒</div>
            <h3 style='color: #ffffff; margin: 0 0 8px 0; font-size: 18px;'>Private & Secure</h3>
            <p style='color: #8b949e; font-size: 13px; line-height: 1.6;'>
                Your study materials stay private and secure on your own database
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # QUICK STATS SUMMARY
    # ==========================================
    if total_docs == 0:
        st.markdown("""
        <div class="glass-surface" style='text-align: center; padding: 32px; 
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
                    border: 2px solid rgba(99, 102, 241, 0.2);'>
            <div style='font-size: 48px; margin-bottom: 16px;'>📁</div>
            <h3 style='color: #ffffff; margin: 0 0 12px 0;'>Get Started!</h3>
            <p style='color: #8b949e; font-size: 14px; line-height: 1.6; max-width: 500px; margin: 0 auto;'>
                Upload your course materials, notes, and assignments to start getting AI-powered help with your studies.
                Navigate to <strong style='color: #6366f1;'>Upload Materials</strong> to begin!
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="glass-surface" style='text-align: center; padding: 24px;'>
            <h3 style='color: #ffffff; margin: 0 0 16px 0;'>📈 Your Progress</h3>
            <div style='display: flex; justify-content: center; gap: 40px; flex-wrap: wrap;'>
                <div>
                    <div style='font-size: 32px; font-weight: 700; color: #6366f1;'>{total_docs}</div>
                    <div style='font-size: 12px; color: #8b949e; margin-top: 4px;'>Total Materials</div>
                </div>
                <div>
                    <div style='font-size: 32px; font-weight: 700; color: #8b5cf6;'>{app_stats['total_questions']}</div>
                    <div style='font-size: 12px; color: #8b949e; margin-top: 4px;'>Questions Asked</div>
                </div>
                <div>
                    <div style='font-size: 32px; font-weight: 700; color: #10b981;'>{app_stats['documents_uploaded']}</div>
                    <div style='font-size: 12px; color: #8b949e; margin-top: 4px;'>Recent Uploads</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # ==========================================
    # CREATOR INFO
    # ==========================================
    st.markdown("""
    <div class="glass-surface" style='text-align: center; padding: 24px;'>
        <div style='font-size: 24px; margin-bottom: 12px;'>👨‍💻</div>
        <h3 style='color: #ffffff; margin: 0 0 8px 0;'>Created By</h3>
        <div style='font-size: 20px; font-weight: 600; color: #6366f1; margin: 8px 0;'>
            Manish Suryawanshi
        </div>
        <p style='color: #8b949e; font-size: 12px; margin: 8px 0 0 0;'>
            MCA Study Assistant v1.0.0 • Made with ❤️ for Students
        </p>
    </div>
    """, unsafe_allow_html=True)
