import MasteryBadge from './MasteryBadge';

interface ModuleCardProps {
  name: string;
  description: string;
  mastery: number;
  topicsCount: number;
  exercisesDone: number;
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

export default function ModuleCard({ name, description, mastery, topicsCount, exercisesDone, onClick }: ModuleCardProps) {
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
          <div className="flex gap-4 text-xs text-slate-500">
            <span>{topicsCount} topics</span>
            <span>{exercisesDone} exercises done</span>
          </div>
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
    </div>
  );
}
