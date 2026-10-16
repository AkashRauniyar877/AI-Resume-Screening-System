import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export const ErrorMessage = ({
  title = 'Something went wrong',
  message = 'An error occurred while processing your request.',
  onRetry,
}) => {
  const { theme } = useTheme();

  return (
    <div className={`p-4 rounded-xl border flex items-start space-x-3 transition-colors ${
      theme === 'light'
        ? 'border-rose-200 bg-rose-50 text-rose-800'
        : 'border-red-500/30 bg-red-500/10 text-red-300'
    }`}>
      <AlertCircle className={`w-5 h-5 mt-0.5 flex-shrink-0 ${
        theme === 'light' ? 'text-rose-600' : 'text-red-400'
      }`} />
      <div className="flex-1 text-sm">
        <h4 className={`font-semibold mb-0.5 ${
          theme === 'light' ? 'text-rose-900' : 'text-red-200'
        }`}>{title}</h4>
        <p className={`leading-relaxed ${
          theme === 'light' ? 'text-rose-700' : 'text-red-300/90'
        }`}>{message}</p>
        {onRetry && (
          <button
            onClick={onRetry}
            className={`mt-3 inline-flex items-center space-x-1.5 text-xs font-semibold underline transition-all ${
              theme === 'light' ? 'text-rose-800 hover:text-rose-950' : 'text-red-200 hover:text-white'
            }`}
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Try again</span>
          </button>
        )}
      </div>
    </div>
  );
};

export default ErrorMessage;
