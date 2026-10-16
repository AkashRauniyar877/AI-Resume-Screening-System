import React, { useState } from 'react';
import { X, User, Mail, Phone, Briefcase, GraduationCap, CheckCircle2, AlertCircle, FileText, Download, Loader2, Cpu, Check, AlertTriangle } from 'lucide-react';
import ScoreBreakdown from './ScoreBreakdown';
import { viewResumeApi, downloadResumeApi } from '../api/resumes';
import { useTheme } from '../context/ThemeContext';

export const CandidateDetails = ({ candidate, onClose }) => {
  const { theme } = useTheme();
  const [actionLoading, setActionLoading] = useState(null);
  const [actionError, setActionError] = useState(null);

  if (!candidate) return null;

  const info = candidate.candidate_info || candidate;
  const match = candidate.match_results || candidate.match_results_detail || candidate;

  const matchedSkills = match.matched_skills || info.matched_skills || candidate.matched_skills || [];
  const missingSkills = match.missing_skills || info.missing_skills || candidate.missing_skills || [];
  const allSkills = info.skills || candidate.skills || [];

  const name = info.name || candidate.name || (candidate.filename ? `Candidate (${candidate.filename})` : 'Unknown Candidate');
  const email = info.email || candidate.email || 'N/A';
  const phone = info.phone || candidate.phone || 'N/A';
  const experienceYears = info.experience_years ?? candidate.experience_years;
  const expDisplay = (experienceYears !== undefined && experienceYears !== null && experienceYears > 0)
    ? `${experienceYears} Years`
    : 'N/A';
  const education = info.education || candidate.education || [];
  const resumeId = candidate.resume_id || info.resume_id || candidate.candidate_id;

  const handleView = async () => {
    if (!resumeId) {
      setActionError('Resume ID unavailable for this candidate.');
      return;
    }
    setActionError(null);
    setActionLoading('view');
    try {
      await viewResumeApi(resumeId);
    } catch (err) {
      setActionError(err.message || 'Failed to view resume.');
    } finally {
      setActionLoading(null);
    }
  };

  const handleDownload = async () => {
    if (!resumeId) {
      setActionError('Resume ID unavailable for this candidate.');
      return;
    }
    setActionError(null);
    setActionLoading('download');
    try {
      await downloadResumeApi(resumeId);
    } catch (err) {
      setActionError(err.message || 'Failed to download resume.');
    } finally {
      setActionLoading(null);
    }
  };

  const isViewing = actionLoading === 'view';
  const isDownloading = actionLoading === 'download';

  return (
    <div className={`fixed inset-0 z-50 flex items-center justify-center p-4 backdrop-blur-sm animate-fade-in ${
      theme === 'light' ? 'bg-slate-900/60' : 'bg-[#080a0d]/85'
    }`}>
      <div className={`relative w-full max-w-3xl rounded-lg shadow-2xl max-h-[90vh] flex flex-col overflow-hidden border transition-colors ${
        theme === 'light' ? 'bg-white border-slate-200 text-slate-900' : 'bg-[#0e1219] border-[#1e2634] text-slate-100'
      }`}>
        {/* Modal Header */}
        <div className={`px-5 py-3.5 border-b flex items-center justify-between ${
          theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#090b0e] border-[#1e2634]'
        }`}>
          <div className="flex items-center space-x-3">
            <div className={`w-9 h-9 rounded font-mono font-bold text-sm flex items-center justify-center border ${
              theme === 'light' ? 'bg-cyan-50 border-cyan-200 text-cyan-700' : 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400'
            }`}>
              {name.charAt(0).toUpperCase()}
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className={`text-base font-bold ${theme === 'light' ? 'text-slate-900' : 'text-slate-100'}`}>{name}</h3>
                <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${
                  theme === 'light' ? 'bg-slate-100 text-cyan-700 border-slate-300' : 'bg-[#131822] text-cyan-400 border-[#1e2634]'
                }`}>
                  Rank #{candidate.rank || 1}
                </span>
              </div>
              <p className={`text-[10px] font-mono ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>
                Candidate ID: {candidate.candidate_id || candidate.filename || 'Unspecified'}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className={`p-1.5 rounded border transition-colors ${
              theme === 'light' ? 'bg-slate-100 hover:bg-slate-200 border-slate-300 text-slate-600' : 'bg-[#131822] hover:text-white text-slate-400 border-[#1e2634]'
            }`}
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-5 overflow-y-auto space-y-5 flex-1">
          {actionError && (
            <div className={`p-3 rounded border text-xs flex items-center justify-between ${
              theme === 'light' ? 'bg-rose-50 border-rose-200 text-rose-800' : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
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

          {/* Original Resume Action Bar */}
          <div className={`p-3.5 rounded border flex flex-col sm:flex-row items-center justify-between gap-3 ${
            theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#090b0e] border-[#1e2634]'
          }`}>
            <div>
              <h5 className={`text-xs font-mono font-bold uppercase ${theme === 'light' ? 'text-slate-800' : 'text-slate-200'}`}>Original Resume File</h5>
              <p className={`text-[11px] ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>Recruiter isolated view & download endpoints</p>
            </div>
            <div className="flex items-center space-x-2 w-full sm:w-auto">
              <button
                onClick={handleView}
                disabled={isViewing || isDownloading}
                className={`flex-1 sm:flex-none px-3 py-1.5 rounded text-xs font-mono font-bold flex items-center justify-center space-x-1.5 transition-all border ${
                  theme === 'light'
                    ? 'bg-cyan-50 hover:bg-cyan-100 text-cyan-700 border-cyan-200'
                    : 'bg-[#131822] hover:bg-cyan-500/20 text-cyan-300 border-[#1e2634] hover:border-cyan-500/40'
                }`}
              >
                {isViewing ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <FileText className="w-3.5 h-3.5" />}
                <span>View Resume</span>
              </button>
              <button
                onClick={handleDownload}
                disabled={isViewing || isDownloading}
                className={`flex-1 sm:flex-none px-3 py-1.5 rounded text-xs font-mono font-bold flex items-center justify-center space-x-1.5 transition-all border ${
                  theme === 'light'
                    ? 'bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border-emerald-200'
                    : 'bg-[#131822] hover:bg-emerald-500/20 text-emerald-300 border-[#1e2634] hover:border-emerald-500/40'
                }`}
              >
                {isDownloading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Download className="w-3.5 h-3.5" />}
                <span>Download Resume</span>
              </button>
            </div>
          </div>

          {/* Contact Details Panel */}
          <div className={`grid grid-cols-1 sm:grid-cols-2 gap-2.5 p-3 rounded border text-xs font-mono ${
            theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#090b0e] border-[#1e2634]'
          }`}>
            <div className={`flex items-center space-x-2 ${theme === 'light' ? 'text-slate-700' : 'text-slate-300'}`}>
              <Mail className="w-3.5 h-3.5 text-cyan-500" />
              <span className={theme === 'light' ? 'text-slate-500' : 'text-slate-400'}>Email:</span>
              <span className="truncate">{email}</span>
            </div>
            <div className={`flex items-center space-x-2 ${theme === 'light' ? 'text-slate-700' : 'text-slate-300'}`}>
              <Phone className="w-3.5 h-3.5 text-cyan-500" />
              <span className={theme === 'light' ? 'text-slate-500' : 'text-slate-400'}>Phone:</span>
              <span>{phone}</span>
            </div>
            <div className={`flex items-center space-x-2 ${theme === 'light' ? 'text-slate-700' : 'text-slate-300'}`}>
              <Briefcase className="w-3.5 h-3.5 text-cyan-500" />
              <span className={theme === 'light' ? 'text-slate-500' : 'text-slate-400'}>Experience:</span>
              <span>{expDisplay}</span>
            </div>
            <div className={`flex items-center space-x-2 ${theme === 'light' ? 'text-slate-700' : 'text-slate-300'}`}>
              <GraduationCap className="w-3.5 h-3.5 text-cyan-500" />
              <span className={theme === 'light' ? 'text-slate-500' : 'text-slate-400'}>Education:</span>
              <span className="truncate">
                {Array.isArray(education) && education.length > 0 ? education.join(', ') : 'Unspecified'}
              </span>
            </div>
          </div>

          {/* Score Breakdown Section */}
          {match && Object.keys(match).length > 0 && (
            <div>
              <h4 className={`text-[11px] font-mono font-bold uppercase tracking-wider mb-2 ${
                theme === 'light' ? 'text-slate-600' : 'text-slate-400'
              }`}>
                Matching Analysis & Sub-Scores
              </h4>
              <ScoreBreakdown matchResults={match} />
            </div>
          )}

          {/* AI Explanation & Match Analysis Panel */}
          <div className={`p-4 rounded border space-y-3 ${
            theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#090b0e] border-[#1e2634]'
          }`}>
            <div className={`flex items-center space-x-2 border-b pb-2 ${
              theme === 'light' ? 'border-slate-200' : 'border-[#1e2634]'
            }`}>
              <Cpu className="w-4 h-4 text-cyan-500" />
              <h4 className={`text-xs font-mono font-bold uppercase tracking-wider ${
                theme === 'light' ? 'text-slate-800' : 'text-slate-200'
              }`}>
                AI ANALYSIS & MATCH EXPLANATION
              </h4>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {/* Why Candidate Matches */}
              <div className="space-y-2">
                <span className="text-[11px] font-mono font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider flex items-center space-x-1">
                  <Check className="w-3.5 h-3.5" />
                  <span>Why Candidate Matches</span>
                </span>
                <ul className={`space-y-1 text-xs ${theme === 'light' ? 'text-slate-700' : 'text-slate-300'}`}>
                  {matchedSkills.slice(0, 4).map((skill, idx) => (
                    <li key={idx} className="flex items-center space-x-1.5">
                      <span className="text-emerald-500 font-bold">✓</span>
                      <span>Strong {skill} skills detected</span>
                    </li>
                  ))}
                  {experienceYears > 0 ? (
                    <li className="flex items-center space-x-1.5">
                      <span className="text-emerald-500 font-bold">✓</span>
                      <span>{experienceYears} years relevant industry experience</span>
                    </li>
                  ) : null}
                  {matchedSkills.length === 0 && (
                    <li className={`italic text-[11px] ${theme === 'light' ? 'text-slate-400' : 'text-slate-500'}`}>No direct skill matches detected.</li>
                  )}
                </ul>
              </div>

              {/* Skill Gaps Detected */}
              <div className="space-y-2">
                <span className="text-[11px] font-mono font-bold text-amber-600 dark:text-amber-400 uppercase tracking-wider flex items-center space-x-1">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>Skill Gaps Detected</span>
                </span>
                <ul className={`space-y-1 text-xs ${theme === 'light' ? 'text-slate-700' : 'text-slate-300'}`}>
                  {missingSkills.slice(0, 4).map((skill, idx) => (
                    <li key={idx} className="flex items-center space-x-1.5">
                      <span className="text-amber-500 font-bold">!</span>
                      <span>{skill} experience not detected</span>
                    </li>
                  ))}
                  {missingSkills.length === 0 && (
                    <li className="text-emerald-600 dark:text-emerald-400 italic text-[11px]">✓ No missing skill gaps detected.</li>
                  )}
                </ul>
              </div>
            </div>
          </div>

          {/* Matched vs Missing Skills Badges */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <h4 className="text-[11px] font-mono font-bold uppercase text-emerald-600 dark:text-emerald-400 mb-2">
                Matched Skills ({matchedSkills.length})
              </h4>
              <div className="flex flex-wrap gap-1">
                {matchedSkills.map((s, idx) => (
                  <span key={idx} className={`px-2 py-0.5 rounded text-[11px] font-mono border ${
                    theme === 'light'
                      ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      : 'bg-emerald-500/10 text-emerald-300 border-emerald-500/20'
                  }`}>
                    {s}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h4 className="text-[11px] font-mono font-bold uppercase text-amber-600 dark:text-amber-400 mb-2">
                Missing Job Skills ({missingSkills.length})
              </h4>
              <div className="flex flex-wrap gap-1">
                {missingSkills.map((s, idx) => (
                  <span key={idx} className={`px-2 py-0.5 rounded text-[11px] font-mono border ${
                    theme === 'light'
                      ? 'bg-amber-50 text-amber-700 border-amber-200'
                      : 'bg-amber-500/10 text-amber-300 border-amber-500/20'
                  }`}>
                    {s}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CandidateDetails;
