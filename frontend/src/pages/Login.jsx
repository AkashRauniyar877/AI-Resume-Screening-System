import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Mail, Lock, Eye, EyeOff, Brain, Loader2, AlertCircle, ArrowRight, Home, Sun, Moon } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export const Login = () => {
  const { login } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const from = location.state?.from?.pathname || '/dashboard';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    if (!email || !password) {
      setErrorMessage('Please enter both email and password.');
      return;
    }

    setLoading(true);
    try {
      await login(email, password);
      navigate(from, { replace: true });
    } catch (err) {
      setErrorMessage(err.message || 'Invalid email or password.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`min-h-screen flex items-center justify-center p-4 md:p-8 bg-tech-grid relative ${
      theme === 'light' ? 'bg-slate-50 text-slate-900' : 'bg-[#07090e] text-slate-100'
    }`}>
      {/* Top Header Actions */}
      <div className="absolute top-6 left-6 right-6 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-2 text-xs font-semibold text-cyan-500 hover:text-cyan-400">
          <Home className="w-4 h-4" />
          <span>Back to Home</span>
        </Link>
        <button
          onClick={toggleTheme}
          className={`p-2 rounded-lg border transition-all ${
            theme === 'light' ? 'bg-slate-100 border-slate-300 text-amber-600' : 'bg-slate-900 border-slate-800 text-cyan-400'
          }`}
          aria-label="Toggle theme"
        >
          {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>
      </div>

      <div className={`w-full max-w-4xl border rounded-2xl shadow-2xl overflow-hidden grid grid-cols-1 md:grid-cols-12 ${
        theme === 'light' ? 'bg-white border-slate-200 shadow-slate-200/50' : 'bg-[#0b101b] border-slate-800'
      }`}>
        {/* LEFT PANEL: Technical AI Visual Section */}
        <div className={`md:col-span-6 p-6 md:p-8 border-b md:border-b-0 md:border-r flex flex-col justify-between relative overflow-hidden ${
          theme === 'light' ? 'bg-slate-100/70 border-slate-200' : 'bg-[#080c14] border-slate-800'
        }`}>
          <div className="relative z-10 space-y-4">
            <div className="flex items-center space-x-2.5">
              <div className="w-8 h-8 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center">
                <Brain className="w-4 h-4" />
              </div>
              <span className="text-base font-extrabold tracking-tight">
                Resume<span className="text-cyan-500">AI</span>
              </span>
            </div>

            <div>
              <h1 className="text-xl font-bold tracking-tight">
                Recruiter Portal Sign In
              </h1>
              <p className={`text-xs mt-1 leading-relaxed ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
                Turn unstructured resumes into structured, ranked candidate insights using NLP, TF-IDF, and SentenceTransformers.
              </p>
            </div>

            {/* Visual Flow Box */}
            <div className="py-2 space-y-2 font-mono text-xs">
              <div className={`p-3 rounded-lg border flex items-center justify-between ${
                theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#0e1422] border-slate-800'
              }`}>
                <span className="text-[11px]">RESUME INTAKE</span>
                <span className="text-cyan-400 font-bold">PDF / DOCX</span>
              </div>
              <div className="text-center text-slate-500 text-xs font-bold">↓</div>
              <div className={`p-3 rounded-lg border flex items-center justify-between ${
                theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#0e1422] border-slate-800'
              }`}>
                <span className="text-[11px]">AI MATCHING</span>
                <span className="text-amber-400 font-bold">384-d EMBEDDINGS</span>
              </div>
              <div className="text-center text-slate-500 text-xs font-bold">↓</div>
              <div className="p-3 rounded-lg border border-cyan-500/40 flex items-center justify-between text-cyan-400 bg-cyan-500/10">
                <span className="text-[11px] font-bold">RANKING RESULT</span>
                <span className="text-emerald-400 font-bold">HYBRID SCORE</span>
              </div>
            </div>
          </div>

          <div className="relative z-10 pt-4 border-t border-slate-800/60 flex items-center justify-between text-[11px] font-mono text-slate-500">
            <span className="flex items-center space-x-1 text-emerald-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              <span>FastAPI Backend Online</span>
            </span>
            <span>Recruiter Workstation</span>
          </div>
        </div>

        {/* RIGHT PANEL: Recruiter Authentication Form */}
        <div className="md:col-span-6 p-6 md:p-8 flex flex-col justify-center space-y-5">
          <div>
            <h2 className="text-lg font-bold tracking-wide uppercase">Recruiter Sign In</h2>
            <p className={`text-xs mt-1 ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
              Authenticate to access recruiter-scoped candidate datasets
            </p>
          </div>

          {errorMessage && (
            <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs flex items-start space-x-2">
              <AlertCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className={`block text-[11px] font-mono uppercase tracking-wider mb-1 ${
                theme === 'light' ? 'text-slate-600' : 'text-slate-400'
              }`}>
                Recruiter Email
              </label>
              <div className="relative">
                <Mail className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="recruiter@company.com"
                  className={`w-full pl-9 pr-3 py-2 rounded-lg border text-xs focus:outline-none focus:border-cyan-500 font-medium transition-all ${
                    theme === 'light'
                      ? 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400'
                      : 'bg-[#080c14] border-slate-800 text-slate-100 placeholder-slate-600'
                  }`}
                />
              </div>
            </div>

            <div>
              <label className={`block text-[11px] font-mono uppercase tracking-wider mb-1 ${
                theme === 'light' ? 'text-slate-600' : 'text-slate-400'
              }`}>
                Password
              </label>
              <div className="relative">
                <Lock className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className={`w-full pl-9 pr-9 py-2 rounded-lg border text-xs focus:outline-none focus:border-cyan-500 font-medium transition-all ${
                    theme === 'light'
                      ? 'bg-slate-50 border-slate-300 text-slate-900 placeholder-slate-400'
                      : 'bg-[#080c14] border-slate-800 text-slate-100 placeholder-slate-600'
                  }`}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200"
                >
                  {showPassword ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs uppercase tracking-wider shadow-md shadow-cyan-500/20 transition-all flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Authenticating...</span>
                </>
              ) : (
                <>
                  <span>Sign In</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          <p className={`text-center text-xs pt-2 border-t ${theme === 'light' ? 'border-slate-200 text-slate-600' : 'border-slate-800 text-slate-400'}`}>
            Don't have an account?{' '}
            <Link to="/register" className="text-cyan-500 font-bold hover:underline">
              Register
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
