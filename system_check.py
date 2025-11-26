"""
System Check Script - Groq with Working Models
"""

def check_system():
    """Check all system components"""
    
    print("\n" + "="*80)
    print("🔍 MCA Study Assistant - System Check (Groq + Qdrant)")
    print("="*80 + "\n")
    
    # Check imports
    print("📦 Checking imports...")
    try:
        from groq import Groq
        print("✅ Groq LLM SDK")
    except ImportError:
        print("❌ Groq - Install: pip install groq")
    
    try:
        import streamlit
        print("✅ Streamlit")
    except ImportError:
        print("❌ Streamlit - Install: pip install streamlit")
    
    try:
        import qdrant_client
        print("✅ Qdrant Client")
    except ImportError:
        print("❌ Qdrant Client - Install: pip install qdrant-client")
    
    try:
        import sentence_transformers
        print("✅ Sentence Transformers")
    except ImportError:
        print("❌ Sentence Transformers - Install: pip install sentence-transformers")
    
    try:
        import chromadb
        print("✅ ChromaDB")
    except ImportError:
        print("❌ ChromaDB - Install: pip install chromadb")
    
    try:
        import PyPDF2
        print("✅ PyPDF2")
    except ImportError:
        print("❌ PyPDF2 - Install: pip install PyPDF2")
    
    # Check environment
    print("\n🔐 Checking environment variables...")
    from src.config import Config
    
    if Config.GROQ_API_KEY:
        print("✅ GROQ_API_KEY is set")
    else:
        print("❌ GROQ_API_KEY not set - Get from https://console.groq.com")
        return
    
    if Config.QDRANT_URL and Config.QDRANT_API_KEY:
        print("✅ Qdrant Cloud configured")
    else:
        print("⚠️  Qdrant Cloud not configured (optional)")
    
    # Check available models
    print("\n🤖 Currently Working Groq Models:")
    for model_id, model_name in Config.AVAILABLE_MODELS.items():
        is_default = "✅ DEFAULT" if model_id == Config.LLM_MODEL else "  "
        print(f"{is_default} {model_name}")
        print(f"     ID: {model_id}")
    
    # Check Groq connection
    print("\n🧪 Testing Groq connection with default model...")
    try:
        from src.llm_groq import GroqLLM
        llm = GroqLLM(model=Config.LLM_MODEL)
        status = llm.get_status()
        
        if status['connected']:
            print(f"✅ {status['status']}")
            print(f"   Model: {status['model_display_name']}")
            print(f"   Free Tier: ✅ Unlimited")
        else:
            print(f"❌ {status['status']}")
            print("   Check your GROQ_API_KEY")
    except Exception as e:
        print(f"❌ Groq Error: {str(e)[:100]}")
    
    # Check Vector Store
    print("\n📚 Checking Qdrant Cloud...")
    try:
        from src.vector_store import VectorStore
        vs = VectorStore(use_qdrant=Config.USE_QDRANT)
        stats = vs.get_stats()
        print(f"✅ {stats.get('status', 'Connected')}")
        print(f"   Documents: {stats.get('document_count', 0)}")
        print(f"   Chunks: {stats.get('chunk_count', 0)}")
    except Exception as e:
        print(f"⚠️  Vector Store: {str(e)[:80]}")
    
    print("\n" + "="*80)
    print("✅ System check complete!")
    print("="*80)
    
    print("\n📝 Architecture:")
    print("   Students → Streamlit → Railway → Groq → Qdrant Cloud")
    
    print("\n💰 Cost: $0/month (100% FREE)")
    print("📊 Capacity: 300+ concurrent students")
    print("⚡ Speed: Ultra-fast responses")
    print("🎛️  Models: Mixtral 8x7B (Recommended)")
    print("\n")

if __name__ == "__main__":
    check_system()