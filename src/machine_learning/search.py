import faiss
import numpy as np


class FaissIndexer:
    def __init__(self, dimension: int) -> None:
        self.dimension = dimension
        self.flat_idx = faiss.IndexFlatL2(dimension)
        self.index = faiss.IndexIDMap(self.flat_idx)

    def add_embeddings(self, embeddings: np.ndarray, ids: np.ndarray) -> None:
        """
        Add embeddings and their corresponding IDs to the index.

        :param embeddings: 2D numpy array of shape (n, dimension)
        :param ids: 1D numpy array of shape (n, ) containing IDs for each embedding
        """
        normalized_embeddings = embeddings
        if embeddings.shape[0] != ids.shape[0]:
            raise ValueError("Embeddings and IDs must have the same number of rows.")

        print(normalized_embeddings.shape)

        self.index.add_with_ids(normalized_embeddings, ids)

    def query(self, embeddings: np.ndarray, top_k: int = 1) -> np.ndarray:
        """
        Query the index with embeddings and get closest IDs.

        :param embeddings: 2D numpy array of shape (n, dimension)
        :param k: Number of closest embeddings to retrieve
        :return: 2D numpy array of shape (n, k) containing k closest IDs for each query embedding
        """
        normalized_embeddings = embeddings
        _, indices = self.index.search(normalized_embeddings, top_k)
        return indices
