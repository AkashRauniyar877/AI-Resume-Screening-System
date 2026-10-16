/**
 * Candidates API services connecting to FastAPI backend.
 */

import request from './client';

export const listCandidatesApi = async () => {
  return request('/api/v1/candidates', {
    method: 'GET',
  });
};
