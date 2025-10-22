import React from 'react';
import { FaRobot } from 'react-icons/fa';

const TypingIndicator = () => {
  return (
    <div className="flex gap-3 p-4 message-animation">
      {/* Avatar */}
      <div className="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center bg-gray-200 text-gray-700">
        <FaRobot size={18} />
      </div>

      {/* Typing Animation */}
      <div className="flex items-center px-4 py-3 bg-white rounded-2xl rounded-tl-none border border-gray-200 shadow-sm">
        <div className="typing-indicator flex gap-1">
          <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
          <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
          <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;
