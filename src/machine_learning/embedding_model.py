from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss 


class TextEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)
        
    def embed(self, texts: List[str]) -> np.ndarray:
        embeddings = self.model.encode(texts)
        return embeddings


