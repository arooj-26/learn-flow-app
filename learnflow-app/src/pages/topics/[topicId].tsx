/**
 * Topic detail page - shows content, exercises, and quizzes
 */
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import Layout from '@/components/Layout';
import { useRequireAuth } from '@/components/withAuth';
import {
  Loader2, ChevronRight, ChevronLeft, BookOpen, Code, CheckCircle, XCircle,
  Circle, Play, RefreshCw, Lightbulb, Trophy, Target, HelpCircle
} from 'lucide-react';
import Link from 'next/link';
import dynamic from 'next/dynamic';
import QuizPanel from '@/components/QuizPanel';

// Dynamic import for code editor to avoid SSR issues
const MonacoEditor = dynamic(() => import('@monaco-editor/react'), { ssr: false });

interface Exercise {
  id: string;
  title: string;
  description: string;
  difficulty: 'basic' | 'intermediate' | 'advanced';
  starter_code: string;
  expected_output: string;
  test_cases: string;
  hints: string[];
  solution?: string;
  completed: boolean;
}

interface TopicData {
  id: string;
  name: string;
  description: string;
  module_id: string;
  module_name: string;
  content: string;
  exercises: Exercise[];
  mastery: number;
  exercises_done: number;
}

const DIFFICULTY_COLORS = {
  basic: 'bg-green-500/20 text-green-400 border-green-500/30',
  intermediate: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  advanced: 'bg-red-500/20 text-red-400 border-red-500/30',
};

