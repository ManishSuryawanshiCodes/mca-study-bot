"""
Statistics Manager
Tracks and manages application metrics
"""
import streamlit as st
from datetime import datetime, timedelta
from typing import Dict

class StatsManager:
    """Manage application statistics"""

    @staticmethod
    def initialize_stats():
        """Initialize stats in session state"""
        if 'app_stats' not in st.session_state:
            st.session_state.app_stats = {
                'total_questions': 0,
                'total_documents': 0,
                'total_chunks': 0,
                'session_start': datetime.now(),
                'questions_today': 0,
                'last_question_time': None,
                'avg_response_time': 0,
                'queries': [],
                'documents_uploaded': 0
            }

    @staticmethod
    def increment_question():
        """Increment question counter"""
        StatsManager.initialize_stats()
        st.session_state.app_stats['total_questions'] += 1
        st.session_state.app_stats['questions_today'] += 1
        st.session_state.app_stats['last_question_time'] = datetime.now()

    @staticmethod
    def add_query(query: str, answer: str, response_time: float = 0):
        """Add query to history"""
        StatsManager.initialize_stats()
        st.session_state.app_stats['queries'].append({
            'timestamp': datetime.now(),
            'query': query,
            'answer': answer[:100],
            'response_time': response_time
        })

    @staticmethod
    def update_documents(doc_count: int, chunk_count: int):
        """Update document statistics"""
        StatsManager.initialize_stats()
        st.session_state.app_stats['total_documents'] = doc_count
        st.session_state.app_stats['total_chunks'] = chunk_count

    @staticmethod
    def increment_uploads():
        """Increment document uploads"""
        StatsManager.initialize_stats()
        st.session_state.app_stats['documents_uploaded'] += 1

    @staticmethod
    def get_stats() -> Dict:
        """Get all statistics"""
        StatsManager.initialize_stats()
        return st.session_state.app_stats

    @staticmethod
    def get_session_duration() -> str:
        """Get session duration"""
        StatsManager.initialize_stats()
        session_start = st.session_state.app_stats['session_start']
        duration = datetime.now() - session_start
        
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

    @staticmethod
    def reset_stats():
        """Reset statistics"""
        st.session_state.app_stats = {
            'total_questions': 0,
            'total_documents': 0,
            'total_chunks': 0,
            'session_start': datetime.now(),
            'questions_today': 0,
            'last_question_time': None,
            'avg_response_time': 0,
            'queries': [],
            'documents_uploaded': 0
        }