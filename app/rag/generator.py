import requests
from app.config import settings
from app.rag.retriever import get_relevant_context

def generate_response(query: str, client_id: str, bot_config: dict) -> str:
    # 1. Retrieve Context
    context = get_relevant_context(query, client_id)
    
    # 2. Build Prompt
    company_name = bot_config.get("company_name", "the company")
    tone = bot_config.get("tone", "Professional")
    custom_instructions = bot_config.get("custom_instructions", "")
    fallback = bot_config.get("fallback_message", "I'm sorry, I don't have that information.")
    
    prompt = f"""You are a helpful customer support agent for {company_name}.
Your tone should be {tone}.

{custom_instructions}

Answer the user's question using ONLY the business context provided below.
If the answer is not contained in the context, you MUST reply with exactly this message: "{fallback}"
Do not hallucinate or make up information. Do not mention that you are an AI or reading from a context.

BUSINESS CONTEXT:
{context}

USER QUESTION:
{query}
"""

    # 3. Call Groq API
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}
        ],
        "temperature": 0.2,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "Sorry, our support system is currently experiencing issues. Please try again later."
