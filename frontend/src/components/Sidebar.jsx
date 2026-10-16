import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  PlusSquare,
  Briefcase,
  Users,
  User,
  LogOut,
  Brain,
  ChevronRight,
  Home,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export const Sidebar = ({ mobileOpen, setMobileOpen }) => {
  const { user, logout } = useAuth();
  const { theme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { label: 'New Screening', path: '/screening/new', icon: PlusSquare },
    { label: 'Screening Jobs', path: '/jobs', icon: Briefcase },
    { label: 'Candidates', path: '/candidates', icon: Users },
    { label: 'Account Profile', path: '/profile', icon: User },
  ];

  const content = (
    <div className="flex flex-col h-full justify-between">
      <div>
        {/* Product Brand Header */}
        <div className={`px-3 py-4 mb-4 border-b ${theme === 'light' ? 'border-slate-200' : 'border-slate-800'}`}>
          <div className="flex items-center space-x-2.5 cursor-pointer" onClick={() => navigate('/dashboard')}>
            <div className={`w-8 h-8 rounded-lg ${theme === 'light' ? 'bg-cyan-600 text-white' : 'bg-cyan-500/10 border border-cyan-500/30 text-cyan-400'} flex items-center justify-center shadow-sm`}>
              <Brain className="w-4.5 h-4.5" />
            </div>
            <div>
              <h1 className="text-base font-extrabold tracking-tight leading-tight">
                Resume<span className="text-cyan-500">AI</span>
              </h1>
              <p className={`text-[10px] font-mono font-semibold uppercase tracking-wider ${theme === 'light' ? 'text-slate-500' : 'text-cyan-400'}`}>
                Screening Platform
              </p>
            </div>
          </div>

          {/* Engine Status Indicator */}
          <div className={`mt-3 px-2.5 py-1.5 rounded-lg border flex items-center justify-between text-[11px] ${
            theme === 'light' ? 'bg-slate-100 border-slate-200' : 'bg-[#101622] border-slate-800'
          }`}>
            <span className={theme === 'light' ? 'text-slate-600 font-medium' : 'text-slate-400 font-medium'}>Engine Status</span>
            <span className="flex items-center space-x-1.5 text-emerald-500 font-mono text-[10px] font-semibold">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              <span>Online</span>
            </span>
          </div>
        </div>

        {/* Navigation Section */}
        <div className="px-1 mb-2">
          <p className={`text-[10px] font-mono uppercase tracking-widest px-3 mb-2 font-semibold ${
            theme === 'light' ? 'text-slate-400' : 'text-slate-500'
          }`}>
            Workstation
          </p>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileOpen && setMobileOpen(false)}
                  className={({ isActive }) =>
                    `flex items-center justify-between px-3 py-2.5 rounded-lg font-medium text-xs transition-all duration-150 ${
                      isActive
                        ? theme === 'light'
                          ? 'bg-cyan-500/10 text-cyan-700 font-bold border-l-2 border-cyan-600'
                          : 'bg-cyan-500/10 text-cyan-300 font-bold border-l-2 border-cyan-400'
                        : theme === 'light'
                          ? 'text-slate-600 hover:text-slate-900 hover:bg-slate-100 border-l-2 border-transparent'
                          : 'text-slate-400 hover:text-slate-200 hover:bg-[#101622] border-l-2 border-transparent'
                    }`
                  }
                >
                  <div className="flex items-center space-x-2.5">
                    <Icon className="w-4 h-4 flex-shrink-0" />
                    <span>{item.label}</span>
                  </div>
                  <ChevronRight className="w-3 h-3 opacity-40" />
                </NavLink>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Recruiter Profile & Logout */}
      <div className={`pt-3 border-t ${theme === 'light' ? 'border-slate-200' : 'border-slate-800'}`}>
        {user && (
          <div className={`p-2.5 rounded-lg border mb-2.5 flex items-center justify-between ${
            theme === 'light' ? 'bg-slate-100 border-slate-200' : 'bg-[#101622] border-slate-800'
          }`}>
            <div className="flex items-center space-x-2.5 min-w-0">
              <div className="w-7 h-7 rounded-lg bg-cyan-500/20 text-cyan-400 font-mono font-bold text-xs flex items-center justify-center border border-cyan-500/30 flex-shrink-0">
                {user.name ? user.name.charAt(0).toUpperCase() : 'R'}
              </div>
              <div className="truncate">
                <p className={`text-xs font-semibold truncate ${theme === 'light' ? 'text-slate-800' : 'text-slate-200'}`}>{user.name || 'Recruiter'}</p>
                <p className="text-[10px] text-slate-400 font-mono truncate">{user.email}</p>
              </div>
            </div>
          </div>
        )}

        <button
          onClick={handleLogout}
          className={`w-full flex items-center justify-center space-x-2 px-3 py-2 rounded-lg text-xs font-medium border transition-all duration-150 ${
            theme === 'light'
              ? 'text-slate-600 hover:text-rose-600 hover:bg-rose-50 border-slate-200 hover:border-rose-200'
              : 'text-slate-400 hover:text-rose-300 hover:bg-rose-500/10 border-slate-800 hover:border-rose-500/30'
          }`}
        >
          <LogOut className="w-3.5 h-3.5" />
          <span>Sign Out</span>
        </button>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Navigation Rail */}
      <aside className={`hidden md:flex flex-col w-60 border-r p-3 min-h-screen sticky top-0 h-screen z-30 transition-colors ${
        theme === 'light' ? 'border-slate-200 bg-white' : 'border-slate-800 bg-[#07090e]'
      }`}>
        {content}
      </aside>

      {/* Mobile Drawer Overlay */}
      {mobileOpen && (
        <div className="md:hidden fixed inset-0 z-50 flex">
          <div
            className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm transition-opacity"
            onClick={() => setMobileOpen(false)}
          />
          <div className={`relative flex-1 flex flex-col max-w-xs w-full border-r p-3 ${
            theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#07090e] border-slate-800'
          }`}>
            {content}
          </div>
        </div>
      )}
    </>
  );
};

export default Sidebar;
