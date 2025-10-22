# QSS Technosoft Q&A Chatbot with RAG

A full-stack application that allows users to ask questions about QSS Technosoft and receive AI-generated answers based on company documents using Retrieval-Augmented Generation (RAG).

## Tech Stack

### Frontend
- React 18
- Tailwind CSS
- Axios
- React Icons

### Backend
- Python 3.10+
- FastAPI
- LangChain
- ChromaDB (Vector Database)
- Google Gemini (gemini-1.5-flash)
- Google text-embedding-004

## Project Structure

```
AskQss/
├── frontend/                 # React frontend application
│   ├── public/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   ├── utils/           # Utility functions
│   │   ├── styles/          # CSS styles
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── tailwind.config.js
│
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── services/       # Business logic
│   │   ├── models/         # Data models
│   │   ├── config/         # Configuration
│   │   └── main.py         # FastAPI app
│   ├── documents/          # QSS Technosoft documents storage
│   ├── chroma_db/          # ChromaDB persistent storage
│   ├── requirements.txt
│   └── .env.example
│
├── .gitignore
└── README.md
```

## Features

- Modern, responsive chat interface
- Real-time message streaming
- Context-aware responses using RAG
- Document-based knowledge retrieval
- Error handling and loading states
- Auto-scroll to latest messages
- Typing indicators
- Accessible design

## Setup Instructions

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
```

5. Add your Google API key to `.env`:
```
GOOGLE_API_KEY=your_api_key_here
```

6. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The backend will run on `http://localhost:8000`

## Environment Variables

### Backend (.env)
- `GOOGLE_API_KEY`: Your Google API key for Gemini and embeddings
- `CHROMA_DB_PATH`: Path to ChromaDB storage (default: ./chroma_db)
- `UPLOAD_DIR`: Directory for document uploads (default: ./documents)

## Usage

1. Start both frontend and backend servers
2. Navigate to the frontend URL
3. Upload QSS Technosoft documents (will be implemented in backend)
4. Start asking questions about QSS Technosoft
5. Receive AI-generated answers based on the uploaded documents

## API Endpoints

- `POST /api/chat`: Send a question and receive an answer
- `POST /api/upload`: Upload company documents
- `GET /api/documents`: List uploaded documents
- `DELETE /api/documents/{id}`: Delete a document

## Development

### Frontend Development
- Uses Vite for fast development and hot module replacement
- Tailwind CSS for styling
- Component-based architecture

### Backend Development
- FastAPI with automatic API documentation
- Async/await for optimal performance
- RAG implementation with LangChain
- Persistent vector storage with ChromaDB

## License

MIT
