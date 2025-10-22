import React, { useState, useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import TypingIndicator from './TypingIndicator';
import ErrorMessage from './ErrorMessage';
import { chatAPI } from '../services/api';
import { FaComments } from 'react-icons/fa';

const ChatContainer = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [latestMessageId, setLatestMessageId] = useState(null);
  const messagesEndRef = useRef(null);
  const messagesContainerRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Add welcome message on mount
  useEffect(() => {
    setMessages([
      {
        id: Date.now(),
        text: "Hello! I'm your QSS Technosoft Q&A assistant. Ask me anything about QSS Technosoft, and I'll provide answers based on our documents.",
        isUser: false,
        timestamp: new Date().toISOString(),
      },
    ]);
  }, []);

  const handleSendMessage = async (messageText) => {
    // Clear any previous errors
    setError(null);

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: messageText,
      isUser: true,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessage]);

    // Set loading state
    setIsLoading(true);

    try {
      // Call API
      const response = await chatAPI.sendMessage(messageText);

      // Add assistant response
      const assistantMessageId = Date.now() + 1;
      const assistantMessage = {
        id: assistantMessageId,
        text: response.answer || response.message || 'I apologize, but I could not generate a response.',
        isUser: false,
        timestamp: new Date().toISOString(),
        sources: response.sources || [],
      };

      setLatestMessageId(assistantMessageId);
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError(err.message || 'Failed to send message. Please try again.');

      // Optionally add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        text: 'I apologize, but I encountered an error processing your request. Please try again.',
        isUser: false,
        timestamp: new Date().toISOString(),
        isError: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary-500 rounded-full flex items-center justify-center">
              <FaComments className="text-white" size={20} />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">QSS Technosoft Q&A Assistant</h1>
              <p className="text-sm text-gray-500">Ask questions about QSS Technosoft</p>
            </div>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <ErrorMessage message={error} onClose={() => setError(null)} />
      )}

      {/* Messages Container */}
      <div
        ref={messagesContainerRef}
        className="flex-1 overflow-y-auto scrollbar-thin px-4 py-6"
      >
        <div className="max-w-4xl mx-auto space-y-2">
          {messages.length === 0 && (
            <div className="text-center text-gray-400 py-12">
              <FaComments size={48} className="mx-auto mb-4 opacity-50" />
              <p className="text-lg">Start a conversation</p>
              <p className="text-sm mt-2">Ask any question about QSS Technosoft</p>
            </div>
          )}

          {messages.map((msg) => (
            <ChatMessage
              key={msg.id}
              message={msg.text}
              isUser={msg.isUser}
              timestamp={msg.timestamp}
              enableTyping={msg.id === latestMessageId}
            />
          ))}

          {isLoading && <TypingIndicator />}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <ChatInput
        onSendMessage={handleSendMessage}
        disabled={isLoading}
        placeholder="Ask a question about QSS Technosoft..."
      />
    </div>
  );
};

export default ChatContainer;
