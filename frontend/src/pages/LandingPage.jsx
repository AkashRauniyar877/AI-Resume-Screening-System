import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Sparkles,
  FileText,
  Brain,
  Award,
  TrendingUp,
  CheckCircle2,
  ShieldCheck,
  Zap,
  Layers,
  Search,
  Users,
  Sun,
  Moon,
  ArrowRight,
  ChevronRight,
  Menu,
  X,
  Lock,
  Download,
  Eye,
  BarChart3,
  Cpu,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export const LandingPage = () => {
  const { isAuthenticated } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleActionClick = () => {
    if (isAuthenticated) {
      navigate('/dashboard');
    } else {
      navigate('/login');
    }
  };

  const scrollToSection = (id) => {
    setMobileMenuOpen(false);
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className={`min-h-screen ${theme === 'light' ? 'bg-slate-50 text-slate-900' : 'bg-[#07090e] text-slate-100'} transition-colors duration-200 bg-tech-grid relative overflow-hidden`}>
      {/* Background Glow Effects */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-96 bg-radial-glow pointer-events-none z-0" />

      {/* NAVBAR */}
      <nav className={`sticky top-0 z-50 w-full border-b ${theme === 'light' ? 'border-slate-200 bg-white/80' : 'border-slate-800/80 bg-[#07090e]/80'} backdrop-blur-md transition-colors duration-200`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          {/* Logo & Product Name */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate('/')}>
            <div className={`w-9 h-9 rounded-xl ${theme === 'light' ? 'bg-cyan-600 text-white shadow-md shadow-cyan-600/20' : 'bg-cyan-500/10 border border-cyan-500/30 text-cyan-400'} flex items-center justify-center transition-all`}>
              <Brain className="w-5 h-5" />
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="text-lg font-extrabold tracking-tight">Resume<span className="text-cyan-500">AI</span></span>
              <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${theme === 'light' ? 'bg-cyan-100 text-cyan-800' : 'bg-cyan-500/15 text-cyan-300'} font-semibold uppercase tracking-wider`}>
                PRO
              </span>
            </div>
          </div>

          {/* Desktop Nav Links */}
          <div className="hidden md:flex items-center space-x-8 text-sm font-medium">
            <button onClick={() => navigate('/')} className={`transition-colors ${theme === 'light' ? 'text-slate-900 font-semibold' : 'text-slate-100 font-semibold'}`}>
              Home
            </button>
            <button onClick={() => scrollToSection('how-it-works')} className={`transition-colors hover:text-cyan-500 ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
              How It Works
            </button>
            <button onClick={() => scrollToSection('features')} className={`transition-colors hover:text-cyan-500 ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
              Features
            </button>
            <button onClick={() => scrollToSection('scoring')} className={`transition-colors hover:text-cyan-500 ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
              AI Scoring
            </button>
            <button onClick={() => scrollToSection('why-us')} className={`transition-colors hover:text-cyan-500 ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
              About
            </button>
          </div>

          {/* Right Action Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            {/* Dark/Light Toggle */}
            <button
              onClick={toggleTheme}
              className={`p-2 rounded-lg border transition-all ${
                theme === 'light'
                  ? 'bg-slate-100 border-slate-300 text-amber-600 hover:bg-slate-200'
                  : 'bg-slate-900 border-slate-800 text-cyan-400 hover:bg-slate-800'
              }`}
              title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} mode`}
              aria-label="Toggle dark/light mode"
            >
              {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>

            {isAuthenticated ? (
              <button
                onClick={() => navigate('/dashboard')}
                className="px-4 py-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs tracking-wide uppercase transition-all shadow-md shadow-cyan-500/20"
              >
                Go to Dashboard
              </button>
            ) : (
              <>
                <button
                  onClick={() => navigate('/login')}
                  className={`px-4 py-2 rounded-lg text-xs font-semibold tracking-wide transition-all border ${
                    theme === 'light'
                      ? 'border-slate-300 text-slate-700 hover:bg-slate-100'
                      : 'border-slate-800 text-slate-300 hover:bg-slate-800/80 hover:text-slate-100'
                  }`}
                >
                  Login
                </button>
                <button
                  onClick={() => navigate('/login')}
                  className="px-4 py-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs tracking-wide uppercase transition-all shadow-md shadow-cyan-500/20 flex items-center space-x-1.5"
                >
                  <span>Get Started</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center space-x-2">
            <button
              onClick={toggleTheme}
              className={`p-2 rounded-lg border ${
                theme === 'light' ? 'bg-slate-100 border-slate-300 text-amber-600' : 'bg-slate-900 border-slate-800 text-cyan-400'
              }`}
            >
              {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className={`p-2 rounded-lg border ${theme === 'light' ? 'border-slate-300 bg-slate-100' : 'border-slate-800 bg-slate-900'}`}
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation Drawer */}
        {mobileMenuOpen && (
          <div className={`md:hidden border-b px-4 py-6 space-y-4 ${theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#0a0e17] border-slate-800'}`}>
            <div className="flex flex-col space-y-3 font-medium text-sm">
              <button onClick={() => { navigate('/'); setMobileMenuOpen(false); }} className="text-left py-1 text-cyan-500 font-bold">
                Home
              </button>
              <button onClick={() => scrollToSection('how-it-works')} className="text-left py-1 hover:text-cyan-500">
                How It Works
              </button>
              <button onClick={() => scrollToSection('features')} className="text-left py-1 hover:text-cyan-500">
                Features
              </button>
              <button onClick={() => scrollToSection('scoring')} className="text-left py-1 hover:text-cyan-500">
                AI Scoring
              </button>
              <button onClick={() => scrollToSection('why-us')} className="text-left py-1 hover:text-cyan-500">
                About
              </button>
            </div>
            <div className="pt-4 border-t border-slate-800 flex flex-col space-y-2">
              <button
                onClick={() => { navigate('/login'); setMobileMenuOpen(false); }}
                className="w-full py-2.5 rounded-lg border border-slate-700 text-center font-medium text-xs"
              >
                Login
              </button>
              <button
                onClick={() => { handleActionClick(); setMobileMenuOpen(false); }}
                className="w-full py-2.5 rounded-lg bg-cyan-500 text-slate-950 font-bold text-xs text-center uppercase"
              >
                Get Started
              </button>
            </div>
          </div>
        )}
      </nav>

      {/* HERO SECTION */}
      <section className="relative pt-12 pb-20 md:pt-20 md:pb-28 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
          {/* Left Column: Copy & Actions */}
          <div className="lg:col-span-6 space-y-6 text-left">
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-mono border border-cyan-500/30 bg-cyan-500/10 text-cyan-400">
              <Sparkles className="w-3.5 h-3.5 animate-pulse" />
              <span>Next-Gen AI Resume Screening Engine</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight leading-[1.1]">
              Find the Right Talent,{' '}
              <span className="bg-gradient-to-r from-cyan-400 via-teal-300 to-blue-500 bg-clip-text text-transparent">
                Faster.
              </span>
            </h1>

            <p className={`text-base sm:text-lg leading-relaxed ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'} max-w-xl`}>
              AI-powered resume screening that analyzes skills, experience and relevance to help recruiters discover the strongest candidates.
            </p>

            <div className="pt-2 flex flex-col sm:flex-row items-stretch sm:items-center space-y-3 sm:space-y-0 sm:space-x-4">
              <button
                onClick={handleActionClick}
                className="px-6 py-3.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-sm tracking-wide transition-all shadow-lg shadow-cyan-500/25 flex items-center justify-center space-x-2 group"
              >
                <span>Get Started</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </button>

              <button
                onClick={() => scrollToSection('how-it-works')}
                className={`px-6 py-3.5 rounded-xl border text-sm font-semibold transition-all flex items-center justify-center space-x-2 ${
                  theme === 'light'
                    ? 'border-slate-300 bg-white text-slate-800 hover:bg-slate-100'
                    : 'border-slate-800 bg-slate-900/80 text-slate-200 hover:bg-slate-800 hover:border-slate-700'
                }`}
              >
                <span>Explore How It Works</span>
              </button>
            </div>

            {/* Quick Metrics */}
            <div className="pt-6 border-t border-slate-800/60 grid grid-cols-3 gap-4">
              <div>
                <p className="text-2xl font-black text-cyan-400 font-mono">90%</p>
                <p className={`text-xs ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>Time Saved</p>
              </div>
              <div>
                <p className="text-2xl font-black text-teal-400 font-mono">4-Way</p>
                <p className={`text-xs ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>Hybrid AI Evaluation</p>
              </div>
              <div>
                <p className="text-2xl font-black text-indigo-400 font-mono">100%</p>
                <p className={`text-xs ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>Objective Ranking</p>
              </div>
            </div>
          </div>

          {/* Right Column: Visual AI Recruitment Card */}
          <div className="lg:col-span-6 relative">
            {/* Visual Process Flow Box */}
            <div className={`rounded-2xl border p-6 sm:p-8 shadow-2xl relative transition-colors ${
              theme === 'light'
                ? 'bg-white border-slate-200 shadow-slate-200/50'
                : 'bg-[#0b101b] border-slate-800 shadow-cyan-950/20'
            }`}>
              {/* Header Badge */}
              <div className="flex items-center justify-between pb-4 mb-6 border-b border-slate-800/60">
                <div className="flex items-center space-x-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
                  <span className="text-xs font-mono font-bold tracking-wider uppercase text-emerald-400">
                    AI Pipeline Active
                  </span>
                </div>
                <span className={`text-xs font-mono ${theme === 'light' ? 'text-slate-500' : 'text-slate-500'}`}>
                  Model: SentenceTransformer + TF-IDF
                </span>
              </div>

              {/* Workflow Flow Steps */}
              <div className="flex items-center justify-between gap-2 mb-8 text-center text-xs font-mono">
                <div className={`p-2.5 rounded-lg border flex-1 ${theme === 'light' ? 'bg-slate-100 border-slate-300' : 'bg-[#131b2c] border-slate-800'}`}>
                  <FileText className="w-4 h-4 mx-auto mb-1 text-cyan-400" />
                  <span className="font-semibold block">RESUME</span>
                </div>
                <ChevronRight className="w-4 h-4 text-cyan-500 flex-shrink-0" />
                <div className={`p-2.5 rounded-lg border flex-1 ${theme === 'light' ? 'bg-cyan-50 border-cyan-200' : 'bg-cyan-950/40 border-cyan-800/60'}`}>
                  <Brain className="w-4 h-4 mx-auto mb-1 text-cyan-400" />
                  <span className="font-semibold block text-cyan-400">AI ANALYSIS</span>
                </div>
                <ChevronRight className="w-4 h-4 text-cyan-500 flex-shrink-0" />
                <div className={`p-2.5 rounded-lg border flex-1 ${theme === 'light' ? 'bg-teal-50 border-teal-200' : 'bg-teal-950/40 border-teal-800/60'}`}>
                  <BarChart3 className="w-4 h-4 mx-auto mb-1 text-teal-400" />
                  <span className="font-semibold block text-teal-400">SCORES</span>
                </div>
                <ChevronRight className="w-4 h-4 text-teal-500 flex-shrink-0" />
                <div className={`p-2.5 rounded-lg border flex-1 ${theme === 'light' ? 'bg-emerald-50 border-emerald-200' : 'bg-emerald-950/40 border-emerald-800/60'}`}>
                  <Award className="w-4 h-4 mx-auto mb-1 text-emerald-400" />
                  <span className="font-semibold block text-emerald-400">TOP MATCH</span>
                </div>
              </div>

              {/* Sample Evaluated Candidate Card */}
              <div className={`p-4 rounded-xl border relative ${
                theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#121927] border-slate-800'
              }`}>
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-lg bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 flex items-center justify-center font-bold font-mono">
                      AC
                    </div>
                    <div>
                      <h4 className="text-sm font-bold tracking-tight">Ajay Chaudhary</h4>
                      <p className={`text-xs ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>Full Stack Developer</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-xs font-mono font-bold px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 inline-flex items-center space-x-1">
                      <Award className="w-3 h-3" />
                      <span>94.8% Rank #1</span>
                    </span>
                  </div>
                </div>

                {/* Score Components breakdown */}
                <div className="space-y-2.5 text-xs font-mono">
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className={theme === 'light' ? 'text-slate-600' : 'text-slate-400'}>Skill Match (35%)</span>
                      <span className="font-bold text-cyan-400">84.6%</span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
                      <div className="h-full bg-cyan-400 rounded-full" style={{ width: '84.6%' }} />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between mb-1">
                      <span className={theme === 'light' ? 'text-slate-600' : 'text-slate-400'}>Semantic Match (30%)</span>
                      <span className="font-bold text-teal-400">95.9%</span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
                      <div className="h-full bg-teal-400 rounded-full" style={{ width: '95.9%' }} />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between mb-1">
                      <span className={theme === 'light' ? 'text-slate-600' : 'text-slate-400'}>TF-IDF Lexical (20%)</span>
                      <span className="font-bold text-indigo-400">100.0%</span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
                      <div className="h-full bg-indigo-400 rounded-full" style={{ width: '100%' }} />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* HOW IT WORKS SECTION */}
      <section id="how-it-works" className={`py-20 border-t ${theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#090d16] border-slate-800/80'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
            <span className="text-xs font-mono font-bold text-cyan-400 uppercase tracking-widest px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20">
              Streamlined Workflow
            </span>
            <h2 className="text-3xl sm:text-4xl font-black tracking-tight">
              How ResumeAI Works
            </h2>
            <p className={`text-base ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
              Four effortless steps to evaluate hundreds of applicants with mathematical objectivity.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                step: '01',
                title: 'Upload Resumes',
                desc: 'Upload multiple PDF or DOCX candidate resumes simultaneously.',
                icon: FileText,
                color: 'text-cyan-400',
              },
              {
                step: '02',
                title: 'Add Job Description',
                desc: 'Paste requirements, required skills, and experience criteria.',
                icon: Layers,
                color: 'text-teal-400',
              },
              {
                step: '03',
                title: 'AI Analyzes Candidates',
                desc: 'Our NLP pipeline extracts skills, experience & calculates semantic embeddings.',
                icon: Cpu,
                color: 'text-blue-400',
              },
              {
                step: '04',
                title: 'Get Ranked Results',
                desc: 'View ranked candidates with transparent hybrid score breakdowns.',
                icon: Award,
                color: 'text-emerald-400',
              },
            ].map((item) => {
              const Icon = item.icon;
              return (
                <div
                  key={item.step}
                  className={`p-6 rounded-2xl border transition-all duration-200 hover:-translate-y-1 ${
                    theme === 'light'
                      ? 'bg-slate-50 border-slate-200 hover:border-slate-300 hover:shadow-lg'
                      : 'bg-[#0f1420] border-slate-800/80 hover:border-cyan-500/30'
                  }`}
                >
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-2xl font-black font-mono text-cyan-500/40">{item.step}</span>
                    <div className={`p-2.5 rounded-xl ${theme === 'light' ? 'bg-slate-200/70' : 'bg-slate-800/70'} ${item.color}`}>
                      <Icon className="w-5 h-5" />
                    </div>
                  </div>
                  <h3 className="text-lg font-bold mb-2 tracking-tight">{item.title}</h3>
                  <p className={`text-xs leading-relaxed ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>{item.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <section id="features" className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <span className="text-xs font-mono font-bold text-teal-400 uppercase tracking-widest px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/20">
            Intelligent Platform Features
          </span>
          <h2 className="text-3xl sm:text-4xl font-black tracking-tight">
            Built for Modern Recruitment Teams
          </h2>
          <p className={`text-base ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
            Comprehensive AI tooling designed for speed, accuracy, and absolute recruiter confidence.
          </p>
        </div>

        {/* Asymmetric Grid Hierarchy */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1: AI Resume Screening (Large) */}
          <div className={`md:col-span-2 p-8 rounded-2xl border ${
            theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#0b101b] border-slate-800'
          }`}>
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center mb-6">
              <Zap className="w-5 h-5" />
            </div>
            <h3 className="text-xl font-bold mb-2">AI Resume Screening</h3>
            <p className={`text-sm leading-relaxed ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'} max-w-xl`}>
              Automatic text extraction from PDF and DOCX formats. Cleanses unformatted text, standardizes candidate records, and normalizes candidate qualifications for instant matching.
            </p>
          </div>

          {/* Card 2: Skill Matching */}
          <div className={`p-8 rounded-2xl border ${
            theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#0b101b] border-slate-800'
          }`}>
            <div className="w-10 h-10 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-400 flex items-center justify-center mb-6">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <h3 className="text-xl font-bold mb-2">Skill Matching</h3>
            <p className={`text-sm leading-relaxed ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
              Domain-specific taxonomy extraction identifying technical, soft, and specialized skills directly against job criteria.
            </p>
          </div>

          {/* Card 3: Semantic Similarity */}
          <div className={`p-8 rounded-2xl border ${
            theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#0b101b] border-slate-800'
          }`}>
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 flex items-center justify-center mb-6">
              <Brain className="w-5 h-5" />
            </div>
            <h3 className="text-xl font-bold mb-2">Semantic Similarity</h3>
            <p className={`text-sm leading-relaxed ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
              Uses SentenceTransformers (<code className="text-xs font-mono">all-MiniLM-L6-v2</code>) to evaluate conceptual relevance beyond mere word matching.
            </p>
          </div>

          {/* Card 4: TF-IDF Analysis */}
          <div className={`p-8 rounded-2xl border ${
            theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#0b101b] border-slate-800'
          }`}>
            <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/30 text-blue-400 flex items-center justify-center mb-6">
              <Search className="w-5 h-5" />
            </div>
            <h3 className="text-xl font-bold mb-2">TF-IDF Analysis</h3>
            <p className={`text-sm leading-relaxed ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
              Lexical term frequency weighting highlights critical job keywords and specialized candidate terminology.
            </p>
          </div>

          {/* Card 5: Candidate Ranking */}
          <div className={`p-8 rounded-2xl border ${
            theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#0b101b] border-slate-800'
          }`}>
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center mb-6">
              <Award className="w-5 h-5" />
            </div>
            <h3 className="text-xl font-bold mb-2">Candidate Ranking</h3>
            <p className={`text-sm leading-relaxed ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
              Min-Max normalized scoring provides fair, mathematically consistent candidate shortlists.
            </p>
          </div>

          {/* Card 6: Resume View & Download */}
          <div className={`p-8 rounded-2xl border ${
            theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#0b101b] border-slate-800'
          }`}>
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center mb-6">
              <Eye className="w-5 h-5" />
            </div>
            <h3 className="text-xl font-bold mb-2">Resume View & Download</h3>
            <p className={`text-sm leading-relaxed ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
              In-browser PDF preview and direct file downloads for verified recruiters.
            </p>
          </div>

          {/* Card 7: Recruiter Auth & Security (Large) */}
          <div className={`md:col-span-2 p-8 rounded-2xl border ${
            theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#0b101b] border-slate-800'
          }`}>
            <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400 flex items-center justify-center mb-6">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h3 className="text-xl font-bold mb-2">Recruiter Authentication & Data Isolation</h3>
            <p className={`text-sm leading-relaxed ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'} max-w-xl`}>
              Protected routes powered by JWT tokens ensure that each recruiter retains strict workspace isolation over uploaded resumes, screening jobs, and candidate evaluation metrics.
            </p>
          </div>
        </div>
      </section>

      {/* AI SCORING VISUALIZATION SECTION */}
      <section id="scoring" className={`py-20 border-t ${theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#090d16] border-slate-800/80'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
            <span className="text-xs font-mono font-bold text-cyan-400 uppercase tracking-widest px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20">
              Transparent Evaluation Model
            </span>
            <h2 className="text-3xl sm:text-4xl font-black tracking-tight">
              How ResumeAI Evaluates Candidates
            </h2>
            <p className={`text-base ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
              Every candidate score is calculated using our validated 4-part weighted evaluation formula.
            </p>
          </div>

          {/* Scoring Visual Breakdown */}
          <div className={`p-8 rounded-2xl border max-w-4xl mx-auto ${
            theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#0c121e] border-slate-800'
          }`}>
            <div className="space-y-6">
              {/* Skill Match: 35% */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="w-3 h-3 rounded-full bg-cyan-400" />
                    <span className="font-bold text-sm">Skill Matching</span>
                  </div>
                  <span className="font-mono font-bold text-cyan-400 text-sm">35% Weight</span>
                </div>
                <div className="w-full h-3 rounded-full bg-slate-800 overflow-hidden">
                  <div className="h-full bg-cyan-400 rounded-full" style={{ width: '35%' }} />
                </div>
                <p className={`text-xs mt-1 ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>
                  Direct technical and domain skill overlap extracted from job description criteria.
                </p>
              </div>

              {/* Semantic Similarity: 30% */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="w-3 h-3 rounded-full bg-teal-400" />
                    <span className="font-bold text-sm">Semantic Similarity</span>
                  </div>
                  <span className="font-mono font-bold text-teal-400 text-sm">30% Weight</span>
                </div>
                <div className="w-full h-3 rounded-full bg-slate-800 overflow-hidden">
                  <div className="h-full bg-teal-400 rounded-full" style={{ width: '30%' }} />
                </div>
                <p className={`text-xs mt-1 ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>
                  SentenceTransformer contextual embedding similarity score.
                </p>
              </div>

              {/* TF-IDF: 20% */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="w-3 h-3 rounded-full bg-indigo-400" />
                    <span className="font-bold text-sm">TF-IDF Lexical Similarity</span>
                  </div>
                  <span className="font-mono font-bold text-indigo-400 text-sm">20% Weight</span>
                </div>
                <div className="w-full h-3 rounded-full bg-slate-800 overflow-hidden">
                  <div className="h-full bg-indigo-400 rounded-full" style={{ width: '20%' }} />
                </div>
                <p className={`text-xs mt-1 ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>
                  Inverse document frequency keyword density and exact match importance.
                </p>
              </div>

              {/* Experience: 15% */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="w-3 h-3 rounded-full bg-amber-400" />
                    <span className="font-bold text-sm">Experience Evaluation</span>
                  </div>
                  <span className="font-mono font-bold text-amber-400 text-sm">15% Weight</span>
                </div>
                <div className="w-full h-3 rounded-full bg-slate-800 overflow-hidden">
                  <div className="h-full bg-amber-400 rounded-full" style={{ width: '15%' }} />
                </div>
                <p className={`text-xs mt-1 ${theme === 'light' ? 'text-slate-500' : 'text-slate-400'}`}>
                  Extracted years of experience compared against job requirement thresholds.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* WHY USE RESUMEAI SECTION */}
      <section id="why-us" className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <span className="text-xs font-mono font-bold text-emerald-400 uppercase tracking-widest px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20">
            Why ResumeAI
          </span>
          <h2 className="text-3xl sm:text-4xl font-black tracking-tight">
            From Hundreds of Resumes to a Focused Shortlist
          </h2>
          <p className={`text-base ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
            Replace manual resume scanning with an intelligent automated pipeline.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            {
              title: 'Faster Screening',
              desc: 'Screen 50+ candidate resumes in seconds instead of spending hours reading documents manually.',
              icon: Zap,
            },
            {
              title: 'Consistent Evaluation',
              desc: 'Apply standardized NLP matching rules across every single applicant without human bias.',
              icon: CheckCircle2,
            },
            {
              title: 'Data-Driven Ranking',
              desc: 'Understand exactly why a candidate received their score with itemized metric breakdowns.',
              icon: BarChart3,
            },
            {
              title: 'Recruiter-Friendly',
              desc: 'Simple intuitive workflow built specifically for modern HR professionals and technical recruiters.',
              icon: Users,
            },
          ].map((item, idx) => {
            const Icon = item.icon;
            return (
              <div
                key={idx}
                className={`p-6 rounded-2xl border ${
                  theme === 'light' ? 'bg-white border-slate-200' : 'bg-[#0f1420] border-slate-800'
                }`}
              >
                <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center mb-4">
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="text-base font-bold mb-2 tracking-tight">{item.title}</h3>
                <p className={`text-xs leading-relaxed ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>{item.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* FINAL CTA */}
      <section className={`py-20 border-t ${theme === 'light' ? 'bg-slate-100 border-slate-200' : 'bg-[#080b12] border-slate-800'}`}>
        <div className="max-w-4xl mx-auto px-4 text-center space-y-6">
          <h2 className="text-3xl sm:text-5xl font-black tracking-tight">
            Ready to screen smarter?
          </h2>
          <p className={`text-base sm:text-lg max-w-2xl mx-auto ${theme === 'light' ? 'text-slate-600' : 'text-slate-400'}`}>
            Start screening candidates today with our AI-powered resume intelligence system.
          </p>
          <div className="pt-4">
            <button
              onClick={handleActionClick}
              className="px-8 py-4 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-base tracking-wide uppercase transition-all shadow-xl shadow-cyan-500/30 inline-flex items-center space-x-2"
            >
              <span>Start Screening</span>
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className={`py-8 border-t ${theme === 'light' ? 'border-slate-200 bg-white text-slate-500' : 'border-slate-800 bg-[#05070a] text-slate-500'} text-xs text-center`}>
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <Brain className="w-4 h-4 text-cyan-500" />
            <span className="font-bold tracking-tight text-slate-300">ResumeAI Platform</span>
          </div>
          <p>© {new Date().getFullYear()} ResumeAI — AI-Powered Resume Screening System. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
