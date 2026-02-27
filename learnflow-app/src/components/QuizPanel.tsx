import { useState, useEffect, useCallback } from 'react';
import {
  CheckCircle,
  XCircle,
  ChevronRight,
  ChevronLeft,
  Trophy,
  RefreshCw,
  Lightbulb,
  Award,
  Target,
  Save,
} from 'lucide-react';

interface Quiz {
  id: string;
  question: string;
  options: string[];
  correct: number;
  explanation: string;
  difficulty: 'easy' | 'medium' | 'hard';
}

interface QuizPanelProps {
  topicId: string;
  topicName: string;
}

interface QuizResult {
  quizId: string;
  selectedAnswer: number;
  isCorrect: boolean;
}

interface SavedProgress {
  currentIndex: number;
  results: QuizResult[];
  answers: Record<string, number>; // quizId -> selected answer
  timestamp: number;
}

const PROGRESS_KEY_PREFIX = 'quiz_progress_';

export default function QuizPanel({ topicId, topicName }: QuizPanelProps) {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [results, setResults] = useState<QuizResult[]>([]);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [showSummary, setShowSummary] = useState(false);
  const [progressLoaded, setProgressLoaded] = useState(false);

  // Load quizzes and saved progress
  useEffect(() => {
    fetchQuizzes();
  }, [topicId]);

  // Load saved progress after quizzes are loaded
  useEffect(() => {
    if (quizzes.length > 0 && !progressLoaded) {
      loadProgress();
      setProgressLoaded(true);
    }
  }, [quizzes, progressLoaded]);

  // Save progress whenever it changes
  useEffect(() => {
    if (quizzes.length > 0 && progressLoaded && !showSummary) {
      saveProgress();
    }
  }, [currentIndex, results, answers, progressLoaded, showSummary]);

  const fetchQuizzes = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`/api/quizzes/${topicId}`, {
        credentials: 'include',
      });

      if (response.ok) {
        const data = await response.json();
        setQuizzes(data.quizzes);
      }
    } catch (error) {
      console.error('Failed to fetch quizzes:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getProgressKey = () => `${PROGRESS_KEY_PREFIX}${topicId}`;

  const saveProgress = useCallback(() => {
    try {
      const progress: SavedProgress = {
        currentIndex,
        results,
        answers,
        timestamp: Date.now(),
      };
      localStorage.setItem(getProgressKey(), JSON.stringify(progress));
    } catch (error) {
      console.error('Failed to save progress:', error);
    }
  }, [currentIndex, results, answers, topicId]);

  const loadProgress = () => {
    try {
      const saved = localStorage.getItem(getProgressKey());
      if (saved) {
        const progress: SavedProgress = JSON.parse(saved);

        // Check if progress is less than 24 hours old
        const oneDayAgo = Date.now() - 24 * 60 * 60 * 1000;
        if (progress.timestamp > oneDayAgo) {
          setCurrentIndex(progress.currentIndex);
          setResults(progress.results);
          setAnswers(progress.answers);

          // If we have an answer for the current quiz, show the result
          const currentQuiz = quizzes[progress.currentIndex];
          if (currentQuiz && progress.answers[currentQuiz.id] !== undefined) {
            setSelectedAnswer(progress.answers[currentQuiz.id]);
            setShowResult(true);
          }
        } else {
          // Progress expired, clear it
          localStorage.removeItem(getProgressKey());
        }
      }
    } catch (error) {
      console.error('Failed to load progress:', error);
    }
  };

  const clearProgress = () => {
    try {
      localStorage.removeItem(getProgressKey());
    } catch (error) {
      console.error('Failed to clear progress:', error);
    }
  };

  const currentQuiz = quizzes[currentIndex];

  const handleAnswerSelect = (index: number) => {
    if (showResult) return;
    setSelectedAnswer(index);
  };

  const handleSubmit = () => {
    if (selectedAnswer === null || !currentQuiz) return;

    const isCorrect = selectedAnswer === currentQuiz.correct;

    // Update results
    const newResult: QuizResult = {
      quizId: currentQuiz.id,
      selectedAnswer,
      isCorrect,
    };

    setResults((prev) => {
      // Check if we already have a result for this quiz
      const existingIndex = prev.findIndex((r) => r.quizId === currentQuiz.id);
      if (existingIndex >= 0) {
        const updated = [...prev];
        updated[existingIndex] = newResult;
        return updated;
      }
      return [...prev, newResult];
    });

    // Save the answer
    setAnswers((prev) => ({
      ...prev,
      [currentQuiz.id]: selectedAnswer,
    }));

    setShowResult(true);
  };

  const handleNext = () => {
    if (currentIndex < quizzes.length - 1) {
      const nextIndex = currentIndex + 1;
      setCurrentIndex(nextIndex);

      // Check if we have a saved answer for the next quiz
      const nextQuiz = quizzes[nextIndex];
      if (nextQuiz && answers[nextQuiz.id] !== undefined) {
        setSelectedAnswer(answers[nextQuiz.id]);
        setShowResult(true);
      } else {
        setSelectedAnswer(null);
        setShowResult(false);
      }
    } else {
      setShowSummary(true);
      // Save final results to API
      saveQuizResults();
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      const prevIndex = currentIndex - 1;
      setCurrentIndex(prevIndex);

      // Load the saved answer for the previous quiz
      const prevQuiz = quizzes[prevIndex];
      if (prevQuiz && answers[prevQuiz.id] !== undefined) {
        setSelectedAnswer(answers[prevQuiz.id]);
        setShowResult(true);
      } else {
        setSelectedAnswer(null);
        setShowResult(false);
      }
    }
  };

  const handleRestart = () => {
    setCurrentIndex(0);
    setSelectedAnswer(null);
    setShowResult(false);
    setResults([]);
    setAnswers({});
    setShowSummary(false);
    clearProgress();
  };

  const saveQuizResults = async () => {
    try {
      await fetch('/api/quiz-results', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          topicId,
          results,
          score: getScore(),
          total: results.length,
        }),
      });
      // Clear saved progress after completing
      clearProgress();
    } catch (error) {
      console.error('Failed to save quiz results:', error);
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy':
        return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'medium':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'hard':
        return 'bg-red-500/20 text-red-400 border-red-500/30';
      default:
        return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
    }
  };

  const getScore = () => {
    return results.filter((r) => r.isCorrect).length;
  };

  const getPercentage = () => {
    if (results.length === 0) return 0;
    return Math.round((getScore() / quizzes.length) * 100);
  };

  const getAnsweredCount = () => {
    return Object.keys(answers).length;
  };

  if (isLoading) {
    return (
      <div className="bg-slate-800 rounded-xl border border-slate-700 p-8">
        <div className="flex items-center justify-center">
          <RefreshCw className="animate-spin text-blue-400" size={24} />
          <span className="ml-2 text-slate-400">Loading quizzes...</span>
        </div>
      </div>
    );
  }

  if (quizzes.length === 0) {
    return (
      <div className="bg-slate-800 rounded-xl border border-slate-700 p-8 text-center">
        <Target size={48} className="mx-auto text-slate-600 mb-4" />
        <h3 className="text-lg font-semibold text-white mb-2">No Quizzes Available</h3>
        <p className="text-slate-400">
          Quizzes for this topic are coming soon!
        </p>
      </div>
    );
  }

  if (showSummary) {
    const score = getScore();
    const percentage = Math.round((score / quizzes.length) * 100);
    const isPassing = percentage >= 70;

    return (
      <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
        <div className="p-6 border-b border-slate-700 bg-gradient-to-r from-slate-800 to-slate-750">
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Trophy className={isPassing ? 'text-yellow-400' : 'text-slate-400'} size={20} />
            Quiz Complete!
          </h3>
        </div>

        <div className="p-8 text-center">
          {/* Score Circle */}
          <div className="relative w-32 h-32 mx-auto mb-6">
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="64"
                cy="64"
                r="56"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                className="text-slate-700"
              />
              <circle
                cx="64"
                cy="64"
                r="56"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                strokeDasharray={`${percentage * 3.52} 352`}
                className={isPassing ? 'text-green-500' : 'text-yellow-500'}
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-3xl font-bold text-white">{percentage}%</span>
            </div>
          </div>

          <div className="mb-6">
            <p className="text-2xl font-bold text-white mb-2">
              {score} / {quizzes.length} Correct
            </p>
            <p className={`text-lg ${isPassing ? 'text-green-400' : 'text-yellow-400'}`}>
              {isPassing ? 'Great job! You passed!' : 'Keep practicing!'}
            </p>
          </div>

          {/* Results breakdown */}
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="bg-slate-700/50 rounded-lg p-3">
              <div className="text-2xl font-bold text-green-400">{score}</div>
              <div className="text-xs text-slate-400">Correct</div>
            </div>
            <div className="bg-slate-700/50 rounded-lg p-3">
              <div className="text-2xl font-bold text-red-400">{quizzes.length - score}</div>
              <div className="text-xs text-slate-400">Incorrect</div>
            </div>
            <div className="bg-slate-700/50 rounded-lg p-3">
              <div className="text-2xl font-bold text-blue-400">{quizzes.length}</div>
              <div className="text-xs text-slate-400">Total</div>
            </div>
          </div>

          {/* Achievement Badge */}
          {isPassing && (
            <div className="mb-6 inline-flex items-center gap-2 bg-yellow-500/20 text-yellow-400 px-4 py-2 rounded-full">
              <Award size={20} />
              <span className="font-medium">
                {percentage === 100 ? 'Perfect Score!' : percentage >= 90 ? 'Excellent!' : 'Well Done!'}
              </span>
            </div>
          )}

          <button
            onClick={handleRestart}
            className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium transition flex items-center justify-center gap-2"
          >
            <RefreshCw size={18} />
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-slate-700 bg-gradient-to-r from-slate-800 to-slate-750">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <Target size={20} className="text-blue-400" />
            Quiz: {topicName}
          </h3>
          <div className="flex items-center gap-3">
            <span className={`px-2 py-1 text-xs font-medium rounded border ${getDifficultyColor(currentQuiz.difficulty)}`}>
              {currentQuiz.difficulty}
            </span>
            <span className="text-sm text-slate-400">
              {currentIndex + 1} / {quizzes.length}
            </span>
          </div>
        </div>

        {/* Progress bar */}
        <div className="mt-3 h-1.5 bg-slate-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-300"
            style={{ width: `${((currentIndex + 1) / quizzes.length) * 100}%` }}
          />
        </div>

        {/* Progress indicator */}
        {getAnsweredCount() > 0 && (
          <div className="mt-2 flex items-center gap-2 text-xs text-slate-400">
            <Save size={12} />
            <span>Progress saved ({getAnsweredCount()}/{quizzes.length} answered)</span>
          </div>
        )}
      </div>

      {/* Question */}
      <div className="p-6">
        <p className="text-lg text-white mb-6 leading-relaxed">{currentQuiz.question}</p>

        {/* Options */}
        <div className="space-y-3">
          {currentQuiz.options.map((option, index) => {
            const isSelected = selectedAnswer === index;
            const isCorrect = index === currentQuiz.correct;
            const showCorrectness = showResult;

            let optionClass = 'border-slate-600 hover:border-slate-500 bg-slate-700/50';

            if (isSelected && !showCorrectness) {
              optionClass = 'border-blue-500 bg-blue-500/20';
            } else if (showCorrectness) {
              if (isCorrect) {
                optionClass = 'border-green-500 bg-green-500/20';
              } else if (isSelected && !isCorrect) {
                optionClass = 'border-red-500 bg-red-500/20';
              }
            }

            return (
              <button
                key={index}
                onClick={() => handleAnswerSelect(index)}
                disabled={showResult}
                className={`w-full p-4 rounded-lg border text-left transition-all ${optionClass} ${
                  showResult ? 'cursor-default' : 'cursor-pointer'
                }`}
              >
                <div className="flex items-center gap-3">
                  <span
                    className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                      isSelected ? 'bg-blue-500 text-white' : 'bg-slate-600 text-slate-300'
                    } ${showCorrectness && isCorrect ? 'bg-green-500 text-white' : ''} ${
                      showCorrectness && isSelected && !isCorrect ? 'bg-red-500 text-white' : ''
                    }`}
                  >
                    {showCorrectness && isCorrect ? (
                      <CheckCircle size={16} />
                    ) : showCorrectness && isSelected && !isCorrect ? (
                      <XCircle size={16} />
                    ) : (
                      String.fromCharCode(65 + index)
                    )}
                  </span>
                  <span className="text-white flex-1">{option}</span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Explanation */}
        {showResult && (
          <div
            className={`mt-6 p-4 rounded-lg ${
              selectedAnswer === currentQuiz.correct
                ? 'bg-green-500/10 border border-green-500/30'
                : 'bg-yellow-500/10 border border-yellow-500/30'
            }`}
          >
            <div className="flex items-start gap-2">
              <Lightbulb
                size={20}
                className={selectedAnswer === currentQuiz.correct ? 'text-green-400' : 'text-yellow-400'}
              />
              <div>
                <p
                  className={`font-medium mb-1 ${
                    selectedAnswer === currentQuiz.correct ? 'text-green-400' : 'text-yellow-400'
                  }`}
                >
                  {selectedAnswer === currentQuiz.correct ? 'Correct!' : 'Not quite right'}
                </p>
                <p className="text-slate-300 text-sm">{currentQuiz.explanation}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="p-4 border-t border-slate-700 bg-slate-800/50 flex items-center justify-between">
        <button
          onClick={handlePrevious}
          disabled={currentIndex === 0}
          className="px-4 py-2 text-slate-400 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1 transition"
        >
          <ChevronLeft size={18} />
          Previous
        </button>

        <div className="flex items-center gap-2">
          {!showResult ? (
            <button
              onClick={handleSubmit}
              disabled={selectedAnswer === null}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              Check Answer
            </button>
          ) : (
            <button
              onClick={handleNext}
              className="px-6 py-2 bg-green-600 hover:bg-green-500 text-white rounded-lg font-medium flex items-center gap-1 transition"
            >
              {currentIndex < quizzes.length - 1 ? (
                <>
                  Next
                  <ChevronRight size={18} />
                </>
              ) : (
                <>
                  <Trophy size={18} />
                  See Results
                </>
              )}
            </button>
          )}
        </div>

        <div className="text-sm text-slate-400">
          Score: <span className="text-green-400 font-medium">{getScore()}</span> /{' '}
          <span className="text-slate-300">{getAnsweredCount()}</span>
        </div>
      </div>
    </div>
  );
}
