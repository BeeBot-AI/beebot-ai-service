from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from app.config import settings

# Load model locally
model = SentenceTransformer("all-MiniLM-L6-v2")

pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index(settings.PINECONE_INDEX_NAME)

def get_relevant_context(query: str, client_id: str, top_k: int = 5) -> str:
    query_embedding = model.encode(query).tolist()
    
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter={
            "client_id": {"$eq": client_id}
        }
    )
    
    contexts = []
    for match in results["matches"]:
        if "metadata" in match and "text" in match["metadata"]:
            contexts.append(match["metadata"]["text"])
            
    return "\n\n---\n\n".join(contexts)
