"""Tests for Code Review Agent analysis logic."""
import pytest
from src.api.agents.code_review_agent.main import check_syntax, check_style, check_efficiency, check_correctness


class TestSyntaxCheck:
    def test_valid_code(self):
        ok, msg = check_syntax("x = 1\nprint(x)")
        assert ok is True

    def test_syntax_error(self):
        ok, msg = check_syntax("def foo(\n")
        assert ok is False
        assert "Syntax error" in msg


class TestStyleCheck:
    def test_long_lines(self):
        code = "x = " + "a" * 80
        deductions, issues = check_style(code)
        assert deductions >= 1
        assert any("79 characters" in i for i in issues)

    def test_clean_code(self):
        code = "x = 1\ny = 2\nprint(x + y)\n"
        deductions, issues = check_style(code)
        assert deductions == 0

    def test_tab_indentation(self):
        code = "def foo():\n\treturn 1"
        deductions, issues = check_style(code)
        assert any("tabs" in i.lower() for i in issues)


class TestEfficiencyCheck:
    def test_range_len_detected(self):
        code = "for i in range(len(items)):\n    print(items[i])"
        deductions, suggestions = check_efficiency(code)
        assert any("enumerate" in s for s in suggestions)

    def test_set_membership(self):
        code = "if x in [1, 2, 3]:\n    pass"
        deductions, suggestions = check_efficiency(code)
        assert any("set" in s for s in suggestions)


class TestCorrectnessCheck:
    def test_bare_except(self):
        code = "try:\n    x = 1\nexcept:\n    pass"
        deductions, issues = check_correctness(code)
        assert any("Bare" in i for i in issues)

    def test_mutable_default(self):
        code = "def foo(items=[]):\n    items.append(1)\n    return items"
        deductions, issues = check_correctness(code)
        assert any("mutable default" in i for i in issues)

    def test_clean_code(self):
        code = "def add(a, b):\n    return a + b\n\nresult = add(1, 2)\nprint(result)"
        deductions, issues = check_correctness(code)
        assert deductions == 0
