import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Briefcase,
  Users,
  FileCheck,
  Plus,
  ArrowRight,
  Cpu,
  Activity,
  Database,
  Server,
  Sparkles,
  BarChart3,
  Clock,
} from 'lucide-react';
import { listJobsApi } from '../api/jobs';
import { listCandidatesApi } from '../api/candidates';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import LoadingSpinner, { CardSkeleton, TableSkeleton } from '../components/LoadingState';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

export const Dashboard = () => {
  const { user } = useAuth();
  const { theme } = useTheme();
  const navigate = useNavigate();

  const [jobs, setJobs] = useState([]);
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [jobsData, candidatesData] = await Promise.all([
        listJobsApi().catch(() => []),
        listCandidatesApi().catch(() => []),
      ]);
      setJobs(Array.isArray(jobsData) ? jobsData : []);
      setCandidates(Array.isArray(candidatesData) ? candidatesData : []);
    } catch (err) {
      setError(err.message || 'Failed to load dashboard metrics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const totalJobs = jobs.length;
  const totalCandidates = candidates.length;
  const totalScreenings = jobs.length;

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <CardSkeleton />
          <CardSkeleton />
          <CardSkeleton />
          <CardSkeleton />
        </div>
        <TableSkeleton rows={5} />
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Top System Status Header */}
      <div className={`p-5 rounded-lg border transition-colors flex flex-col lg:flex-row lg:items-center justify-between gap-4 ${
        theme === 'light' ? 'bg-white border-slate-200 shadow-sm' : 'bg-[#0e1219] border-[#1e2634]'
      }`}>
        <div>
          <div className="flex items-center space-x-2 mb-1">
            <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase tracking-widest ${
              theme === 'light'
                ? 'bg-cyan-50 text-cyan-700 border border-cyan-200'
                : 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30'
            }`}>
              AI Command Station
            </span>
            <span className={`text-xs font-mono ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>v1.0.0</span>
          </div>
          <h1 className={`text-xl md:text-2xl font-bold tracking-tight ${theme === 'light' ? 'text-slate-900' : 'text-slate-100'}`}>
            Resume Intelligence
          </h1>
          <p className={`text-xs mt-0.5 ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
            AI-assisted candidate screening, parsing, semantic embedding matching, and shortlisting
          </p>
        </div>

        {/* System Component Health Monitors */}
        <div className={`flex items-center space-x-3 p-2.5 rounded border ${
          theme === 'light' ? 'bg-slate-100 border-slate-200' : 'bg-[#131822] border-[#1e2634]'
        }`}>
          <div className={`flex items-center space-x-2 px-2.5 py-1 rounded border text-xs ${
            theme === 'light' ? 'bg-white border-slate-200 text-slate-800' : 'bg-[#090b0e] border-[#1e2634] text-slate-300'
          }`}>
            <Cpu className="w-3.5 h-3.5 text-cyan-500" />
            <span className="text-[11px] font-medium">AI Engine</span>
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          </div>

          <div className={`flex items-center space-x-2 px-2.5 py-1 rounded border text-xs ${
            theme === 'light' ? 'bg-white border-slate-200 text-slate-800' : 'bg-[#090b0e] border-[#1e2634] text-slate-300'
          }`}>
            <Server className="w-3.5 h-3.5 text-cyan-500" />
            <span className="text-[11px] font-medium">FastAPI</span>
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
          </div>

          <div className={`flex items-center space-x-2 px-2.5 py-1 rounded border text-xs ${
            theme === 'light' ? 'bg-white border-slate-200 text-slate-800' : 'bg-[#090b0e] border-[#1e2634] text-slate-300'
          }`}>
            <Database className="w-3.5 h-3.5 text-cyan-500" />
            <span className="text-[11px] font-medium">MongoDB</span>
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
          </div>
        </div>
      </div>

      {error && <ErrorMessage title="Dashboard Sync Error" message={error} onRetry={loadDashboardData} />}

      {/* Structured Screening Overview Panel */}
      <div className={`p-4 rounded-lg border space-y-3 transition-colors ${
        theme === 'light' ? 'bg-white border-slate-200 shadow-sm' : 'bg-[#0e1219] border-[#1e2634]'
      }`}>
        <div className={`flex items-center justify-between border-b pb-2.5 ${
          theme === 'light' ? 'border-slate-200' : 'border-[#1e2634]'
        }`}>
          <span className={`text-xs font-mono uppercase tracking-widest font-bold flex items-center space-x-2 ${
            theme === 'light' ? 'text-slate-600' : 'text-slate-400'
          }`}>
            <BarChart3 className="w-3.5 h-3.5 text-cyan-500" />
            <span>Screening Overview</span>
          </span>
          <button
            onClick={() => navigate('/screening/new')}
            className="px-3 py-1 rounded bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs flex items-center space-x-1.5 transition-all shadow-sm"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Start Screening</span>
          </button>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <div className={`p-3.5 rounded border transition-colors ${
            theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#131822] border-[#1e2634]'
          }`}>
            <p className={`text-[11px] font-mono uppercase tracking-wider ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>Total Candidates</p>
            <div className="flex items-baseline justify-between mt-1">
              <span className={`text-2xl font-bold font-mono ${theme === 'light' ? 'text-cyan-700' : 'text-cyan-400'}`}>{totalCandidates}</span>
              <Users className={`w-4 h-4 ${theme === 'light' ? 'text-slate-400' : 'text-slate-500'}`} />
            </div>
          </div>

          <div className={`p-3.5 rounded border transition-colors ${
            theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#131822] border-[#1e2634]'
          }`}>
            <p className={`text-[11px] font-mono uppercase tracking-wider ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>Active Jobs</p>
            <div className="flex items-baseline justify-between mt-1">
              <span className={`text-2xl font-bold font-mono ${theme === 'light' ? 'text-slate-900' : 'text-slate-100'}`}>{totalJobs}</span>
              <Briefcase className={`w-4 h-4 ${theme === 'light' ? 'text-slate-400' : 'text-slate-500'}`} />
            </div>
          </div>

          <div className={`p-3.5 rounded border transition-colors ${
            theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#131822] border-[#1e2634]'
          }`}>
            <p className={`text-[11px] font-mono uppercase tracking-wider ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>Screenings Run</p>
            <div className="flex items-baseline justify-between mt-1">
              <span className={`text-2xl font-bold font-mono ${theme === 'light' ? 'text-slate-900' : 'text-slate-100'}`}>{totalScreenings}</span>
              <FileCheck className={`w-4 h-4 ${theme === 'light' ? 'text-slate-400' : 'text-slate-500'}`} />
            </div>
          </div>

          <div className={`p-3.5 rounded border transition-colors ${
            theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#131822] border-[#1e2634]'
          }`}>
            <p className={`text-[11px] font-mono uppercase tracking-wider ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>AI Pipeline</p>
            <div className="flex items-baseline justify-between mt-1">
              <span className={`text-sm sm:text-base font-bold font-mono ${theme === 'light' ? 'text-cyan-700' : 'text-cyan-400'}`}>Hybrid Scoring</span>
              <Sparkles className="w-4 h-4 text-cyan-500" />
            </div>
          </div>
        </div>
      </div>

      {/* Candidate Intelligence & Recent Screening Workstation */}
      <div className={`p-4 rounded-lg border space-y-4 transition-colors ${
        theme === 'light' ? 'bg-white border-slate-200 shadow-sm' : 'bg-[#0e1219] border-[#1e2634]'
      }`}>
        <div className={`flex items-center justify-between border-b pb-3 ${
          theme === 'light' ? 'border-slate-200' : 'border-[#1e2634]'
        }`}>
          <div>
            <h3 className={`text-sm font-bold uppercase tracking-wide flex items-center space-x-2 ${
              theme === 'light' ? 'text-slate-900' : 'text-slate-200'
            }`}>
              <span>Candidate Intelligence Workstation</span>
            </h3>
            <p className={`text-[11px] ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>Recent job screenings and candidate evaluations</p>
          </div>
          {jobs.length > 0 && (
            <button
              onClick={() => navigate('/jobs')}
              className={`text-xs font-mono flex items-center space-x-1 font-semibold ${
                theme === 'light' ? 'text-cyan-600 hover:text-cyan-700' : 'text-cyan-400 hover:text-cyan-300'
              }`}
            >
              <span>View All Jobs</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          )}
        </div>

        {jobs.length === 0 ? (
          <EmptyState
            icon={Briefcase}
            title="No Screening Workflows Initiated"
            description="Upload candidate resumes and job criteria to launch your first screening run."
            actionLabel="Start Resume Screening"
            onAction={() => navigate('/screening/new')}
          />
        ) : (
          <div className="space-y-3">
            {jobs.slice(0, 5).map((job) => {
              const jobId = job._id || job.job_id;
              return (
                <div
                  key={jobId}
                  onClick={() => navigate(`/screening/${jobId}/results`)}
                  className={`p-3.5 rounded border cursor-pointer transition-all duration-150 flex flex-col md:flex-row md:items-center justify-between gap-3 group ${
                    theme === 'light'
                      ? 'bg-slate-50 border-slate-200 hover:border-cyan-500/50 hover:bg-cyan-50/20'
                      : 'bg-[#131822] border-[#1e2634] hover:border-cyan-500/40'
                  }`}
                >
                  <div className="min-w-0">
                    <div className="flex items-center space-x-2">
                      <span className="w-2 h-2 rounded-full bg-cyan-500" />
                      <h4 className={`font-bold transition-colors text-sm truncate ${
                        theme === 'light' ? 'text-slate-900 group-hover:text-cyan-700' : 'text-slate-100 group-hover:text-cyan-300'
                      }`}>
                        {job.job_title || 'Untitled Job Position'}
                      </h4>
                    </div>
                    <p className={`text-xs line-clamp-1 mt-1 pl-4 ${
                      theme === 'light' ? 'text-slate-600' : 'text-slate-400'
                    }`}>
                      {job.job_description || 'No description available.'}
                    </p>
                  </div>

                  <div className={`flex items-center justify-between md:justify-end space-x-4 shrink-0 border-t md:border-t-0 pt-2 md:pt-0 ${
                    theme === 'light' ? 'border-slate-200' : 'border-[#1e2634]'
                  }`}>
                    <div className={`text-[11px] font-mono flex items-center space-x-1 ${
                      theme === 'light' ? 'text-slate-500' : 'text-slate-400'
                    }`}>
                      <Clock className="w-3.5 h-3.5 opacity-60" />
                      <span>{job.created_at ? new Date(job.created_at).toLocaleDateString() : 'Recent'}</span>
                    </div>

                    <div className="flex items-center space-x-2">
                      <span className={`px-2.5 py-1 rounded text-xs font-mono font-semibold transition-colors ${
                        theme === 'light'
                          ? 'bg-white border border-slate-300 text-cyan-700 group-hover:border-cyan-500'
                          : 'bg-[#090b0e] border border-[#1e2634] text-cyan-400 group-hover:border-cyan-500/40'
                      }`}>
                        View Rankings &rarr;
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
