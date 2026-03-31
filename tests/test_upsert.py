import uuid
from app.ingestion.parsers import parse_file
from app.ingestion.chunker import chunk_text
from app.embeddings.sparse import generate_sparse_embeddings
from app.embeddings.dense import generate_dense_embeddings
from app.retrieval.vector_store import upsert_vectors

business_id = "test-business"
source_id = str(uuid.uuid4())
source = "test.txt"

try:
    print("Testing parser...")
    text = parse_file(b"Hello world from BeeBot!", "test.txt")
    
    print("Testing chunker...")
    chunks = chunk_text(text)
    
    print("Testing sparse embeddings...")
    sparse_emb = generate_sparse_embeddings(chunks)
    
    print("Testing dense embeddings...")
    dense_emb = generate_dense_embeddings(chunks)
    
    vectors_to_upsert = []
    for i, chunk in enumerate(chunks):
        vector_id = f"{business_id}-{source_id}-{i}"
        vectors_to_upsert.append({
            "id": vector_id,
            "values": dense_emb[i],
            "sparse_values": sparse_emb[i],
            "metadata": {
                "business_id": business_id,
                "source": source,
                "source_id": source_id,
                "text": chunk
            }
        })
        
    print("Testing Pinecone upsert...")
    chunks_added = upsert_vectors(vectors_to_upsert)
    print(f"Upsert Success, added {chunks_added}")
    
except Exception as e:
    import traceback
    traceback.print_exc()
    print("FAILED")
