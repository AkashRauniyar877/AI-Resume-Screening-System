import React from 'react';
import { Award, Zap, Code, Clock, Star } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

export const ScoreBreakdown = ({ matchResults, compact = false }) => {
  const { theme } = useTheme();

  if (!matchResults) return null;

  const {
    skill_coverage = 0,
    semantic_score = 0,
    semantic_normalized = 0,
    tfidf_score = 0,
    tfidf_normalized = 0,
    experience_score = 0,
    hybrid_score = 0,
  } = matchResults;

  const scoreItems = [
    {
      label: 'Skill Match',
      weight: '35%',
      value: skill_coverage,
      icon: Code,
      color: 'bg-emerald-500',
      textColor: theme === 'light' ? 'text-emerald-700' : 'text-emerald-400',
    },
    {
      label: 'Semantic AI',
      weight: '30%',
      value: semantic_normalized || semantic_score,
      icon: Zap,
      color: 'bg-cyan-500',
      textColor: theme === 'light' ? 'text-cyan-700' : 'text-cyan-400',
    },
    {
      label: 'TF-IDF Keyword',
      weight: '20%',
      value: tfidf_normalized || tfidf_score,
      icon: Star,
      color: 'bg-amber-500',
      textColor: theme === 'light' ? 'text-amber-700' : 'text-amber-400',
    },
    {
      label: 'Experience',
      weight: '15%',
      value: experience_score,
      icon: Clock,
      color: 'bg-blue-500',
      textColor: theme === 'light' ? 'text-blue-700' : 'text-blue-400',
    },
  ];

  if (compact) {
    return (
      <div className="flex items-center space-x-2 font-mono text-xs">
        <div className={`px-2 py-0.5 rounded border font-bold ${
          theme === 'light'
            ? 'bg-cyan-50 border-cyan-200 text-cyan-700'
            : 'bg-cyan-500/10 border-cyan-500/30 text-cyan-300'
        }`}>
          {Number(hybrid_score).toFixed(1)}%
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {/* Overall Hybrid Score Banner */}
      <div className={`p-3.5 rounded border flex items-center justify-between transition-colors ${
        theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#090b0e] border-[#1e2634]'
      }`}>
        <div>
          <span className={`text-[10px] font-mono font-bold uppercase tracking-widest flex items-center space-x-1 ${
            theme === 'light' ? 'text-cyan-700' : 'text-cyan-400'
          }`}>
            <Award className="w-3.5 h-3.5" />
            <span>AI Authoritative Hybrid Score</span>
          </span>
          <p className={`text-xl font-bold font-mono mt-0.5 ${
            theme === 'light' ? 'text-slate-900' : 'text-slate-100'
          }`}>
            {Number(hybrid_score).toFixed(1)}
            <span className={`text-xs font-normal ml-1 ${theme === 'light' ? 'text-slate-500' : 'text-slate-500'}`}>/ 100</span>
          </p>
        </div>
        <div className={`px-3 py-1.5 rounded font-mono font-bold text-sm border ${
          theme === 'light'
            ? 'bg-cyan-50 border-cyan-200 text-cyan-700'
            : 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400'
        }`}>
          {Math.round(hybrid_score)}% Match
        </div>
      </div>

      {/* Matching Meters Breakdown */}
      <div className="space-y-2">
        {scoreItems.map((item, idx) => {
          const Icon = item.icon;
          const roundedVal = Math.min(100, Math.max(0, Number(item.value) || 0));
          return (
            <div key={idx} className={`p-2.5 rounded border space-y-1.5 transition-colors ${
              theme === 'light' ? 'bg-slate-50 border-slate-200' : 'bg-[#090b0e] border-[#1e2634]'
            }`}>
              <div className="flex items-center justify-between text-xs font-mono">
                <span className={`font-medium flex items-center space-x-1.5 ${
                  theme === 'light' ? 'text-slate-800' : 'text-slate-300'
                }`}>
                  <Icon className={`w-3.5 h-3.5 ${item.textColor}`} />
                  <span>{item.label}</span>
                </span>
                <div className="flex items-center space-x-2">
                  <span className={`text-[10px] ${theme === 'light' ? 'text-slate-500' : 'text-slate-500'}`}>Weight: {item.weight}</span>
                  <span className={`font-bold ${item.textColor}`}>{roundedVal.toFixed(1)}%</span>
                </div>
              </div>

              {/* Horizontal Score Meter */}
              <div className={`w-full h-1.5 rounded overflow-hidden ${
                theme === 'light' ? 'bg-slate-200' : 'bg-[#131822]'
              }`}>
                <div
                  className={`h-full ${item.color} transition-all duration-300`}
                  style={{ width: `${Math.min(100, roundedVal)}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ScoreBreakdown;
