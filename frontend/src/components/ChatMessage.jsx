import React from 'react';
import { FaUser, FaRobot } from 'react-icons/fa';
import ReactMarkdown from 'react-markdown';
import { useTypingEffect } from '../hooks/useTypingEffect';

const ChatMessage = ({ message, isUser, timestamp, enableTyping = false }) => {
  const { displayedText, isTyping } = useTypingEffect(
    message,
    5,
    !isUser && enableTyping
  );

  // Show the displayed text (either typed or full text)
  const textToShow = (!isUser && enableTyping) ? displayedText : message;
  return (
    <div
      className={`flex gap-3 p-4 message-animation ${
        isUser ? 'flex-row-reverse' : 'flex-row'
      }`}
    >
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
          isUser
            ? 'bg-primary-500 text-white'
            : 'bg-gray-200 text-gray-700'
        }`}
      >
        {isUser ? <FaUser size={18} /> : <FaRobot size={18} />}
      </div>

      {/* Message Content */}
      <div
        className={`flex flex-col max-w-[75%] ${
          isUser ? 'items-end' : 'items-start'
        }`}
      >
        <div
          className={`px-4 py-3 rounded-2xl shadow-sm ${
            isUser
              ? 'bg-primary-500 text-white rounded-tr-none'
              : 'bg-white text-gray-800 rounded-tl-none border border-gray-200'
          }`}
        >
          {isUser ? (
            <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
              {textToShow}
            </p>
          ) : (
            <div className="text-sm leading-relaxed markdown-content">
              <ReactMarkdown
                components={{
                  ul: ({node, ...props}) => <ul className="list-disc list-inside space-y-1 my-2" {...props} />,
                  ol: ({node, ...props}) => <ol className="list-decimal list-inside space-y-1 my-2" {...props} />,
                  li: ({node, ...props}) => <li className="ml-2" {...props} />,
                  p: ({node, ...props}) => <p className="mb-2 last:mb-0" {...props} />,
                  strong: ({node, ...props}) => <strong className="font-semibold" {...props} />,
                  em: ({node, ...props}) => <em className="italic" {...props} />,
                }}
              >
                {textToShow}
              </ReactMarkdown>
              {isTyping && <span className="typing-cursor">|</span>}
            </div>
          )}
        </div>

        {/* Timestamp */}
        {timestamp && (
          <span className="text-xs text-gray-400 mt-1 px-2">
            {new Date(timestamp).toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </span>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
