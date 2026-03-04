from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from app.config import settings
import uuid

# Load model locally (downloads the first time)
model = SentenceTransformer("all-MiniLM-L6-v2")

pc = Pinecone(api_key=settings.PINECONE_API_KEY)
# In production, ensure the index exists before initializing
index = pc.Index(settings.PINECONE_INDEX_NAME)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
)

def process_document(text: str, client_id: str, source: str) -> int:
    chunks = text_splitter.split_text(text)
    
    if not chunks:
        return 0
        
    embeddings = model.encode(chunks).tolist()
    
    vectors_to_upsert = []
    for i, chunk in enumerate(chunks):
        vector_id = f"{client_id}-{source}-{uuid.uuid4()}"
        vectors_to_upsert.append({
            "id": vector_id,
            "values": embeddings[i],
            "metadata": {
                "client_id": client_id,
                "source": source,
                "text": chunk
            }
        })
    
    # Batch upsert to Pinecone
    batch_size = 100
    for i in range(0, len(vectors_to_upsert), batch_size):
        batch = vectors_to_upsert[i:i + batch_size]
        index.upsert(vectors=batch)
        
    return len(vectors_to_upsert)
