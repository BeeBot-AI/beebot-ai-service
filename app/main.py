from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.rag.generator import generate_response
from app.rag.embedder import process_document
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="BeeBot AI Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str
    client_id: str
    bot_config: dict = {}

class DocumentRequest(BaseModel):
    client_id: str
    text: str
    source: str

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        response = generate_response(req.query, req.client_id, req.bot_config)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/documents/process")
async def process_document_endpoint(req: DocumentRequest):
    try:
        chunks_count = process_document(req.text, req.client_id, req.source)
        return {"status": "success", "chunks_added": chunks_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
