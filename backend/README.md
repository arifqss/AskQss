# Company Q&A Backend

FastAPI-based backend with RAG (Retrieval-Augmented Generation) capabilities using LangChain, ChromaDB, and Google Gemini.

## Features (To Be Implemented)

- RAG-based question answering
- Document upload and processing
- Vector similarity search with ChromaDB
- Google Gemini LLM integration
- Google text-embedding-004 embeddings
- Multiple document format support (PDF, DOCX, TXT, etc.)

## Prerequisites

- Python 3.10 or higher
- Google API key for Gemini
- pip or conda for package management

## Installation

1. Create a virtual environment:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Add your Google API key to `.env`:
```
GOOGLE_API_KEY=your_api_key_here
```

## Getting Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

## Running the Server

Start the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation at `http://localhost:8000/docs`

## Project Structure

```
app/
├── api/                    # API endpoints
│   ├── chat.py            # Chat endpoints
│   └── documents.py       # Document management
├── config/                # Configuration
│   └── settings.py        # App settings
├── models/                # Data models
│   └── schemas.py         # Pydantic schemas
├── services/              # Business logic
│   ├── rag_service.py     # RAG implementation
│   ├── document_processor.py  # Document processing
│   └── vector_store.py    # ChromaDB operations
└── main.py               # FastAPI application

documents/                # Uploaded documents storage
chroma_db/               # ChromaDB persistent storage
```

## Implementation Roadmap

### Phase 1: Document Processing
- [ ] Implement document loaders (PDF, DOCX, TXT)
- [ ] Text extraction and cleaning
- [ ] Document chunking with LangChain

### Phase 2: Vector Store Setup
- [ ] Initialize ChromaDB
- [ ] Implement embedding generation with Google
- [ ] Document storage and retrieval

### Phase 3: RAG Implementation
- [ ] Query processing
- [ ] Similarity search
- [ ] Context retrieval
- [ ] LLM response generation with Gemini

### Phase 4: API Endpoints
- [ ] Chat endpoint with streaming support
- [ ] Document upload endpoint
- [ ] Document management endpoints
- [ ] Error handling and validation

### Phase 5: Optimization
- [ ] Caching strategies
- [ ] Performance optimization
- [ ] Batch processing
- [ ] Rate limiting

## API Endpoints (To Be Implemented)

### Chat
- `POST /api/chat` - Send question, receive answer
- `POST /api/chat/stream` - Streaming responses

### Documents
- `POST /api/documents/upload` - Upload document
- `GET /api/documents` - List all documents
- `GET /api/documents/{id}` - Get document details
- `DELETE /api/documents/{id}` - Delete document

## Configuration

Edit `.env` file or `app/config/settings.py` for:
- Model selection (LLM and embeddings)
- Chunk size and overlap
- Top-K results for retrieval
- Temperature and max tokens
- ChromaDB settings

## Development

### Adding New Endpoints
1. Create route file in `app/api/`
2. Define Pydantic schemas in `app/models/schemas.py`
3. Implement business logic in `app/services/`
4. Register router in `app/main.py`

### Testing
```bash
pytest tests/
```

## Environment Variables

See `.env.example` for all available configuration options.

## Troubleshooting

### ChromaDB Issues
If you encounter ChromaDB errors, delete the `chroma_db/` directory and restart.

### Google API Errors
Ensure your API key is valid and has access to:
- Gemini API (gemini-1.5-flash)
- Embedding API (text-embedding-004)

## Next Steps

This backend structure is ready for implementation. Next phase will include:
1. Implementing the RAG service
2. Document processing logic
3. API endpoint implementations
4. Testing and optimization

## License

MIT
