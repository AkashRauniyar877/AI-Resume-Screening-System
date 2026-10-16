import React, { useState } from 'react';
import { Award, Eye, User, FileText, Download, Loader2, AlertCircle, Sparkles } from 'lucide-react';
import CandidateDetails from './CandidateDetails';
import { viewResumeApi, downloadResumeApi } from '../api/resumes';
import { useTheme } from '../context/ThemeContext';

export const CandidateTable = ({ candidates = [] }) => {
  const { theme } = useTheme();
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [actionLoading, setActionLoading] = useState(null); // { id, type: 'view'|'download' }
  const [actionError, setActionError] = useState(null);

  if (!candidates || candidates.length === 0) {
    return null;
  }

  const handleViewResume = async (e, resumeId) => {
    e.stopPropagation();
    if (!resumeId) {
      setActionError('Resume ID not available for this candidate.');
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
      setActionError('Resume ID not available for this candidate.');
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

  return (
    <div className="space-y-3">
      {actionError && (
        <div className={`p-3 rounded border text-xs flex items-center justify-between animate-fade-in ${
          theme === 'light' ? 'bg-rose-50 border-rose-200 text-rose-800' : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
        }`}>
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0 text-rose-500" />
            <span>{actionError}</span>
          </div>
          <button
            onClick={() => setActionError(null)}
            className="font-bold ml-2 opacity-80 hover:opacity-100"
          >
            ×
          </button>
        </div>
      )}

      {/* Structured Ranked Candidate Workstation List */}
      <div className={`rounded-lg border overflow-hidden transition-colors ${
        theme === 'light' ? 'border-slate-200 bg-white shadow-sm' : 'border-[#1e2634] bg-[#0e1219]'
      }`}>
        <div className="w-full overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className={`border-b font-mono text-[10px] uppercase tracking-wider ${
                theme === 'light' ? 'border-slate-200 bg-slate-100 text-slate-600' : 'border-[#1e2634] bg-[#090b0e] text-slate-400'
              }`}>
                <th className="py-3 px-3 text-center w-14">Rank</th>
                <th className="py-3 px-4">Candidate Profile</th>
                <th className="py-3 px-3">Experience</th>
                <th className="py-3 px-4">Matched Skills</th>
                <th className="py-3 px-3 text-right">Coverage</th>
                <th className="py-3 px-3 text-right">Semantic</th>
                <th className="py-3 px-3 text-right">TF-IDF</th>
                <th className="py-3 px-4 text-right">Hybrid Match</th>
                <th className="py-3 px-4 text-center">Actions</th>
              </tr>
            </thead>
            <tbody className={`divide-y ${theme === 'light' ? 'divide-slate-200' : 'divide-[#1e2634]'}`}>
              {candidates.map((cand, idx) => {
                const info = cand.candidate_info || cand;
                const match = cand.match_results || cand.match_results_detail || cand;
                const rank = cand.rank || idx + 1;
                const resumeId = cand.resume_id || info.resume_id || cand.candidate_id;

                const matchedSkills = match.matched_skills || info.matched_skills || cand.matched_skills || [];
                const displayName = info.name || cand.name || (cand.filename ? `Candidate (${cand.filename})` : 'Unknown Candidate');
                const displayEmail = info.email || cand.email || 'N/A';
                const displayExp = (info.experience_years !== undefined && info.experience_years !== null && info.experience_years > 0)
                  ? `${info.experience_years} yrs`
                  : 'N/A';

                const hybridVal = Number(cand.hybrid_score || match.hybrid_score || 0);

                const isViewing = actionLoading?.id === resumeId && actionLoading?.type === 'view';
                const isDownloading = actionLoading?.id === resumeId && actionLoading?.type === 'download';
                const isRankOne = rank === 1;

                return (
                  <tr
                    key={cand.candidate_id || cand._id || idx}
                    onClick={() => setSelectedCandidate(cand)}
                    className={`transition-colors cursor-pointer group ${
                      theme === 'light'
                        ? isRankOne ? 'bg-amber-500/10 hover:bg-amber-500/15' : 'hover:bg-slate-50'
                        : isRankOne ? 'bg-amber-500/[0.03] hover:bg-[#131822]' : 'hover:bg-[#131822]'
                    }`}
                  >
                    {/* Rank Badge */}
                    <td className="py-3.5 px-3 text-center">
                      <span
                        className={`inline-flex items-center justify-center w-6 h-6 rounded font-mono font-bold text-xs border ${
                          isRankOne
                            ? 'bg-amber-500/20 text-amber-600 dark:text-amber-300 border-amber-500/40 shadow-sm'
                            : rank === 2
                            ? theme === 'light' ? 'bg-slate-200 text-slate-700 border-slate-300' : 'bg-slate-300/10 text-slate-200 border-slate-500/30'
                            : rank === 3
                            ? theme === 'light' ? 'bg-amber-100 text-amber-800 border-amber-300' : 'bg-amber-700/15 text-amber-400 border-amber-600/30'
                            : theme === 'light' ? 'bg-slate-100 text-slate-500 border-slate-200' : 'bg-[#131822] text-slate-400 border-[#1e2634]'
                        }`}
                      >
                        {rank}
                      </span>
                    </td>

                    {/* Candidate Name & Info */}
                    <td className="py-3.5 px-4">
                      <div className="flex items-center space-x-2.5">
                        <div className={`w-7 h-7 rounded font-mono font-bold text-xs flex items-center justify-center flex-shrink-0 border ${
                          theme === 'light'
                            ? 'bg-cyan-50 border-cyan-200 text-cyan-700'
                            : 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400'
                        }`}>
                          {displayName.charAt(0).toUpperCase()}
                        </div>
                        <div className="truncate max-w-[200px]">
                          <div className="flex items-center space-x-1.5">
                            <p className={`font-semibold transition-colors truncate ${
                              theme === 'light' ? 'text-slate-900 group-hover:text-cyan-600' : 'text-slate-100 group-hover:text-cyan-300'
                            }`}>
                              {displayName}
                            </p>
                            {isRankOne && (
                              <span className="px-1.5 py-0.2 rounded text-[9px] font-mono font-bold bg-amber-500/20 text-amber-600 dark:text-amber-300 border border-amber-500/40">
                                TOP MATCH
                              </span>
                            )}
                          </div>
                          <p className={`text-[10px] font-mono truncate ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>{displayEmail}</p>
                        </div>
                      </div>
                    </td>

                    {/* Experience */}
                    <td className={`py-3.5 px-3 font-mono text-[11px] whitespace-nowrap ${theme === 'light' ? 'text-slate-700' : 'text-slate-300'}`}>
                      {displayExp}
                    </td>

                    {/* Skill Badges Preview */}
                    <td className="py-3.5 px-4">
                      <div className="flex flex-wrap gap-1 max-w-[220px]">
                        {matchedSkills.slice(0, 3).map((s, i) => (
                          <span
                            key={i}
                            className={`px-1.5 py-0.5 rounded text-[10px] font-mono border truncate ${
                              theme === 'light'
                                ? 'bg-cyan-50 text-cyan-700 border-cyan-200'
                                : 'bg-cyan-500/10 text-cyan-300 border-cyan-500/20'
                            }`}
                          >
                            {s}
                          </span>
                        ))}
                        {matchedSkills.length > 3 && (
                          <span className={`px-1 py-0.5 rounded text-[10px] font-mono ${
                            theme === 'light' ? 'bg-slate-100 text-slate-500' : 'bg-[#131822] text-slate-400'
                          }`}>
                            +{matchedSkills.length - 3}
                          </span>
                        )}
                        {matchedSkills.length === 0 && (
                          <span className={`text-[10px] italic ${theme === 'light' ? 'text-slate-400' : 'text-slate-500'}`}>No skill tags match</span>
                        )}
                      </div>
                    </td>

                    {/* Coverage */}
                    <td className={`py-3.5 px-3 text-right font-mono text-xs ${theme === 'light' ? 'text-slate-700' : 'text-slate-300'}`}>
                      {match.skill_coverage !== undefined ? `${Number(match.skill_coverage).toFixed(0)}%` : '-'}
                    </td>

                    {/* Semantic */}
                    <td className={`py-3.5 px-3 text-right font-mono font-semibold text-xs ${theme === 'light' ? 'text-cyan-700' : 'text-cyan-400'}`}>
                      {match.semantic_normalized !== undefined
                        ? `${Number(match.semantic_normalized).toFixed(0)}%`
                        : match.semantic_score !== undefined
                        ? `${Number(match.semantic_score).toFixed(0)}%`
                        : '-'}
                    </td>

                    {/* TF-IDF */}
                    <td className={`py-3.5 px-3 text-right font-mono font-semibold text-xs ${theme === 'light' ? 'text-amber-700' : 'text-amber-400'}`}>
                      {match.tfidf_normalized !== undefined
                        ? `${Number(match.tfidf_normalized).toFixed(0)}%`
                        : match.tfidf_score !== undefined
                        ? `${Number(match.tfidf_score).toFixed(0)}%`
                        : '-'}
                    </td>

                    {/* Hybrid Match Bar */}
                    <td className="py-3.5 px-4 text-right">
                      <div className="inline-flex items-center space-x-2">
                        <div className={`w-16 h-2 rounded overflow-hidden border hidden sm:block ${
                          theme === 'light' ? 'bg-slate-200 border-slate-300' : 'bg-[#090b0e] border-[#1e2634]'
                        }`}>
                          <div
                            className={`h-full ${
                              isRankOne ? 'bg-gradient-to-r from-amber-500 to-cyan-500' : 'bg-cyan-500'
                            }`}
                            style={{ width: `${Math.min(100, hybridVal)}%` }}
                          />
                        </div>
                        <span className={`font-mono font-bold text-xs px-2 py-0.5 rounded border ${
                          theme === 'light'
                            ? 'bg-slate-100 text-slate-800 border-slate-300'
                            : 'bg-[#131822] text-slate-100 border-[#1e2634]'
                        }`}>
                          {hybridVal.toFixed(1)}%
                        </span>
                      </div>
                    </td>

                    {/* Action Buttons */}
                    <td className="py-3.5 px-4 text-center">
                      <div className="flex items-center justify-center space-x-1">
                        <button
                          onClick={(e) => handleViewResume(e, resumeId)}
                          disabled={isViewing || isDownloading}
                          className={`px-2 py-1 rounded text-[10px] font-mono font-bold flex items-center space-x-1 transition-all border ${
                            theme === 'light'
                              ? 'bg-cyan-50 hover:bg-cyan-100 text-cyan-700 border-cyan-200'
                              : 'bg-[#131822] hover:bg-cyan-500/20 text-cyan-300 border-[#1e2634] hover:border-cyan-500/40'
                          }`}
                          title="View Original Resume File"
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
                          title="Download Original Resume File"
                        >
                          {isDownloading ? <Loader2 className="w-3 h-3 animate-spin" /> : <Download className="w-3 h-3" />}
                          <span className="hidden sm:inline">Download</span>
                        </button>

                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedCandidate(cand);
                          }}
                          className={`p-1 rounded border transition-all ${
                            theme === 'light'
                              ? 'bg-slate-100 hover:bg-slate-200 text-slate-700 border-slate-300'
                              : 'bg-[#131822] hover:bg-[#1c2433] text-slate-300 border-[#1e2634]'
                          }`}
                          title="View AI Analysis & Details"
                        >
                          <User className="w-3 h-3" />
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

      {/* Candidate Analysis Modal */}
      {selectedCandidate && (
        <CandidateDetails candidate={selectedCandidate} onClose={() => setSelectedCandidate(null)} />
      )}
    </div>
  );
};

export default CandidateTable;
