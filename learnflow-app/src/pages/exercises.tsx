import { useState } from 'react';
import Layout from '@/components/Layout';
import ExercisePanel from '@/components/ExercisePanel';
import { BookOpen, ChevronRight } from 'lucide-react';
import type { Exercise } from '@/utils/api';

const DEMO_STUDENT_ID = '00000000-0000-0000-0000-000000000001';

// Demo exercises - in production, fetched from exercise-agent
const DEMO_EXERCISES: Record<string, Exercise[]> = {
  basics: [
    {
      exercise_id: 'ex-1', title: 'Variable Swap', description: 'Swap two variables without a third variable.', difficulty: 'easy',
      starter_code: 'a = 5\nb = 10\n# Swap a and b\n\nprint(a, b)',
      test_cases: [{ input: '', expected_output: '10 5', description: 'Values should be swapped' }],
      hints: ['Python allows multiple assignment', 'Try: a, b = b, a'],
    },
    {
      exercise_id: 'ex-2', title: 'Temperature Converter', description: 'Convert Celsius to Fahrenheit. F = C * 9/5 + 32', difficulty: 'medium',
      starter_code: 'def celsius_to_fahrenheit(celsius):\n    # Your code\n    pass\n\nprint(celsius_to_fahrenheit(100))',
      test_cases: [{ input: '', expected_output: '212.0', description: '100C = 212F' }],
      hints: ['Formula: F = C * 9/5 + 32', 'Make sure to return the value'],
    },
  ],
  loops: [
    {
      exercise_id: 'ex-3', title: 'FizzBuzz', description: 'Print FizzBuzz for numbers 1-20.', difficulty: 'medium',
      starter_code: '# FizzBuzz: multiples of 3="Fizz", 5="Buzz", both="FizzBuzz"\n',
      test_cases: [{ input: '', expected_output: '1\n2\nFizz\n4\nBuzz', description: 'FizzBuzz output' }],
      hints: ['Check 15 first, then 3, then 5', 'Use modulo: n % 3 == 0'],
    },
    {
      exercise_id: 'ex-4', title: 'Sum of Numbers', description: 'Sum numbers from 1 to 10 using a loop.', difficulty: 'easy',
      starter_code: 'total = 0\n# Sum 1 to 10\n\nprint(total)',
      test_cases: [{ input: '', expected_output: '55', description: 'Sum is 55' }],
      hints: ['Use range(1, 11)', 'Add each number to total'],
    },
  ],
  functions: [
    {
      exercise_id: 'ex-5', title: 'Recursive Fibonacci', description: 'Write fibonacci(n) returning the nth Fibonacci number.', difficulty: 'hard',
      starter_code: 'def fibonacci(n):\n    # Your code\n    pass\n\nprint(fibonacci(10))',
      test_cases: [{ input: '', expected_output: '55', description: 'fib(10) = 55' }],
      hints: ['Base: fib(0)=0, fib(1)=1', 'Recursive: fib(n) = fib(n-1) + fib(n-2)'],
    },
  ],
};

const TOPICS = [
  { key: 'basics', label: 'Basics' },
  { key: 'loops', label: 'Loops' },
  { key: 'functions', label: 'Functions' },
];

export default function ExercisesPage() {
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);
  const [completedExercises, setCompletedExercises] = useState<Set<string>>(new Set());

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <BookOpen className="text-green-400" />
            Practice Exercises
          </h1>
          <p className="text-slate-400 mt-1">Sharpen your Python skills with guided exercises</p>
        </div>

        {!selectedTopic ? (
          <div className="space-y-3">
            {TOPICS.map((topic) => {
              const exercises = DEMO_EXERCISES[topic.key] || [];
              const completed = exercises.filter((e) => completedExercises.has(e.exercise_id)).length;
              return (
                <button
                  key={topic.key}
                  onClick={() => setSelectedTopic(topic.key)}
                  className="w-full bg-slate-800 border border-slate-700 rounded-xl p-5 flex items-center justify-between hover:border-blue-500 transition group"
                >
                  <div className="text-left">
                    <h3 className="font-semibold text-white group-hover:text-blue-300 transition">{topic.label}</h3>
                    <p className="text-sm text-slate-400 mt-1">{exercises.length} exercises - {completed} completed</p>
                  </div>
                  <ChevronRight className="text-slate-500 group-hover:text-blue-400 transition" />
                </button>
              );
            })}
          </div>
        ) : (
          <div>
            <button
              onClick={() => setSelectedTopic(null)}
              className="text-sm text-blue-400 hover:text-blue-300 mb-4 transition"
            >
              &larr; Back to topics
            </button>
            <div className="space-y-6">
              {(DEMO_EXERCISES[selectedTopic] || []).map((exercise) => (
                <ExercisePanel
                  key={exercise.exercise_id}
                  exercise={exercise}
                  studentId={DEMO_STUDENT_ID}
                  onComplete={(passed, score) => {
                    if (passed) {
                      setCompletedExercises((prev) => new Set([...prev, exercise.exercise_id]));
                    }
                  }}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
