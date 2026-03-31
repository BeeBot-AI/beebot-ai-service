import uuid
import asyncio
from app.workers.tasks import process_document_task
from app.rag_pipeline.generator import generate_answer

def run_test():
    business_id = "test-business"
    source_id = str(uuid.uuid4())
    
    print("1. Testing Langchain Ingestion Pipeline...")
    try:
        result = process_document_task(
            file_bytes=b"BeeBot is an intelligent customer support AI created for SaaS companies. It uses modern RAG to answer queries accurately.",
            filename="beebot_info.txt",
            business_id=business_id,
            source="beebot_info.txt",
            source_id=source_id
        )
        print(f"Ingestion Result: {result}")
    except Exception as e:
        print(f"Ingestion Failed: {e}")
        return
        
    print("\n2. Testing Langchain Generation Pipeline...")
    try:
        # Wait a sec for Pinecone index propagation
        import time
        time.sleep(2)
        
        chat_result = generate_answer(
            query="What is BeeBot?",
            business_id=business_id,
            bot_settings={}
        )
        print(f"Chat Result: {chat_result['answer']}")
        print(f"Sources Used: {chat_result['sources']}")
        
    except Exception as e:
        print(f"Generation Failed: {e}")

if __name__ == "__main__":
    run_test()
