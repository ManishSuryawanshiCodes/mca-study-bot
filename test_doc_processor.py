from src.document_processor import DocumentProcessor

# Initialize
dp = DocumentProcessor()

# Test with a sample PDF (replace with your path)
test_file = "path/to/your/test.pdf"

try:
    chunks = dp.process_pdf(
        test_file,
        doc_type="notes",
        subject="Computer Science",
        year="MCA 1st Year"
    )
    
    print(f"\n✅ Success!")
    print(f"Generated {len(chunks)} chunks")
    
    if chunks:
        print(f"\n📊 Statistics:")
        stats = dp.get_stats(chunks)
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print(f"\n📝 First chunk preview:")
        print(f"Content: {chunks[0]['content'][:200]}...")
        print(f"Metadata: {chunks[0]['metadata']}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
