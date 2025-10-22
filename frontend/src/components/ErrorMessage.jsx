import React from 'react';
import { FaExclamationTriangle, FaTimes } from 'react-icons/fa';

const ErrorMessage = ({ message, onClose }) => {
  return (
    <div className="mx-4 mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3 message-animation">
      <FaExclamationTriangle className="text-red-500 flex-shrink-0 mt-0.5" size={18} />
      <div className="flex-1">
        <h4 className="text-sm font-semibold text-red-800 mb-1">Error</h4>
        <p className="text-sm text-red-700">{message}</p>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="text-red-400 hover:text-red-600 transition-colors flex-shrink-0"
          aria-label="Close error message"
        >
          <FaTimes size={16} />
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;
