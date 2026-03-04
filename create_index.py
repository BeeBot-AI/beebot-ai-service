import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = os.getenv("PINECONE_INDEX_NAME", "beebot-index")

# Replace this with the region you want to use
region = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if index_name not in existing_indexes:
    print(f"Creating index '{index_name}'...")
    pc.create_index(
        name=index_name,
        dimension=384, # all-MiniLM-L6-v2 outputs 384 dimensions
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region=region
        )
    )
    print("Index created successfully!")
else:
    print(f"Index '{index_name}' already exists.")
