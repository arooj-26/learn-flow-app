import { useState, useCallback } from 'react';
import dynamic from 'next/dynamic';
import { Play, RotateCcw, Search, Loader2 } from 'lucide-react';
import { executeCode, reviewCode, debugCode } from '@/utils/api';
import { useAuth } from '@/contexts/AuthContext';

const MonacoEditor = dynamic(() => import('@monaco-editor/react'), { ssr: false });

interface CodeEditorProps {
  initialCode?: string;
  topicId?: string;
  onExecutionResult?: (result: { stdout: string; stderr: string; success: boolean }) => void;
}

export default function CodeEditor({ initialCode = '# Write your Python code here\nprint("Hello, LearnFlow!")\n', topicId, onExecutionResult }: CodeEditorProps) {
  const { user } = useAuth();
  const studentId = user?.id || '';
  const [code, setCode] = useState(initialCode);
  const [output, setOutput] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [isReviewing, setIsReviewing] = useState(false);
  const [reviewResult, setReviewResult] = useState<{ score: number; feedback: string[]; suggestions: string[] } | null>(null);
  const [activeTab, setActiveTab] = useState<'output' | 'review' | 'debug'>('output');

  const handleRun = useCallback(async () => {
    setIsRunning(true);
    setActiveTab('output');
    setOutput('Running...\n');
    try {
      const result = await executeCode(code);
      const text = result.success
        ? result.stdout || '(No output)'
        : `Error:\n${result.stderr}`;
      setOutput(text);
      onExecutionResult?.(result);

      // Auto-debug on error
      if (!result.success && result.stderr) {
        try {
          const dbg = await debugCode(studentId, code, result.stderr);
          setActiveTab('debug');
          setOutput(prev => prev + `\n\n--- Debug Help ---\n${dbg.error_explanation}\n\nHint 1: ${dbg.hint_1}\nHint 2: ${dbg.hint_2}\nRelated: ${dbg.related_concept}`);
        } catch { /* debug service unavailable */ }
      }
    } catch (e) {
      setOutput(`Failed to execute: ${e instanceof Error ? e.message : 'Unknown error'}`);
    } finally {
      setIsRunning(false);
    }
  }, [code, studentId, onExecutionResult]);

  const handleReview = useCallback(async () => {
    if (!topicId) return;
    setIsReviewing(true);
    setActiveTab('review');
    try {
      const result = await reviewCode(studentId, topicId, code);
      setReviewResult(result);
    } catch (e) {
      setReviewResult({ score: 0, feedback: ['Review service unavailable'], suggestions: [] });
    } finally {
      setIsReviewing(false);
    }
  }, [code, studentId, topicId]);

  return (
    <div className="flex flex-col h-full bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2 bg-slate-750 border-b border-slate-700">
        <span className="text-sm text-slate-300 font-medium">Python Editor</span>
        <div className="flex gap-2">
          <button
            onClick={() => setCode(initialCode)}
            className="flex items-center gap-1 px-3 py-1.5 text-xs bg-slate-700 text-slate-300 rounded-md hover:bg-slate-600 transition"
          >
            <RotateCcw size={14} /> Reset
          </button>
          {topicId && (
            <button
              onClick={handleReview}
              disabled={isReviewing}
              className="flex items-center gap-1 px-3 py-1.5 text-xs bg-purple-600 text-white rounded-md hover:bg-purple-500 transition disabled:opacity-50"
            >
              {isReviewing ? <Loader2 size={14} className="animate-spin" /> : <Search size={14} />}
              Review
            </button>
          )}
          <button
            onClick={handleRun}
            disabled={isRunning}
            className="flex items-center gap-1 px-4 py-1.5 text-xs bg-green-600 text-white rounded-md hover:bg-green-500 transition disabled:opacity-50"
          >
            {isRunning ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
            Run
          </button>
        </div>
      </div>

      {/* Editor */}
      <div className="flex-1 min-h-[300px]">
        <MonacoEditor
          height="100%"
          language="python"
          theme="vs-dark"
          value={code}
          onChange={(value) => setCode(value || '')}
          options={{
            fontSize: 14,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
            wordWrap: 'on',
            padding: { top: 12 },
          }}
        />
      </div>

      {/* Output Panel */}
      <div className="border-t border-slate-700">
        <div className="flex border-b border-slate-700">
          {(['output', 'review', 'debug'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 text-xs font-medium transition ${
                activeTab === tab
                  ? 'text-blue-400 border-b-2 border-blue-400'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>
        <div className="h-40 overflow-auto p-3">
          {activeTab === 'output' && (
            <pre className="text-sm text-slate-300 font-mono whitespace-pre-wrap">
              {output || 'Click "Run" to execute your code'}
            </pre>
          )}
          {activeTab === 'review' && reviewResult && (
            <div className="text-sm space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-slate-400">Score:</span>
                <span className={`font-bold text-lg ${
                  reviewResult.score >= 8 ? 'text-green-400' :
                  reviewResult.score >= 5 ? 'text-yellow-400' : 'text-red-400'
                }`}>{reviewResult.score}/10</span>
              </div>
              {reviewResult.feedback.map((f, i) => (
                <p key={i} className="text-slate-300">{f}</p>
              ))}
              {reviewResult.suggestions.length > 0 && (
                <div className="mt-2">
                  <p className="text-slate-400 text-xs font-medium">Suggestions:</p>
                  {reviewResult.suggestions.map((s, i) => (
                    <p key={i} className="text-blue-300 text-xs ml-2">- {s}</p>
                  ))}
                </div>
              )}
            </div>
          )}
          {activeTab === 'debug' && (
            <pre className="text-sm text-orange-300 font-mono whitespace-pre-wrap">
              {output || 'Debug info will appear here when errors occur'}
            </pre>
          )}
        </div>
      </div>
    </div>
  );
}
