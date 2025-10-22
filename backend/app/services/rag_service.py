"""
RAG (Retrieval-Augmented Generation) Service

This service handles:
1. Document embedding and storage in ChromaDB
2. Query processing and similarity search
3. Context retrieval from relevant documents
4. LLM response generation using Google Gemini
"""

from typing import List, Dict, Any
import uuid
from datetime import datetime
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from app.services.vector_store import vector_store
from app.services.document_processor import document_processor
from app.config.settings import settings
import json
from pathlib import Path

class RAGService:
    """
    RAG service for document retrieval and question answering
    """

    def __init__(self):
        """
        Initialize RAG service with:
        - Google Gemini LLM
        - Google text-embedding-004 embeddings
        - ChromaDB vector store
        - LangChain components
        """
        self.embeddings = None
        self.llm = None
        self.initialized = False
        self.documents_metadata = {}

    async def initialize(self):
        """Initialize vector store and models"""
        if self.initialized:
            return

        # Initialize embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.google_api_key
        )

        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=settings.llm_model,
            google_api_key=settings.google_api_key,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens
        )

        # Initialize vector store
        await vector_store.initialize(
            persist_directory=settings.chroma_db_path,
            collection_name=settings.collection_name
        )

        self.initialized = True

    async def add_document(self, document_path: str, metadata: Dict[str, Any]) -> str:
        """
        Process and add document to vector store

        Steps:
        1. Load document
        2. Split into chunks
        3. Generate embeddings
        4. Store in ChromaDB
        """
        if not self.initialized:
            await self.initialize()

        # Process document
        doc_data = await document_processor.process_file(document_path)

        # Chunk text
        chunks = document_processor.chunk_text(
            doc_data['text'],
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )

        if not chunks:
            raise ValueError("No text content could be extracted from the document")

        # Generate unique document ID
        doc_id = str(uuid.uuid4())

        # Generate embeddings for all chunks
        chunk_embeddings = self.embeddings.embed_documents(chunks)

        # Prepare metadata for each chunk
        chunk_ids = []
        chunk_metadatas = []
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc_id}_chunk_{i}"
            chunk_ids.append(chunk_id)

            chunk_metadata = {
                "source": doc_data['filename'],
                "document_id": doc_id,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "file_type": doc_data['file_type'],
                **metadata
            }
            chunk_metadatas.append(chunk_metadata)

        # Add to vector store
        await vector_store.add_documents(
            documents=chunks,
            embeddings=chunk_embeddings,
            metadatas=chunk_metadatas,
            ids=chunk_ids
        )

        # Store document metadata
        self.documents_metadata[doc_id] = {
            "id": doc_id,
            "filename": doc_data['filename'],
            "file_type": doc_data['file_type'],
            "size": doc_data['size'],
            "upload_date": datetime.now().isoformat(),
            "chunks_count": len(chunks),
            **metadata
        }

        return doc_id

    async def query(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Process user question and generate answer

        Steps:
        1. Generate query embedding
        2. Perform similarity search in ChromaDB
        3. Retrieve relevant document chunks
        4. Create context from retrieved chunks
        5. Generate answer using Gemini
        6. Return answer with sources
        """
        if not self.initialized:
            await self.initialize()

        # Generate query embedding
        query_embedding = self.embeddings.embed_query(question)

        # Perform similarity search
        search_results = await vector_store.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        if not search_results:
            return {
                "answer": "I don't have enough information in the knowledge base to answer this question. Please upload relevant documents first.",
                "sources": [],
                "context_used": False
            }

        # Build context from retrieved chunks
        context_parts = []
        sources = []

        for i, result in enumerate(search_results, 1):
            context_parts.append(f"[Source {i}]: {result['document']}")
            sources.append({
                "document_name": result['metadata'].get('source', 'Unknown'),
                "content": result['document'][:200] + "..." if len(result['document']) > 200 else result['document'],
                "relevance_score": float(1 - result['distance'])  # Convert distance to similarity score
            })

        context = "\n\n".join(context_parts)

        # Create prompt
        prompt = f"""You are a helpful AI assistant for QSS Technosoft. Answer the user's question based on the following context from the company documents.

Context:
{context}

Question: {question}

Instructions:
- First, determine if the question is related to QSS Technosoft, the company's services, products, or business
- If the question is NOT related to QSS Technosoft (e.g., general knowledge questions, unrelated topics), respond with: "This question is not related to QSS Technosoft. Please ask questions about our company, services, products, or business operations."
- If the question IS related to QSS Technosoft but the context doesn't have the answer, respond with: "I don't have specific information about this in the available documents. Please contact QSS Technosoft directly for more details."
- For valid company-related questions with available information:
  - Provide a direct, clear and concise answer based on the context provided
  - Format your answer using bullet points (using - or *) when listing multiple items or facts
  - For single fact answers, you can respond in a sentence without bullets
  - Do NOT mention sources, source numbers, or where the information came from
  - Do NOT use phrases like "according to", "mentioned in", "as stated in", "this document", or similar references
  - Answer naturally as if you are stating a fact
- Maintain a professional and helpful tone

Answer:"""

        # Generate response using LLM
        try:
            response = self.llm.invoke(prompt)
            answer = response.content
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

        return {
            "answer": answer,
            "sources": sources,
            "context_used": True
        }

    async def delete_document(self, document_id: str):
        """Remove document from vector store"""
        if not self.initialized:
            await self.initialize()

        # Get all chunk IDs for this document
        all_data = vector_store.collection.get(
            where={"document_id": document_id}
        )

        if all_data and 'ids' in all_data and len(all_data['ids']) > 0:
            await vector_store.delete_documents(all_data['ids'])

        # Remove from metadata
        if document_id in self.documents_metadata:
            del self.documents_metadata[document_id]

    async def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get list of all documents in vector store"""
        if not self.initialized:
            await self.initialize()

        return list(self.documents_metadata.values())

    async def get_document_by_id(self, document_id: str) -> Dict[str, Any]:
        """Get specific document metadata"""
        if not self.initialized:
            await self.initialize()

        return self.documents_metadata.get(document_id)

    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store collection"""
        if not self.initialized:
            await self.initialize()

        info = await vector_store.get_collection_info()
        return {
            "total_documents": len(self.documents_metadata),
            "total_chunks": info['count'],
            "collection_name": info['name']
        }

# Global RAG service instance
rag_service = RAGService()
