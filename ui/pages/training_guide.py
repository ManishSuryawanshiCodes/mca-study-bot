import streamlit as st

def training_guide():
    """Complete guide on training and using the system"""
    
    st.markdown("""
    <div class="chat-header">
        <div class="chat-header-title">🎓 Training & Setup Guide</div>
        <div class="chat-header-subtitle">How to use and train the MCA Study Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Training steps
    st.markdown("""
    ## 📚 Step-by-Step Training Guide
    
    ### Step 1: Upload Your Materials
    
    1. Click on **📁 Upload** in the sidebar
    2. Enter the admin password (default: `ADMin@manish`)
    3. Select PDF files from your computer
    4. Click **📤 Upload & Process Files**
    
    The system will:
    - Extract text from PDFs
    - Split into chunks (500 words each)
    - Create embeddings using AI
    - Store in vector database
    
    ### Step 2: What Gets Stored
    
    Each uploaded PDF is processed as follows:
    
    ```
    PDF File
       ↓
    Text Extraction
       ↓
    Chunking (500 word chunks)
       ↓
    Embedding Generation
       ↓
    Vector Storage (Qdrant)
    ```
    
    ### Step 3: Start Chatting
    
    1. Go to **💬 Chat**
    2. Type your question
    3. The system will:
       - Search for relevant chunks
       - Generate an answer using Gemini AI
       - Provide source references
    
    ### Step 4: Tips for Better Results
    
    ✅ **Do:**
    - Upload clear, well-structured PDFs
    - Ask specific questions
    - Provide context in your questions
    - Use keywords from materials
    
    ❌ **Don't:**
    - Upload corrupted PDFs
    - Ask vague questions
    - Upload non-academic materials
    - Expect exact sentence matches
    
    ---
    
    ## 🔧 Technical Details
    
    ### Configuration
    
    Open `src/config.py` to customize:
    
    ```python
    CHUNK_SIZE = 500           # Words per chunk
    CHUNK_OVERLAP = 100        # Overlap between chunks
    TOP_K_RESULTS = 5          # Search results to use
    LLM_MODEL = "gemini-2.0-flash-exp"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    ```
    
    ### Vector Database Setup
    
    **Option 1: Using Qdrant Cloud (Current)**
    
    Set in `.env`:
    ```
    QDRANT_URL=https://your-url.cloud.qdrant.io:6333
    QDRANT_API_KEY=your-api-key
    USE_QDRANT=True
    ```
    
    **Option 2: Using Local ChromaDB**
    
    Set in `.env`:
    ```
    QDRANT_URL=
    QDRANT_API_KEY=
    USE_QDRANT=False
    ```
    
    ---
    
    ## 🧪 Testing
    
    ### Test 1: Simple Greeting
    
    **Input:** "hello"
    
    **Expected Output:** "Hello! 👋 How can I help you with your MCA studies today?"
    
    ### Test 2: Without Documents
    
    **Input:** "What is Python?"
    
    **Expected Output:** General knowledge answer about Python
    
    ### Test 3: With Documents
    
    1. Upload a Python tutorial PDF
    2. **Input:** "Explain list comprehension from the materials"
    3. **Expected Output:** Answer based on the uploaded document
    
    ### Test 4: Follow-up Questions
    
    1. Ask a question and get an answer
    2. Ask a follow-up: "Can you explain more?"
    3. **Expected:** System remembers context
    
    ---
    
    ## 📊 Sample Test Code
    
    ### Test the LLM directly
    
    ```python
    from src.llm_interface import LLMInterface
    from src.config import Config
    
    # Initialize
    llm = LLMInterface()
    
    # Test 1: Greeting
    response = llm.generate_answer("hello")
    print(response["answer"])
    
    # Test 2: General question
    response = llm.generate_answer("What is machine learning?")
    print(response["answer"])
    ```
    
    ### Test the Vector Store
    
    ```python
    from src.vector_store import VectorStore
    
    # Initialize
    vs = VectorStore(use_qdrant=True)
    
    # Search
    results = vs.search("Python programming", n_results=3)
    for doc in results:
        print(doc["content"][:200])
    ```
    
    ### Test Document Processing
    
    ```python
    from src.document_processor import DocumentProcessor
    
    # Initialize
    dp = DocumentProcessor()
    
    # Process PDF
    chunks = dp.process_pdf("path/to/document.pdf")
    print(f"Created {len(chunks)} chunks")
    
    for chunk in chunks[:3]:
        print(chunk["content"][:100])
    ```
    
    ---
    
    ## 🐛 Troubleshooting
    
    ### "Error: API Key Invalid"
    - Check `.env` file has correct `GOOGLE_API_KEY`
    - Regenerate key from Google Cloud Console
    
    ### "No results found"
    - Upload documents first in Upload section
    - Wait for processing to complete
    - Check vector store status
    
    ### "Response is slow"
    - Reduce `TOP_K_RESULTS` in config
    - Use fewer documents
    - Check internet connection
    
    ### "PDF not processing"
    - Ensure PDF is not corrupted
    - Try a different PDF
    - Check file format (must be .pdf)
    
    ---
    
    ## 📈 Performance Tips
    
    1. **Optimize Chunks:** Smaller chunks = faster search, less context
    2. **Update Embeddings:** Re-embed if you change embedding model
    3. **Clean Data:** Remove unnecessary PDFs from storage
    4. **Monitor API Usage:** Check Google Cloud Console for API calls
    
    """, unsafe_allow_html=True)
    
    # Quick reference
    st.markdown("""
    <div class="glass-surface">
        <h3 style="color: #ffffff; margin-top: 0;">🚀 Quick Reference</h3>
        
        <strong>Admin Password:</strong> ADMin@manish<br>
        <strong>Default Chunk Size:</strong> 500 words<br>
        <strong>Max Search Results:</strong> 5<br>
        <strong>Supported Format:</strong> PDF only<br>
        <strong>API:</strong> Google Gemini 2.0 Flash<br>
        <strong>Vector DB:</strong> Qdrant Cloud<br>
    </div>
    """, unsafe_allow_html=True)