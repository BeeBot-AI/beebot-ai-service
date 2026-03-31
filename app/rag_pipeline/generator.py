from app.core.config import settings
from app.retrieval.hybrid_search import hybrid_search
from app.prompts.templates import build_prompt
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

def generate_answer(query: str, business_id: str, bot_settings: dict) -> dict:
    """
    Core RAG orchestrator:
    1. Retrieve relevant chunks using Langchain VectorStore Search
    2. Build context-aware prompt
    3. Generate response using Langchain ChatGroq
    """
    
    # 1. Retrieve
    # Matches are Langchain Document objects now
    matches = hybrid_search(query, business_id, top_k=4)
    
    # Extract sources for citation returned to frontend
    sources_used = list(set([m.metadata.get("source", "Unknown") for m in matches]))
    
    # 2. Build Prompt
    system_message = build_prompt(query, matches)
    
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=query)
    ]
    
    # 3. Call LLM (Langchain ChatGroq)
    try:
        chat_model = ChatGroq(
            temperature=0.1,
            model_name="llama-3.3-70b-versatile",
            groq_api_key=settings.GROQ_API_KEY,
            max_tokens=1024
        )
        
        response = chat_model.invoke(messages)
        
        return {
            "answer": response.content,
            "sources": sources_used,
            "success": True
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"LLM Generation Error: {e}")
        return {
            "answer": "I am experiencing temporary technical difficulties. Please try again later.",
            "sources": [],
            "success": False
        }
