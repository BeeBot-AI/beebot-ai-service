from app.ingestion.parsers import parse_file
from app.ingestion.chunker import chunk_text
from app.embeddings.sparse import generate_sparse_embeddings
from app.embeddings.dense import generate_dense_embeddings

try:
    print("Testing parser...")
    text = parse_file(b"Hello world from BeeBot!", "test.txt")
    print(f"Parsed: {text[:20]}")
    
    print("Testing chunker...")
    chunks = chunk_text(text)
    print(f"Chunks: {len(chunks)}")
    
    print("Testing sparse embeddings...")
    sparse_emb = generate_sparse_embeddings(chunks)
    print(f"Sparse Success, length: {len(sparse_emb)}")
    
    print("Testing dense embeddings...")
    dense_emb = generate_dense_embeddings(chunks)
    print(f"Dense Success, dimension: {len(dense_emb[0]) if dense_emb else 0}")
    
except Exception as e:
    import traceback
    traceback.print_exc()
    print("FAILED")
