"""Tests for code sandbox execution."""
import pytest
from src.api.sandbox.executor import execute_sandboxed


class TestSandboxExecution:
    def test_simple_print(self):
        result = execute_sandboxed('print("hello")')
        assert result["success"] is True
        assert "hello" in result["stdout"]

    def test_math(self):
        result = execute_sandboxed("print(2 + 3)")
        assert result["success"] is True
        assert "5" in result["stdout"]

    def test_syntax_error(self):
        result = execute_sandboxed("def foo(")
        assert result["success"] is False
        assert result["error_type"] == "syntax"

    def test_runtime_error(self):
        result = execute_sandboxed("print(1/0)")
        assert result["success"] is False
        assert result["error_type"] == "runtime"
        assert "ZeroDivisionError" in result["stderr"]

    def test_multiline(self):
        code = "for i in range(3):\n    print(i)"
        result = execute_sandboxed(code)
        assert result["success"] is True
        assert "0" in result["stdout"]
        assert "2" in result["stdout"]

    def test_function_definition(self):
        code = "def add(a, b):\n    return a + b\nprint(add(3, 4))"
        result = execute_sandboxed(code)
        assert result["success"] is True
        assert "7" in result["stdout"]

    def test_execution_time_reported(self):
        result = execute_sandboxed("x = 1")
        assert "execution_time_ms" in result
        assert isinstance(result["execution_time_ms"], int)
