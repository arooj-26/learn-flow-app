import { useState } from 'react';
import Layout from '@/components/Layout';
import QuizPanel from '@/components/QuizPanel';
import { ClipboardList } from 'lucide-react';

const DEMO_STUDENT_ID = '00000000-0000-0000-0000-000000000001';

const MODULES = [
  { key: 'basics', label: 'Basics' },
  { key: 'control-flow', label: 'Control Flow' },
  { key: 'data-structures', label: 'Data Structures' },
  { key: 'functions', label: 'Functions' },
  { key: 'oop', label: 'OOP' },
];

export default function QuizzesPage() {
  const [selectedModule, setSelectedModule] = useState<string | null>(null);
  const [scores, setScores] = useState<Record<string, { score: number; total: number }>>({});

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <ClipboardList className="text-blue-400" />
            Quizzes
          </h1>
          <p className="text-slate-400 mt-1">Test your knowledge with multiple choice and code completion questions</p>
        </div>

        {!selectedModule ? (
          <div className="grid grid-cols-2 gap-4">
            {MODULES.map((mod) => {
              const result = scores[mod.key];
              return (
                <button
                  key={mod.key}
                  onClick={() => setSelectedModule(mod.key)}
                  className="bg-slate-800 border border-slate-700 rounded-xl p-6 text-left hover:border-blue-500 transition group"
                >
                  <h3 className="font-semibold text-white group-hover:text-blue-300 transition">{mod.label}</h3>
                  <p className="text-sm text-slate-400 mt-1">Quiz on {mod.label.toLowerCase()}</p>
                  {result && (
                    <p className={`text-sm mt-2 font-medium ${
                      result.score / result.total >= 0.7 ? 'text-green-400' : 'text-yellow-400'
                    }`}>
                      Last score: {result.score}/{result.total} ({Math.round(result.score / result.total * 100)}%)
                    </p>
                  )}
                </button>
              );
            })}
          </div>
        ) : (
          <div>
            <button
              onClick={() => setSelectedModule(null)}
              className="text-sm text-blue-400 hover:text-blue-300 mb-4 transition"
            >
              &larr; Back to quizzes
            </button>
            <QuizPanel
              module={selectedModule}
              studentId={DEMO_STUDENT_ID}
              onComplete={(score, total) => {
                setScores((prev) => ({ ...prev, [selectedModule]: { score, total } }));
              }}
            />
          </div>
        )}
      </div>
    </Layout>
  );
}
