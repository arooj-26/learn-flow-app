import { useState } from 'react';
import { CheckCircle, XCircle, ArrowRight, Trophy } from 'lucide-react';
import type { QuizQuestion } from '@/utils/api';
import { useAuth } from '@/contexts/AuthContext';

// Sample quiz data per module
const SAMPLE_QUIZZES: Record<string, QuizQuestion[]> = {
  basics: [
    { id: 1, question: 'What is the output of: print(type(42))?', question_type: 'multiple_choice', options: ["<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'number'>"], correct_answer: "<class 'int'>" },
    { id: 2, question: 'Which is a valid variable name?', question_type: 'multiple_choice', options: ['2name', 'my-var', '_count', 'class'], correct_answer: '_count' },
    { id: 3, question: 'Complete the code to swap a and b:', question_type: 'code_completion', code_template: 'a = 5\nb = 10\n____', correct_answer: 'a, b = b, a' },
  ],
  'control-flow': [
    { id: 1, question: 'What does "break" do in a loop?', question_type: 'multiple_choice', options: ['Skips iteration', 'Exits the loop', 'Restarts the loop', 'Pauses execution'], correct_answer: 'Exits the loop' },
    { id: 2, question: 'What is range(3) equivalent to?', question_type: 'multiple_choice', options: ['[1, 2, 3]', '[0, 1, 2]', '[0, 1, 2, 3]', '[1, 2]'], correct_answer: '[0, 1, 2]' },
    { id: 3, question: 'Complete the loop to print even numbers 0-10:', question_type: 'code_completion', code_template: 'for i in range(____):  \n    if i % 2 == 0:\n        print(i)', correct_answer: '11' },
  ],
  'data-structures': [
    { id: 1, question: 'What is the output of: [1,2,3][1:]?', question_type: 'multiple_choice', options: ['[1, 2]', '[2, 3]', '[1]', '[2]'], correct_answer: '[2, 3]' },
    { id: 2, question: 'Which method adds to end of list?', question_type: 'multiple_choice', options: ['add()', 'append()', 'insert()', 'push()'], correct_answer: 'append()' },
    { id: 3, question: 'Complete: get value with default:', question_type: 'code_completion', code_template: "d = {'a': 1}\nval = d.____('b', 0)", correct_answer: 'get' },
  ],
  functions: [
    { id: 1, question: 'What does a function return if no return statement?', question_type: 'multiple_choice', options: ['0', 'None', 'False', 'Error'], correct_answer: 'None' },
    { id: 2, question: 'What is *args in a function?', question_type: 'multiple_choice', options: ['Keyword arguments', 'Tuple of positional args', 'List of args', 'Required args'], correct_answer: 'Tuple of positional args' },
  ],
  oop: [
    { id: 1, question: 'What is __init__ in a class?', question_type: 'multiple_choice', options: ['Destructor', 'Constructor', 'Static method', 'Iterator'], correct_answer: 'Constructor' },
    { id: 2, question: 'What does "self" refer to?', question_type: 'multiple_choice', options: ['The class', 'The instance', 'The module', 'The parent'], correct_answer: 'The instance' },
  ],
};

interface QuizPanelProps {
  module?: string;
  onComplete?: (score: number, total: number) => void;
}

