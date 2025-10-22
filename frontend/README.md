# Company Q&A Frontend

React-based frontend for the Company Q&A chatbot application.

## Features

- Modern, responsive chat interface
- Real-time messaging with typing indicators
- Error handling and loading states
- Auto-scroll to latest messages
- Tailwind CSS styling with smooth animations
- Axios-based API service layer

## Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

## Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Project Structure

```
src/
├── components/         # React components
│   ├── ChatContainer.jsx    # Main chat container
│   ├── ChatMessage.jsx      # Individual message component
│   ├── ChatInput.jsx        # Message input field
│   ├── TypingIndicator.jsx  # Typing animation
│   └── ErrorMessage.jsx     # Error display
├── services/          # API services
│   └── api.js              # Axios API client
├── styles/            # CSS styles
│   └── index.css           # Global styles with Tailwind
├── App.jsx            # Root component
└── main.jsx           # Entry point
```

## Components

### ChatContainer
Main container managing chat state and message flow.

### ChatMessage
Displays individual messages with user/assistant styling.

### ChatInput
Text input with auto-resize and keyboard shortcuts.

### TypingIndicator
Animated typing indicator for loading states.

### ErrorMessage
User-friendly error display with dismiss option.

## API Integration

The frontend communicates with the backend through:
- `/api/chat` - Send questions and receive answers
- `/api/documents/upload` - Upload company documents
- `/api/documents` - Manage documents

API configuration in `src/services/api.js`

## Customization

### Styling
Modify `tailwind.config.js` for color schemes and themes.

### API Endpoint
Update `vite.config.js` proxy settings to change backend URL.

## Building for Production

```bash
npm run build
```

Output will be in the `dist/` directory.
