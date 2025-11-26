"""
Vector Store Module - Qdrant Cloud Edition
Supports 300+ concurrent students with proper document tracking
"""
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct, Filter, 
    FieldCondition, MatchValue, PayloadSchemaType
)
from sentence_transformers import SentenceTransformer
from src.config import Config
from typing import List, Dict, Optional
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
import hashlib

class VectorStore:
    """Vector store with Qdrant Cloud support"""

    def __init__(self, use_qdrant: bool = True):
        """Initialize vector store"""
        self.use_qdrant = use_qdrant or Config.USE_QDRANT
        
        print(f"Loading embedding model: {Config.EMBEDDING_MODEL}...")
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        print("✓ Embedding model loaded")
        
        if self.use_qdrant:
            self._init_qdrant()
        else:
            self._init_chromadb()

    def _create_payload_indexes(self):
        """Create payload indexes for efficient filtering"""
        try:
            if self.use_qdrant:
                indexes_to_create = [
                    ("type", PayloadSchemaType.KEYWORD),
                    ("subject", PayloadSchemaType.KEYWORD),
                    ("year", PayloadSchemaType.KEYWORD),
                    ("source", PayloadSchemaType.KEYWORD)
                ]
                for field_name, schema_type in indexes_to_create:
                    try:
                        self.client.create_payload_index(
                            collection_name=Config.COLLECTION_NAME,
                            field_name=field_name,
                            field_schema=schema_type
                        )
                        print(f"✓ Created index for '{field_name}'")
                    except Exception as e:
                        error_msg = str(e).lower()
                        if "already exists" not in error_msg and "cannot create" not in error_msg:
                            print(f"⚠️ Index warning for '{field_name}': {e}")
        except Exception as e:
            print(f"⚠️ Error creating payload indexes: {e}")

    def _init_qdrant(self):
        """Initialize Qdrant Cloud client with payload indexes"""
        try:
            self.client = QdrantClient(
                url=Config.QDRANT_URL,
                api_key=Config.QDRANT_API_KEY,
                timeout=60,
                prefer_grpc=False
            )
            
            collections = self.client.get_collections()
            collection_exists = any(
                c.name == Config.COLLECTION_NAME 
                for c in collections.collections
            )
            if not collection_exists:
                self.client.create_collection(
                    collection_name=Config.COLLECTION_NAME,
                    vectors_config=VectorParams(
                        size=384,  # MiniLM-L6-v2 embedding size
                        distance=Distance.COSINE
                    )
                )
                print(f"✅ Created Qdrant collection: {Config.COLLECTION_NAME}")
            else:
                print(f"✅ Qdrant collection '{Config.COLLECTION_NAME}' exists")
            
            self._create_payload_indexes()
            print("✅ Qdrant Cloud connected successfully")
        except Exception as e:
            print(f"❌ Qdrant connection error: {str(e)}")
            raise RuntimeError(f"Qdrant connection failed: {str(e)}")

    def _init_chromadb(self):
        """Initialize ChromaDB (fallback)"""
        try:
            self.client = chromadb.PersistentClient(
                path=Config.CHROMA_PERSIST_DIR
            )
            self.collection = self.client.get_or_create_collection(
                name=Config.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            print("✅ ChromaDB initialized (fallback mode)")
        except Exception as e:
            raise RuntimeError(f"ChromaDB init failed: {str(e)}")

    def get_uploaded_documents(self, limit=1000):
        """Return a list of all uploaded documents (distinct by source/subject/year/type)."""
        docs = []
        try:
            if self.use_qdrant:
                scroll_result = self.client.scroll(
                    collection_name=Config.COLLECTION_NAME,
                    limit=limit,
                    with_payload=True
                )
                unique_keys = set()
                for point in scroll_result[0]:
                    payload = point.payload
                    key = (
                        payload.get("source", ""),
                        payload.get("subject", ""),
                        payload.get("year", ""),
                        payload.get("type", "")
                    )
                    if key not in unique_keys:
                        unique_keys.add(key)
                        docs.append({
                            "source": payload.get("source", ""),
                            "subject": payload.get("subject", ""),
                            "year": payload.get("year", ""),
                            "type": payload.get("type", ""),
                            "page": payload.get("page", None),
                            "uploaded": True
                        })
                # Sort by subject then year etc.
                docs = sorted(docs, key=lambda d: (d["subject"], d["year"], d["type"], d["source"]))
            else:
                # Chroma fallback (example, not guaranteed)
                results = self.collection.get(limit=limit)
                seen = set()
                for meta in results["metadatas"]:
                    key = (
                        meta.get("source", ""),
                        meta.get("subject", ""),
                        meta.get("year", ""),
                        meta.get("type", "")
                    )
                    if key not in seen:
                        seen.add(key)
                        docs.append({
                            "source": meta.get("source", ""),
                            "subject": meta.get("subject", ""),
                            "year": meta.get("year", ""),
                            "type": meta.get("type", ""),
                            "page": meta.get("page", None),
                            "uploaded": True
                        })
            return docs
        except Exception as e:
            print(f"Error loading uploaded docs: {e}")
            return []

    def add_documents(self, chunks: List[Dict], batch_size: int = 100) -> Dict:
        """
        Add documents to vector store in batches
        
        Args:
            chunks: List of dicts with 'content' and 'metadata' keys
            batch_size: Number of documents to process at once
        """
        try:
            if not chunks:
                return {
                    "status": "error",
                    "message": "No chunks provided"
                }
            total_added = 0
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i + batch_size]
                points = []
                for chunk in batch:
                    if 'content' not in chunk or 'metadata' not in chunk:
                        print(f"⚠️ Skipping invalid chunk: {chunk}")
                        continue
                    embedding = self.embedding_model.encode(chunk['content'])
                    content_hash = hashlib.md5(
                        (chunk['content'] + str(chunk['metadata'])).encode()
                    ).hexdigest()
                    if self.use_qdrant:
                        point_id = int(content_hash[:16], 16) % (2**63 - 1)
                        points.append(
                            PointStruct(
                                id=point_id,
                                vector=embedding.tolist(),
                                payload={
                                    "text": chunk['content'],
                                    "source": chunk['metadata'].get('source', 'Unknown'),
                                    "type": chunk['metadata'].get('type', 'general'),
                                    "subject": chunk['metadata'].get('subject', 'General'),
                                    "year": chunk['metadata'].get('year', 'N/A'),
                                    "page": chunk['metadata'].get('page', 'N/A'),
                                    **chunk['metadata']
                                }
                            )
                        )
                    else:
                        self.collection.add(
                            ids=[content_hash],
                            embeddings=[embedding.tolist()],
                            documents=[chunk['content']],
                            metadatas=[chunk['metadata']]
                        )
                if self.use_qdrant and points:
                    self.client.upsert(
                        collection_name=Config.COLLECTION_NAME,
                        points=points
                    )
                    total_added += len(points)
                elif not self.use_qdrant:
                    total_added += len(batch)
                print(f"✓ Processed batch {i//batch_size + 1}: {len(points)} documents")
            return {
                "status": "success",
                "documents_added": total_added,
                "message": f"✅ Added {total_added} documents to {Config.COLLECTION_NAME}"
            }
        except Exception as e:
            print(f"❌ Error adding documents: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to add documents: {str(e)}"
            }

    def search(
        self, 
        query: str, 
        top_k: int = 5, 
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search documents with optional filters
        
        Args:
            query: Search query text
            top_k: Number of results to return
            filters: Dict with 'subject', 'year', 'type' filters
        """
        try:
            query_embedding = self.embedding_model.encode(query)
            if self.use_qdrant:
                search_filter = None
                if filters:
                    conditions = []
                    for key, value in filters.items():
                        if value and value != "All":
                            conditions.append(
                                FieldCondition(
                                    key=key,
                                    match=MatchValue(value=value)
                                )
                            )
                    if conditions:
                        search_filter = Filter(must=conditions)
                results = self.client.search(
                    collection_name=Config.COLLECTION_NAME,
                    query_vector=query_embedding.tolist(),
                    limit=top_k,
                    score_threshold=0.3,
                    query_filter=search_filter,
                    with_payload=True
                )
                documents = []
                for r in results:
                    documents.append({
                        'text': r.payload.get('text', ''),
                        'metadata': {
                            'source': r.payload.get('source', 'Unknown'),
                            'type': r.payload.get('type', 'general'),
                            'subject': r.payload.get('subject', 'General'),
                            'year': r.payload.get('year', 'N/A'),
                            'page': r.payload.get('page', 'N/A')
                        },
                        'score': r.score
                    })
                return documents
            else:
                where_filter = None
                if filters:
                    where_filter = {
                        k: v for k, v in filters.items() 
                        if v and v != "All"
                    }
                results = self.collection.query(
                    query_embeddings=[query_embedding.tolist()],
                    n_results=top_k,
                    where=where_filter
                )
                documents = []
                if results['documents']:
                    for i, doc in enumerate(results['documents'][0]):
                        documents.append({
                            'text': doc,
                            'metadata': results['metadatas'][0][i] if i < len(results['metadatas'][0]) else {},
                            'distance': results['distances'][0][i] if i < len(results['distances'][0]) else 0
                        })
                return documents
        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            return []
        
    def delete_document_by_metadata(self, source, subject, year, doc_type):
        """Delete by metadata (Qdrant Cloud, correct API)"""
        try:
            if self.use_qdrant:
                qdrant_filter = Filter(
                    must=[
                        FieldCondition(key="source", match=MatchValue(value=source)),
                        FieldCondition(key="subject", match=MatchValue(value=subject)),
                        FieldCondition(key="year", match=MatchValue(value=year)),
                        FieldCondition(key="type", match=MatchValue(value=doc_type)),
                    ]
                )
                resp = self.client.delete(
                    collection_name=Config.COLLECTION_NAME,
                    filter=qdrant_filter,
                    wait=True
                )
                return True  # If no exception, it's fine
            else:
                return False
        except Exception as e:
            print(f"Delete error: {e}")
            return False



    def get_stats(self) -> Dict:
        """Get vector store statistics"""
        try:
            if self.use_qdrant:
                info = self.client.get_collection(Config.COLLECTION_NAME)
                return {
                    "document_count": info.points_count,
                    "chunk_count": info.points_count,
                    "embedding_count": info.points_count,
                    "status": "✅ Qdrant Cloud",
                    "provider": "Qdrant"
                }
            else:
                count = self.collection.count()
                return {
                    "document_count": count,
                    "chunk_count": count,
                    "embedding_count": count,
                    "status": "✅ ChromaDB",
                    "provider": "ChromaDB"
                }
        except Exception as e:
            return {
                "document_count": 0,
                "chunk_count": 0,
                "embedding_count": 0,
                "status": f"❌ Error: {str(e)}",
                "provider": "Error"
            }

    def get_document_stats_by_type(self) -> Dict:
        """Get count of documents by type for dashboard"""
        try:
            if self.use_qdrant:
                stats = {}
                doc_types = ["notes", "assignments", "question_papers", "textbooks", "syllabus"]
                for doc_type in doc_types:
                    try:
                        scroll_result = self.client.scroll(
                            collection_name=Config.COLLECTION_NAME,
                            scroll_filter=Filter(
                                must=[FieldCondition(
                                    key="type",
                                    match=MatchValue(value=doc_type)
                                )]
                            ),
                            limit=10000,
                            with_payload=True
                        )
                        unique_sources = set()
                        for point in scroll_result[0]:
                            source = point.payload.get("source", "")
                            if source:
                                unique_sources.add(source)
                        stats[doc_type] = len(unique_sources)
                    except Exception as e:
                        print(f"⚠️ Error getting stats for '{doc_type}': {e}")
                        stats[doc_type] = 0
                return stats
            else:
                stats = {}
                doc_types = ["notes", "assignments", "question_papers", "textbooks", "syllabus"]
                for doc_type in doc_types:
                    results = self.collection.get(
                        where={"type": doc_type}
                    )
                    unique_sources = set()
                    if results and 'metadatas' in results:
                        for metadata in results['metadatas']:
                            source = metadata.get("source", "")
                            if source:
                                unique_sources.add(source)
                    stats[doc_type] = len(unique_sources)
                return stats
        except Exception as e:
            print(f"❌ Error getting document stats: {str(e)}")
            return {
                "notes": 0,
                "assignments": 0,
                "question_papers": 0,
                "textbooks": 0,
                "syllabus": 0
            }

    def delete_collection(self) -> Dict:
        """Delete collection (admin only)"""
        try:
            if self.use_qdrant:
                self.client.delete_collection(Config.COLLECTION_NAME)
                self.client.create_collection(
                    collection_name=Config.COLLECTION_NAME,
                    vectors_config=VectorParams(
                        size=384,
                        distance=Distance.COSINE
                    )
                )
                self._create_payload_indexes()
            else:
                self.client.delete_collection(Config.COLLECTION_NAME)
                self._init_chromadb()
            return {
                "status": "success",
                "message": "✅ Collection cleared and recreated"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"❌ Failed to delete collection: {str(e)}"
            }

    def delete_document_by_metadata(self, source, subject, year, doc_type):
        """
        Delete all chunks for a document with matching metadata fields in Qdrant Cloud.
        Returns True if successful, False otherwise.
        """
        try:
            if self.use_qdrant:
                filt = Filter(
                    must=[
                        FieldCondition(key="source", match=MatchValue(value=source)),
                        FieldCondition(key="subject", match=MatchValue(value=subject)),
                        FieldCondition(key="year", match=MatchValue(value=year)),
                        FieldCondition(key="type", match=MatchValue(value=doc_type)),
                    ]
                )
                resp = self.client.delete(
                    collection_name=Config.COLLECTION_NAME,
                    points_selector=filt,
                    wait=True
                )
                return True  # If no exception is thrown, deletion is successful
            else:
                return False
        except Exception as e:
            print(f"Delete error: {e}")
            return False
