"""
Document management API endpoints
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, status
from typing import List
from app.models.schemas import DocumentInfo, DocumentUploadResponse
from app.services.rag_service import rag_service
from app.config.settings import settings
from pathlib import Path
import shutil
from datetime import datetime
import os

router = APIRouter(prefix="/documents", tags=["documents"])

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.xlsx', '.xls', '.csv'}

def validate_file(file: UploadFile) -> None:
    """Validate uploaded file"""
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not supported. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process QSS Technosoft documents

    This endpoint:
    - Validates file type (PDF, DOCX, TXT, XLSX, CSV)
    - Extracts text from document
    - Splits text into chunks
    - Generates embeddings using Google text-embedding-004
    - Stores embeddings in ChromaDB for retrieval

    Supported formats: PDF, DOCX, TXT, XLSX, XLS, CSV
    Max file size: 10MB
    """
    try:
        # Validate file
        validate_file(file)

        # Initialize RAG service
        if not rag_service.initialized:
            await rag_service.initialize()

        # Create upload directory if it doesn't exist
        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Save file temporarily
        file_path = upload_dir / file.filename

        # Check if file already exists
        if file_path.exists():
            # Add timestamp to make filename unique
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_stem = file_path.stem
            file_ext = file_path.suffix
            file_path = upload_dir / f"{file_stem}_{timestamp}{file_ext}"

        # Save uploaded file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process and add document to RAG system
        doc_id = await rag_service.add_document(
            document_path=str(file_path),
            metadata={
                "upload_date": datetime.now().isoformat(),
                "status": "active"
            }
        )

        return DocumentUploadResponse(
            id=doc_id,
            filename=file.filename,
            message="Document uploaded and processed successfully",
            status="success"
        )

    except ValueError as e:
        # Clean up file if processing failed
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Clean up file if processing failed
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading document: {str(e)}"
        )

@router.get("", response_model=List[DocumentInfo])
async def get_documents():
    """
    Retrieve list of all uploaded documents

    Returns metadata for all documents in the system including:
    - Document ID
    - Filename
    - File type
    - Size
    - Upload date
    - Status
    """
    try:
        # Initialize RAG service
        if not rag_service.initialized:
            await rag_service.initialize()

        documents = await rag_service.get_all_documents()

        return [
            DocumentInfo(
                id=doc['id'],
                filename=doc['filename'],
                file_type=doc['file_type'],
                size=doc['size'],
                upload_date=datetime.fromisoformat(doc['upload_date']),
                status=doc.get('status', 'active')
            )
            for doc in documents
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving documents: {str(e)}"
        )

@router.delete("/{document_id}", status_code=status.HTTP_200_OK)
async def delete_document(document_id: str):
    """
    Delete a document and its embeddings from the system

    This will:
    - Remove document from ChromaDB vector store
    - Delete associated embeddings
    - Remove document metadata
    """
    try:
        # Initialize RAG service
        if not rag_service.initialized:
            await rag_service.initialize()

        # Check if document exists
        doc = await rag_service.get_document_by_id(document_id)
        if not doc:
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {document_id} not found"
            )

        # Delete document
        await rag_service.delete_document(document_id)

        # Try to delete physical file
        try:
            file_path = Path(settings.upload_dir) / doc['filename']
            if file_path.exists():
                os.remove(file_path)
        except Exception:
            pass  # File might not exist or already deleted

        return {
            "message": f"Document {document_id} deleted successfully",
            "id": document_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting document: {str(e)}"
        )

@router.get("/{document_id}", response_model=DocumentInfo)
async def get_document(document_id: str):
    """
    Get details of a specific document

    Returns complete metadata for the requested document
    """
    try:
        # Initialize RAG service
        if not rag_service.initialized:
            await rag_service.initialize()

        doc = await rag_service.get_document_by_id(document_id)

        if not doc:
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {document_id} not found"
            )

        return DocumentInfo(
            id=doc['id'],
            filename=doc['filename'],
            file_type=doc['file_type'],
            size=doc['size'],
            upload_date=datetime.fromisoformat(doc['upload_date']),
            status=doc.get('status', 'active')
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving document: {str(e)}"
        )
