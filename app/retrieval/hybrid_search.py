from app.retrieval.vector_store import get_vector_store

def hybrid_search(query: str, business_id: str, top_k: int = 4):
    """
    Search Pinecone using Langchain Dense Vector Search.
    (BM25 Hybrid is disabled to prevent worker hang during initialization)
    """
    vector_store = get_vector_store()
    
    # Query Pinecone with filter constraints
    results = vector_store.similarity_search(
        query=query,
        k=top_k,
        filter={"business_id": business_id}
    )
    
    return results
