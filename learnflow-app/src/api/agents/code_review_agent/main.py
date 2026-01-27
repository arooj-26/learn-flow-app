"""Code Review Agent - Analyzes Python code for correctness, PEP 8 style, and efficiency.

Returns: score (1-10), correctness feedback, style feedback, efficiency feedback.
"""
import ast
import logging
import re
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from src.api.shared.schemas import CodeReviewRequest, CodeReviewResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("code-review-agent")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Code Review Agent starting")
    yield
    logger.info("Code Review Agent shutting down")


app = FastAPI(title="LearnFlow Code Review Agent", version="1.0.0", lifespan=lifespan)


# --- Analysis helpers ---

def check_syntax(code: str) -> tuple[bool, str]:
    """Check if code has syntax errors."""
    try:
        ast.parse(code)
        return True, "No syntax errors found."
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"


def check_style(code: str) -> tuple[int, list[str]]:
    """Check PEP 8 style issues. Returns (deductions, issues)."""
    issues: list[str] = []
    deductions = 0
    lines = code.split("\n")

    for i, line in enumerate(lines, 1):
        # Line length
        if len(line) > 79:
            issues.append(f"Line {i}: exceeds 79 characters ({len(line)} chars)")
            deductions += 1

        # Trailing whitespace
        if line != line.rstrip():
            issues.append(f"Line {i}: trailing whitespace")
            deductions += 1

        # Tabs instead of spaces
        if "\t" in line:
            issues.append(f"Line {i}: use spaces instead of tabs")
            deductions += 1

    # Missing blank lines around functions/classes
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("def ") or stripped.startswith("class "):
            if i > 0 and lines[i - 1].strip() != "" and not lines[i - 1].strip().startswith("@"):
                issues.append(f"Line {i+1}: missing blank line before function/class definition")
                deductions += 1

    # Naming conventions
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name) and node.name != "__init__":
                    issues.append(f"Function '{node.name}': use snake_case naming")
                    deductions += 1
            elif isinstance(node, ast.ClassDef):
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    issues.append(f"Class '{node.name}': use PascalCase naming")
                    deductions += 1
    except SyntaxError:
        pass

    return min(deductions, 5), issues[:10]


def check_efficiency(code: str) -> tuple[int, list[str]]:
    """Check for common efficiency issues. Returns (deductions, suggestions)."""
    suggestions: list[str] = []
    deductions = 0

    # Repeated string concatenation in loop
    if re.search(r'for\s+.*:.*\n\s+\w+\s*\+=\s*["\']', code, re.MULTILINE):
        suggestions.append("Avoid string concatenation in loops; use ''.join() or list append instead")
        deductions += 1

    # Using list when set would work for membership tests
    if re.search(r'if\s+\w+\s+in\s+\[', code):
        suggestions.append("Consider using a set instead of a list for membership testing (faster lookup)")
        deductions += 1

    # Nested loops that could use comprehensions
    try:
        tree = ast.parse(code)
        loop_depth = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if isinstance(child, (ast.For, ast.While)) and child is not node:
                        loop_depth += 1
        if loop_depth > 0:
            suggestions.append("Consider list comprehensions or itertools for nested loops")
            deductions += 1
    except SyntaxError:
        pass

    # Using range(len(...))
    if "range(len(" in code:
        suggestions.append("Use enumerate() instead of range(len()) for cleaner iteration")
        deductions += 1

    # Global variables
    if re.search(r'^[a-z_]\w*\s*=', code, re.MULTILINE):
        try:
            tree = ast.parse(code)
            globals_count = sum(1 for node in ast.iter_child_nodes(tree) if isinstance(node, ast.Assign))
            if globals_count > 3:
                suggestions.append("Consider reducing global variables; encapsulate in functions or classes")
                deductions += 1
        except SyntaxError:
            pass

    return min(deductions, 3), suggestions[:5]


def check_correctness(code: str) -> tuple[int, list[str]]:
    """Check for common correctness issues."""
    issues: list[str] = []
    deductions = 0

    syntax_ok, syntax_msg = check_syntax(code)
    if not syntax_ok:
        issues.append(syntax_msg)
        deductions += 3
        return deductions, issues

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return 3, ["Code has syntax errors"]

    # Check for bare except
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append("Bare 'except:' catches all exceptions including SystemExit/KeyboardInterrupt; specify exception types")
            deductions += 1

    # Check for mutable default arguments
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for default in node.args.defaults + node.args.kw_defaults:
                if default and isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    issues.append(f"Function '{node.name}': mutable default argument; use None and set inside function")
                    deductions += 1

    # Check for unused imports
    imports = set()
    used_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.add(alias.asname or alias.name)
        elif isinstance(node, ast.Name):
            used_names.add(node.id)

    unused = imports - used_names
    for name in unused:
        issues.append(f"Import '{name}' appears unused")
        deductions += 1

    return min(deductions, 4), issues[:8]


@app.post("/review", response_model=CodeReviewResponse)
async def review(request: CodeReviewRequest) -> CodeReviewResponse:
    """Analyze submitted code for correctness, style, and efficiency."""
    code = request.code
    logger.info("Reviewing code from student %s (topic %s)", request.student_id, request.topic_id)

    correctness_deductions, correctness_issues = check_correctness(code)
    style_deductions, style_issues = check_style(code)
    efficiency_deductions, efficiency_suggestions = check_efficiency(code)

    total_deductions = correctness_deductions + style_deductions + efficiency_deductions
    score = max(1, 10 - total_deductions)

    correctness_text = "Code looks correct!" if not correctness_issues else "\n".join(f"- {i}" for i in correctness_issues)
    style_text = "Good PEP 8 compliance!" if not style_issues else "\n".join(f"- {i}" for i in style_issues)
    efficiency_text = "No major efficiency concerns." if not efficiency_suggestions else "\n".join(f"- {s}" for s in efficiency_suggestions)

    all_feedback = correctness_issues + style_issues
    all_suggestions = efficiency_suggestions

    logger.info("Review complete: score=%d/10", score)

    return CodeReviewResponse(
        score=score,
        correctness=correctness_text,
        style=style_text,
        efficiency=efficiency_text,
        feedback=all_feedback if all_feedback else ["Code looks good!"],
        suggestions=all_suggestions if all_suggestions else ["No suggestions - well done!"],
    )


class HealthResponse(BaseModel):
    status: str
    agent: str


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy", agent="code-review-agent")


@app.get("/dapr/subscribe")
async def subscribe():
    return []
