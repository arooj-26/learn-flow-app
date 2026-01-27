import MasteryBadge from './MasteryBadge';
import type { TopicProgress } from '@/utils/api';

interface ProgressCardProps {
  topic: TopicProgress;
  onClick?: () => void;
}

export default function ProgressCard({ topic, onClick }: ProgressCardProps) {
  return (
    <div
      onClick={onClick}
      className="bg-slate-800 border border-slate-700 rounded-xl p-4 hover:border-slate-500 transition-all cursor-pointer animate-slide-up"
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <h3 className="font-semibold text-white text-sm">{topic.topic_name}</h3>
          <div className="mt-2 flex items-center gap-4 text-xs text-slate-400">
            <span>Exercises: {topic.exercises_done}</span>
            <span>Quiz: {topic.quiz_score}%</span>
            <span>Streak: {topic.streak}</span>
          </div>
          {/* Progress bar */}
          <div className="mt-3 h-2 bg-slate-700 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-500 ${
                topic.mastery >= 91 ? 'bg-blue-500' :
                topic.mastery >= 71 ? 'bg-green-500' :
                topic.mastery >= 41 ? 'bg-yellow-500' : 'bg-red-500'
              }`}
              style={{ width: `${topic.mastery}%` }}
            />
          </div>
        </div>
        <div className="ml-4">
          <MasteryBadge mastery={topic.mastery} size="sm" />
        </div>
      </div>
    </div>
  );
}
