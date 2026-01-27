"""Tests for Concepts Agent topic matching and explanation."""
import pytest
from src.api.agents.concepts_agent.main import find_topic, get_mastery_tier


class TestFindTopic:
    def test_direct_match(self):
        assert find_topic("variables") == "variables"
        assert find_topic("loops") == "loops"
        assert find_topic("lists") == "lists"

    def test_synonym_match(self):
        assert find_topic("how does a for loop work") == "loops"
        assert find_topic("explain dictionaries") == "dicts"
        assert find_topic("what is a class") == "oop"
        assert find_topic("how to import modules") == "libraries"

    def test_case_insensitive(self):
        assert find_topic("VARIABLES") == "variables"
        assert find_topic("For Loops") == "loops"

    def test_no_match(self):
        assert find_topic("quantum physics") is None

    def test_keyword_match(self):
        assert find_topic("tell me about inheritance") == "oop"
        assert find_topic("how to handle exceptions") == "errors"
        assert find_topic("what is append") == "lists"


class TestMasteryTier:
    def test_beginner(self):
        assert get_mastery_tier(0) == "beginner"
        assert get_mastery_tier(40) == "beginner"

    def test_intermediate(self):
        assert get_mastery_tier(41) == "intermediate"
        assert get_mastery_tier(100) == "intermediate"
