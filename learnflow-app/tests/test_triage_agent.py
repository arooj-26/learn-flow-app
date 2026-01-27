"""Tests for Triage Agent routing logic."""
import pytest
from src.api.agents.triage_agent.main import classify_query


class TestClassifyQuery:
    def test_error_with_code_routes_to_debug(self):
        assert classify_query("I'm getting an error in my code", has_code=True) == "debug"

    def test_exception_with_code_routes_to_debug(self):
        assert classify_query("There's a traceback exception", has_code=True) == "debug"

    def test_fix_code_routes_to_review(self):
        assert classify_query("Can you fix my code?", has_code=True) == "code_review"

    def test_review_routes_to_review(self):
        assert classify_query("Review this code for PEP 8 style", has_code=True) == "code_review"

    def test_how_does_routes_to_concepts(self):
        assert classify_query("How does a for loop work?", has_code=False) == "concepts"

    def test_explain_routes_to_concepts(self):
        assert classify_query("Explain list comprehensions", has_code=False) == "concepts"

    def test_stuck_without_code_routes_to_concepts(self):
        assert classify_query("I'm stuck and confused", has_code=False) == "concepts"

    def test_stuck_with_code_routes_to_debug(self):
        assert classify_query("I'm stuck on this", has_code=True) == "debug"

    def test_code_only_routes_to_review(self):
        assert classify_query("Here's what I wrote", has_code=True) == "code_review"

    def test_default_routes_to_concepts(self):
        assert classify_query("hello there", has_code=False) == "concepts"
