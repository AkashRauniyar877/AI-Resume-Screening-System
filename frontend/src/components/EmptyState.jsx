import React from 'react';
import { Inbox } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export const EmptyState = ({
  icon: Icon = Inbox,
  title = 'No Data Found',
  description = 'There are no items to display at this time.',
  actionLabel,
  onAction,
}) => {
  const { theme } = useTheme();

  return (
    <div className={`flex flex-col items-center justify-center p-12 text-center rounded-2xl border border-dashed transition-colors ${
      theme === 'light'
        ? 'border-slate-300 bg-slate-50/70'
        : 'border-slate-700/80 bg-slate-900/30'
    }`}>
      <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mb-4 border ${
        theme === 'light'
          ? 'bg-cyan-50 border-cyan-200 text-cyan-700'
          : 'bg-cyan-500/10 border-cyan-500/20 text-cyan-400'
      }`}>
        <Icon className="w-7 h-7" />
      </div>
      <h3 className={`text-lg font-semibold mb-1 ${
        theme === 'light' ? 'text-slate-900' : 'text-slate-200'
      }`}>{title}</h3>
      <p className={`text-sm max-w-sm mb-6 leading-relaxed ${
        theme === 'light' ? 'text-slate-600' : 'text-slate-400'
      }`}>{description}</p>
      {actionLabel && onAction && (
        <button
          onClick={onAction}
          className="px-5 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-sm transition-all shadow-md flex items-center space-x-2"
        >
          <span>{actionLabel}</span>
        </button>
      )}
    </div>
  );
};

export default EmptyState;
