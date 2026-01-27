import { AlertTriangle } from 'lucide-react';
import MasteryBadge from './MasteryBadge';

interface StudentData {
  student_id: string;
  name: string;
  overall_mastery: number;
  struggling_topics: string[];
}

interface TeacherStudentRowProps {
  student: StudentData;
  onClick?: () => void;
}

export default function TeacherStudentRow({ student, onClick }: TeacherStudentRowProps) {
  const hasStruggles = student.struggling_topics.length > 0;

  return (
    <div
      onClick={onClick}
      className={`flex items-center gap-4 p-4 rounded-lg border transition cursor-pointer ${
        hasStruggles
          ? 'border-red-800 bg-red-900/10 hover:bg-red-900/20'
          : 'border-slate-700 bg-slate-800 hover:bg-slate-750'
      }`}
    >
      {/* Avatar */}
      <div className="w-10 h-10 rounded-full bg-slate-600 flex items-center justify-center text-sm font-bold text-white">
        {student.name.charAt(0).toUpperCase()}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="font-medium text-white text-sm">{student.name}</span>
          {hasStruggles && (
            <AlertTriangle size={14} className="text-red-400" />
          )}
        </div>
        {hasStruggles && (
          <p className="text-xs text-red-400 truncate">
            Struggling: {student.struggling_topics.join(', ')}
          </p>
        )}
      </div>

      {/* Mastery */}
      <MasteryBadge mastery={student.overall_mastery} size="sm" showLabel={false} />
    </div>
  );
}
