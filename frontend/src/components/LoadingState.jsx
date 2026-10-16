import React from 'react';
import { Loader2 } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export const LoadingSpinner = ({ label = 'Loading AI Engine data...', size = 'md' }) => {
  const { theme } = useTheme();
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-10 h-10',
  };

  return (
    <div className={`flex flex-col items-center justify-center p-8 ${
      theme === 'light' ? 'text-slate-600' : 'text-slate-400'
    }`}>
      <Loader2 className={`animate-spin ${sizeClasses[size] || sizeClasses.md} text-cyan-500 mb-3`} />
      {label && <p className="text-xs font-mono tracking-wide">{label}</p>}
    </div>
  );
};

export const CardSkeleton = () => {
  const { theme } = useTheme();
  return (
    <div className={`animate-pulse rounded-lg p-5 border space-y-3 ${
      theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#0e1219] border-[#1e2634]'
    }`}>
      <div className={`h-3 rounded w-1/3 ${theme === 'light' ? 'bg-slate-200' : 'bg-[#1e2634]'}`}></div>
      <div className={`h-7 rounded w-1/2 ${theme === 'light' ? 'bg-slate-200' : 'bg-[#1e2634]'}`}></div>
      <div className={`h-3 rounded w-2/3 ${theme === 'light' ? 'bg-slate-200' : 'bg-[#1e2634]'}`}></div>
    </div>
  );
};

export const TableSkeleton = ({ rows = 5 }) => {
  const { theme } = useTheme();
  return (
    <div className="animate-pulse space-y-2">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className={`h-12 border rounded-lg flex items-center px-4 space-x-4 ${
          theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#0e1219] border-[#1e2634]'
        }`}>
          <div className={`h-4 rounded w-6 ${theme === 'light' ? 'bg-slate-200' : 'bg-[#1e2634]'}`}></div>
          <div className={`h-4 rounded w-36 ${theme === 'light' ? 'bg-slate-200' : 'bg-[#1e2634]'}`}></div>
          <div className={`h-4 rounded w-44 ${theme === 'light' ? 'bg-slate-200' : 'bg-[#1e2634]'}`}></div>
          <div className={`h-4 rounded flex-1 ${theme === 'light' ? 'bg-slate-200' : 'bg-[#1e2634]'}`}></div>
          <div className={`h-5 rounded w-16 ${theme === 'light' ? 'bg-slate-200' : 'bg-[#1e2634]'}`}></div>
        </div>
      ))}
    </div>
  );
};

export default LoadingSpinner;
