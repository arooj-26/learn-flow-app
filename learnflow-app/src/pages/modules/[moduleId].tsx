/**
 * Module detail page - shows all topics in a module
 */
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import Layout from '@/components/Layout';
import { useRequireAuth } from '@/components/withAuth';
import { Loader2, ChevronRight, BookOpen, CheckCircle, Circle } from 'lucide-react';
import Link from 'next/link';

interface Topic {
  id: string;
  name: string;
  description: string;
  mastery: number;
  exercises_done: number;
  total_exercises: number;
}

interface ModuleData {
  id: string;
  name: string;
  description: string;
  topics: Topic[];
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

export default function ModulePage() {
  const router = useRouter();
  const { moduleId } = router.query;
  const { user, isReady } = useRequireAuth();
  const [moduleData, setModuleData] = useState<ModuleData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isReady && user && moduleId) {
      fetchModuleData();
    }
  }, [isReady, user, moduleId]);

  const fetchModuleData = async () => {
    try {
      const response = await fetch(`/api/modules/${moduleId}`, {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setModuleData(data);
      }
    } catch (error) {
      console.error('Error fetching module:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!isReady || loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <Loader2 className="animate-spin text-blue-400" size={32} />
        </div>
      </Layout>
    );
  }

  if (!moduleData) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-slate-400">Module not found</p>
        </div>
      </Layout>
    );
  }

  const overallProgress = moduleData.topics.length > 0
    ? Math.round(moduleData.topics.reduce((sum, t) => sum + t.mastery, 0) / moduleData.topics.length)
    : 0;

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-2 text-slate-400 text-sm mb-2">
            <Link href="/dashboard" className="hover:text-white">Dashboard</Link>
            <ChevronRight size={16} />
            <span className="text-white">{moduleData.name}</span>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-4xl">{MODULE_ICONS[moduleData.name] || '📚'}</span>
            <div>
              <h1 className="text-2xl font-bold text-white">{moduleData.name}</h1>
              <p className="text-slate-400">{moduleData.description}</p>
            </div>
          </div>
        </div>

        {/* Progress bar */}
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-4 mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-slate-400">Module Progress</span>
            <span className="text-sm font-semibold text-white">{overallProgress}%</span>
          </div>
          <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-green-500 transition-all duration-500"
              style={{ width: `${overallProgress}%` }}
            />
          </div>
        </div>

        {/* Topics list */}
        <h2 className="text-lg font-semibold text-white mb-4">Topics</h2>
        <div className="space-y-3">
          {moduleData.topics.map((topic, index) => (
            <Link
              key={topic.id}
              href={`/topics/${topic.id}`}
              className="block bg-slate-800 hover:bg-slate-750 border border-slate-700 hover:border-slate-600 rounded-xl p-4 transition-all"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-sm font-medium text-white">
                    {index + 1}
                  </div>
                  <div>
                    <h3 className="font-medium text-white">{topic.name}</h3>
                    <p className="text-sm text-slate-400">{topic.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <div className="flex items-center gap-1 text-sm">
                      <BookOpen size={14} className="text-slate-400" />
                      <span className="text-slate-400">{topic.exercises_done}/{topic.total_exercises} exercises</span>
                    </div>
                    <div className="flex items-center gap-1 mt-1">
                      {topic.mastery >= 70 ? (
                        <CheckCircle size={14} className="text-green-400" />
                      ) : (
                        <Circle size={14} className="text-slate-500" />
                      )}
                      <span className={topic.mastery >= 70 ? 'text-green-400 text-sm' : 'text-slate-500 text-sm'}>
                        {topic.mastery}% mastery
                      </span>
                    </div>
                  </div>
                  <ChevronRight className="text-slate-500" size={20} />
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </Layout>
  );
}
