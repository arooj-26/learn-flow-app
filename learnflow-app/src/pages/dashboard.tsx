import Layout from '@/components/Layout';
import ModuleCard from '@/components/ModuleCard';
import MasteryBadge from '@/components/MasteryBadge';
import ProgressCard from '@/components/ProgressCard';
import { BarChart3, TrendingUp, BookOpen, Flame, Loader2 } from 'lucide-react';
import { useRequireAuth } from '@/components/withAuth';

// Demo data - in production, fetched from progress-agent
const MODULES = [
  { name: 'Basics', description: 'Variables, types, operators, I/O', mastery: 78, topicsCount: 4, exercisesDone: 12 },
  { name: 'Control Flow', description: 'Conditionals, loops, flow control', mastery: 65, topicsCount: 4, exercisesDone: 8 },
  { name: 'Data Structures', description: 'Lists, tuples, dicts, sets', mastery: 45, topicsCount: 5, exercisesDone: 5 },
  { name: 'Functions', description: 'Defining and using functions', mastery: 30, topicsCount: 5, exercisesDone: 3 },
  { name: 'OOP', description: 'Object-oriented programming', mastery: 15, topicsCount: 5, exercisesDone: 1 },
  { name: 'Files', description: 'File handling and I/O', mastery: 0, topicsCount: 4, exercisesDone: 0 },
  { name: 'Errors', description: 'Exception handling', mastery: 0, topicsCount: 4, exercisesDone: 0 },
  { name: 'Libraries', description: 'Standard library and packages', mastery: 0, topicsCount: 4, exercisesDone: 0 },
];

const RECENT_TOPICS = [
  { topic_id: '1', topic_name: 'For Loops', mastery: 72, level: 'proficient' as const, exercises_done: 5, quiz_score: 80, code_quality: 70, streak: 3 },
  { topic_id: '2', topic_name: 'Lists', mastery: 45, level: 'learning' as const, exercises_done: 3, quiz_score: 60, code_quality: 50, streak: 1 },
  { topic_id: '3', topic_name: 'Variables & Types', mastery: 92, level: 'mastered' as const, exercises_done: 10, quiz_score: 95, code_quality: 85, streak: 7 },
  { topic_id: '4', topic_name: 'Functions', mastery: 28, level: 'beginner' as const, exercises_done: 2, quiz_score: 40, code_quality: 30, streak: 0 },
];

export default function Dashboard() {
  const { user, isReady } = useRequireAuth();
  const overallMastery = Math.round(MODULES.reduce((sum, m) => sum + m.mastery, 0) / MODULES.length);
  const totalExercises = MODULES.reduce((sum, m) => sum + m.exercisesDone, 0);
  const currentStreak = 5; // demo

  if (!isReady || !user) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <Loader2 className="animate-spin text-blue-400" size={32} />
      </div>
    );
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white">Welcome, {user.name}!</h1>
          <p className="text-slate-400 mt-1">Track your Python learning progress</p>
        </div>

        {/* Stats row */}
        <div className="grid grid-cols-4 gap-4 mb-8">
          <StatCard icon={<BarChart3 className="text-blue-400" />} label="Overall Mastery" value={`${overallMastery}%`} />
          <StatCard icon={<BookOpen className="text-green-400" />} label="Exercises Done" value={totalExercises.toString()} />
          <StatCard icon={<Flame className="text-orange-400" />} label="Current Streak" value={`${currentStreak} days`} />
          <StatCard icon={<TrendingUp className="text-purple-400" />} label="Modules Started" value={`${MODULES.filter(m => m.mastery > 0).length}/8`} />
        </div>

        {/* Overall mastery ring */}
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-6 mb-8 flex items-center gap-8">
          <MasteryBadge mastery={overallMastery} size="lg" />
          <div>
            <h2 className="text-lg font-semibold text-white">Overall Progress</h2>
            <p className="text-sm text-slate-400 mt-1">
              {overallMastery >= 71 ? "Great progress! Keep it up!" :
               overallMastery >= 41 ? "Good progress. Focus on weak areas." :
               "Keep practicing! Every exercise helps."}
            </p>
            <div className="mt-3 flex gap-4 text-xs">
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-red-500" /> Beginner (0-40%)</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-yellow-500" /> Learning (41-70%)</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-green-500" /> Proficient (71-90%)</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-blue-500" /> Mastered (91-100%)</span>
            </div>
          </div>
        </div>

        {/* Modules grid */}
        <h2 className="text-lg font-semibold text-white mb-4">Python Modules</h2>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {MODULES.map((mod) => (
            <ModuleCard key={mod.name} {...mod} />
          ))}
        </div>

        {/* Recent topic progress */}
        <h2 className="text-lg font-semibold text-white mb-4">Recent Topic Activity</h2>
        <div className="grid grid-cols-2 gap-4">
          {RECENT_TOPICS.map((topic) => (
            <ProgressCard key={topic.topic_id} topic={topic} />
          ))}
        </div>
      </div>
    </Layout>
  );
}

function StatCard({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 flex items-center gap-3">
      <div className="p-2 bg-slate-700 rounded-lg">{icon}</div>
      <div>
        <p className="text-xs text-slate-400">{label}</p>
        <p className="text-lg font-bold text-white">{value}</p>
      </div>
    </div>
  );
}
