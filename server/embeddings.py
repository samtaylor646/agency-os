import os
from abc import ABC, abstractmethod
from typing import List
import openai

class EmbeddingProvider(ABC):
    @abstractmethod
    async def get_embedding(self, text: str) -> List[float]:
        """Returns a single vector embedding for a given string."""
        pass

    @abstractmethod
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Returns a list of vector embeddings for batch processing."""
        pass

class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.client = openai.AsyncClient(api_key=api_key)
        self.model = model

    async def get_embedding(self, text: str) -> List[float]:
        response = await self.client.embeddings.create(input=[text], model=self.model)
        return response.data[0].embedding

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        response = await self.client.embeddings.create(input=texts, model=self.model)
        return [data.embedding for data in response.data]

def get_embedding_provider_factory() -> EmbeddingProvider:
    provider_type = os.getenv("EMBEDDING_PROVIDER_TYPE", "openai").lower()
    
    if provider_type == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI provider.")
        return OpenAIEmbeddingProvider(api_key=api_key)
    
    raise ValueError(f"Unsupported embedding provider type: {provider_type}")

# Singleton instance initialized lazily or injected
_embedding_provider_instance = None

def get_embedding_provider() -> EmbeddingProvider:
    global _embedding_provider_instance
    if _embedding_provider_instance is None:
        _embedding_provider_instance = get_embedding_provider_factory()
    return _embedding_provider_instance