export default function QuizPanel({ module = 'basics', onComplete }: QuizPanelProps) {
  const { user } = useAuth();
  // studentId available for future API calls if needed
  const studentId = user?.id || '';
  const questions = SAMPLE_QUIZZES[module] || SAMPLE_QUIZZES.basics;
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [showResult, setShowResult] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const question = questions[currentQ];
  const isLast = currentQ === questions.length - 1;
  const selectedAnswer = answers[question.id];

  const handleSelect = (answer: string) => {
    if (submitted) return;
    setAnswers((prev) => ({ ...prev, [question.id]: answer }));
  };

  const handleNext = () => {
    if (isLast) {
      setSubmitted(true);
      setShowResult(true);
      const correct = questions.filter((q) => answers[q.id] === q.correct_answer).length;
      onComplete?.(correct, questions.length);
    } else {
      setCurrentQ((prev) => prev + 1);
    }
  };

  if (showResult) {
    const correct = questions.filter((q) => answers[q.id] === q.correct_answer).length;
    const pct = Math.round((correct / questions.length) * 100);
    return (
      <div className="bg-slate-800 rounded-xl border border-slate-700 p-8 text-center">
        <Trophy size={48} className={`mx-auto mb-4 ${pct >= 70 ? 'text-yellow-400' : 'text-slate-400'}`} />
        <h2 className="text-2xl font-bold text-white mb-2">Quiz Complete!</h2>
        <p className="text-4xl font-bold mb-2">
          <span className={pct >= 70 ? 'text-green-400' : pct >= 50 ? 'text-yellow-400' : 'text-red-400'}>{pct}%</span>
        </p>
        <p className="text-slate-400 mb-6">{correct}/{questions.length} correct</p>
        {/* Show answers review */}
        <div className="text-left space-y-3 max-w-lg mx-auto">
          {questions.map((q) => {
            const isCorrect = answers[q.id] === q.correct_answer;
            return (
              <div key={q.id} className={`p-3 rounded-lg border ${isCorrect ? 'border-green-700 bg-green-900/20' : 'border-red-700 bg-red-900/20'}`}>
                <div className="flex items-start gap-2">
                  {isCorrect ? <CheckCircle size={16} className="text-green-400 mt-0.5" /> : <XCircle size={16} className="text-red-400 mt-0.5" />}
                  <div>
                    <p className="text-sm text-slate-200">{q.question}</p>
                    {!isCorrect && <p className="text-xs text-green-400 mt-1">Correct: {q.correct_answer}</p>}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        <button
          onClick={() => { setCurrentQ(0); setAnswers({}); setShowResult(false); setSubmitted(false); }}
          className="mt-6 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-500 transition"
        >
          Retry Quiz
        </button>
      </div>
    );
  }

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
      {/* Progress */}
      <div className="flex items-center justify-between mb-6">
        <span className="text-xs text-slate-400">Question {currentQ + 1} of {questions.length}</span>
        <div className="flex gap-1">
          {questions.map((_, i) => (
            <div key={i} className={`w-8 h-1.5 rounded-full ${
              i < currentQ ? 'bg-blue-500' : i === currentQ ? 'bg-blue-400' : 'bg-slate-600'
            }`} />
          ))}
        </div>
      </div>

      {/* Question */}
      <h3 className="text-lg font-semibold text-white mb-6">{question.question}</h3>

      {/* Multiple choice */}
      {question.question_type === 'multiple_choice' && question.options && (
        <div className="space-y-3 mb-6">
          {question.options.map((option) => (
            <button
              key={option}
              onClick={() => handleSelect(option)}
              className={`w-full text-left p-4 rounded-lg border text-sm transition ${
                selectedAnswer === option
                  ? 'border-blue-500 bg-blue-900/30 text-blue-300'
                  : 'border-slate-600 bg-slate-750 text-slate-300 hover:border-slate-500'
              }`}
            >
              {option}
            </button>
          ))}
        </div>
      )}

      {/* Code completion */}
      {question.question_type === 'code_completion' && (
        <div className="mb-6">
          <pre className="bg-slate-900 p-4 rounded-lg text-sm text-slate-300 font-mono mb-3">
            {question.code_template}
          </pre>
          <input
            type="text"
            value={selectedAnswer || ''}
            onChange={(e) => handleSelect(e.target.value)}
            placeholder="Type the missing code..."
            className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-sm font-mono text-white focus:outline-none focus:border-blue-500"
          />
        </div>
      )}

      {/* Next button */}
      <button
        onClick={handleNext}
        disabled={!selectedAnswer}
        className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-500 transition disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLast ? 'Submit Quiz' : 'Next'}
        <ArrowRight size={16} />
      </button>
    </div>
  );
}
