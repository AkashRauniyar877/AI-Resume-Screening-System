/**
 * Resume Screening API services connecting to FastAPI backend.
 */

import request from './client';

/**
 * Screen multiple resumes in batch against a job description.
 * formData must contain:
 * - files (multiple File objects)
 * - job_description (string)
 * - job_title (optional string)
 */
export const screenCandidatesApi = async (formData) => {
  return request('/api/v1/screen-candidates', {
    method: 'POST',
    body: formData,
  });
};

/**
 * Screen a single resume against a job description.
 */
export const screenSingleResumeApi = async (formData) => {
  return request('/api/v1/screen', {
    method: 'POST',
    body: formData,
  });
};

/**
 * Parse a raw resume file to preview text and contact/skill info.
 */
export const parseResumeApi = async (formData) => {
  return request('/api/v1/parse-resume', {
    method: 'POST',
    body: formData,
  });
};
