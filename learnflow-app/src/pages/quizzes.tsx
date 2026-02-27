import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Layout from '@/components/Layout';
import QuizPanel from '@/components/QuizPanel';
import { ClipboardList, Loader2, ChevronRight, BookOpen, Target } from 'lucide-react';
import { useRequireAuth } from '@/components/withAuth';
import Link from 'next/link';

interface Module {
  id: string;
  name: string;
  topics: Array<{
    id: string;
    name: string;
  }>;
}

export default function QuizzesPage() {
  const router = useRouter();
  const { moduleId } = router.query;
  const { user, isReady } = useRequireAuth();
  const [modules, setModules] = useState<Module[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<{ id: string; name: string } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isReady && user) {
      fetchModules();
    }
  }, [isReady, user]);

  // Auto-scroll to selected module when moduleId changes
  useEffect(() => {
    if (moduleId && modules.length > 0 && !selectedTopic) {
      const element = document.getElementById(`module-${moduleId}`);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  }, [moduleId, modules, selectedTopic]);

  const fetchModules = async () => {
    try {
      const response = await fetch('/api/modules', {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setModules(data.modules || []);
      }
    } catch (error) {
      console.error('Error fetching modules:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!isReady || !user || loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-96">
          <Loader2 className="animate-spin text-blue-400" size={32} />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Target className="text-purple-400" />
            Quiz Center
            {moduleId && modules.find(m => m.id === moduleId) && (
              <span className="text-lg font-normal text-slate-400">
                / {modules.find(m => m.id === moduleId)?.name}
              </span>
            )}
          </h1>
          <p className="text-slate-400 mt-1">
            Test your Python knowledge with 8 questions per topic
          </p>
          {moduleId && (
            <button
              onClick={() => router.push('/quizzes')}
              className="mt-3 text-sm text-purple-400 hover:text-purple-300 flex items-center gap-1 transition"
            >
              <ChevronRight size={14} className="rotate-180" />
              Show All Modules
            </button>
          )}
        </div>

        {!selectedTopic ? (
          <>
            {/* Stats */}
            <div className="grid grid-cols-3 gap-4 mb-8">
              <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
                <div className="text-3xl font-bold text-purple-400">
                  {modules.reduce((acc, m) => acc + (m.topics?.length || 0), 0) * 8}
                </div>
                <div className="text-sm text-slate-400">Total Questions</div>
              </div>
              <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
                <div className="text-3xl font-bold text-blue-400">
                  {modules.reduce((acc, m) => acc + (m.topics?.length || 0), 0)}
                </div>
                <div className="text-sm text-slate-400">Topics with Quizzes</div>
              </div>
              <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
                <div className="text-3xl font-bold text-green-400">{modules.length}</div>
                <div className="text-sm text-slate-400">Modules</div>
              </div>
            </div>

            {/* Module Grid */}
            <div className="space-y-6">
              {modules
                .filter(m => !moduleId || m.id === moduleId)
                .map((module) => (
                <div
                  key={module.id}
                  id={`module-${module.id}`}
                  className={`bg-slate-800 rounded-xl border overflow-hidden transition-all ${
                    moduleId === module.id
                      ? 'border-purple-500 ring-2 ring-purple-500/20'
                      : 'border-slate-700'
                  }`}
                >
                  <div className={`p-4 border-b transition-all ${
                    moduleId === module.id
                      ? 'border-purple-500/30 bg-purple-900/20'
                      : 'border-slate-700 bg-slate-750'
                  }`}>
                    <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                      <BookOpen size={18} className={moduleId === module.id ? 'text-purple-400' : 'text-blue-400'} />
                      {module.name}
                      {moduleId === module.id && (
                        <span className="text-xs px-2 py-0.5 bg-purple-500/30 text-purple-300 rounded-full ml-2">
                          Selected
                        </span>
                      )}
                    </h2>
                  </div>
                  <div className="p-4 grid grid-cols-2 md:grid-cols-3 gap-3">
                    {module.topics?.map((topic) => (
                      <button
                        key={topic.id}
                        onClick={() => setSelectedTopic(topic)}
                        className="p-3 bg-slate-700/50 hover:bg-slate-700 border border-slate-600 hover:border-purple-500 rounded-lg text-left transition group"
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-white group-hover:text-purple-300 transition">
                            {topic.name}
                          </span>
                          <ChevronRight
                            size={16}
                            className="text-slate-500 group-hover:text-purple-400 transition"
                          />
                        </div>
                        <span className="text-xs text-slate-500 mt-1 block">8 questions</span>
                      </button>
                    ))}
                    {(!module.topics || module.topics.length === 0) && (
                      <p className="text-slate-500 text-sm col-span-full">
                        No topics available yet
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {modules.length === 0 && (
              <div className="text-center py-12">
                <Target size={48} className="mx-auto text-slate-600 mb-4" />
                <h3 className="text-lg font-semibold text-white mb-2">No Quizzes Available</h3>
                <p className="text-slate-400 mb-4">Start learning to unlock quizzes!</p>
                <Link
                  href="/dashboard"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition"
                >
                  Go to Dashboard
                  <ChevronRight size={16} />
                </Link>
              </div>
            )}
          </>
        ) : (
          <div>
            <button
              onClick={() => setSelectedTopic(null)}
              className="text-sm text-purple-400 hover:text-purple-300 mb-4 transition flex items-center gap-1"
            >
              <ChevronRight size={16} className="rotate-180" />
              Back to Quiz Center
            </button>
            <QuizPanel topicId={selectedTopic.id} topicName={selectedTopic.name} />
          </div>
        )}
      </div>
    </Layout>
  );
}
