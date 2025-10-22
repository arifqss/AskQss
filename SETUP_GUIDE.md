# Company Q&A Chatbot - Complete Setup Guide

This guide will walk you through setting up the complete application from scratch.

## Prerequisites

### Required Software
- **Node.js** 18+ and npm
- **Python** 3.10 or higher
- **Git** (optional, for version control)
- **Google API Key** for Gemini and embeddings

### Getting Your Google API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key - you'll need it later

## Project Structure

After setup, your project will look like this:
```
AskQss/
├── frontend/          # React application
├── backend/           # FastAPI application
├── .gitignore
└── README.md
```

## Step 1: Frontend Setup

### 1.1 Navigate to Frontend Directory
```bash
cd frontend
```

### 1.2 Install Dependencies
```bash
npm install
```

This will install:
- React 18
- Tailwind CSS
- Axios
- React Icons
- Vite (build tool)

### 1.3 Start Development Server
```bash
npm run dev
```

The frontend will start on `http://localhost:5173`

**Note:** Keep this terminal window open!

## Step 2: Backend Setup

### 2.1 Open New Terminal
Open a new terminal window and navigate to the backend directory:
```bash
cd backend
```

### 2.2 Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 2.3 Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- FastAPI and Uvicorn
- LangChain
- Google Generative AI SDK
- ChromaDB
- Document processing libraries

### 2.4 Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# On Windows, use:
copy .env.example .env
```

Edit `.env` file and add your Google API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### 2.5 Start Backend Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will start on `http://localhost:8000`

**Note:** Keep this terminal window open too!

## Step 3: Verify Setup

### 3.1 Check Backend
Open your browser and go to:
- `http://localhost:8000` - Should show API info
- `http://localhost:8000/docs` - Interactive API documentation
- `http://localhost:8000/api/health` - Health check

### 3.2 Check Frontend
Open your browser and go to:
- `http://localhost:5173` - Should show the chat interface

### 3.3 Test the Application
1. You should see a welcome message in the chat
2. Type a message in the input field
3. Currently, you'll get an error (expected - backend not fully implemented yet)

## Step 4: Next Steps - Backend Implementation

The frontend is complete! Now you need to implement the backend. Here's what needs to be done:

### 4.1 Implement RAG Service (`backend/app/services/rag_service.py`)
- Initialize Google Gemini LLM
- Set up text embeddings
- Implement ChromaDB vector store
- Create query processing logic

### 4.2 Implement Document Processor (`backend/app/services/document_processor.py`)
- PDF text extraction
- DOCX text extraction
- Text chunking
- Metadata extraction

### 4.3 Implement Vector Store (`backend/app/services/vector_store.py`)
- ChromaDB initialization
- Document embedding and storage
- Similarity search
- Document management

### 4.4 Implement API Endpoints
- **Chat Endpoint** (`backend/app/api/chat.py`)
  - Receive question
  - Retrieve relevant context
  - Generate answer with Gemini
  - Return response with sources

- **Document Endpoints** (`backend/app/api/documents.py`)
  - Upload documents
  - List documents
  - Delete documents

### 4.5 Update Main App (`backend/app/main.py`)
- Register API routers
- Add startup/shutdown events
- Initialize services

## Common Issues and Solutions

### Issue: Port Already in Use

**Frontend (5173):**
```bash
# Kill the process on port 5173
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5173 | xargs kill -9
```

**Backend (8000):**
```bash
# Kill the process on port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Issue: Module Not Found (Python)
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: npm Install Fails
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue: Google API Key Invalid
1. Verify the key is correct in `.env`
2. Check API is enabled in Google Cloud Console
3. Ensure no extra spaces in the `.env` file

## Development Workflow

### Running Both Servers

**Option 1: Two Terminal Windows**
- Terminal 1: Frontend (`npm run dev`)
- Terminal 2: Backend (`uvicorn app.main:app --reload`)

**Option 2: Using tmux/screen (Linux/macOS)**
```bash
# Start tmux
tmux

# Split window
Ctrl+B then %

# Navigate between panes
Ctrl+B then arrow keys
```

### Making Changes

**Frontend Changes:**
- Edit files in `frontend/src/`
- Hot reload is automatic
- Check browser console for errors

**Backend Changes:**
- Edit files in `backend/app/`
- Auto-reload is enabled with `--reload` flag
- Check terminal for errors

## Testing the Complete System

Once backend is implemented:

1. **Upload Documents**
   - Use API or create upload UI
   - Documents stored in `backend/documents/`
   - Embeddings stored in `backend/chroma_db/`

2. **Ask Questions**
   - Type question in frontend
   - Backend retrieves relevant context
   - Gemini generates answer
   - Response appears in chat

3. **Verify Sources**
   - Answers should reference source documents
   - Check ChromaDB has documents

## Production Deployment

### Frontend
```bash
cd frontend
npm run build
# Deploy dist/ folder to hosting service
```

### Backend
```bash
# Use production WSGI server
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Resources

- [React Documentation](https://react.dev)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [LangChain Documentation](https://python.langchain.com)
- [Google AI Documentation](https://ai.google.dev)
- [ChromaDB Documentation](https://docs.trychroma.com)
- [Tailwind CSS Documentation](https://tailwindcss.com)

## Getting Help

If you encounter issues:
1. Check the error messages carefully
2. Review the README files in frontend and backend directories
3. Check API documentation at `http://localhost:8000/docs`
4. Verify all environment variables are set correctly
5. Ensure both servers are running

## What's Next?

You now have:
- ✅ Complete frontend implementation
- ✅ Backend folder structure
- ✅ Configuration files
- ✅ API scaffolding

Next phase:
- 🚧 Implement backend RAG logic
- 🚧 Implement document processing
- 🚧 Connect everything together
- 🚧 Test end-to-end

Let's implement the backend when you're ready!
