from langchain_pinecone import PineconeVectorStore
from app.embeddings.dense import embeddings
from app.core.config import settings

def get_vector_store() -> PineconeVectorStore:
    """
    Returns an initialized LangChain PineconeVectorStore matching the BeeBot index.
    """
    return PineconeVectorStore(
        index_name=settings.PINECONE_INDEX_NAME,
        embedding=embeddings,
        pinecone_api_key=settings.PINECONE_API_KEY
    )

def delete_vectors_by_source(business_id: str, source_id: str):
    """Delete all vectors for a specific source ID within a business."""
    # Since we are using standard Langchain add_documents, we don't manually track IDs.
    # Standard practice is to query IDs by metadata to delete, or if using a paid tier,
    # delete by metadata directly.
    
    # We will initialize raw pinecone client purely for deletion
    from pinecone import Pinecone
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    index = pc.Index(settings.PINECONE_INDEX_NAME)
    
    ids_to_check = [f"{business_id}-{source_id}-{i}" for i in range(5000)]
    
    deleted_count = 0
    for i in range(0, len(ids_to_check), 1000):
        batch_ids = ids_to_check[i:i+1000]
        try:
            index.delete(ids=batch_ids)
            deleted_count += len(batch_ids)
        except Exception:
            pass
            
    return deleted_count
