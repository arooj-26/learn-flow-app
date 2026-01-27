"""Tests for Progress Agent mastery calculation and struggle detection."""
import pytest
from src.api.agents.progress_agent.main import calculate_mastery, get_mastery_level
from src.api.shared.schemas import MasteryLevel


class TestMasteryCalculation:
    def test_zero_inputs(self):
        assert calculate_mastery(0, 0, 0, 0) == 0

    def test_max_inputs(self):
        # exercises_done=10 → exercise_score=100
        # quiz=100, quality=100, streak=10→100
        # 0.4*100 + 0.3*100 + 0.2*100 + 0.1*100 = 100
        assert calculate_mastery(10, 100, 100, 10) == 100

    def test_partial_progress(self):
        # exercises_done=5 → score=50
        # quiz=60, quality=40, streak=3 → 30
        # 0.4*50 + 0.3*60 + 0.2*40 + 0.1*30 = 20+18+8+3 = 49
        assert calculate_mastery(5, 60, 40, 3) == 49

    def test_exercises_capped_at_100(self):
        # exercises_done=20 → capped at 100
        result = calculate_mastery(20, 0, 0, 0)
        assert result == 40  # 0.4 * 100

    def test_streak_capped_at_100(self):
        result = calculate_mastery(0, 0, 0, 15)
        assert result == 10  # 0.1 * 100

    def test_result_capped_at_100(self):
        assert calculate_mastery(100, 100, 100, 100) == 100

    def test_formula_accuracy(self):
        # exercises=3→30, quiz=70, quality=50, streak=2→20
        # 0.4*30 + 0.3*70 + 0.2*50 + 0.1*20 = 12+21+10+2 = 45
        assert calculate_mastery(3, 70, 50, 2) == 45


class TestMasteryLevel:
    def test_beginner(self):
        assert get_mastery_level(0) == MasteryLevel.BEGINNER
        assert get_mastery_level(20) == MasteryLevel.BEGINNER
        assert get_mastery_level(40) == MasteryLevel.BEGINNER

    def test_learning(self):
        assert get_mastery_level(41) == MasteryLevel.LEARNING
        assert get_mastery_level(55) == MasteryLevel.LEARNING
        assert get_mastery_level(70) == MasteryLevel.LEARNING

    def test_proficient(self):
        assert get_mastery_level(71) == MasteryLevel.PROFICIENT
        assert get_mastery_level(80) == MasteryLevel.PROFICIENT
        assert get_mastery_level(90) == MasteryLevel.PROFICIENT

    def test_mastered(self):
        assert get_mastery_level(91) == MasteryLevel.MASTERED
        assert get_mastery_level(100) == MasteryLevel.MASTERED
