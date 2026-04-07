# BeeBot AI Service — FastAPI RAG Pipeline

The BeeBot AI Service is a Python FastAPI application that powers the chatbot's intelligence. It handles document ingestion, vector indexing, hybrid retrieval, and response generation using a RAG (Retrieval-Augmented Generation) pipeline.

**Live URL:** https://beebot-ai-service.onrender.com

---

## Architecture

```
Document Ingestion
        │
        ▼
  Text Chunking (sliding window, 512 tokens, 64 overlap)
        │
        ▼
  HuggingFace Embeddings (dense vectors)  +  BM25 (sparse)
        │
        ▼
  Pinecone Upsert (hybrid index)
        │
        ▼
─────────────────────────────────
         Chat Request
        │
        ▼
  Query Embedding (HuggingFace)
        │
        ▼
  Hybrid Retrieval (dense α + sparse BM25, top-k=5)
        │
        ▼
  Context Assembly → Prompt Construction
        │
        ▼
  Groq LLM (llama3-8b-8192) → Response
```

### Why Hybrid Search?

Pure vector search excels at semantic similarity but misses exact keyword matches (e.g. product names, error codes). BM25 is the opposite — great for exact matches, poor for paraphrases. Combining both (via a weighted alpha parameter) gives the best of both worlds: more accurate retrieval, fewer hallucinations, and better coverage of user queries.

---

## API Endpoints

| Method | Path                              | Auth         | Description                                       |
|--------|-----------------------------------|--------------|---------------------------------------------------|
| `POST` | `/chat`                           | `x-api-key`  | Send a user message; returns AI response          |
| `POST` | `/knowledge/upload-file`          | Internal     | Upload a PDF, DOCX, TXT, or CSV file              |
| `POST` | `/knowledge/url`                  | Internal     | Crawl and index a URL                             |
| `DELETE`| `/knowledge/{source_id}`         | Internal     | Delete a knowledge source and its vectors         |

---

## Environment Variables

| Variable              | Description                                                        |
|-----------------------|--------------------------------------------------------------------|
| `PINECONE_API_KEY`    | Pinecone API key for vector database access                        |
| `PINECONE_INDEX_NAME` | Name of the Pinecone index (must be created first)                 |
| `GROQ_API_KEY`        | Groq API key for LLM inference (llama3-8b-8192)                   |
| `HF_API_KEY`          | HuggingFace API key for embedding model access                     |
| `NODE_BACKEND_URL`    | URL of the Express backend (for internal callbacks)                |
| `ALLOWED_ORIGINS`     | Comma-separated CORS origins                                       |

---

## Local Setup

```bash
# 1. Create and activate virtual environment
cd ai-service
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Create the Pinecone index (run once)
python create_index.py

# 5. Start the development server
uvicorn app.main:app --reload --port 8000
```

The service starts at `http://localhost:8000`.

---

## Celery Async Task Queue

Large file ingestion (PDFs, large DOCX files) is handled asynchronously via **Celery** with a Redis broker. This prevents HTTP timeouts on the upload endpoint:

1. `POST /knowledge/upload-file` receives the file and immediately returns a `task_id`.
2. The Celery worker processes the file in the background: chunking → embedding → Pinecone upsert.
3. The Express backend can poll `/knowledge/status/{task_id}` to check completion.

To start the Celery worker locally:
```bash
celery -A app.celery_app worker --loglevel=info
```

---

## Deployment on Render.com

1. Connect your GitHub repo to Render.
2. Create a new **Web Service** pointing to the `ai-service/` directory.
3. Set **Build Command:** `pip install -r requirements.txt`
4. Set **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add all environment variables in the Render dashboard.
6. Deploy — Render auto-deploys on every push to `main`.
