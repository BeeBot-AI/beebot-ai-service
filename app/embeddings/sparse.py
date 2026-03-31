# NOTE: BM25 hybrid search is disabled.
# pinecone-text (BM25Encoder) is excluded from requirements to keep
# the bundle size small for Vercel deployment.
# Pure dense vector search is used instead (see hybrid_search.py).

def generate_sparse_embeddings(texts: list) -> list:
    """Stub: BM25 sparse embeddings are disabled. Dense-only search is active."""
    return []

def encode_queries(queries: list) -> list:
    """Stub: BM25 query encoding is disabled. Dense-only search is active."""
    return []
