import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '@/components/Layout';
import ModuleCard from '@/components/ModuleCard';
import MasteryBadge from '@/components/MasteryBadge';
import ProgressCard from '@/components/ProgressCard';
import { BarChart3, TrendingUp, BookOpen, Flame, Loader2, AlertCircle, Users, GraduationCap, Activity } from 'lucide-react';
import { useRequireAuth } from '@/components/withAuth';

interface Module {
  id: string;
  name: string;
  description: string;
  icon: string;
  mastery: number;
  topicsCount: number;
  exercisesDone: number;
  quizzesDone: number;
  quizzesTotal: number;
  bestQuizScore: number;
}

interface TopicProgress {
  topic_id: string;
  topic_name: string;
  mastery: number;
  level: 'beginner' | 'learning' | 'proficient' | 'mastered';
  exercises_done: number;
  quiz_score: number;
  code_quality: number;
  streak: number;
}

interface ProgressData {
  modules: Module[];
  recentTopics: TopicProgress[];
  stats: {
    overallMastery: number;
    totalExercises: number;
    currentStreak: number;
    modulesStarted: number;
    totalModules: number;
  };
}

interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: 'student' | 'teacher';
}

interface Student {
  id: string;
  name: string;
  email: string;
  overallMastery: number;
  totalExercises: number;
  topicsStarted: number;
  lastActivity: string | null;
  moduleProgress: { module_name: string; mastery: number; topics_completed: number }[];
}

interface TeacherData {
  students: Student[];
  stats: {
    totalStudents: number;
    avgMastery: number;
    activeToday: number;
  };
}

