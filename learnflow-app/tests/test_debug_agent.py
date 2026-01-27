"""Tests for Debug Agent error detection."""
import pytest
from src.api.agents.debug_agent.main import detect_error_type


class TestErrorDetection:
    def test_syntax_error_detected(self):
        code = "def foo(\n"
        result = detect_error_type(code, None)
        assert result["error_type"].value == "syntax"

    def test_name_error_from_output(self):
        code = "print(undefined_var)"
        error = "NameError: name 'undefined_var' is not defined"
        result = detect_error_type(code, error)
        assert result["error_type"].value == "runtime"
        assert "variable" in result["explanation"].lower() or "defined" in result["explanation"].lower()

    def test_type_error_from_output(self):
        error = "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
        result = detect_error_type("x = 1 + 'hello'", error)
        assert result["error_type"].value == "runtime"
        assert "type" in result["explanation"].lower()

    def test_index_error(self):
        error = "IndexError: list index out of range"
        result = detect_error_type("x = [1,2]; print(x[5])", error)
        assert result["error_type"].value == "runtime"
        assert "index" in result["explanation"].lower() or "list" in result["explanation"].lower()

    def test_zero_division(self):
        error = "ZeroDivisionError: division by zero"
        result = detect_error_type("print(1/0)", error)
        assert result["error_type"].value == "runtime"
        assert "zero" in result["explanation"].lower()

    def test_hints_provided(self):
        error = "SyntaxError: unexpected EOF while parsing"
        result = detect_error_type("def foo():", error)
        assert result["hint1"]
        assert result["hint2"]
        assert result["concept"]

    def test_unknown_error_fallback(self):
        result = detect_error_type("x = 1", "SomeWeirdError: something happened")
        assert result["hint1"]
        assert result["hint2"]
