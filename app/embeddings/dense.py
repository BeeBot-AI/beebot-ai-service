from langchain_huggingface import HuggingFaceEmbeddings

# Load model once at startup for LangChain compatibility
# Explicitly use CPU to prevent CUDA multiprocessing crash in Celery prefork workers
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)
