import { useState } from 'react';
import dynamic from 'next/dynamic';
import { Play, Lightbulb, CheckCircle, XCircle, Loader2 } from 'lucide-react';
import { gradeExercise, executeCode } from '@/utils/api';
import type { Exercise } from '@/utils/api';
import { useAuth } from '@/contexts/AuthContext';

const MonacoEditor = dynamic(() => import('@monaco-editor/react'), { ssr: false });

interface ExercisePanelProps {
  exercise: Exercise;
  onComplete?: (passed: boolean, score: number) => void;
}

export default function ExercisePanel({ exercise, onComplete }: ExercisePanelProps) {
  const { user } = useAuth();
  const studentId = user?.id || '';
  const [code, setCode] = useState(exercise.starter_code);
  const [output, setOutput] = useState('');
  const [hintsShown, setHintsShown] = useState(0);
  const [grading, setGrading] = useState(false);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<{ passed: boolean; score: number; feedback: string } | null>(null);

  const handleRun = async () => {
    setRunning(true);
    setOutput('Running...');
    try {
      const res = await executeCode(code);
      setOutput(res.success ? (res.stdout || '(No output)') : `Error:\n${res.stderr}`);
    } catch {
      setOutput('Failed to execute code');
    } finally {
      setRunning(false);
    }
  };

  const handleSubmit = async () => {
    setGrading(true);
    try {
      const res = await gradeExercise(studentId, exercise.exercise_id, code);
      setResult({ passed: res.passed, score: res.score, feedback: res.feedback });
      onComplete?.(res.passed, res.score);
    } catch {
      setResult({ passed: false, score: 0, feedback: 'Grading service unavailable' });
    } finally {
      setGrading(false);
    }
  };

  const difficultyColor = {
    easy: 'text-green-400 bg-green-900/30 border-green-700',
    medium: 'text-yellow-400 bg-yellow-900/30 border-yellow-700',
    hard: 'text-red-400 bg-red-900/30 border-red-700',
  }[exercise.difficulty];

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-slate-700">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-semibold text-white">{exercise.title}</h3>
          <span className={`px-2 py-0.5 text-xs rounded-full border ${difficultyColor}`}>
            {exercise.difficulty}
          </span>
        </div>
        <p className="text-sm text-slate-300">{exercise.description}</p>
      </div>

      {/* Editor */}
      <div className="h-64">
        <MonacoEditor
          height="100%"
          language="python"
          theme="vs-dark"
          value={code}
          onChange={(v) => setCode(v || '')}
          options={{ fontSize: 14, minimap: { enabled: false }, scrollBeyondLastLine: false, automaticLayout: true, tabSize: 4 }}
        />
      </div>

      {/* Actions */}
      <div className="p-4 border-t border-slate-700 flex items-center gap-3">
        <button onClick={handleRun} disabled={running} className="flex items-center gap-1 px-4 py-2 text-xs bg-slate-700 text-white rounded-md hover:bg-slate-600 disabled:opacity-50">
          {running ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />} Run
        </button>
        <button onClick={handleSubmit} disabled={grading} className="flex items-center gap-1 px-4 py-2 text-xs bg-green-600 text-white rounded-md hover:bg-green-500 disabled:opacity-50">
          {grading ? <Loader2 size={14} className="animate-spin" /> : <CheckCircle size={14} />} Submit
        </button>
        {exercise.hints.length > 0 && hintsShown < exercise.hints.length && (
          <button
            onClick={() => setHintsShown((p) => p + 1)}
            className="flex items-center gap-1 px-3 py-2 text-xs text-yellow-400 hover:bg-slate-700 rounded-md"
          >
            <Lightbulb size={14} /> Hint ({hintsShown}/{exercise.hints.length})
          </button>
        )}
      </div>

      {/* Hints */}
      {hintsShown > 0 && (
        <div className="px-4 pb-3 space-y-2">
          {exercise.hints.slice(0, hintsShown).map((hint, i) => (
            <div key={i} className="flex items-start gap-2 text-sm text-yellow-300 bg-yellow-900/20 px-3 py-2 rounded-lg">
              <Lightbulb size={14} className="mt-0.5 flex-shrink-0" />
              {hint}
            </div>
          ))}
        </div>
      )}

      {/* Output */}
      {output && (
        <div className="px-4 pb-3">
          <pre className="bg-slate-900 rounded-lg p-3 text-xs text-slate-300 font-mono max-h-32 overflow-auto">{output}</pre>
        </div>
      )}

      {/* Grading result */}
      {result && (
        <div className={`mx-4 mb-4 p-4 rounded-lg border ${result.passed ? 'bg-green-900/20 border-green-700' : 'bg-red-900/20 border-red-700'}`}>
          <div className="flex items-center gap-2 mb-2">
            {result.passed ? <CheckCircle size={20} className="text-green-400" /> : <XCircle size={20} className="text-red-400" />}
            <span className={`font-semibold ${result.passed ? 'text-green-400' : 'text-red-400'}`}>
              {result.passed ? 'Passed!' : 'Not quite...'} ({result.score}%)
            </span>
          </div>
          <p className="text-sm text-slate-300">{result.feedback}</p>
        </div>
      )}
    </div>
  );
}
