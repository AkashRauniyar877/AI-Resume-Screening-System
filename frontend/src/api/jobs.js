/**
 * Jobs API services connecting to FastAPI backend.
 */

import request from './client';

export const listJobsApi = async () => {
  return request('/api/v1/jobs', {
    method: 'GET',
  });
};

export const getJobResultsApi = async (jobId) => {
  return request(`/api/v1/jobs/${jobId}/results`, {
    method: 'GET',
  });
};
