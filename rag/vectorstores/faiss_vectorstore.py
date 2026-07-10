"""
FAISS vector store.
"""
import pickle
from pathlib import Path
from utils.logger import logger
import faiss
import numpy as np
from langchain_core.documents import Document
from rag.vectorstores.base_vectorstore import BaseVectorStore

class FAISSStore(BaseVectorStore):
    """
    FAISS vector store.
    """

    def __init__(self,index_path: Path,metadata_path: Path,) :

        self.index_path = index_path
        self.metadata_path = metadata_path
        self.index = None
        self.documents = []

    def build(self, documents, embeddings):
        """build FAISS index"""
        vectors=np.array(embeddings,dtype=np.float32,)
        dimensions=vectors.shape[1]
        self.index=faiss.IndexFlatIP(dimensions)
        self.index.add(vectors)
        self.documents=documents

        logger.info("created FAISS index with %d vectors",len(documents),)

    def save(self):
        """save FAISS index"""
        self.index_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

        self.metadata_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            str(self.index_path),
        )

        with open(
            self.metadata_path,
            "wb",
        ) as file:

            pickle.dump(
                self.documents,
                file,
            )

        logger.info("Saved vector store")

    def load(self):
        """load FAISS index"""

        self.index=faiss.read_index(str(self.index_path))
        with open(self.metadata_path,"rb")as f:
            self.documents=pickle.load(f)

        logger.info("Loaded vector store")

    def search(self, query_embedding, top_k = 5):
        """search the FAISS index"""

        if self.index is None:
            raise RuntimeError("Vector store is not loaded")
        
        query=np.array([query_embedding],dtype=np.float32,)
        _,indices=self.index.search(query,top_k,)
        
        return [self.documents[i] for i in indices[0] if i !=-1]
