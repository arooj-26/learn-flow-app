interface MasteryBadgeProps {
  mastery: number;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
}

const LEVELS = {
  beginner:   { label: 'Beginner',   color: 'bg-red-500',    text: 'text-red-400',    min: 0 },
  learning:   { label: 'Learning',   color: 'bg-yellow-500', text: 'text-yellow-400', min: 41 },
  proficient: { label: 'Proficient', color: 'bg-green-500',  text: 'text-green-400',  min: 71 },
  mastered:   { label: 'Mastered',   color: 'bg-blue-500',   text: 'text-blue-400',   min: 91 },
} as const;

function getLevel(mastery: number) {
  if (mastery >= 91) return LEVELS.mastered;
  if (mastery >= 71) return LEVELS.proficient;
  if (mastery >= 41) return LEVELS.learning;
  return LEVELS.beginner;
}

const sizes = {
  sm: { ring: 'w-10 h-10', text: 'text-xs', label: 'text-[10px]' },
  md: { ring: 'w-16 h-16', text: 'text-sm', label: 'text-xs' },
  lg: { ring: 'w-24 h-24', text: 'text-lg', label: 'text-sm' },
};

export default function MasteryBadge({ mastery, size = 'md', showLabel = true }: MasteryBadgeProps) {
  const level = getLevel(mastery);
  const s = sizes[size];
  const circumference = 2 * Math.PI * 40;
  const strokeDashoffset = circumference - (mastery / 100) * circumference;

  return (
    <div className="flex flex-col items-center gap-1">
      <div className={`relative ${s.ring} flex items-center justify-center`}>
        <svg className="absolute inset-0 -rotate-90" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="40" fill="none" stroke="#334155" strokeWidth="8" />
          <circle
            cx="50" cy="50" r="40" fill="none"
            stroke="currentColor"
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            className={level.text}
          />
        </svg>
        <span className={`${s.text} font-bold ${level.text}`}>{mastery}%</span>
      </div>
      {showLabel && (
        <span className={`${s.label} font-medium ${level.text}`}>{level.label}</span>
      )}
    </div>
  );
}
