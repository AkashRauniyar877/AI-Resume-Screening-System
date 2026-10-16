/**
 * Authentication API services connecting to FastAPI backend.
 */

import request from './client';

export const registerApi = async (userData) => {
  return request('/api/v1/auth/register', {
    method: 'POST',
    body: userData,
  });
};

export const loginApi = async (credentials) => {
  return request('/api/v1/auth/login', {
    method: 'POST',
    body: credentials,
  });
};

export const getMeApi = async () => {
  return request('/api/v1/auth/me', {
    method: 'GET',
  });
};
