"""
Test RAG Integration
"""
from src.vector_store import VectorStore
from src.llm_groq import GroqLLM
from src.config import Config

# Initialize
vs = VectorStore(use_qdrant=Config.USE_QDRANT)
llm = GroqLLM()

# Test 1: Check if documents are indexed
print("📊 Checking vector store...")
stats = vs.get_stats()
print(f"Total documents: {stats['document_count']}")
print(f"Total chunks: {stats['chunk_count']}")

# Test 2: Search for documents
print("\n🔍 Searching for 'data structures'...")
results = vs.search("data structures", top_k=3)
print(f"Found {len(results)} results")

if results:
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. {doc['metadata']['source']}")
        print(f"   Subject: {doc['metadata'].get('subject', 'N/A')}")
        print(f"   Content preview: {doc['content'][:100]}...")

# Test 3: RAG with LLM
print("\n🤖 Testing RAG with LLM...")
query = "What are data structures?"
response = llm.generate_answer(query, results, [])
print(f"\nAnswer: {response['answer']}")

print("\n✅ RAG Integration Test Complete!")
