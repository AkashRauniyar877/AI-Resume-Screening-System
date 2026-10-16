import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { User, Mail, Lock, Eye, EyeOff, Brain, Loader2, AlertCircle, ArrowRight, Home, Sun, Moon } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export const Register = () => {
  const { register } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    if (!name || !email || !password) {
      setErrorMessage('All fields are required.');
      return;
    }

    if (password.length < 8) {
      setErrorMessage('Password must be at least 8 characters long.');
      return;
    }

    setLoading(true);
    try {
      await register(name, email, password);
      navigate('/dashboard', { replace: true });
    } catch (err) {
      setErrorMessage(err.message || 'Registration failed. Email may already be in use.');
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
                Create Recruiter Workspace
              </h1>
              <p className={`text-xs mt-1 leading-relaxed ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
                Register your account to unlock private screening jobs, AI scoring metrics, and candidate management.
              </p>
            </div>

            {/* Platform Features Checklist */}
            <div className="py-2 space-y-2 text-xs">
              {[
                'SentenceTransformer Contextual Match',
                'TF-IDF Keyword Density Analysis',
                'Skill & Experience Extraction',
                'Isolated Recruiter Workspaces',
              ].map((feat, i) => (
                <div key={i} className={`p-2.5 rounded-lg border flex items-center space-x-2 ${
                  theme === 'light' ? 'bg-white border-slate-200 text-slate-700' : 'bg-[#0e1422] border-slate-800 text-slate-300'
                }`}>
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                  <span className="font-mono text-[11px] font-semibold">{feat}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="relative z-10 pt-4 border-t border-slate-800/60 flex items-center justify-between text-[11px] font-mono text-slate-500">
            <span className="flex items-center space-x-1 text-emerald-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              <span>JWT Authentication</span>
            </span>
            <span>Argon2 Security</span>
          </div>
        </div>

        {/* RIGHT PANEL: Recruiter Register Form */}
        <div className="md:col-span-6 p-6 md:p-8 flex flex-col justify-center space-y-5">
          <div>
            <h2 className="text-lg font-bold tracking-wide uppercase">Register Account</h2>
            <p className={`text-xs mt-1 ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
              Fill details to provision your recruiter access
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
                Full Name / Recruiter Name
              </label>
              <div className="relative">
                <User className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Jane Doe"
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
                Password (min 8 characters)
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
                  <span>Provisioning...</span>
                </>
              ) : (
                <>
                  <span>Create Account</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          <p className={`text-center text-xs pt-2 border-t ${theme === 'light' ? 'border-slate-200 text-slate-600' : 'border-slate-800 text-slate-400'}`}>
            Already have an account?{' '}
            <Link to="/login" className="text-cyan-500 font-bold hover:underline">
              Login
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
