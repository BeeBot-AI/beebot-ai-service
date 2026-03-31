import os
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

# Use HuggingFace Inference API instead of loading the model locally.
# This avoids bundling PyTorch/sentence-transformers (~4 GB) into the deployment.
# The model runs on HuggingFace's servers; we just send text and get back vectors.
_hf_api_key = os.getenv("HF_API_KEY", "")

embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=_hf_api_key,
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
