import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // You can add auth tokens here if needed
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle errors globally
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;

      switch (status) {
        case 400:
          error.message = data.detail || 'Bad request';
          break;
        case 401:
          error.message = 'Unauthorized access';
          break;
        case 403:
          error.message = 'Access forbidden';
          break;
        case 404:
          error.message = 'Resource not found';
          break;
        case 500:
          error.message = 'Internal server error';
          break;
        default:
          error.message = data.detail || 'An error occurred';
      }
    } else if (error.request) {
      // Request made but no response received
      error.message = 'No response from server. Please check your connection.';
    } else {
      // Error in request setup
      error.message = 'Error setting up request';
    }

    return Promise.reject(error);
  }
);

// Chat API endpoints
export const chatAPI = {
  // Send a question and get answer
  sendMessage: async (message) => {
    try {
      const response = await api.post('/chat', { question: message });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Optional: Stream response (if implementing WebSocket/SSE)
  streamMessage: async (message, onChunk, onComplete, onError) => {
    try {
      const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: message }),
      });

      if (!response.ok) {
        throw new Error('Stream request failed');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          if (onComplete) onComplete();
          break;
        }

        const chunk = decoder.decode(value, { stream: true });
        if (onChunk) onChunk(chunk);
      }
    } catch (error) {
      if (onError) onError(error);
      throw error;
    }
  },
};

// Document API endpoints
export const documentAPI = {
  // Upload documents
  uploadDocument: async (file, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/documents/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (onProgress) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            onProgress(percentCompleted);
          }
        },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Get all documents
  getDocuments: async () => {
    try {
      const response = await api.get('/documents');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Delete a document
  deleteDocument: async (documentId) => {
    try {
      const response = await api.delete(`/documents/${documentId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default api;
