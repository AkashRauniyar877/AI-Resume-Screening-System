import React, { useState } from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import LoadingSpinner from './LoadingState';

export const ProtectedRoute = () => {
  const { isAuthenticated, loading } = useAuth();
  const { theme } = useTheme();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  if (loading) {
    return (
      <div className={`min-h-screen flex items-center justify-center ${
        theme === 'light' ? 'bg-slate-50 text-slate-900' : 'bg-[#07090e] text-slate-100'
      }`}>
        <LoadingSpinner label="Verifying recruiter authorization..." size="lg" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Determine section title based on pathname
  const getTitle = () => {
    const path = location.pathname;
    if (path.startsWith('/dashboard')) return 'Dashboard Overview';
    if (path.startsWith('/screening/new')) return 'Create AI Resume Screening';
    if (path.includes('/results')) return 'Candidate Ranking Results';
    if (path.startsWith('/jobs')) return 'Screening Jobs Directory';
    if (path.startsWith('/candidates')) return 'Recruiter Candidates Database';
    if (path.startsWith('/profile')) return 'Recruiter Account Profile';
    return 'Recruiter Portal';
  };

  return (
    <div className={`flex min-h-screen transition-colors duration-200 ${
      theme === 'light' ? 'bg-slate-50 text-slate-900' : 'bg-[#07090e] text-slate-100'
    }`}>
      <Sidebar mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar onOpenMobileMenu={() => setMobileOpen(true)} title={getTitle()} />
        <main className="flex-1 p-4 md:p-8 max-w-7xl w-full mx-auto animate-fade-in">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default ProtectedRoute;
