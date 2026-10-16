import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Briefcase, Clock, ArrowRight, RefreshCw, Plus, Cpu } from 'lucide-react';
import { listJobsApi } from '../api/jobs';
import { useTheme } from '../context/ThemeContext';
import LoadingSpinner, { TableSkeleton } from '../components/LoadingState';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

export const Jobs = () => {
  const { theme } = useTheme();
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchJobs = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await listJobsApi();
      setJobs(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message || 'Failed to load jobs directory.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  if (loading) {
    return (
      <div className="space-y-6">
        <div className={`h-8 w-48 animate-pulse rounded ${theme === 'light' ? 'bg-slate-200' : 'bg-[#131822]'}`} />
        <TableSkeleton rows={6} />
      </div>
    );
  }

  return (
    <div className="space-y-5 animate-fade-in">
      {/* Header Panel */}
      <div className={`p-4 rounded-lg border flex flex-col md:flex-row md:items-center justify-between gap-4 transition-colors ${
        theme === 'light' ? 'bg-white border-slate-200 shadow-sm' : 'bg-[#0e1219] border-[#1e2634]'
      }`}>
        <div>
          <div className="flex items-center space-x-2">
            <Briefcase className="w-4 h-4 text-cyan-500" />
            <h1 className={`text-xl font-bold tracking-tight ${theme === 'light' ? 'text-slate-900' : 'text-slate-100'}`}>
              Screening Jobs Directory
            </h1>
            <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${
              theme === 'light' ? 'bg-cyan-50 text-cyan-700 border border-cyan-200' : 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30'
            }`}>
              {jobs.length} Active Jobs
            </span>
          </div>
          <p className={`text-xs mt-0.5 ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
            Recruiter job postings and candidate evaluation datasets stored in MongoDB
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => navigate('/screening/new')}
            className="px-3.5 py-1.5 rounded bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs flex items-center space-x-1.5 transition-all shadow-sm"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>New Job Screening</span>
          </button>
          <button
            onClick={fetchJobs}
            className={`p-1.5 rounded border transition-colors ${
              theme === 'light'
                ? 'bg-slate-100 border-slate-300 text-slate-700 hover:bg-slate-200'
                : 'bg-[#131822] border-[#1e2634] text-slate-300 hover:text-white'
            }`}
            title="Refresh list"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {error && <ErrorMessage title="Jobs Sync Error" message={error} onRetry={fetchJobs} />}

      {/* Jobs Workstation List */}
      {jobs.length === 0 ? (
        <EmptyState
          icon={Briefcase}
          title="No Screening Jobs Posted"
          description="Create your first job description to initiate candidate AI screening."
          actionLabel="Create First Screening Job"
          onAction={() => navigate('/screening/new')}
        />
      ) : (
        <div className="space-y-2">
          {jobs.map((job) => {
            const jobId = job._id || job.job_id;
            return (
              <div
                key={jobId}
                onClick={() => navigate(`/screening/${jobId}/results`)}
                className={`p-3.5 rounded border cursor-pointer transition-all duration-150 flex flex-col md:flex-row md:items-center justify-between gap-3 group ${
                  theme === 'light'
                    ? 'bg-white border-slate-200 hover:border-cyan-500/50 hover:bg-cyan-50/20 shadow-sm'
                    : 'bg-[#0e1219] border-[#1e2634] hover:border-cyan-500/40'
                }`}
              >
                <div className="min-w-0">
                  <div className="flex items-center space-x-2">
                    <span className="w-2 h-2 rounded-full bg-cyan-500" />
                    <h3 className={`font-bold transition-colors text-sm truncate ${
                      theme === 'light' ? 'text-slate-900 group-hover:text-cyan-600' : 'text-slate-100 group-hover:text-cyan-300'
                    }`}>
                      {job.job_title || 'Untitled Job Position'}
                    </h3>
                  </div>
                  <p className={`text-xs line-clamp-1 mt-1 pl-4 ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
                    {job.job_description}
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

                  <span className={`px-3 py-1 rounded text-xs font-mono font-bold transition-colors border ${
                    theme === 'light'
                      ? 'bg-cyan-50 text-cyan-700 border-cyan-200 group-hover:bg-cyan-100'
                      : 'bg-[#131822] border-[#1e2634] text-cyan-400 group-hover:border-cyan-500/40'
                  }`}>
                    View Results &rarr;
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default Jobs;
