import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Briefcase, Loader2, AlertCircle, ArrowRight, Cpu, Layers, CheckCircle2 } from 'lucide-react';
import ResumeUploader from '../components/ResumeUploader';
import { screenCandidatesApi } from '../api/screening';
import { listJobsApi } from '../api/jobs';
import { useTheme } from '../context/ThemeContext';

export const NewScreening = () => {
  const { theme } = useTheme();
  const navigate = useNavigate();

  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0); // 0: Idle, 1: PARSING, 2: EXTRACTION, 3: MATCHING, 4: SCORING, 5: RANKING
  const [errorMessage, setErrorMessage] = useState('');
  const [fileError, setFileError] = useState('');

  const steps = [
    { label: 'PARSING', desc: 'Extracting text streams via PyMuPDF / python-docx' },
    { label: 'EXTRACTION', desc: 'Isolating skills, education & work experience' },
    { label: 'MATCHING', desc: 'Computing TF-IDF & SentenceTransformer dense vectors' },
    { label: 'SCORING', desc: 'Calculating composite hybrid evaluation metrics' },
    { label: 'RANKING', desc: 'Generating authoritative candidate shortlist' },
  ];

  const simulateProcessingSteps = async () => {
    for (let i = 1; i <= 5; i++) {
      setCurrentStep(i);
      await new Promise((resolve) => setTimeout(resolve, 350));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setFileError('');

    if (!jobDescription || !jobDescription.trim()) {
      setErrorMessage('Please provide a job description.');
      return;
    }

    if (!files || files.length === 0) {
      setFileError('Please upload at least one candidate resume document.');
      return;
    }

    setLoading(true);
    setCurrentStep(1);

    try {
      const formData = new FormData();
      formData.append('job_title', jobTitle.trim() || 'Job Position');
      formData.append('job_description', jobDescription.trim());
      files.forEach((file) => {
        formData.append('files', file);
      });

      // Trigger animated processing steps indicator
      simulateProcessingSteps();

      // Call FastAPI batch screening endpoint
      const response = await screenCandidatesApi(formData);

      // Fetch latest job list to obtain newly stored MongoDB job_id
      const jobs = await listJobsApi();
      if (jobs && jobs.length > 0) {
        const latestJobId = jobs[0]._id || jobs[0].job_id;
        navigate(`/screening/${latestJobId}/results`, {
          state: { batchResponse: response, jobTitle: jobTitle || 'Job Position' },
        });
      } else {
        navigate('/jobs');
      }
    } catch (err) {
      setErrorMessage(err.message || 'Error occurred while screening resumes.');
    } finally {
      setLoading(false);
      setCurrentStep(0);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Workstation Header */}
      <div className={`p-4 rounded-lg border flex flex-col md:flex-row md:items-center justify-between gap-4 transition-colors ${
        theme === 'light' ? 'bg-white border-slate-200 shadow-sm' : 'bg-[#0e1219] border-[#1e2634]'
      }`}>
        <div>
          <div className="flex items-center space-x-2 mb-1">
            <Cpu className="w-4 h-4 text-cyan-500" />
            <span className={`text-xs font-mono font-bold uppercase tracking-widest ${
              theme === 'light' ? 'text-cyan-700' : 'text-cyan-400'
            }`}>
              AI Analysis Workstation
            </span>
          </div>
          <h1 className={`text-xl font-bold tracking-tight ${theme === 'light' ? 'text-slate-900' : 'text-slate-100'}`}>
            Create AI Resume Screening Run
          </h1>
          <p className={`text-xs ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
            Define target job criteria and upload candidate documents for real-time NLP parsing and vector ranking
          </p>
        </div>
      </div>

      {errorMessage && (
        <div className={`p-3.5 rounded border text-xs flex items-start space-x-2.5 ${
          theme === 'light'
            ? 'bg-rose-50 border-rose-200 text-rose-800'
            : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
        }`}>
          <AlertCircle className="w-4 h-4 text-rose-500 flex-shrink-0 mt-0.5" />
          <span className="leading-relaxed">{errorMessage}</span>
        </div>
      )}

      {/* Two-Stage Workstation Grid */}
      <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* LEFT PANEL: Job Requirements Input */}
        <div className={`lg:col-span-7 space-y-4 p-5 rounded-lg border transition-colors ${
          theme === 'light' ? 'bg-white border-slate-200 shadow-sm' : 'bg-[#0e1219] border-[#1e2634]'
        }`}>
          <div className={`flex items-center space-x-2 border-b pb-3 ${
            theme === 'light' ? 'border-slate-200' : 'border-[#1e2634]'
          }`}>
            <span className={`w-5 h-5 rounded font-mono text-xs font-bold flex items-center justify-center border ${
              theme === 'light' ? 'bg-cyan-50 border-cyan-200 text-cyan-700' : 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400'
            }`}>
              1
            </span>
            <h3 className={`text-xs font-mono font-bold uppercase tracking-wider ${
              theme === 'light' ? 'text-slate-800' : 'text-slate-200'
            }`}>
              JOB REQUIREMENTS & SPECIFICATIONS
            </h3>
          </div>

          <div>
            <label className={`block text-[11px] font-mono uppercase tracking-wider mb-1.5 ${
              theme === 'light' ? 'text-slate-600' : 'text-slate-400'
            }`}>
              Job Position Title
            </label>
            <div className="relative">
              <Briefcase className={`w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 ${
                theme === 'light' ? 'text-slate-400' : 'text-slate-500'
              }`} />
              <input
                type="text"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                placeholder="e.g. Senior Backend Engineer / Financial Analyst"
                className={`w-full pl-9 pr-3 py-2 rounded text-xs font-medium focus:outline-none focus:border-cyan-500 transition-all border ${
                  theme === 'light'
                    ? 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400'
                    : 'bg-[#090b0e] border-[#1e2634] text-slate-100 placeholder-slate-600'
                }`}
              />
            </div>
          </div>

          <div>
            <label className={`block text-[11px] font-mono uppercase tracking-wider mb-1.5 ${
              theme === 'light' ? 'text-slate-600' : 'text-slate-400'
            }`}>
              Job Description & Criteria <span className="text-cyan-500">*</span>
            </label>
            <textarea
              required
              rows={10}
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste complete job description text detailing required technical skills, minimum experience years, education degrees, and key responsibilities..."
              className={`w-full p-3.5 rounded text-xs leading-relaxed focus:outline-none focus:border-cyan-500 transition-all border ${
                theme === 'light'
                  ? 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400'
                  : 'bg-[#090b0e] border-[#1e2634] text-slate-100 placeholder-slate-600'
              }`}
            />
          </div>
        </div>

        {/* RIGHT PANEL: Resume Intake & AI Trigger Action */}
        <div className={`lg:col-span-5 space-y-4 p-5 rounded-lg border flex flex-col justify-between transition-colors ${
          theme === 'light' ? 'bg-white border-slate-200 shadow-sm' : 'bg-[#0e1219] border-[#1e2634]'
        }`}>
          <div className="space-y-4">
            <div className={`flex items-center space-x-2 border-b pb-3 ${
              theme === 'light' ? 'border-slate-200' : 'border-[#1e2634]'
            }`}>
              <span className={`w-5 h-5 rounded font-mono text-xs font-bold flex items-center justify-center border ${
                theme === 'light' ? 'bg-cyan-50 border-cyan-200 text-cyan-700' : 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400'
              }`}>
                2
              </span>
              <h3 className={`text-xs font-mono font-bold uppercase tracking-wider ${
                theme === 'light' ? 'text-slate-800' : 'text-slate-200'
              }`}>
                RESUME DOCUMENTS INTAKE
              </h3>
            </div>

            <ResumeUploader files={files} setFiles={setFiles} error={fileError} setError={setFileError} />
          </div>

          {/* Animated AI Processing Pipeline Indicator */}
          {loading && (
            <div className={`p-3.5 rounded border space-y-2.5 animate-pulse-glow ${
              theme === 'light' ? 'bg-slate-50 border-cyan-500/40' : 'bg-[#090b0e] border-cyan-500/30'
            }`}>
              <div className="flex items-center justify-between text-[11px] font-mono text-cyan-600 dark:text-cyan-400 font-bold">
                <span className="flex items-center space-x-1.5">
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>AI PIPELINE PROCESSING</span>
                </span>
                <span>STEP {currentStep} OF 5</span>
              </div>

              <div className="grid grid-cols-5 gap-1">
                {steps.map((step, idx) => (
                  <div
                    key={idx}
                    className={`h-1.5 rounded-full transition-all duration-300 ${
                      idx + 1 <= currentStep
                        ? 'bg-cyan-500'
                        : theme === 'light'
                        ? 'bg-slate-200'
                        : 'bg-[#1e2634]'
                    }`}
                  />
                ))}
              </div>

              <div className={`text-[10px] font-mono flex items-center justify-between pt-1 ${
                theme === 'light' ? 'text-slate-600' : 'text-slate-400'
              }`}>
                <span className="text-cyan-600 dark:text-cyan-300 font-bold">{steps[Math.max(0, currentStep - 1)]?.label}</span>
                <span className="truncate max-w-[180px]">{steps[Math.max(0, currentStep - 1)]?.desc}</span>
              </div>
            </div>
          )}

          {/* Trigger Button Action */}
          <div className={`pt-4 border-t ${theme === 'light' ? 'border-slate-200' : 'border-[#1e2634]'}`}>
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs uppercase tracking-wider shadow-sm transition-all flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Executing AI Engine Pipeline...</span>
                </>
              ) : (
                <>
                  <Cpu className="w-4 h-4" />
                  <span>RUN AI SCREENING</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default NewScreening;
