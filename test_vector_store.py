from src.vector_store import VectorStore
from src.config import Config

# Test connection
vs = VectorStore(use_qdrant=True)

# Get stats
stats = vs.get_stats()
print(f"Stats: {stats}")

# Get document stats by type
doc_stats = vs.get_document_stats_by_type()
print(f"Document Stats: {doc_stats}")

# Test search
results = vs.search("What is polymorphism?", top_k=3)
print(f"Search Results: {len(results)} found")
