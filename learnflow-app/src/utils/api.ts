/** API client for LearnFlow backend services. */

const API_BASE = process.env.API_BASE_URL || 'http://localhost:8000';
const SANDBOX_URL = process.env.SANDBOX_URL || 'http://localhost:8010';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const error = await res.text().catch(() => res.statusText);
    throw new Error(`API Error ${res.status}: ${error}`);
  }
  return res.json();
}

// --- Triage / Chat ---
export async function sendChatMessage(studentId: string, message: string, topicId?: string, code?: string) {
  return request<{ agent: string; response: Record<string, unknown> }>(`${API_BASE}/triage-agent/triage`, {
    method: 'POST',
    body: JSON.stringify({ student_id: studentId, message, topic_id: topicId, code }),
  });
}

// --- Code Execution ---
export async function executeCode(code: string, timeout = 5, memoryMb = 50) {
  return request<{ stdout: string; stderr: string; success: boolean; error_type: string | null; execution_time_ms: number }>(
    `${SANDBOX_URL}/execute`,
    { method: 'POST', body: JSON.stringify({ code, timeout, memory_mb: memoryMb }) }
  );
}

// --- Code Review ---
export async function reviewCode(studentId: string, topicId: string, code: string) {
  return request<{ score: number; correctness: string; style: string; efficiency: string; feedback: string[]; suggestions: string[] }>(
    `${API_BASE}/code-review-agent/review`,
    { method: 'POST', body: JSON.stringify({ student_id: studentId, topic_id: topicId, code }) }
  );
}

// --- Debug ---
export async function debugCode(studentId: string, code: string, errorOutput?: string) {
  return request<{ error_type: string; error_explanation: string; hint_1: string; hint_2: string; related_concept: string }>(
    `${API_BASE}/debug-agent/analyze`,
    { method: 'POST', body: JSON.stringify({ student_id: studentId, code, error_output: errorOutput }) }
  );
}

// --- Exercises ---
export async function getExercises(topicId: string, difficulty = 'medium', count = 3) {
  return request<Exercise[]>(`${API_BASE}/exercise-agent/generate`, {
    method: 'POST',
    body: JSON.stringify({ topic_id: topicId, difficulty, count }),
  });
}

export async function gradeExercise(studentId: string, exerciseId: string, code: string) {
  return request<{ passed: boolean; tests_passed: number; tests_total: number; feedback: string; score: number }>(
    `${API_BASE}/exercise-agent/grade`,
    { method: 'POST', body: JSON.stringify({ student_id: studentId, exercise_id: exerciseId, code }) }
  );
}

// --- Progress ---
export async function getProgress(studentId: string) {
  return request<ProgressData>(`${API_BASE}/progress-agent/calculate`, {
    method: 'POST',
    body: JSON.stringify({ student_id: studentId }),
  });
}

export async function getClassProgress(classId: string) {
  return request<ClassProgressData>(`${API_BASE}/api/classes/${classId}/progress`);
}

// --- Concepts ---
export async function explainConcept(studentId: string, topic: string, masteryLevel = 0) {
  return request<{ topic: string; explanation: string; examples: string[]; difficulty_adapted: string }>(
    `${API_BASE}/concepts-agent/explain`,
    { method: 'POST', body: JSON.stringify({ student_id: studentId, topic, mastery_level: masteryLevel }) }
  );
}

// --- Types ---
export interface Exercise {
  exercise_id: string;
  title: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard';
  starter_code: string;
  test_cases: { input: string; expected_output: string; description: string }[];
  hints: string[];
}

export interface TopicProgress {
  topic_id: string;
  topic_name: string;
  mastery: number;
  level: 'beginner' | 'learning' | 'proficient' | 'mastered';
  exercises_done: number;
  quiz_score: number;
  code_quality: number;
  streak: number;
}

export interface ProgressData {
  student_id: string;
  overall_mastery: number;
  topics: TopicProgress[];
  struggling_topics: TopicProgress[];
}

export interface ClassProgressData {
  class_id: string;
  students: {
    student_id: string;
    name: string;
    overall_mastery: number;
    struggling_topics: string[];
  }[];
}

export interface QuizQuestion {
  id: number;
  question: string;
  question_type: 'multiple_choice' | 'code_completion';
  options?: string[];
  code_template?: string;
  correct_answer: string;
}
