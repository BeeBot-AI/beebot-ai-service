import requests
from langchain_core.embeddings import Embeddings
from typing import List

_HF_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
_HF_ROUTER_URL = f"https://router.huggingface.co/hf-inference/models/{_HF_MODEL}/pipeline/feature-extraction"


class HuggingFaceRouterEmbeddings(Embeddings):
    """
    Custom LangChain-compatible embeddings using HuggingFace's new router API.
    The old api-inference.huggingface.co endpoint was retired (410 Gone).
    """

    def _embed(self, texts: List[str]) -> List[List[float]]:
        from app.core.config import settings
        response = requests.post(
            _HF_ROUTER_URL,
            headers={
                "Authorization": f"Bearer {settings.HF_API_KEY}",
                "Content-Type": "application/json",
            },
            json={"inputs": texts},
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()
        # Router returns [[vec], [vec], ...] for a list of inputs
        return result

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self._embed(texts)

    def embed_query(self, text: str) -> List[float]:
        return self._embed([text])[0]


embeddings = HuggingFaceRouterEmbeddings()