export default function TopicPage() {
  const router = useRouter();
  const { topicId } = router.query;
  const { user, isReady } = useRequireAuth();
  const [topicData, setTopicData] = useState<TopicData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'content' | 'exercises' | 'quiz'>('content');
  const [selectedExercise, setSelectedExercise] = useState<Exercise | null>(null);
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [running, setRunning] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [exerciseResult, setExerciseResult] = useState<'passed' | 'failed' | null>(null);
  const [showSolution, setShowSolution] = useState(false);

  useEffect(() => {
    if (isReady && user && topicId) {
      fetchTopicData();
    }
  }, [isReady, user, topicId]);

  const fetchTopicData = async () => {
    try {
      const response = await fetch(`/api/topics/${topicId}`, {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setTopicData(data);
        if (data.exercises.length > 0) {
          setSelectedExercise(data.exercises[0]);
          setCode(data.exercises[0].starter_code);
        }
      }
    } catch (error) {
      console.error('Error fetching topic:', error);
    } finally {
      setLoading(false);
    }
  };

  const runCode = async () => {
    if (!selectedExercise) return;
    setRunning(true);
    setOutput('');
    setExerciseResult(null);
    setShowSolution(false);

    try {
      const response = await fetch('/api/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          code,
          exerciseId: selectedExercise.id,
          topicId,
          expectedOutput: selectedExercise.expected_output,
        }),
      });

      const result = await response.json();
      setOutput(result.output || result.error || 'No output');

      if (result.success && result.passed) {
        setExerciseResult('passed');
        // Refresh topic data to update progress
        await fetchTopicData();
      } else if (result.success && !result.passed) {
        setExerciseResult('failed');
      } else if (!result.success) {
        setExerciseResult('failed');
      }
    } catch (error) {
      setOutput('Error executing code');
      setExerciseResult('failed');
    } finally {
      setRunning(false);
    }
  };

  const selectExercise = (exercise: Exercise) => {
    setSelectedExercise(exercise);
    setCode(exercise.starter_code);
    setOutput('');
    setShowHint(false);
    setExerciseResult(null);
    setShowSolution(false);
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

  if (!topicData) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-slate-400">Topic not found</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        {/* Breadcrumb */}
        <div className="flex items-center gap-2 text-slate-400 text-sm mb-4">
          <Link href="/dashboard" className="hover:text-white">Dashboard</Link>
          <ChevronRight size={16} />
          <Link href={`/modules/${topicData.module_id}`} className="hover:text-white">
            {topicData.module_name}
          </Link>
          <ChevronRight size={16} />
          <span className="text-white">{topicData.name}</span>
        </div>

        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-white">{topicData.name}</h1>
            <p className="text-slate-400">{topicData.description}</p>
          </div>
          <div className="flex items-center gap-2">
            <div className="bg-slate-800 px-4 py-2 rounded-lg">
              <span className="text-slate-400 text-sm">Mastery:</span>
              <span className="text-white font-semibold ml-2">{topicData.mastery}%</span>
            </div>
            <div className="bg-slate-800 px-4 py-2 rounded-lg">
              <span className="text-slate-400 text-sm">Exercises:</span>
              <span className="text-white font-semibold ml-2">{topicData.exercises_done}/6</span>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setActiveTab('content')}
            className={`px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 ${
              activeTab === 'content'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:text-white'
            }`}
          >
            <BookOpen size={16} />
            Learn
          </button>
          <button
            onClick={() => setActiveTab('exercises')}
            className={`px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 ${
              activeTab === 'exercises'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:text-white'
            }`}
          >
            <Code size={16} />
            Practice ({topicData.exercises_done}/6)
          </button>
          <button
            onClick={() => setActiveTab('quiz')}
            className={`px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 ${
              activeTab === 'quiz'
                ? 'bg-purple-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:text-white'
            }`}
          >
            <HelpCircle size={16} />
            Quiz (8 Questions)
          </button>
        </div>

        {/* Content Tab */}
        {activeTab === 'content' && (
          <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
            <div
              className="prose prose-invert max-w-none"
              dangerouslySetInnerHTML={{ __html: topicData.content }}
            />
            <div className="mt-8 flex justify-between">
              <button
                onClick={() => setActiveTab('quiz')}
                className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium flex items-center gap-2"
              >
                <HelpCircle size={18} />
                Take Quiz
              </button>
              <button
                onClick={() => setActiveTab('exercises')}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium flex items-center gap-2"
              >
                Start Exercises
                <ChevronRight size={18} />
              </button>
            </div>
          </div>
        )}

        {/* Quiz Tab */}
        {activeTab === 'quiz' && topicId && (
          <QuizPanel topicId={topicId as string} topicName={topicData.name} />
        )}

        {/* Exercises Tab */}
        {activeTab === 'exercises' && (
          <div className="grid grid-cols-4 gap-4">
            {/* Exercise list */}
            <div className="col-span-1 space-y-2">
              <h3 className="text-sm font-medium text-slate-400 mb-3">Exercises</h3>
              {topicData.exercises.map((exercise, index) => (
                <button
                  key={exercise.id}
                  onClick={() => selectExercise(exercise)}
                  className={`w-full text-left p-3 rounded-lg border transition-all ${
                    selectedExercise?.id === exercise.id
                      ? 'bg-slate-700 border-blue-500'
                      : 'bg-slate-800 border-slate-700 hover:border-slate-600'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    {exercise.completed ? (
                      <CheckCircle size={16} className="text-green-400" />
                    ) : (
                      <Circle size={16} className="text-slate-500" />
                    )}
                    <span className="text-sm text-white">{index + 1}. {exercise.title}</span>
                  </div>
                  <span className={`text-xs px-2 py-0.5 rounded border mt-1 inline-block ${DIFFICULTY_COLORS[exercise.difficulty]}`}>
                    {exercise.difficulty}
                  </span>
                </button>
              ))}

              {/* Quiz CTA in exercise sidebar */}
              <div className="mt-4 p-3 bg-purple-500/10 border border-purple-500/30 rounded-lg">
                <div className="flex items-center gap-2 text-purple-400 text-sm font-medium mb-2">
                  <Target size={16} />
                  Test Your Knowledge
                </div>
                <p className="text-xs text-slate-400 mb-2">
                  Take the quiz to test what you've learned!
                </p>
                <button
                  onClick={() => setActiveTab('quiz')}
                  className="w-full py-2 bg-purple-600 hover:bg-purple-500 text-white text-sm rounded-lg font-medium transition"
                >
                  Start Quiz
                </button>
              </div>
            </div>

            {/* Code editor */}
            <div className="col-span-3">
              {selectedExercise && (
                <div className="space-y-4">
                  {/* Exercise description */}
                  <div className="bg-slate-800 rounded-xl border border-slate-700 p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold text-white">{selectedExercise.title}</h3>
                      <span className={`text-xs px-2 py-1 rounded border ${DIFFICULTY_COLORS[selectedExercise.difficulty]}`}>
                        {selectedExercise.difficulty}
                      </span>
                    </div>
                    <p className="text-slate-300 text-sm">{selectedExercise.description}</p>
                    {showHint && selectedExercise.hints.length > 0 && (
                      <div className="mt-3 p-3 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
                        <div className="flex items-center gap-2 text-yellow-400 text-sm font-medium mb-1">
                          <Lightbulb size={14} />
                          Hint
                        </div>
                        <p className="text-yellow-200 text-sm">{selectedExercise.hints[0]}</p>
                      </div>
                    )}
                  </div>

                  {/* Editor */}
                  <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
                    <div className="h-64">
                      <MonacoEditor
                        height="100%"
                        language="python"
                        theme="vs-dark"
                        value={code}
                        onChange={(value) => setCode(value || '')}
                        options={{
                          minimap: { enabled: false },
                          fontSize: 14,
                          lineNumbers: 'on',
                          scrollBeyondLastLine: false,
                          automaticLayout: true,
                        }}
                      />
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    <button
                      onClick={runCode}
                      disabled={running}
                      className="px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-slate-600 text-white rounded-lg font-medium flex items-center gap-2"
                    >
                      {running ? (
                        <Loader2 size={16} className="animate-spin" />
                      ) : (
                        <Play size={16} />
                      )}
                      Run Code
                    </button>
                    <button
                      onClick={() => setCode(selectedExercise.starter_code)}
                      className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-medium flex items-center gap-2"
                    >
                      <RefreshCw size={16} />
                      Reset
                    </button>
                    <button
                      onClick={() => setShowHint(!showHint)}
                      className="px-4 py-2 bg-slate-700 hover:bg-slate-600 text-yellow-400 rounded-lg font-medium flex items-center gap-2"
                    >
                      <Lightbulb size={16} />
                      Hint
                    </button>
                  </div>

                  {/* Output */}
                  <div className="bg-slate-900 rounded-xl border border-slate-700 p-4">
                    <h4 className="text-sm font-medium text-slate-400 mb-2">Output</h4>
                    <pre className="text-sm text-slate-300 font-mono whitespace-pre-wrap">
                      {output || 'Run your code to see output...'}
                    </pre>
                  </div>

                  {/* Exercise Result Feedback */}
                  {exerciseResult === 'passed' && (
                    <div className="bg-green-900/20 border border-green-500/30 rounded-xl p-4 flex items-center gap-3">
                      <CheckCircle size={24} className="text-green-400 flex-shrink-0" />
                      <div>
                        <h4 className="text-green-400 font-semibold">Correct!</h4>
                        <p className="text-green-300 text-sm">Great job! Your output matches the expected result.</p>
                      </div>
                    </div>
                  )}

                  {exerciseResult === 'failed' && (
                    <div className="space-y-3">
                      <div className="bg-red-900/20 border border-red-500/30 rounded-xl p-4">
                        <div className="flex items-center gap-3 mb-3">
                          <XCircle size={24} className="text-red-400 flex-shrink-0" />
                          <div>
                            <h4 className="text-red-400 font-semibold">Not Quite Right</h4>
                            <p className="text-red-300 text-sm">Your output doesn't match the expected result. Try again or view the solution.</p>
                          </div>
                        </div>

                        {selectedExercise.expected_output && (
                          <div className="mt-3 bg-slate-800 rounded-lg p-3">
                            <h5 className="text-xs font-medium text-slate-400 mb-1">Expected Output:</h5>
                            <pre className="text-sm text-emerald-400 font-mono whitespace-pre-wrap">{selectedExercise.expected_output}</pre>
                          </div>
                        )}

                        {selectedExercise.solution && !showSolution && (
                          <button
                            onClick={() => setShowSolution(true)}
                            className="mt-3 px-4 py-2 bg-amber-600 hover:bg-amber-500 text-white rounded-lg text-sm font-medium flex items-center gap-2 transition"
                          >
                            <Lightbulb size={16} />
                            Show Solution
                          </button>
                        )}
                      </div>

                      {showSolution && selectedExercise.solution && (
                        <div className="bg-amber-900/20 border border-amber-500/30 rounded-xl p-4">
                          <div className="flex items-center gap-2 mb-3">
                            <Lightbulb size={18} className="text-amber-400" />
                            <h4 className="text-amber-400 font-semibold text-sm">Solution</h4>
                          </div>
                          <pre className="bg-slate-800 rounded-lg p-3 text-sm text-slate-200 font-mono whitespace-pre-wrap overflow-x-auto">{selectedExercise.solution.trim()}</pre>
                          <button
                            onClick={() => {
                              setCode(selectedExercise.solution || '');
                              setShowSolution(false);
                              setExerciseResult(null);
                            }}
                            className="mt-3 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg text-sm font-medium transition"
                          >
                            Copy Solution to Editor
                          </button>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
