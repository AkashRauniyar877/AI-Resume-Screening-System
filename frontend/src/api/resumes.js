/**
 * API functions for viewing and downloading candidate resumes with JWT authorization.
 */

import { getToken } from '../utils/auth';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

/**
 * View candidate original resume inline in a new browser tab.
 * Uses authenticated fetch, blob creation, and window.open.
 *
 * @param {string} resumeId - Unique resume identifier.
 */
export const viewResumeApi = async (resumeId) => {
  if (!resumeId) {
    throw new Error('Resume ID is missing.');
  }

  const token = getToken();
  if (!token) {
    throw new Error('Authentication token required to view resume.');
  }

  const response = await fetch(`${BASE_URL}/api/v1/resumes/${resumeId}/view`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    let msg = 'Failed to view resume file.';
    try {
      const errJson = await response.json();
      if (errJson.detail) msg = errJson.detail;
    } catch (e) {}
    throw new Error(msg);
  }

  const blob = await response.blob();
  const fileUrl = URL.createObjectURL(blob);
  window.open(fileUrl, '_blank');

  // Revoke Object URL after 60 seconds to release memory
  setTimeout(() => URL.revokeObjectURL(fileUrl), 60000);
};

/**
 * Download candidate original resume file.
 * Uses authenticated fetch, blob creation, and anchor click trigger.
 *
 * @param {string} resumeId - Unique resume identifier.
 */
export const downloadResumeApi = async (resumeId) => {
  if (!resumeId) {
    throw new Error('Resume ID is missing.');
  }

  const token = getToken();
  if (!token) {
    throw new Error('Authentication token required to download resume.');
  }

  const response = await fetch(`${BASE_URL}/api/v1/resumes/${resumeId}/download`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    let msg = 'Failed to download resume file.';
    try {
      const errJson = await response.json();
      if (errJson.detail) msg = errJson.detail;
    } catch (e) {}
    throw new Error(msg);
  }

  // Extract filename from Content-Disposition header if available
  let filename = `resume_${resumeId}.pdf`;
  const disposition = response.headers.get('content-disposition');
  if (disposition && disposition.includes('filename=')) {
    const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(disposition);
    if (matches != null && matches[1]) {
      filename = matches[1].replace(/['"]/g, '');
    }
  }

  const blob = await response.blob();
  const fileUrl = URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.href = fileUrl;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  link.remove();

  setTimeout(() => URL.revokeObjectURL(fileUrl), 60000);
};
