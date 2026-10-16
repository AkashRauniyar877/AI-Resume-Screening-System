/**
 * Centralized API HTTP Client for interacting with the FastAPI backend.
 */

import { getToken, removeToken } from '../utils/auth';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

/**
 * Perform fetch request with automatic headers, JWT token, and error handling.
 */
export const request = async (endpoint, options = {}) => {
  const url = `${BASE_URL}${endpoint}`;
  
  const token = getToken();
  const headers = {
    ...(options.headers || {}),
  };

  if (token && !headers['Authorization']) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // If payload is not FormData and body is an object, set Content-Type JSON
  if (options.body && !(options.body instanceof FormData) && typeof options.body === 'object') {
    headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(options.body);
  }

  const config = {
    ...options,
    headers,
  };

  try {
    const response = await fetch(url, config);

    // Handle 401 Unauthorized globally
    if (response.status === 401) {
      removeToken();
      // Optional: notify or trigger auth refresh event if needed
    }

    let data;
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      data = await response.json();
    } else {
      data = await response.text();
    }

    if (!response.ok) {
      let errorMessage = 'An unexpected error occurred.';
      if (typeof data === 'object' && data !== null) {
        if (data.detail) {
          if (Array.isArray(data.detail)) {
            errorMessage = data.detail.map((err) => `${err.loc?.join('.') || ''}: ${err.msg}`).join(', ');
          } else {
            errorMessage = data.detail;
          }
        } else if (data.message) {
          errorMessage = data.message;
        }
      } else if (typeof data === 'string' && data.length > 0) {
        errorMessage = data;
      }

      const error = new Error(errorMessage);
      error.status = response.status;
      error.data = data;
      throw error;
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      const networkError = new Error('Unable to connect to the backend server. Please verify the FastAPI server is running at ' + BASE_URL);
      networkError.status = 0;
      throw networkError;
    }
    throw error;
  }
};

export default request;
