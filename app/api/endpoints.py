from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from app.workers.tasks import process_document_task
from app.retrieval.vector_store import delete_vectors_by_source
from app.rag_pipeline.generator import generate_answer

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}

@router.post("/knowledge/upload-file")
async def upload_file_endpoint(
    file: UploadFile = File(...),
    business_id: str = Form(...),
    source_id: str = Form("")
):
    """
    Accepts multipart file, validates, and dispatches to Celery Background Worker.
    Returns immediately to keep the API ultra-responsive.
    """
    filename = file.filename
    ext = filename[filename.rfind("."):].lower() if "." in filename else ""
    
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    file_bytes = await file.read()
    
    # 🚨 Dispatch to Celery Worker 🚨
    # Use delay() to send to Redis queue
    process_document_task.delay(
        file_bytes=file_bytes,
        filename=filename,
        business_id=business_id,
        source=filename,
        source_id=source_id
    )
    
    return {
        "success": True, 
        "message": "File processing dispatched to worker queue.",
        "source_id": source_id
    }


class DeleteVectorsRequest(BaseModel):
    business_id: str
    source_id: str

@router.delete("/knowledge/vectors")
async def delete_vectors_endpoint(req: DeleteVectorsRequest):
    """Clean up Pinecone vectors based on source metadata."""
    if not req.business_id or not req.source_id:
        raise HTTPException(status_code=400, detail="Missing required fields")
        
    deleted_count = delete_vectors_by_source(req.business_id, req.source_id)
    return {"success": True, "deleted_count": deleted_count}


# --- Standard Text / FAQ Ingestion --- #
class ProcessRequest(BaseModel):
    text: str
    business_id: str
    source: str
    source_id: str = ""

@router.post("/knowledge/process")
async def process_text_endpoint(req: ProcessRequest):
    """Enqueue raw text / FAQ for async processing."""
    if not req.text or not req.business_id:
        raise HTTPException(status_code=400, detail="Missing text or business_id")
        
    process_document_task.delay(
        file_bytes=req.text.encode("utf-8"),
        filename="text.txt", # Treat as txt
        business_id=req.business_id,
        source=req.source,
        source_id=req.source_id
    )
    return {"success": True, "message": "Text processing enqueued", "source_id": req.source_id}


# --- URL Scraping Ingestion --- #
class UrlRequest(BaseModel):
    url: str
    business_id: str
    source_id: str = ""

@router.post("/knowledge/url")
async def process_url_endpoint(req: UrlRequest):
    """Scrape URL and enqueue text for async processing."""
    if not req.url or not req.business_id:
        raise HTTPException(status_code=400, detail="Missing url or business_id")

    try:
        response = requests.get(req.url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove scripts/styles
        for script in soup(["script", "style", "nav", "footer"]):
            script.extract()
            
        text = soup.get_text(separator="\n", strip=True)
        
        process_document_task.delay(
            file_bytes=text.encode("utf-8"),
            filename="url.txt",
            business_id=req.business_id,
            source=req.url,
            source_id=req.source_id
        )
        return {"success": True, "message": "URL enqueued", "source_id": req.source_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to scrape URL: {str(e)}")


# --- RAG Chat API --- #
class ChatRequest(BaseModel):
    query: str
    business_id: str
    bot_settings: dict = None

@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    """Process query through Hybrid RAG Pipeline and return LLM Answer."""
    if not req.query or not req.business_id:
        raise HTTPException(status_code=400, detail="Missing query or business_id")
        
    result = generate_answer(req.query, req.business_id, req.bot_settings or {})
    return result
