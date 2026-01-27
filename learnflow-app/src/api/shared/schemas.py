"""Shared Pydantic schemas for all agents."""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# Enums
class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ErrorType(str, Enum):
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    LOGIC = "logic"
    TIMEOUT = "timeout"
    MEMORY = "memory"


class MasteryLevel(str, Enum):
    BEGINNER = "beginner"     # 0-40%  Red
    LEARNING = "learning"     # 41-70% Yellow
    PROFICIENT = "proficient" # 71-90% Green
    MASTERED = "mastered"     # 91-100% Blue


# Kafka event schemas
class LearningSubmittedEvent(BaseModel):
    student_id: UUID
    topic_id: UUID
    code: str


class CodeExecutedEvent(BaseModel):
    submission_id: UUID
    success: bool
    error_type: Optional[ErrorType] = None


class ExerciseStartedEvent(BaseModel):
    student_id: UUID
    exercise_id: UUID


class StruggleDetectedEvent(BaseModel):
    student_id: UUID
    topic_id: UUID
    reason: str


# Triage
class TriageRequest(BaseModel):
    student_id: UUID
    message: str
    topic_id: Optional[UUID] = None
    code: Optional[str] = None


class TriageResponse(BaseModel):
    agent: str
    response: dict


# Concepts
class ConceptRequest(BaseModel):
    student_id: UUID
    topic: str
    mastery_level: Optional[int] = 0


class ConceptResponse(BaseModel):
    topic: str
    explanation: str  # Markdown
    examples: list[str]
    difficulty_adapted: str


# Code Review
class CodeReviewRequest(BaseModel):
    student_id: UUID
    topic_id: UUID
    code: str


class CodeReviewResponse(BaseModel):
    score: int = Field(ge=1, le=10)
    correctness: str
    style: str
    efficiency: str
    feedback: list[str]
    suggestions: list[str]


# Debug
class DebugRequest(BaseModel):
    student_id: UUID
    code: str
    error_output: Optional[str] = None
    error_type: Optional[ErrorType] = None


class DebugResponse(BaseModel):
    error_type: ErrorType
    error_explanation: str
    hint_1: str
    hint_2: str
    related_concept: str


# Exercise
class TestCase(BaseModel):
    input: str
    expected_output: str
    description: str


class ExerciseRequest(BaseModel):
    topic_id: UUID
    difficulty: Difficulty = Difficulty.MEDIUM
    count: int = 1


class ExerciseResponse(BaseModel):
    exercise_id: UUID
    title: str
    description: str
    difficulty: Difficulty
    starter_code: str
    test_cases: list[TestCase]
    hints: list[str]


class ExerciseSubmission(BaseModel):
    student_id: UUID
    exercise_id: UUID
    code: str


class ExerciseGradeResponse(BaseModel):
    passed: bool
    tests_passed: int
    tests_total: int
    feedback: str
    score: int = Field(ge=0, le=100)


# Progress
class ProgressRequest(BaseModel):
    student_id: UUID
    topic_id: Optional[UUID] = None


class TopicProgress(BaseModel):
    topic_id: UUID
    topic_name: str
    mastery: int
    level: MasteryLevel
    exercises_done: int
    quiz_score: int
    code_quality: int
    streak: int


class ProgressResponse(BaseModel):
    student_id: UUID
    overall_mastery: int
    topics: list[TopicProgress]
    struggling_topics: list[TopicProgress]


# Quiz
class QuizQuestion(BaseModel):
    id: int
    question: str
    question_type: str  # "multiple_choice" | "code_completion"
    options: Optional[list[str]] = None
    code_template: Optional[str] = None
    correct_answer: str


class QuizSubmission(BaseModel):
    student_id: UUID
    quiz_id: UUID
    answers: dict[str, str]  # question_id -> answer


class QuizResultResponse(BaseModel):
    quiz_id: UUID
    score: int
    total: int
    correct: list[int]
    incorrect: list[int]
    feedback: dict[str, str]


# Chat
class ChatRequest(BaseModel):
    student_id: UUID
    message: str
    topic_id: Optional[UUID] = None
    code: Optional[str] = None


class ChatResponse(BaseModel):
    message: str
    agent_type: str
    suggestions: Optional[list[str]] = None


# Code Execution
class CodeExecutionRequest(BaseModel):
    code: str
    timeout: int = 5
    memory_mb: int = 50


class CodeExecutionResponse(BaseModel):
    stdout: str
    stderr: str
    success: bool
    error_type: Optional[ErrorType] = None
    execution_time_ms: int
