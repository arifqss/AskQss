"""
Pydantic models for request/response validation
To be implemented in backend phase
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)

class Source(BaseModel):
    document_name: str
    page_number: Optional[int] = None
    content: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source] = []
    timestamp: datetime = Field(default_factory=datetime.now)

class DocumentInfo(BaseModel):
    id: str
    filename: str
    file_type: str
    size: int
    upload_date: datetime
    status: str

class DocumentUploadResponse(BaseModel):
    id: str
    filename: str
    message: str
    status: str

class ErrorResponse(BaseModel):
    detail: str
    timestamp: datetime = Field(default_factory=datetime.now)
