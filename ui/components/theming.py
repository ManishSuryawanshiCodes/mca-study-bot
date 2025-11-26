"""
Modern Theming - Fully Mobile Optimized
"""
import streamlit as st

def load_css():
    """Load mobile-first responsive theme"""
    st.markdown("""
    <style>
    
    /* ================================
       GLOBAL RESET & BASE
    ================================= */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        -webkit-tap-highlight-color: transparent;
    }
    
    html, body, .stApp {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%) !important;
        color: #e6edf3 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif !important;
        overflow-x: hidden !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    
    /* Mobile viewport fix */
    @supports (-webkit-touch-callout: none) {
        html, body, .stApp {
            min-height: -webkit-fill-available;
        }
    }
    
    /* ================================
       SMOOTH SCROLLBAR
    ================================= */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.3);
        border-radius: 10px;
        transition: background 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.5);
    }

    /* ================================
       CONTAINER & LAYOUT
    ================================= */
    .block-container {
        padding: 1.5rem 1rem 160px 1rem !important;
        max-width: 900px !important;
        margin: 0 auto !important;
    }

    /* ================================
       CHAT HEADER
    ================================= */
    .chat-header {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(20px);
        animation: slideDown 0.5s ease-out;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .chat-header-title {
        font-size: 24px;
        font-weight: 600;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }
    
    .chat-header-subtitle {
        color: #8b949e;
        font-size: 13px;
        font-weight: 400;
    }

    /* ================================
       MODEL SELECTOR SECTION
    ================================= */
    .model-selector-container {
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        backdrop-filter: blur(10px);
        animation: fadeIn 0.6s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* ================================
       MESSAGE CONTAINER
    ================================= */
    .messages-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 20px;
        animation: fadeIn 0.4s ease-out;
    }

    /* ================================
       MESSAGE BUBBLES - MOBILE OPTIMIZED
    ================================= */
    .message-wrapper {
        display: flex;
        gap: 10px;
        animation: messageSlideIn 0.3s ease-out;
        max-width: 100%;
    }
    
    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .message-wrapper.user {
        justify-content: flex-end;
    }
    
    .message-wrapper.assistant {
        justify-content: flex-start;
    }
    
    /* Avatar */
    .message-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .message-avatar.user {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    .message-avatar.assistant {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    /* Message Content */
    .message-content {
        max-width: 80%;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    
    /* User Bubble */
    .message-bubble.user {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: #ffffff;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        font-size: 15px;
        line-height: 1.5;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        word-wrap: break-word;
        word-break: break-word;
        transition: transform 0.2s ease;
    }
    
    .message-bubble.user:active {
        transform: scale(0.98);
    }
    
    /* Assistant Bubble */
    .message-bubble.assistant {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #e6edf3;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        font-size: 15px;
        line-height: 1.5;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        word-wrap: break-word;
        word-break: break-word;
        transition: transform 0.2s ease;
    }
    
    .message-bubble.assistant:active {
        transform: scale(0.98);
    }
    
    /* Message Metadata */
    .message-meta {
        font-size: 11px;
        color: #6e7681;
        padding: 0 4px;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    .message-meta.user {
        justify-content: flex-end;
    }

    /* ================================
       SOURCES SECTION - MOBILE FRIENDLY
    ================================= */
    .sources-container {
        margin-top: 8px;
        padding: 10px;
        background: rgba(99, 102, 241, 0.05);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 8px;
        animation: fadeIn 0.4s ease-out;
    }
    
    .source-title {
        font-size: 11px;
        font-weight: 600;
        color: #6366f1;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    .source-item {
        font-size: 11px;
        color: #8b949e;
        padding: 6px 8px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 6px;
        margin-bottom: 4px;
        border-left: 2px solid #6366f1;
        transition: all 0.2s ease;
        word-break: break-word;
    }
    
    .source-item:active {
        background: rgba(255, 255, 255, 0.06);
        transform: translateX(2px);
    }

    /* ================================
       MOBILE-OPTIMIZED CHAT INPUT
    ================================= */
    
    /* ================================
       ENHANCED CHAT INPUT - REDESIGNED
    ================================= */
    
    /* Gradient background behind input */
    .stApp::before {
        content: '';
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 200px;
        background: linear-gradient(
            180deg,
            transparent 0%,
            rgba(13, 17, 23, 0.6) 30%,
            rgba(13, 17, 23, 0.95) 70%,
            rgba(13, 17, 23, 1) 100%
        );
        pointer-events: none;
        z-index: 99;
    }
    
    /* Glow effect */
    .stApp::after {
        content: '';
        position: fixed;
        bottom: -60px;
        left: 50%;
        transform: translateX(-50%);
        width: 500px;
        height: 200px;
        background: radial-gradient(
            ellipse at center,
            rgba(99, 102, 241, 0.15) 0%,
            rgba(168, 85, 247, 0.1) 40%,
            transparent 70%
        );
        filter: blur(50px);
        pointer-events: none;
        z-index: 98;
        animation: pulseGlow 5s ease-in-out infinite;
    }
    
    @keyframes pulseGlow {
        0%, 100% {
            opacity: 0.5;
            transform: translateX(-50%) scale(1);
        }
        50% {
            opacity: 0.8;
            transform: translateX(-50%) scale(1.1);
        }
    }
    
    /* Chat input container - mobile first */
    .stChatInputContainer {
        position: fixed !important;
        bottom: 16px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        max-width: 850px !important;
        width: calc(100% - 32px) !important;
        z-index: 100 !important;
        padding: 0 !important;
    }
    
    /* Input wrapper */
    .stChatInputContainer > div {
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
    }
    
    /* Input field - beautiful glassmorphism */
    .stChatInputContainer textarea {
        background: linear-gradient(
            135deg,
            rgba(22, 27, 34, 0.98) 0%,
            rgba(30, 35, 42, 0.95) 100%
        ) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 2px solid rgba(99, 102, 241, 0.35) !important;
        border-radius: 20px !important;
        padding: 14px 50px 14px 18px !important;
        font-size: 15px !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        color: #e6edf3 !important;
        resize: none !important;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.05) inset,
            0 2px 8px rgba(99, 102, 241, 0.15) !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        min-height: 48px !important;
        max-height: 120px !important;
        width: 100% !important;
        -webkit-appearance: none !important;
    }
    
    /* Hover state */
    .stChatInputContainer textarea:hover {
        border-color: rgba(99, 102, 241, 0.6) !important;
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.08) inset,
            0 4px 16px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Focus state */
    .stChatInputContainer textarea:focus {
        border-color: rgba(99, 102, 241, 0.8) !important;
        background: linear-gradient(
            135deg,
            rgba(22, 27, 34, 1) 0%,
            rgba(30, 35, 42, 0.98) 100%
        ) !important;
        box-shadow: 
            0 16px 48px rgba(0, 0, 0, 0.5),
            0 0 0 3px rgba(99, 102, 241, 0.25),
            0 0 20px rgba(99, 102, 241, 0.3),
            0 0 0 1px rgba(255, 255, 255, 0.1) inset !important;
        outline: none !important;
    }
    
    /* Placeholder */
    .stChatInputContainer textarea::placeholder {
        color: #6e7681 !important;
        opacity: 0.75 !important;
    }
    
    /* Send button - positioned inside */
    .stChatInputContainer button {
        position: absolute !important;
        right: 6px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 38px !important;
        height: 38px !important;
        min-width: 38px !important;
        min-height: 38px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4) !important;
        z-index: 10 !important;
        padding: 0 !important;
        touch-action: manipulation !important;
    }
    
    /* Send button hover */
    .stChatInputContainer button:hover {
        transform: translateY(-50%) scale(1.08) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6) !important;
    }
    
    /* Send button active */
    .stChatInputContainer button:active {
        transform: translateY(-50%) scale(0.94) !important;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4) !important;
    }
    
    /* Mobile optimization */
    @media (max-width: 768px) {
        .stChatInputContainer {
            max-width: calc(100% - 16px) !important;
            bottom: 8px !important;
        }
        
        .stChatInputContainer textarea {
            font-size: 16px !important;
            padding: 12px 46px 12px 16px !important;
            min-height: 46px !important;
        }
        
        .stChatInputContainer button {
            width: 36px !important;
            height: 36px !important;
            min-width: 36px !important;
            min-height: 36px !important;
        }
    }


    /* ================================
       SIDEBAR - MOBILE OPTIMIZED
    ================================= */
    .stSidebar {
        background: rgba(13, 17, 23, 0.98) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stSidebar [data-testid="stSidebarNav"] {
        padding-top: 1.5rem;
    }
    
    /* Sidebar navigation items - touch friendly */
    .stSidebar button {
        min-height: 48px !important;
        padding: 12px 16px !important;
        touch-action: manipulation !important;
    }

    /* ================================
       GLASS SURFACE
    ================================= */
    .glass-surface {
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 14px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    /* ================================
       TYPING INDICATOR
    ================================= */
    .typing-indicator {
        display: flex;
        gap: 5px;
        padding: 12px 16px;
    }
    
    .typing-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #6366f1;
        animation: typingAnimation 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typingAnimation {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.7;
        }
        30% {
            transform: translateY(-8px);
            opacity: 1;
        }
    }

    /* ================================
       MOBILE SPECIFIC OPTIMIZATIONS
    ================================= */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 0.75rem 160px 0.75rem !important;
        }
        
        .message-content {
            max-width: 85%;
        }
        
        .chat-header {
            padding: 16px;
            border-radius: 12px;
        }
        
        .chat-header-title {
            font-size: 20px;
        }
        
        .chat-header-subtitle {
            font-size: 12px;
        }
        
        .stChatInputContainer {
            max-width: calc(100% - 16px) !important;
            bottom: 8px !important;
        }
        
        .stChatInputContainer textarea {
            font-size: 16px !important;
            padding: 12px 50px 12px 16px !important;
            min-height: 48px !important;
            border-radius: 18px !important;
        }
        
        .stChatInputContainer button {
            width: 38px !important;
            height: 38px !important;
            min-width: 38px !important;
            min-height: 38px !important;
            right: 5px !important;
        }
        
        .message-bubble.user,
        .message-bubble.assistant {
            font-size: 14px;
            padding: 10px 14px;
        }
        
        .message-avatar {
            width: 28px;
            height: 28px;
            font-size: 14px;
        }
        
        .glass-surface {
            padding: 12px;
        }
        
        .stMetric {
            padding: 10px;
        }
        
        .stMetric [data-testid="stMetricValue"] {
            font-size: 18px !important;
        }
    }
    
    /* Small phones */
    @media (max-width: 480px) {
        .block-container {
            padding: 0.75rem 0.5rem 160px 0.5rem !important;
        }
        
        .chat-header-title {
            font-size: 18px;
        }
        
        .message-content {
            max-width: 90%;
        }
        
        .stChatInputContainer {
            max-width: calc(100% - 12px) !important;
        }
        
        .stChatInputContainer textarea {
            font-size: 16px !important;
            padding: 11px 48px 11px 14px !important;
        }
    }
    
    /* Landscape mode on mobile */
    @media (max-width: 900px) and (max-height: 500px) {
        .block-container {
            padding: 0.75rem 0.5rem 120px 0.5rem !important;
        }
        
        .stChatInputContainer {
            bottom: 6px !important;
        }
        
        .chat-header {
            padding: 12px;
            margin-bottom: 12px;
        }
    }

    </style>
    """, unsafe_allow_html=True)

def apply_auto_theme():
    """Apply theme based on system preference (placeholder)"""
    pass
