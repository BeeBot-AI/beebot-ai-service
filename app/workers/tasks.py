import uuid
import requests
import time
import logging
from app.ingestion.parsers import parse_file
from app.ingestion.chunker import text_splitter
from app.retrieval.vector_store import get_vector_store

import os

# In a real SaaS, this would be loaded from config
NODE_BACKEND_URL = os.getenv("NODE_BACKEND_URL", "http://localhost:5000/api")

def process_document_task(file_bytes: bytes, filename: str, business_id: str, source: str, source_id: str):
    """
    Background job to parse, chunk, embed, and store document in Pinecone via Langchain.
    Now running natively via FastAPI BackgroundTasks (No Redis/Celery required!)
    """
    retries = 3
    for attempt in range(retries):
        try:
            # 1. Parse File into Langchain Documents
            docs = parse_file(file_bytes, filename)
            
            # 2. Chunk Documents
            chunks = text_splitter.split_documents(docs)
            if not chunks:
                _notify_backend_status(business_id, source_id, "done", 0)
                return {"status": "success", "chunks": 0}

            # 3. Enrich Metadata before embedding
            effective_source_id = source_id or str(uuid.uuid4())
            
            # Add required metadata for multi-tenant filtering to every chunk
            chunk_ids = []
            for i, chunk in enumerate(chunks):
                # Maintain source info from the loader, but add business logic
                chunk.metadata.update({
                    "business_id": business_id,
                    "source": source,
                    "source_id": effective_source_id,
                    "chunk_index": i
                })

                # Create deterministic IDs based on our pattern
                chunk_ids.append(f"{business_id}-{effective_source_id}-{i}")
                
            # 4. Embed and Store in Pinecone via Langchain VectorStore
            # add_documents automatically embeds and upserts
            vector_store = get_vector_store()
            ids = vector_store.add_documents(chunks, ids=chunk_ids)
            chunks_added = len(ids)
            
            # 5. Notify Backend (MongoDB update) - fire and forget from worker
            _notify_backend_status(business_id, source_id, "done", chunks_added)
            
            return {"status": "success", "chunks_added": chunks_added}
            
        except Exception as exc:
            logging.error(f"Error processing doc (Attempt {attempt + 1}/{retries}): {exc}")
            if attempt == retries - 1:
                _notify_backend_status(business_id, source_id, "failed", 0)
                return {"status": "failed"}
            time.sleep(10) # Retrying after 10 seconds

def _notify_backend_status(business_id: str, source_id: str, status: str, chunks_added: int):
    """Helper to update Node.js backend on job completion."""
    try:
        response = requests.post(
            f"{NODE_BACKEND_URL}/knowledge/webhook/status",
            json={
                "source_id": source_id,
                "status": status,
                "chunks_added": chunks_added
            },
            timeout=5
        )
        response.raise_for_status()
    except Exception as e:
        import logging
        logging.error(f"Failed to notify backend for {source_id}: {e}")
