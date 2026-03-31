RAG_SYSTEM_PROMPT = """You are BeeBot, an intelligent and helpful AI assistant for a business.
You MUST answer the user's question strictly using ONLY the provided knowledge context below.

Rules:
1. If the answer is not in the knowledge context, simply say "I'm sorry, I don't have enough information to answer that." Do not guess.
2. Be professional, concise, and helpful.
3. If the user greets you, greet them back in a friendly manner.

Knowledge Context:
{context}
"""

def build_prompt(query: str, retrieved_chunks: list) -> str:
    """Combine chunks into a single context string and format the prompt."""
    if not retrieved_chunks:
        context_str = "No specific knowledge found on this topic."
    else:
        # retrieved_chunks are Langchain Document objects
        # Format them with their source for better LLM grounding
        formatted_chunks = []
        for doc in retrieved_chunks:
            source = doc.metadata.get("source", "Unknown Source")
            text = doc.page_content
            formatted_chunks.append(f"[Source: {source}]\n{text}")
            
        context_str = "\n\n---\n\n".join(formatted_chunks)
        
    system_msg = RAG_SYSTEM_PROMPT.format(context=context_str)
    
    return system_msg
