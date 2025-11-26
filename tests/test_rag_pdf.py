from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from src.config import Config

PDF_PATH = "mnt/data/MCA-RAG-Complete-Guide-v2.pdf"

dp = DocumentProcessor()
vs = VectorStore(use_qdrant=Config.USE_QDRANT)

print("Processing PDF...")
chunks = dp.process_pdf(
    PDF_PATH,
    doc_type="notes",
    subject="General",
    year="Year 1"
)
print("Extracted Chunks:", len(chunks))

print("Indexing into Qdrant/Chroma...")
vs.add_documents(chunks)

print("Searching...")
res = vs.search("what is rag?", top_k=5)
print(res[:2])
