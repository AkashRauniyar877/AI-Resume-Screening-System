import React, { useRef, useState } from 'react';
import { Upload, FileText, Trash2, AlertTriangle, CheckCircle2, ShieldCheck } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.txt'];
const MAX_FILE_SIZE_MB = 10;

export const ResumeUploader = ({ files, setFiles, error, setError }) => {
  const { theme } = useTheme();
  const fileInputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  const validateAndAddFiles = (newFileList) => {
    setError(null);
    const validFiles = [];
    const errors = [];

    Array.from(newFileList).forEach((file) => {
      const ext = '.' + file.name.split('.').pop().toLowerCase();
      if (!ALLOWED_EXTENSIONS.includes(ext)) {
        errors.push(`File "${file.name}" has an unsupported format (${ext}). Allowed: PDF, DOCX, TXT.`);
        return;
      }
      if (file.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
        errors.push(`File "${file.name}" exceeds maximum allowed size of ${MAX_FILE_SIZE_MB}MB.`);
        return;
      }
      if (files.some((f) => f.name === file.name)) {
        errors.push(`File "${file.name}" is already selected.`);
        return;
      }
      validFiles.push(file);
    });

    if (errors.length > 0) {
      setError(errors.join(' '));
    }

    if (validFiles.length > 0) {
      setFiles((prev) => [...prev, ...validFiles]);
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndAddFiles(e.target.files);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndAddFiles(e.dataTransfer.files);
    }
  };

  const removeFile = (indexToRemove) => {
    setFiles((prev) => prev.filter((_, idx) => idx !== indexToRemove));
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  return (
    <div className="space-y-3">
      {/* Resume Intake Upload Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`relative border border-dashed rounded-lg p-6 text-center cursor-pointer transition-all duration-150 ${
          isDragging
            ? 'border-cyan-500 bg-cyan-500/10'
            : theme === 'light'
            ? 'border-slate-300 hover:border-cyan-500 bg-slate-50'
            : 'border-[#1e2634] hover:border-cyan-500/50 bg-[#090b0e]'
        }`}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileSelect}
          multiple
          accept=".pdf,.docx,.txt"
          className="hidden"
        />

        <div className={`w-10 h-10 mx-auto mb-2 rounded flex items-center justify-center border ${
          theme === 'light'
            ? 'bg-cyan-50 border-cyan-200 text-cyan-700'
            : 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400'
        }`}>
          <Upload className="w-5 h-5" />
        </div>

        <h4 className={`text-xs font-bold uppercase tracking-wider ${
          theme === 'light' ? 'text-slate-800' : 'text-slate-200'
        }`}>
          RESUME INTAKE
        </h4>
        <p className={`text-xs mt-1 ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
          Drop <span className="text-cyan-600 dark:text-cyan-400 font-mono">PDF / DOCX / TXT</span> files or <span className="text-cyan-600 dark:text-cyan-400 underline font-semibold">Browse files</span>
        </p>

        <p className={`text-[10px] font-mono mt-2 ${theme === 'light' ? 'text-slate-400' : 'text-slate-500'}`}>
          Max file size: {MAX_FILE_SIZE_MB}MB per document
        </p>
      </div>

      {/* Validation Error Message */}
      {error && (
        <div className={`p-2.5 rounded border text-xs flex items-center space-x-2 ${
          theme === 'light'
            ? 'bg-rose-50 border-rose-200 text-rose-800'
            : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
        }`}>
          <AlertTriangle className="w-4 h-4 flex-shrink-0 text-rose-500" />
          <span>{error}</span>
        </div>
      )}

      {/* Uploaded Files Table */}
      {files.length > 0 && (
        <div className="space-y-2">
          <div className={`flex items-center justify-between text-[11px] font-mono uppercase px-1 ${
            theme === 'light' ? 'text-slate-600' : 'text-slate-400'
          }`}>
            <span>Staged Documents ({files.length})</span>
            <button
              type="button"
              onClick={() => setFiles([])}
              className="text-slate-400 hover:text-rose-500 transition-colors"
            >
              Clear All
            </button>
          </div>

          <div className="max-h-48 overflow-y-auto space-y-1.5 pr-1">
            {files.map((file, idx) => {
              const ext = file.name.split('.').pop().toUpperCase();
              return (
                <div
                  key={idx}
                  className={`flex items-center justify-between p-2.5 rounded border text-xs transition-colors ${
                    theme === 'light'
                      ? 'bg-slate-50 border-slate-200 text-slate-900'
                      : 'bg-[#090b0e] border-[#1e2634] text-slate-100'
                  }`}
                >
                  <div className="flex items-center space-x-2.5 truncate">
                    <div className={`w-6 h-6 rounded border flex items-center justify-center flex-shrink-0 font-mono text-[10px] font-bold ${
                      theme === 'light'
                        ? 'bg-cyan-50 border-cyan-200 text-cyan-700'
                        : 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400'
                    }`}>
                      {ext}
                    </div>
                    <div className="truncate">
                      <p className={`font-medium truncate text-xs ${theme === 'light' ? 'text-slate-900' : 'text-slate-200'}`}>{file.name}</p>
                      <p className={`text-[10px] font-mono ${theme === 'light' ? 'text-slate-500' : 'text-slate-500'}`}>{formatFileSize(file.size)}</p>
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      removeFile(idx);
                    }}
                    className="p-1 text-slate-400 hover:text-rose-500 transition-colors ml-2"
                    title="Remove document"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResumeUploader;
