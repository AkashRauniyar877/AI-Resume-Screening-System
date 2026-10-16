import React from 'react';
import { User, Mail, ShieldCheck, Key, LogOut, Cpu } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { useNavigate } from 'react-router-dom';

export const Profile = () => {
  const { user, logout } = useAuth();
  const { theme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 animate-fade-in">
      {/* Profile Header */}
      <div className={`p-4 rounded-lg border flex items-center justify-between transition-colors ${
        theme === 'light' ? 'bg-white border-slate-200 shadow-sm' : 'bg-[#0e1219] border-[#1e2634]'
      }`}>
        <div>
          <h1 className={`text-xl font-bold tracking-tight ${theme === 'light' ? 'text-slate-900' : 'text-slate-100'}`}>
            Recruiter Account & Security
          </h1>
          <p className={`text-xs mt-0.5 ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
            Manage recruiter credentials and data isolation settings
          </p>
        </div>
      </div>

      {/* Recruiter Details Card */}
      <div className={`p-5 rounded-lg border space-y-4 transition-colors ${
        theme === 'light' ? 'bg-white border-slate-200 shadow-sm' : 'bg-[#0e1219] border-[#1e2634]'
      }`}>
        <div className={`flex items-center space-x-3 border-b pb-3 ${
          theme === 'light' ? 'border-slate-200' : 'border-[#1e2634]'
        }`}>
          <div className={`w-10 h-10 rounded font-mono font-bold text-base flex items-center justify-center border ${
            theme === 'light' ? 'bg-cyan-50 border-cyan-200 text-cyan-700' : 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400'
          }`}>
            {user?.name ? user.name.charAt(0).toUpperCase() : 'R'}
          </div>
          <div>
            <h3 className={`text-base font-bold ${theme === 'light' ? 'text-slate-900' : 'text-slate-100'}`}>
              {user?.name || 'Recruiter'}
            </h3>
            <p className={`text-xs font-mono ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>
              Role: {user?.role || 'recruiter'}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono">
          <div className={`p-3 rounded border space-y-1 ${
            theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#090b0e] border-[#1e2634]'
          }`}>
            <span className={`uppercase text-[10px] font-bold ${theme === 'light' ? 'text-slate-500' : 'text-slate-500'}`}>
              Account User ID
            </span>
            <p className={`font-bold truncate ${theme === 'light' ? 'text-slate-800' : 'text-slate-200'}`}>
              {user?.user_id || 'usr_default'}
            </p>
          </div>

          <div className={`p-3 rounded border space-y-1 ${
            theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#090b0e] border-[#1e2634]'
          }`}>
            <span className={`uppercase text-[10px] font-bold ${theme === 'light' ? 'text-slate-500' : 'text-slate-500'}`}>
              Recruiter Email
            </span>
            <p className={`font-bold truncate ${theme === 'light' ? 'text-slate-800' : 'text-slate-200'}`}>
              {user?.email || 'N/A'}
            </p>
          </div>
        </div>

        <div className={`p-3.5 rounded border flex items-center justify-between ${
          theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#090b0e] border-[#1e2634]'
        }`}>
          <div className="flex items-center space-x-2 text-xs">
            <ShieldCheck className="w-4 h-4 text-emerald-500" />
            <span className={theme === 'light' ? 'text-slate-700' : 'text-slate-300'}>
              Recruiter Data Isolation Enforcement Active
            </span>
          </div>
          <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${
            theme === 'light'
              ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
              : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
          }`}>
            PROTECTED
          </span>
        </div>

        <div className={`pt-2 border-t ${theme === 'light' ? 'border-slate-200' : 'border-[#1e2634]'}`}>
          <button
            onClick={handleLogout}
            className={`px-4 py-2 rounded border text-xs font-mono font-bold flex items-center space-x-2 transition-all ${
              theme === 'light'
                ? 'bg-rose-50 hover:bg-rose-100 text-rose-700 border-rose-200'
                : 'bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border-rose-500/30'
            }`}
          >
            <LogOut className="w-4 h-4" />
            <span>Sign Out Recruiter Session</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Profile;
