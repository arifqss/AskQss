"""
Chat API endpoints
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, Source
from app.services.rag_service import rag_service
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Process user question and return AI-generated answer
    based on QSS Technosoft documents using RAG

    This endpoint:
    - Generates query embeddings
    - Performs vector similarity search in ChromaDB
    - Retrieves relevant document chunks
    - Generates answer using Google Gemini LLM
    - Returns answer with source citations
    """
    try:
        # Initialize RAG service if not already initialized
        if not rag_service.initialized:
            await rag_service.initialize()

        # Process query
        result = await rag_service.query(
            question=request.question,
            top_k=5
        )

        # Format sources
        sources = [
            Source(
                document_name=src['document_name'],
                content=src['content']
            )
            for src in result.get('sources', [])
        ]

        return ChatResponse(
            answer=result['answer'],
            sources=sources,
            timestamp=datetime.now()
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )
