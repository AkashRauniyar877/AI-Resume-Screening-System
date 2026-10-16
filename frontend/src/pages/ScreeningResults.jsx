import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { Award, Briefcase, Users, ArrowLeft, RefreshCw, Cpu, Layers } from 'lucide-react';
import { getJobResultsApi, listJobsApi } from '../api/jobs';
import { useTheme } from '../context/ThemeContext';
import CandidateTable from '../components/CandidateTable';
import LoadingSpinner, { TableSkeleton } from '../components/LoadingState';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';

export const ScreeningResults = () => {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const { theme } = useTheme();

  const [jobInfo, setJobInfo] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchResults = async () => {
    setLoading(true);
    setError(null);
    try {
      const jobs = await listJobsApi().catch(() => []);
      const currentJob = jobs.find((j) => (j._id || j.job_id) === jobId);
      if (currentJob) {
        setJobInfo(currentJob);
      }

      const resData = await getJobResultsApi(jobId);
      setResults(resData.results || []);
    } catch (err) {
      setError(err.message || 'Failed to fetch candidate screening results for this job.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResults();
  }, [jobId]);

  if (loading) {
    return (
      <div className="space-y-6">
        <div className={`h-8 w-48 animate-pulse rounded ${theme === 'light' ? 'bg-slate-200' : 'bg-[#131822]'}`} />
        <TableSkeleton rows={6} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6 max-w-2xl mx-auto py-12">
        <ErrorMessage title="Screening Results Error" message={error} onRetry={fetchResults} />
        <button
          onClick={() => navigate('/jobs')}
          className={`px-3 py-1.5 rounded text-xs font-mono font-semibold flex items-center space-x-1.5 border ${
            theme === 'light'
              ? 'bg-slate-100 border-slate-300 text-slate-700 hover:bg-slate-200'
              : 'bg-[#131822] border-[#1e2634] text-slate-300 hover:text-white'
          }`}
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Screening Jobs Directory</span>
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header Bar */}
      <div className={`p-4 rounded-lg border flex flex-col md:flex-row md:items-center justify-between gap-4 transition-colors ${
        theme === 'light' ? 'bg-white border-slate-200 shadow-sm' : 'bg-[#0e1219] border-[#1e2634]'
      }`}>
        <div>
          <button
            onClick={() => navigate('/jobs')}
            className={`text-[11px] font-mono flex items-center space-x-1 mb-1 transition-colors ${
              theme === 'light' ? 'text-slate-500 hover:text-cyan-600' : 'text-slate-400 hover:text-cyan-400'
            }`}
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Jobs Directory</span>
          </button>
          <div className="flex items-center space-x-2">
            <h1 className={`text-xl font-bold tracking-tight ${theme === 'light' ? 'text-slate-900' : 'text-slate-100'}`}>
              {jobInfo?.job_title || location.state?.jobTitle || 'Candidate Screening Results'}
            </h1>
            <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${
              theme === 'light' ? 'bg-cyan-50 text-cyan-700 border border-cyan-200' : 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30'
            }`}>
              {results.length} Candidates Screened
            </span>
          </div>
        </div>

        <button
          onClick={fetchResults}
          className={`px-3.5 py-1.5 rounded text-xs font-mono font-semibold flex items-center space-x-1.5 transition-all border ${
            theme === 'light'
              ? 'bg-slate-100 border-slate-300 text-slate-700 hover:bg-slate-200'
              : 'bg-[#131822] border-[#1e2634] hover:border-cyan-500/40 text-slate-300'
          }`}
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Results</span>
        </button>
      </div>

      {/* Target Job Description Requirements Summary */}
      {jobInfo && (
        <div className={`p-4 rounded-lg border space-y-2.5 transition-colors ${
          theme === 'light' ? 'bg-white border-slate-200 shadow-sm' : 'bg-[#0e1219] border-[#1e2634]'
        }`}>
          <div className={`flex items-center space-x-2 text-xs font-mono font-bold uppercase tracking-wider ${
            theme === 'light' ? 'text-cyan-700' : 'text-cyan-400'
          }`}>
            <Briefcase className="w-3.5 h-3.5" />
            <span>Target Job Requirements Benchmarks</span>
          </div>
          <p className={`text-xs leading-relaxed p-3.5 rounded border ${
            theme === 'light' ? 'bg-slate-50 border-slate-200 text-slate-700' : 'bg-[#090b0e] border-[#1e2634] text-slate-300'
          }`}>
            {jobInfo.job_description}
          </p>
          {Array.isArray(jobInfo.required_skills) && jobInfo.required_skills.length > 0 && (
            <div className="flex flex-wrap items-center gap-1.5 pt-1">
              <span className={`text-xs font-mono font-semibold mr-1 ${
                theme === 'light' ? 'text-slate-500' : 'text-slate-400'
              }`}>Required Skills:</span>
              {jobInfo.required_skills.map((skill, idx) => (
                <span
                  key={idx}
                  className={`px-2 py-0.5 rounded text-[10px] font-mono border ${
                    theme === 'light'
                      ? 'bg-cyan-50 text-cyan-700 border-cyan-200'
                      : 'bg-cyan-500/10 text-cyan-300 border-cyan-500/20'
                  }`}
                >
                  {skill}
                </span>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Candidate Ranking Section */}
      <div className="space-y-3">
        <div className="flex items-center justify-between px-1">
          <h3 className={`text-sm font-bold uppercase tracking-wide flex items-center space-x-2 ${
            theme === 'light' ? 'text-slate-900' : 'text-slate-200'
          }`}>
            <Award className="w-4 h-4 text-cyan-500" />
            <span>Authoritative Candidate Rankings</span>
          </h3>
          <span className={`text-[11px] font-mono ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>
            Ranked by AI Hybrid Composite Scoring
          </span>
        </div>

        {results.length === 0 ? (
          <EmptyState
            icon={Users}
            title="No Candidates Found"
            description="No candidate records were returned for this job screening."
          />
        ) : (
          <CandidateTable candidates={results} />
        )}
      </div>
    </div>
  );
};

export default ScreeningResults;