export default function Dashboard() {
  const router = useRouter();
  const { user, isReady } = useRequireAuth();
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [progressData, setProgressData] = useState<ProgressData | null>(null);
  const [teacherData, setTeacherData] = useState<TeacherData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isReady && user) {
      fetchUserProfile();
    }
  }, [isReady, user]);

  const fetchUserProfile = async () => {
    try {
      const response = await fetch('/api/user/me', { credentials: 'include' });
      if (response.ok) {
        const profile = await response.json();
        setUserProfile(profile);

        // Fetch appropriate data based on role
        if (profile.role === 'teacher') {
          fetchTeacherData();
        } else {
          fetchProgress();
        }
      } else {
        // Default to student view
        fetchProgress();
      }
    } catch (err) {
      console.error('Error fetching profile:', err);
      fetchProgress();
    }
  };

  const fetchTeacherData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch('/api/teacher/students', { credentials: 'include' });

      if (!response.ok) {
        throw new Error('Failed to fetch student data');
      }

      const data = await response.json();
      setTeacherData(data);
    } catch (err) {
      console.error('Error fetching teacher data:', err);
      setError('Failed to load student data');
    } finally {
      setLoading(false);
    }
  };

  const fetchProgress = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch('/api/progress', {
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to fetch progress');
      }

      const data = await response.json();
      setProgressData(data);
    } catch (err) {
      console.error('Error fetching progress:', err);
      setError('Failed to load progress data');
    } finally {
      setLoading(false);
    }
  };

  if (!isReady || !user) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <Loader2 className="animate-spin text-blue-400" size={32} />
      </div>
    );
  }

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <Loader2 className="animate-spin text-blue-400" size={32} />
          <span className="ml-3 text-slate-400">Loading your progress...</span>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="flex flex-col items-center justify-center h-96">
          <AlertCircle className="text-red-400 mb-4" size={48} />
          <p className="text-red-400 mb-4">{error}</p>
          <button
            onClick={userProfile?.role === 'teacher' ? fetchTeacherData : fetchProgress}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </Layout>
    );
  }

  // Teacher Dashboard
  if (userProfile?.role === 'teacher' && teacherData) {
    return (
      <Layout>
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-1">
              <GraduationCap className="text-purple-400" size={28} />
              <h1 className="text-2xl font-bold text-white">Teacher Dashboard</h1>
            </div>
            <p className="text-slate-400">Monitor your students' Python learning progress</p>
          </div>

          {/* Stats row */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-8">
            <StatCard icon={<Users className="text-blue-400" />} label="Total Students" value={teacherData.stats.totalStudents.toString()} />
            <StatCard icon={<BarChart3 className="text-green-400" />} label="Average Mastery" value={`${teacherData.stats.avgMastery}%`} />
            <StatCard icon={<Activity className="text-orange-400" />} label="Active Today" value={teacherData.stats.activeToday.toString()} />
          </div>

          {/* Students Table */}
          <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
            <div className="p-4 border-b border-slate-700">
              <h2 className="text-lg font-semibold text-white">Students Progress</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-700/50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Student</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Email</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-slate-400 uppercase tracking-wider">Mastery</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-slate-400 uppercase tracking-wider">Exercises</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-slate-400 uppercase tracking-wider">Topics</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">Last Active</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700">
                  {teacherData.students.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="px-4 py-8 text-center text-slate-400">
                        No students registered yet
                      </td>
                    </tr>
                  ) : (
                    teacherData.students.map((student) => (
                      <tr key={student.id} className="hover:bg-slate-700/30 transition">
                        <td className="px-4 py-4">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm font-medium">
                              {student.name.charAt(0).toUpperCase()}
                            </div>
                            <span className="text-white font-medium">{student.name}</span>
                          </div>
                        </td>
                        <td className="px-4 py-4 text-slate-400 text-sm">{student.email}</td>
                        <td className="px-4 py-4 text-center">
                          <div className="flex items-center justify-center gap-2">
                            <div className="w-16 h-2 bg-slate-700 rounded-full overflow-hidden">
                              <div
                                className={`h-full rounded-full ${
                                  student.overallMastery >= 71 ? 'bg-green-500' :
                                  student.overallMastery >= 41 ? 'bg-yellow-500' : 'bg-red-500'
                                }`}
                                style={{ width: `${student.overallMastery}%` }}
                              />
                            </div>
                            <span className="text-white text-sm font-medium">{student.overallMastery}%</span>
                          </div>
                        </td>
                        <td className="px-4 py-4 text-center text-slate-300">{student.totalExercises}</td>
                        <td className="px-4 py-4 text-center text-slate-300">{student.topicsStarted}</td>
                        <td className="px-4 py-4 text-slate-400 text-sm">
                          {student.lastActivity
                            ? new Date(student.lastActivity).toLocaleDateString()
                            : 'Never'}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  // Student Dashboard
  if (!progressData) {
    return (
      <Layout>
        <div className="flex flex-col items-center justify-center h-96">
          <AlertCircle className="text-red-400 mb-4" size={48} />
          <p className="text-red-400 mb-4">Failed to load progress</p>
          <button
            onClick={fetchProgress}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </Layout>
    );
  }

  const { modules, recentTopics, stats } = progressData;

  return (
    <Layout>
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white">Welcome, {user.name}!</h1>
          <p className="text-slate-400 mt-1">Track your Python learning progress</p>
        </div>

        {/* Stats row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
          <StatCard icon={<BarChart3 className="text-blue-400" />} label="Overall Mastery" value={`${stats.overallMastery}%`} />
          <StatCard icon={<BookOpen className="text-green-400" />} label="Exercises Done" value={stats.totalExercises.toString()} />
          <StatCard icon={<Flame className="text-orange-400" />} label="Current Streak" value={`${stats.currentStreak} days`} />
          <StatCard icon={<TrendingUp className="text-purple-400" />} label="Modules Started" value={`${stats.modulesStarted}/${stats.totalModules}`} />
        </div>

        {/* Overall mastery ring */}
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-5 mb-8 flex flex-col sm:flex-row items-center sm:items-start gap-5 sm:gap-8">
          <MasteryBadge mastery={stats.overallMastery} size="lg" />
          <div className="text-center sm:text-left">
            <h2 className="text-lg font-semibold text-white">Overall Progress</h2>
            <p className="text-sm text-slate-400 mt-1">
              {stats.overallMastery >= 71 ? "Great progress! Keep it up!" :
               stats.overallMastery >= 41 ? "Good progress. Focus on weak areas." :
               stats.overallMastery > 0 ? "Keep practicing! Every exercise helps." :
               "Start learning! Complete exercises to track your progress."}
            </p>
            <div className="mt-3 flex flex-wrap justify-center sm:justify-start gap-x-4 gap-y-1 text-xs">
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-red-500" /> Beginner (0-40%)</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-yellow-500" /> Learning (41-70%)</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-green-500" /> Proficient (71-90%)</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-blue-500" /> Mastered (91-100%)</span>
            </div>
          </div>
        </div>

        {/* Modules grid */}
        <h2 className="text-lg font-semibold text-white mb-4">Python Modules</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-8">
          {modules.map((mod) => (
            <ModuleCard
              key={mod.id}
              name={mod.name}
              description={mod.description}
              mastery={mod.mastery}
              topicsCount={mod.topicsCount}
              exercisesDone={mod.exercisesDone}
              quizzesDone={mod.quizzesDone}
              quizzesTotal={mod.quizzesTotal}
              bestQuizScore={mod.bestQuizScore}
              onClick={() => router.push(`/modules/${mod.id}`)}
            />
          ))}
        </div>

        {/* Recent topic progress */}
        <h2 className="text-lg font-semibold text-white mb-4">Recent Topic Activity</h2>
        {recentTopics.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {recentTopics.map((topic) => (
              <ProgressCard key={topic.topic_id} topic={topic} />
            ))}
          </div>
        ) : (
          <div className="bg-slate-800 rounded-xl border border-slate-700 p-8 text-center">
            <p className="text-slate-400">No recent activity yet.</p>
            <p className="text-slate-500 text-sm mt-2">Complete exercises to start tracking your progress!</p>
          </div>
        )}
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
