from pinecone_text.sparse import BM25Encoder
import os

# We save the state of BM25 if needed or just initialize a default one.
# For production SaaS, you'd fit this on your corpus. Default works reasonably well.
bm25 = BM25Encoder().default()

def generate_sparse_embeddings(texts: list[str]) -> list[dict]:
    """
    Generate sparse vectors (BM25) for a list of text chunks.
    Used for keyword matching in Hybrid Search.
    Returns format: {"indices": [1,2,3], "values": [0.1, 0.5, 0.4]}
    """
    if not texts:
        return []
    
    sparse_vectors = []
    for text in texts:
        sparse_vectors.append(bm25.encode_documents(text))
        
    return sparse_vectors
    
def encode_queries(queries: list[str]) -> list[dict]:
    """Encode user queries sparsely."""
    sparse_vectors = []
    for query in queries:
        sparse_vectors.append(bm25.encode_queries(query))
        
    return sparse_vectors
