"""
FastAPI main application file for QSS Technosoft Q&A System
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, documents
from app.services.rag_service import rag_service
from app.config.settings import settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown
    """
    # Startup: Initialize RAG service
    await rag_service.initialize()
    print("✓ RAG Service initialized")
    print(f"✓ Vector store ready at: {settings.chroma_db_path}")
    print(f"✓ Upload directory: {settings.upload_dir}")

    yield

    # Shutdown: cleanup if needed
    print("Shutting down...")

app = FastAPI(
    title="QSS Technosoft Q&A API",
    description="""
    ## RAG-based Q&A Chatbot API for QSS Technosoft

    This API provides intelligent question-answering capabilities based on company documents
    using Retrieval-Augmented Generation (RAG) technology.

    ### Features
    - **Document Upload**: Upload and process company documents (PDF, DOCX, TXT, XLSX, CSV)
    - **Intelligent Q&A**: Ask questions and get AI-generated answers based on your documents
    - **Source Citations**: Answers include references to source documents
    - **Document Management**: List, view, and delete uploaded documents

    ### Technology Stack
    - **LLM**: Google Gemini 1.5 Flash
    - **Embeddings**: Google text-embedding-004
    - **Vector Database**: ChromaDB
    - **Framework**: FastAPI + LangChain

    ### Getting Started
    1. Upload your company documents using the `/api/documents/upload` endpoint
    2. Ask questions using the `/api/chat` endpoint
    3. Manage your documents through the documents endpoints
    """,
    version="1.0.0",
    contact={
        "name": "QSS Technosoft",
        "url": "https://qsstechnosoft.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api")
app.include_router(documents.router, prefix="/api")

@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "QSS Technosoft Q&A API",
        "status": "active",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/api/health", tags=["health"])
async def health_check():
    """
    Health check endpoint
    """
    try:
        stats = await rag_service.get_collection_stats()
        return {
            "status": "healthy",
            "rag_service": "initialized" if rag_service.initialized else "not initialized",
            "vector_store": stats
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e)
        }

@app.get("/api/stats", tags=["statistics"])
async def get_stats():
    """
    Get system statistics
    """
    try:
        stats = await rag_service.get_collection_stats()
        documents = await rag_service.get_all_documents()

        return {
            "total_documents": len(documents),
            "total_chunks": stats.get('total_chunks', 0),
            "collection_name": stats.get('collection_name', ''),
            "embedding_model": settings.embedding_model,
            "llm_model": settings.llm_model
        }
    except Exception as e:
        return {
            "error": str(e)
        }
