from app.retrieval.vector_store import index
try:
    stats = index.describe_index_stats()
    print("SUCCESS")
    print(stats)
except Exception as e:
    print("FAILED")
    print(str(e))
