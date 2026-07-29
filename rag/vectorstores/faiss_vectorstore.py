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
        """
        Initialize the FAISS vector store.

        Args:
            index_path: Path to the FAISS index file.
            metadata_path: Path to the metadata file.
        """

        self.index_path = index_path
        self.metadata_path = metadata_path
        self.index = None
        self.documents = []

    def build(self, documents, embeddings):
        """
        Build a FAISS vector index.

        Args:
            documents: Documents associated with the embeddings.
            embeddings: Embedding vectors.

        Returns:
            None
        """
        vectors=np.array(embeddings,dtype=np.float32,)
        dimensions=vectors.shape[1]
        self.index=faiss.IndexFlatIP(dimensions)
        self.index.add(vectors)
        self.documents=documents

        logger.info("created FAISS index with %d vectors",len(documents),)

    def save(self):
        """
        Save the FAISS index and document metadata.

        Raises:
            RuntimeError:
                If the index cannot be written.
        """
        try:
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
        except Exception as exc:
            logger.exception(
                "Failed to save vector store."
            )
            raise RuntimeError(
                "Unable to save vector store."
            ) from exc

    def load(self):
        """
        Load the FAISS index and metadata.

        Raises:
            RuntimeError:
                If the index or metadata cannot be loaded.
        """
        try:
            self.index=faiss.read_index(str(self.index_path))
            with open(self.metadata_path,"rb")as f:
                self.documents=pickle.load(f)

            logger.info("Loaded vector store")
        except Exception as exc:
            logger.exception(
                "Failed to load vector store."
            )
            raise RuntimeError(
                "Unable to load vector store."
            ) from exc

    def search(self, query_embedding, top_k = 5):
        """
        Search the vector store.

        Args:
            query_embedding: Query embedding vector.
            top_k: Maximum number of documents to return.

        Returns:
            List of retrieved documents.

        Raises:
            RuntimeError:
                If the vector store has not been loaded.
        """

        if self.index is None:
            raise RuntimeError("Vector store is not loaded")
        
        query=np.array([query_embedding],dtype=np.float32,)
        _,indices=self.index.search(query,top_k,)
        
        return [self.documents[i] for i in indices[0] if i !=-1]
