import React from 'react';
import { Menu, Plus, Terminal, Brain, Sun, Moon } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export const Navbar = ({ onOpenMobileMenu, title = 'Recruiter Portal' }) => {
  const { user } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  return (
    <header className={`sticky top-0 z-20 w-full border-b px-4 md:px-6 py-3 flex items-center justify-between transition-colors ${
      theme === 'light'
        ? 'border-slate-200 bg-white/90 text-slate-800'
        : 'border-slate-800/80 bg-[#07090e]/90 text-slate-100'
    } backdrop-blur-md`}>
      <div className="flex items-center space-x-3">
        {/* Mobile menu trigger */}
        <button
          onClick={onOpenMobileMenu}
          className={`md:hidden p-1.5 rounded border transition-colors ${
            theme === 'light' ? 'bg-slate-100 border-slate-300 text-slate-700' : 'bg-slate-900 border-slate-800 text-slate-300'
          }`}
          aria-label="Open Navigation Menu"
        >
          <Menu className="w-4 h-4" />
        </button>

        <div className="flex items-center space-x-2.5 cursor-pointer" onClick={() => navigate('/dashboard')}>
          <div className={`w-7 h-7 rounded-lg ${theme === 'light' ? 'bg-cyan-600 text-white' : 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30'} flex items-center justify-center`}>
            <Brain className="w-4 h-4" />
          </div>
          <span className="text-sm md:text-base font-extrabold tracking-tight">
            Resume<span className="text-cyan-500">AI</span>
          </span>
          <span className="text-slate-400 text-xs hidden sm:inline">|</span>
          <span className={`text-xs font-semibold hidden sm:inline ${theme === 'light' ? 'text-slate-600' : 'text-slate-300'}`}>
            {title}
          </span>
        </div>
      </div>

      <div className="flex items-center space-x-3">
        {/* Theme Toggle Button */}
        <button
          onClick={toggleTheme}
          className={`p-1.5 rounded-lg border transition-all ${
            theme === 'light'
              ? 'bg-slate-100 border-slate-300 text-amber-600 hover:bg-slate-200'
              : 'bg-slate-900 border-slate-800 text-cyan-400 hover:bg-slate-800'
          }`}
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} mode`}
          aria-label="Toggle theme"
        >
          {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>

        <button
          onClick={() => navigate('/screening/new')}
          className="px-3.5 py-1.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs flex items-center space-x-1.5 transition-all shadow-sm shadow-cyan-500/20"
        >
          <Plus className="w-3.5 h-3.5 stroke-[2.5]" />
          <span className="hidden sm:inline">New Screening</span>
        </button>

        {user && (
          <div
            onClick={() => navigate('/profile')}
            className={`flex items-center space-x-2 px-2.5 py-1 rounded-lg border cursor-pointer transition-all ${
              theme === 'light'
                ? 'bg-slate-100 border-slate-300 hover:border-cyan-500/50'
                : 'bg-[#121824] border-slate-800 hover:border-cyan-500/40'
            }`}
          >
            <div className="w-6 h-6 rounded bg-cyan-500/20 text-cyan-400 font-mono font-bold text-[11px] flex items-center justify-center border border-cyan-500/30">
              {user.name ? user.name.charAt(0).toUpperCase() : 'R'}
            </div>
            <span className={`hidden md:inline text-xs font-medium ${theme === 'light' ? 'text-slate-700' : 'text-slate-300'}`}>{user.name}</span>
          </div>
        )}
      </div>
    </header>
  );
};

export default Navbar;
