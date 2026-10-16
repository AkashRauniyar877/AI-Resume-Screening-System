import React, { useEffect, useState } from 'react';
import { Users, Search, Filter, RefreshCw, FileText, Download, User, AlertCircle, Loader2 } from 'lucide-react';
import { listCandidatesApi } from '../api/candidates';
import { useTheme } from '../context/ThemeContext';
import LoadingSpinner, { TableSkeleton } from '../components/LoadingState';
import ErrorMessage from '../components/ErrorMessage';
import EmptyState from '../components/EmptyState';
import CandidateDetails from '../components/CandidateDetails';
import { viewResumeApi, downloadResumeApi } from '../api/resumes';

export const Candidates = () => {
  const { theme } = useTheme();
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [actionLoading, setActionLoading] = useState(null);
  const [actionError, setActionError] = useState(null);

  const fetchCandidates = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await listCandidatesApi();
      setCandidates(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message || 'Failed to load candidates database.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCandidates();
  }, []);

  const filteredCandidates = candidates.filter((c) => {
    const name = (c.name || c.candidate_info?.name || '').toLowerCase();
    const email = (c.email || c.candidate_info?.email || '').toLowerCase();
    const query = searchQuery.toLowerCase();
    return name.includes(query) || email.includes(query);
  });

  const handleViewResume = async (e, resumeId) => {
    e.stopPropagation();
    if (!resumeId) {
      setActionError('Resume ID unavailable.');
      return;
    }
    setActionError(null);
    setActionLoading({ id: resumeId, type: 'view' });
    try {
      await viewResumeApi(resumeId);
    } catch (err) {
      setActionError(err.message || 'Failed to view original resume.');
    } finally {
      setActionLoading(null);
    }
  };

  const handleDownloadResume = async (e, resumeId) => {
    e.stopPropagation();
    if (!resumeId) {
      setActionError('Resume ID unavailable.');
      return;
    }
    setActionError(null);
    setActionLoading({ id: resumeId, type: 'download' });
    try {
      await downloadResumeApi(resumeId);
    } catch (err) {
      setActionError(err.message || 'Failed to download original resume.');
    } finally {
      setActionLoading(null);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className={`h-8 w-48 animate-pulse rounded ${theme === 'light' ? 'bg-slate-200' : 'bg-[#131822]'}`} />
        <TableSkeleton rows={8} />
      </div>
    );
  }

  return (
    <div className="space-y-5 animate-fade-in">
      {/* Header & Search Bar */}
      <div className={`p-4 rounded-lg border flex flex-col md:flex-row md:items-center justify-between gap-4 transition-colors ${
        theme === 'light' ? 'bg-white border-slate-200 shadow-sm' : 'bg-[#0e1219] border-[#1e2634]'
      }`}>
        <div>
          <div className="flex items-center space-x-2">
            <Users className="w-4 h-4 text-cyan-500" />
            <h1 className={`text-xl font-bold tracking-tight ${theme === 'light' ? 'text-slate-900' : 'text-slate-100'}`}>
              Recruiter Candidates Database
            </h1>
            <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold ${
              theme === 'light' ? 'bg-cyan-50 text-cyan-700 border border-cyan-200' : 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30'
            }`}>
              {candidates.length} Profiles
            </span>
          </div>
          <p className={`text-xs mt-0.5 ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
            Recruiter isolated database containing extracted skills, experience metadata, and resume files
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <div className="relative flex-1 md:w-64">
            <Search className={`w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 ${
              theme === 'light' ? 'text-slate-400' : 'text-slate-500'
            }`} />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search candidate name or email..."
              className={`w-full pl-9 pr-3 py-1.5 rounded text-xs focus:outline-none focus:border-cyan-500 transition-all font-medium ${
                theme === 'light'
                  ? 'bg-slate-50 border border-slate-300 text-slate-900 placeholder-slate-400'
                  : 'bg-[#090b0e] border border-[#1e2634] text-slate-100 placeholder-slate-600'
              }`}
            />
          </div>
          <button
            onClick={fetchCandidates}
            className={`p-1.5 rounded border transition-colors ${
              theme === 'light'
                ? 'bg-slate-100 border-slate-300 text-slate-700 hover:bg-slate-200'
                : 'bg-[#131822] border-[#1e2634] text-slate-300 hover:text-white'
            }`}
            title="Refresh database"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {actionError && (
        <div className={`p-3 rounded border text-xs flex items-center justify-between ${
          theme === 'light'
            ? 'bg-rose-50 border-rose-200 text-rose-800'
            : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
        }`}>
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-500" />
            <span>{actionError}</span>
          </div>
          <button onClick={() => setActionError(null)} className="font-bold ml-2 opacity-80 hover:opacity-100">
            ×
          </button>
        </div>
      )}

      {error && <ErrorMessage title="Candidates Sync Error" message={error} onRetry={fetchCandidates} />}

      {/* High Density Candidates Table */}
      {filteredCandidates.length === 0 ? (
        <EmptyState
          icon={Users}
          title="No Candidate Records Found"
          description={searchQuery ? 'No candidates match your search query.' : 'No candidate profiles recorded.'}
        />
      ) : (
        <div className={`rounded-lg border overflow-hidden transition-colors ${
          theme === 'light' ? 'border-slate-200 bg-white shadow-sm' : 'border-[#1e2634] bg-[#0e1219]'
        }`}>
          <div className="w-full overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className={`border-b font-mono text-[10px] uppercase tracking-wider ${
                  theme === 'light'
                    ? 'border-slate-200 bg-slate-100 text-slate-600'
                    : 'border-[#1e2634] bg-[#090b0e] text-slate-400'
                }`}>
                  <th className="py-3 px-4">Candidate Profile</th>
                  <th className="py-3 px-3">Contact</th>
                  <th className="py-3 px-3">Experience</th>
                  <th className="py-3 px-4">Extracted Skill Taxonomy</th>
                  <th className="py-3 px-4 text-center">Resume Actions</th>
                </tr>
              </thead>
              <tbody className={`divide-y ${theme === 'light' ? 'divide-slate-200' : 'divide-[#1e2634]'}`}>
                {filteredCandidates.map((cand, idx) => {
                  const info = cand.candidate_info || cand;
                  const name = info.name || cand.name || 'Unknown Candidate';
                  const email = info.email || cand.email || 'N/A';
                  const phone = info.phone || cand.phone || 'N/A';
                  const skills = info.skills || cand.skills || [];
                  const exp = (info.experience_years !== undefined && info.experience_years !== null && info.experience_years > 0)
                    ? `${info.experience_years} yrs`
                    : 'N/A';
                  const resumeId = cand.resume_id || info.resume_id || cand.candidate_id;

                  const isViewing = actionLoading?.id === resumeId && actionLoading?.type === 'view';
                  const isDownloading = actionLoading?.id === resumeId && actionLoading?.type === 'download';

                  return (
                    <tr
                      key={cand.candidate_id || cand._id || idx}
                      onClick={() => setSelectedCandidate(cand)}
                      className={`transition-colors cursor-pointer group ${
                        theme === 'light' ? 'hover:bg-slate-50' : 'hover:bg-[#131822]'
                      }`}
                    >
                      <td className="py-3 px-4">
                        <div className="flex items-center space-x-2.5">
                          <div className={`w-7 h-7 rounded font-mono font-bold text-xs flex items-center justify-center flex-shrink-0 border ${
                            theme === 'light'
                              ? 'bg-cyan-50 border-cyan-200 text-cyan-700'
                              : 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400'
                          }`}>
                            {name.charAt(0).toUpperCase()}
                          </div>
                          <div>
                            <p className={`font-semibold transition-colors ${
                              theme === 'light' ? 'text-slate-900 group-hover:text-cyan-600' : 'text-slate-100 group-hover:text-cyan-300'
                            }`}>
                              {name}
                            </p>
                            <p className={`text-[10px] font-mono ${theme === 'light' ? 'text-slate-400' : 'text-slate-500'}`}>ID: {cand.candidate_id || 'N/A'}</p>
                          </div>
                        </div>
                      </td>

                      <td className={`py-3 px-3 font-mono ${theme === 'light' ? 'text-slate-700' : 'text-slate-300'}`}>
                        <p className="text-xs">{email}</p>
                        <p className={`text-[10px] ${theme === 'light' ? 'text-slate-400' : 'text-slate-500'}`}>{phone}</p>
                      </td>

                      <td className={`py-3 px-3 font-mono whitespace-nowrap ${theme === 'light' ? 'text-slate-700' : 'text-slate-300'}`}>
                        {exp}
                      </td>

                      <td className="py-3 px-4">
                        <div className="flex flex-wrap gap-1 max-w-xs">
                          {skills.slice(0, 4).map((s, i) => (
                            <span
                              key={i}
                              className={`px-1.5 py-0.5 rounded text-[10px] font-mono border ${
                                theme === 'light'
                                  ? 'bg-slate-100 text-slate-700 border-slate-200'
                                  : 'bg-[#131822] text-slate-300 border-[#1e2634]'
                              }`}
                            >
                              {s}
                            </span>
                          ))}
                          {skills.length > 4 && (
                            <span className={`px-1 py-0.5 rounded text-[10px] font-mono ${
                              theme === 'light' ? 'bg-slate-100 text-slate-500' : 'bg-[#131822] text-slate-500'
                            }`}>
                              +{skills.length - 4}
                            </span>
                          )}
                          {skills.length === 0 && <span className="text-[10px] text-slate-400 italic">No skills extracted</span>}
                        </div>
                      </td>

                      <td className="py-3 px-4 text-center">
                        <div className="flex items-center justify-center space-x-1.5">
                          <button
                            onClick={(e) => handleViewResume(e, resumeId)}
                            disabled={isViewing || isDownloading}
                            className={`px-2 py-1 rounded text-[10px] font-mono font-bold flex items-center space-x-1 transition-all border ${
                              theme === 'light'
                                ? 'bg-cyan-50 hover:bg-cyan-100 text-cyan-700 border-cyan-200'
                                : 'bg-[#131822] hover:bg-cyan-500/20 text-cyan-300 border-[#1e2634] hover:border-cyan-500/40'
                            }`}
                            title="View Resume"
                          >
                            {isViewing ? <Loader2 className="w-3 h-3 animate-spin" /> : <FileText className="w-3 h-3" />}
                            <span className="hidden sm:inline">View</span>
                          </button>

                          <button
                            onClick={(e) => handleDownloadResume(e, resumeId)}
                            disabled={isViewing || isDownloading}
                            className={`px-2 py-1 rounded text-[10px] font-mono font-bold flex items-center space-x-1 transition-all border ${
                              theme === 'light'
                                ? 'bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border-emerald-200'
                                : 'bg-[#131822] hover:bg-emerald-500/20 text-emerald-300 border-[#1e2634] hover:border-emerald-500/40'
                            }`}
                            title="Download Resume"
                          >
                            {isDownloading ? <Loader2 className="w-3 h-3 animate-spin" /> : <Download className="w-3 h-3" />}
                            <span className="hidden sm:inline">Download</span>
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {selectedCandidate && (
        <CandidateDetails candidate={selectedCandidate} onClose={() => setSelectedCandidate(null)} />
      )}
    </div>
  );
};

export default Candidates;
