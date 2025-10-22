"""
Vector store service using ChromaDB
"""

from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from pathlib import Path

class VectorStoreService:
    """
    Manage ChromaDB vector store operations
    """

    def __init__(self):
        """
        Initialize ChromaDB client and collection

        Will use:
        - Persistent storage
        - Google text-embedding-004 embeddings
        """
        self.client = None
        self.collection = None
        self.initialized = False

    async def initialize(self, persist_directory: str, collection_name: str):
        """
        Initialize ChromaDB client and create/get collection

        Args:
            persist_directory: Path to persistent storage
            collection_name: Name of the collection
        """
        if self.initialized:
            return

        # Create persist directory if it doesn't exist
        Path(persist_directory).mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client with persistent storage
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

        self.initialized = True

    async def add_documents(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
        ids: List[str]
    ):
        """
        Add documents with embeddings to vector store

        Args:
            documents: List of document texts
            embeddings: List of embedding vectors
            metadatas: List of metadata dicts
            ids: List of document IDs
        """
        if not self.initialized or not self.collection:
            raise RuntimeError("Vector store not initialized")

        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    async def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform similarity search

        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filter_dict: Optional metadata filters

        Returns:
            List of matching documents with scores
        """
        if not self.initialized or not self.collection:
            raise RuntimeError("Vector store not initialized")

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_dict,
            include=["documents", "metadatas", "distances"]
        )

        # Format results
        formatted_results = []
        if results and results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i],
                    'id': results['ids'][0][i] if 'ids' in results else None
                })

        return formatted_results

    async def delete_documents(self, document_ids: List[str]):
        """
        Delete documents from vector store

        Args:
            document_ids: List of document IDs to delete
        """
        if not self.initialized or not self.collection:
            raise RuntimeError("Vector store not initialized")

        # Filter out document IDs that don't exist
        try:
            self.collection.delete(ids=document_ids)
        except Exception as e:
            raise Exception(f"Error deleting documents: {str(e)}")

    async def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection

        Returns:
            Dict with collection stats
        """
        if not self.initialized or not self.collection:
            raise RuntimeError("Vector store not initialized")

        count = self.collection.count()
        return {
            "name": self.collection.name,
            "count": count,
            "metadata": self.collection.metadata
        }

    async def clear_collection(self):
        """Clear all documents from collection"""
        if not self.initialized or not self.collection:
            raise RuntimeError("Vector store not initialized")

        # Get all IDs and delete them
        all_data = self.collection.get()
        if all_data and 'ids' in all_data and len(all_data['ids']) > 0:
            self.collection.delete(ids=all_data['ids'])

    async def get_all_document_ids(self) -> List[str]:
        """Get all document IDs in the collection"""
        if not self.initialized or not self.collection:
            raise RuntimeError("Vector store not initialized")

        all_data = self.collection.get()
        return all_data.get('ids', [])

    async def get_documents_by_source(self, source_filename: str) -> List[str]:
        """Get all document IDs for a specific source file"""
        if not self.initialized or not self.collection:
            raise RuntimeError("Vector store not initialized")

        results = self.collection.get(
            where={"source": source_filename},
            include=["metadatas"]
        )

        return results.get('ids', [])

# Global vector store instance
vector_store = VectorStoreService()
