import MasteryBadge from './MasteryBadge';
import { Target, BookOpen } from 'lucide-react';

interface ModuleCardProps {
  name: string;
  description: string;
  mastery: number;
  topicsCount: number;
  exercisesDone: number;
  quizzesDone?: number;
  quizzesTotal?: number;
  bestQuizScore?: number;
  onClick?: () => void;
}

const MODULE_ICONS: Record<string, string> = {
  'Basics': '🔤',
  'Control Flow': '🔀',
  'Data Structures': '📦',
  'Functions': '⚙️',
  'OOP': '🏗️',
  'Files': '📁',
  'Errors': '🐛',
  'Libraries': '📚',
};

export default function ModuleCard({
  name,
  description,
  mastery,
  topicsCount,
  exercisesDone,
  quizzesDone = 0,
  quizzesTotal = 0,
  bestQuizScore,
  onClick
}: ModuleCardProps) {
  return (
    <div
      onClick={onClick}
      className="bg-slate-800 border border-slate-700 rounded-xl p-5 hover:border-slate-500 hover:shadow-lg transition-all cursor-pointer group"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xl">{MODULE_ICONS[name] || '📘'}</span>
            <h3 className="font-semibold text-white group-hover:text-blue-300 transition">{name}</h3>
          </div>
          <p className="text-xs text-slate-400 mb-3">{description}</p>

          {/* Stats row */}
          <div className="flex flex-wrap gap-3 text-xs">
            <span className="text-slate-500">{topicsCount} topics</span>

            {/* Exercises stat */}
            <span className="flex items-center gap-1 text-blue-400">
              <BookOpen size={12} />
              {exercisesDone} exercises
            </span>

            {/* Quiz stat */}
            {quizzesTotal > 0 && (
              <span className="flex items-center gap-1 text-purple-400">
                <Target size={12} />
                {quizzesDone}/{quizzesTotal} quizzes
              </span>
            )}
          </div>

          {/* Best quiz score badge */}
          {bestQuizScore !== undefined && bestQuizScore > 0 && (
            <div className="mt-2">
              <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium ${
                bestQuizScore >= 90 ? 'bg-green-500/20 text-green-400' :
                bestQuizScore >= 70 ? 'bg-blue-500/20 text-blue-400' :
                bestQuizScore >= 50 ? 'bg-yellow-500/20 text-yellow-400' :
                'bg-red-500/20 text-red-400'
              }`}>
                Best Quiz: {bestQuizScore}%
              </span>
            </div>
          )}
        </div>
        <MasteryBadge mastery={mastery} size="sm" />
      </div>

      {/* Progress bar */}
      <div className="mt-4 h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-700 ${
            mastery >= 91 ? 'bg-blue-500' :
            mastery >= 71 ? 'bg-green-500' :
            mastery >= 41 ? 'bg-yellow-500' : 'bg-red-500'
          }`}
          style={{ width: `${mastery}%` }}
        />
      </div>

      {/* Quiz progress bar (if quizzes exist) */}
      {quizzesTotal > 0 && (
        <div className="mt-2">
          <div className="flex items-center justify-between text-[10px] text-slate-500 mb-1">
            <span>Quiz Progress</span>
            <span>{Math.round((quizzesDone / quizzesTotal) * 100)}%</span>
          </div>
          <div className="h-1 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full bg-purple-500 transition-all duration-700"
              style={{ width: `${(quizzesDone / quizzesTotal) * 100}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
