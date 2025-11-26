"""
Document Processor Module
Handles PDF loading, text extraction, chunking, and math-aware splitting.
"""

from typing import List, Dict
import PyPDF2
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.config import Config
import os
import re


class DocumentProcessor:
    """Process PDF documents for RAG"""

    def __init__(self):
        self.chunk_size = Config.CHUNK_SIZE
        self.chunk_overlap = Config.CHUNK_OVERLAP

        # Regular text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    # ----------------------------------------------------------------

    def detect_math_content(self, text: str) -> bool:
        """
        Detect if text contains mathematical content
        
        Args:
            text: Text to analyze
            
        Returns:
            True if math content detected
        """
        # Math patterns to look for
        math_patterns = [
            r'\d+\s*[+\-*/=]\s*\d+',  # Basic arithmetic: 5 + 3
            r'[a-zA-Z]\s*[+\-*/=]\s*[a-zA-Z]',  # Variables: x + y
            r'\\frac|\\sqrt|\\sum|\\int|\\prod',  # LaTeX commands
            r'\^|\^\{',  # Exponents: x^2
            r'∑|∫|√|≈|≠|≤|≥|π|θ|α|β|γ|Δ',  # Math symbols
            r'\b(equation|formula|theorem|proof|lemma|sin|cos|tan|log)\b',  # Math keywords
            r'\([a-zA-Z0-9\s+\-*/=]+\)',  # Expressions in parentheses
        ]
        
        for pattern in math_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False

    # ----------------------------------------------------------------

    def chunk_with_math_preservation(self, text: str, chunk_size: int) -> List[str]:
        """
        Chunk text while trying to keep mathematical expressions together
        
        Args:
            text: Text to chunk
            chunk_size: Maximum chunk size
            
        Returns:
            List of text chunks
        """
        # Split by double newlines first (paragraphs)
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # If adding this paragraph exceeds chunk size
            if len(current_chunk) + len(paragraph) + 2 > chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
            
            # Add paragraph to current chunk
            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

    # ----------------------------------------------------------------

    def extract_text_with_layout(self, file_path: str) -> List[Dict]:
        """
        Extract text while preserving page number and layout.
        Uses pdfplumber (best for clean extraction).
        Falls back to PyPDF2 if pdfplumber fails.
        """
        pages_content = []

        # Try pdfplumber first
        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text()
                    if text and text.strip():
                        pages_content.append({
                            "page_number": page_num,
                            "text": text.strip(),
                            "has_math": self.detect_math_content(text)
                        })
                        
            if pages_content:
                print(f"✓ pdfplumber extracted {len(pages_content)} pages")
                return pages_content
                
        except Exception as e:
            print(f"⚠️ pdfplumber failed: {e}")

        # Fallback to PyPDF2
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(reader.pages, start=1):
                    try:
                        text = page.extract_text()
                        if text and text.strip():
                            pages_content.append({
                                "page_number": page_num,
                                "text": text.strip(),
                                "has_math": self.detect_math_content(text)
                            })
                    except Exception as e:
                        print(f"⚠️ Error on page {page_num}: {e}")
                        continue
                        
            print(f"✓ PyPDF2 extracted {len(pages_content)} pages")
            
        except Exception as e:
            print(f"❌ PyPDF2 also failed: {e}")

        return pages_content

    # ----------------------------------------------------------------

    def chunk_document(self, pages_content: List[Dict], metadata: Dict) -> List[Dict]:
        """
        Split PDF into text chunks while keeping formulas together.
        """
        all_chunks = []

        for page_data in pages_content:
            page_num = page_data["page_number"]
            text = page_data["text"]
            has_math = page_data["has_math"]

            # Use math-aware chunking if needed
            if has_math:
                chunks = self.chunk_with_math_preservation(text, self.chunk_size)
            else:
                chunks = self.text_splitter.split_text(text)

            # Attach metadata to each chunk
            for i, chunk in enumerate(chunks):
                if chunk.strip():  # Only add non-empty chunks
                    chunk_doc = {
                        "content": chunk.strip(),  # Changed from "text" to "content" for vector store compatibility
                        "metadata": {
                            **metadata,
                            "page": page_num,
                            "chunk_id": i,
                            "total_chunks": len(chunks),
                            "has_math": has_math
                        }
                    }
                    all_chunks.append(chunk_doc)

        return all_chunks

    # ----------------------------------------------------------------

    def process_pdf(
        self,
        file_path: str,
        doc_type: str = "notes",
        subject: str = "General",
        year: str = "MCA 1st Year"
    ) -> List[Dict]:
        """
        Full processing pipeline:
        1. Extract text
        2. Detect math
        3. Chunk with metadata
        
        Args:
            file_path: Path to PDF file
            doc_type: Document type (notes, assignments, question_papers, textbooks, syllabus)
            subject: Subject name
            year: Academic year
            
        Returns:
            List of chunks with metadata
        """
        print(f"\n📄 Processing: {os.path.basename(file_path)}")
        
        # Validate file exists
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return []
        
        # Extract text from PDF
        pages_content = self.extract_text_with_layout(file_path)
        
        if not pages_content:
            print(f"⚠️ No text extracted from {file_path}")
            return []

        # File-level metadata (stored in Qdrant)
        metadata = {
            "source": os.path.basename(file_path),
            "type": doc_type,
            "subject": subject,
            "year": year,
            "file_path": file_path,
            "total_pages": len(pages_content)
        }

        # Convert PDF → chunks
        chunks = self.chunk_document(pages_content, metadata)

        print(f"✓ Created {len(chunks)} chunks from {len(pages_content)} pages")

        return chunks

    # ----------------------------------------------------------------

    def batch_process(
        self, 
        file_paths: List[str], 
        doc_type: str = "notes",
        subject: str = "General",
        year: str = "MCA 1st Year",
        batch_size: int = 10
    ) -> List[Dict]:
        """
        Process multiple PDFs in batches.
        Useful when uploading 20–50 PDFs at once.
        
        Args:
            file_paths: List of PDF file paths
            doc_type: Document type
            subject: Subject name
            year: Academic year
            batch_size: Number of files to process at once
            
        Returns:
            List of all chunks from all files
        """
        all_chunks = []
        total_files = len(file_paths)

        print(f"\n📁 Processing {total_files} files in batches of {batch_size}")

        for i in range(0, total_files, batch_size):
            batch = file_paths[i:i + batch_size]
            batch_num = (i // batch_size) + 1

            print(f"\n📦 Batch {batch_num}/{(total_files + batch_size - 1) // batch_size}")

            for file_path in batch:
                try:
                    chunks = self.process_pdf(
                        file_path,
                        doc_type=doc_type,
                        subject=subject,
                        year=year
                    )
                    all_chunks.extend(chunks)
                except Exception as e:
                    print(f"❌ Error processing {file_path}: {e}")

            processed_count = min(i + batch_size, total_files)
            print(f"✓ Processed {processed_count}/{total_files} files")

        print(f"\n✅ Total: {len(all_chunks)} chunks from {total_files} files")
        
        return all_chunks
    
    # ----------------------------------------------------------------
    
    def get_stats(self, chunks: List[Dict]) -> Dict:
        """
        Get statistics about processed chunks
        
        Args:
            chunks: List of processed chunks
            
        Returns:
            Dictionary with statistics
        """
        if not chunks:
            return {
                'total_chunks': 0,
                'unique_sources': 0,
                'avg_chunk_size': 0,
                'math_chunks': 0,
                'pages_processed': 0
            }
        
        unique_sources = set()
        total_length = 0
        math_chunks = 0
        total_pages = 0
        
        for chunk in chunks:
            metadata = chunk.get('metadata', {})
            unique_sources.add(metadata.get('source', 'Unknown'))
            total_length += len(chunk.get('content', ''))
            if metadata.get('has_math', False):
                math_chunks += 1
            # Count unique pages
            if 'total_pages' in metadata:
                total_pages = max(total_pages, metadata['total_pages'])
        
        return {
            'total_chunks': len(chunks),
            'unique_sources': len(unique_sources),
            'avg_chunk_size': total_length // len(chunks) if chunks else 0,
            'math_chunks': math_chunks,
            'pages_processed': total_pages,
            'sources': list(unique_sources)
        }
