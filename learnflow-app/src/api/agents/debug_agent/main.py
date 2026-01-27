"""Debug Agent - Parse errors, identify cause (syntax/runtime/logic), provide hints not solutions.

Returns: error_type, error_explanation, hint_1, hint_2, related_concept
"""
import ast
import logging
import re
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from src.api.shared.schemas import DebugRequest, DebugResponse, ErrorType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("debug-agent")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Debug Agent starting")
    yield
    logger.info("Debug Agent shutting down")


app = FastAPI(title="LearnFlow Debug Agent", version="1.0.0", lifespan=lifespan)

# Error pattern database
ERROR_PATTERNS: dict[str, dict] = {
    "SyntaxError": {
        "type": ErrorType.SYNTAX,
        "patterns": {
            r"unexpected EOF": {
                "explanation": "Your code ended unexpectedly. Python expected more code to follow.",
                "hint1": "Check if you're missing a closing bracket, parenthesis, or quote.",
                "hint2": "Make sure all your if/for/while/def/class blocks have a body (even if just 'pass').",
                "concept": "Python Syntax Basics",
            },
            r"invalid syntax": {
                "explanation": "Python encountered something it doesn't understand in your code.",
                "hint1": "Look at the line number mentioned - the error is usually on that line or the line above.",
                "hint2": "Common causes: missing colons after if/for/while/def, misspelled keywords, or wrong operators.",
                "concept": "Python Syntax Rules",
            },
            r"EOL while scanning string": {
                "explanation": "You started a string but didn't close it properly.",
                "hint1": "Make sure every opening quote has a matching closing quote of the same type.",
                "hint2": "For multi-line strings, use triple quotes (\"\"\" or ''').",
                "concept": "Strings",
            },
        },
    },
    "IndentationError": {
        "type": ErrorType.SYNTAX,
        "patterns": {
            r"unexpected indent": {
                "explanation": "A line is indented more than Python expected.",
                "hint1": "Check that this line's indentation matches the block it belongs to.",
                "hint2": "Make sure you're using consistent indentation (all spaces or all tabs, not mixed).",
                "concept": "Python Indentation",
            },
            r"expected an indented block": {
                "explanation": "Python expected indented code after a colon (:) but didn't find any.",
                "hint1": "After if/for/while/def/class statements, the next line must be indented.",
                "hint2": "If you don't want code there yet, use 'pass' as a placeholder.",
                "concept": "Code Blocks",
            },
        },
    },
    "NameError": {
        "type": ErrorType.RUNTIME,
        "patterns": {
            r"name '(\w+)' is not defined": {
                "explanation": "You're trying to use a variable or function that Python doesn't know about.",
                "hint1": "Check spelling - Python is case-sensitive ('Name' and 'name' are different).",
                "hint2": "Make sure you defined/assigned the variable BEFORE using it. Also check if you need to import a module.",
                "concept": "Variables & Scope",
            },
        },
    },
    "TypeError": {
        "type": ErrorType.RUNTIME,
        "patterns": {
            r"unsupported operand type": {
                "explanation": "You're trying to perform an operation between incompatible types.",
                "hint1": "Check the types of your variables using type(). You might need to convert one.",
                "hint2": "Common fix: use int(), str(), or float() to convert types before the operation.",
                "concept": "Type Conversion",
            },
            r"'(\w+)' object is not callable": {
                "explanation": "You're using parentheses () on something that isn't a function.",
                "hint1": "Check if you accidentally used the same name for a variable and a function.",
                "hint2": "Remember: parentheses mean 'call this function'. Square brackets [] are for indexing.",
                "concept": "Functions vs Variables",
            },
            r"takes (\d+) positional argument": {
                "explanation": "You're calling a function with the wrong number of arguments.",
                "hint1": "Check the function definition to see how many parameters it expects.",
                "hint2": "Don't forget that class methods need 'self' as the first parameter.",
                "concept": "Function Parameters",
            },
        },
    },
    "ValueError": {
        "type": ErrorType.RUNTIME,
        "patterns": {
            r"invalid literal for int": {
                "explanation": "You're trying to convert a string to a number, but the string isn't a valid number.",
                "hint1": "Check what the string actually contains before converting. Use print() to inspect.",
                "hint2": "Consider using try/except to handle cases where the input might not be a number.",
                "concept": "Type Conversion & Input Validation",
            },
            r"too many values to unpack": {
                "explanation": "You're trying to assign more values than you have variables (or vice versa).",
                "hint1": "Count the items on both sides of the assignment. They must match.",
                "hint2": "Use *variable to capture extra values: a, *rest = [1, 2, 3, 4]",
                "concept": "Tuple Unpacking",
            },
        },
    },
    "IndexError": {
        "type": ErrorType.RUNTIME,
        "patterns": {
            r"list index out of range": {
                "explanation": "You're trying to access a list position that doesn't exist.",
                "hint1": "Remember: a list of length N has indices 0 to N-1. Use len() to check.",
                "hint2": "Use negative indices carefully: list[-1] is the last element.",
                "concept": "List Indexing",
            },
        },
    },
    "KeyError": {
        "type": ErrorType.RUNTIME,
        "patterns": {
            r"KeyError": {
                "explanation": "You're trying to access a dictionary key that doesn't exist.",
                "hint1": "Use dict.get(key, default) instead of dict[key] to avoid this error.",
                "hint2": "Check available keys with dict.keys() or use 'if key in dict:' before accessing.",
                "concept": "Dictionaries",
            },
        },
    },
    "AttributeError": {
        "type": ErrorType.RUNTIME,
        "patterns": {
            r"has no attribute '(\w+)'": {
                "explanation": "You're trying to use a method or attribute that doesn't exist on this object.",
                "hint1": "Check the spelling of the method name. Use dir(object) to see available attributes.",
                "hint2": "Make sure the variable has the type you think it does. Use type() to check.",
                "concept": "Object Methods",
            },
        },
    },
    "ZeroDivisionError": {
        "type": ErrorType.RUNTIME,
        "patterns": {
            r"division by zero": {
                "explanation": "You're trying to divide a number by zero, which is mathematically undefined.",
                "hint1": "Check the divisor (the number you're dividing BY) - it might be 0.",
                "hint2": "Add a check: 'if divisor != 0:' before dividing, or use try/except.",
                "concept": "Error Handling",
            },
        },
    },
    "RecursionError": {
        "type": ErrorType.RUNTIME,
        "patterns": {
            r"maximum recursion depth": {
                "explanation": "Your function keeps calling itself without stopping - infinite recursion.",
                "hint1": "Check your base case: is there a condition that stops the recursion?",
                "hint2": "Make sure each recursive call moves toward the base case (e.g., n-1 gets closer to 0).",
                "concept": "Recursion",
            },
        },
    },
}

# Logic error patterns (detected from code analysis)
LOGIC_PATTERNS = [
    {
        "pattern": r"if\s+\w+\s*=\s*\w+",
        "explanation": "Using = (assignment) instead of == (comparison) in a condition.",
        "hint1": "In conditions, use == for comparison, not = for assignment.",
        "hint2": "Python will actually raise a SyntaxError for this, but it's a common logic mistake to watch for.",
        "concept": "Comparison Operators",
    },
    {
        "pattern": r"while\s+True\s*:(?!.*break)",
        "explanation": "Infinite loop detected - 'while True' without a visible 'break' statement.",
        "hint1": "Add a 'break' condition inside the loop to stop it at the right time.",
        "hint2": "Consider using a 'while condition:' loop instead of 'while True:' with break.",
        "concept": "While Loops",
    },
    {
        "pattern": r"return\s+.*\n\s+\S",
        "explanation": "Code exists after a return statement - it will never execute.",
        "hint1": "Any code after 'return' in the same block is unreachable.",
        "hint2": "Move the code before the return, or restructure your logic.",
        "concept": "Functions & Return",
    },
]


def detect_error_type(code: str, error_output: str | None) -> dict:
    """Analyze code and error output to identify the error and provide hints."""
    # First try to parse the error output
    if error_output:
        for error_name, error_info in ERROR_PATTERNS.items():
            if error_name in error_output:
                for pattern, response in error_info["patterns"].items():
                    if re.search(pattern, error_output):
                        return {
                            "error_type": error_info["type"],
                            "explanation": response["explanation"],
                            "hint1": response["hint1"],
                            "hint2": response["hint2"],
                            "concept": response["concept"],
                        }
                # Matched error name but not specific pattern - give generic response
                first_response = next(iter(error_info["patterns"].values()))
                return {
                    "error_type": error_info["type"],
                    "explanation": f"A {error_name} occurred in your code.",
                    "hint1": first_response["hint1"],
                    "hint2": "Try reading the error message carefully - it usually tells you the line number.",
                    "concept": first_response["concept"],
                }

    # Try to detect syntax errors by parsing
    try:
        ast.parse(code)
    except SyntaxError as e:
        return {
            "error_type": ErrorType.SYNTAX,
            "explanation": f"Syntax error at line {e.lineno}: {e.msg}",
            "hint1": "Check the line mentioned and the line above it for missing colons, brackets, or quotes.",
            "hint2": "Python's error sometimes points to the line AFTER the actual mistake.",
            "concept": "Python Syntax",
        }

    # Check for logic errors
    for logic_check in LOGIC_PATTERNS:
        if re.search(logic_check["pattern"], code):
            return {
                "error_type": ErrorType.LOGIC,
                "explanation": logic_check["explanation"],
                "hint1": logic_check["hint1"],
                "hint2": logic_check["hint2"],
                "concept": logic_check["concept"],
            }

    # Default - can't identify specific error
    return {
        "error_type": ErrorType.RUNTIME,
        "explanation": "An error occurred in your code. Let's investigate.",
        "hint1": "Add print() statements at key points to trace your code's execution.",
        "hint2": "Check your variable types and values at each step - something might not be what you expect.",
        "concept": "Debugging Techniques",
    }


@app.post("/analyze", response_model=DebugResponse)
async def analyze(request: DebugRequest) -> DebugResponse:
    """Analyze code error and provide debugging hints (not solutions)."""
    logger.info("Debugging code for student %s", request.student_id)

    result = detect_error_type(request.code, request.error_output)

    return DebugResponse(
        error_type=result["error_type"],
        error_explanation=result["explanation"],
        hint_1=result["hint1"],
        hint_2=result["hint2"],
        related_concept=result["concept"],
    )


class HealthResponse(BaseModel):
    status: str
    agent: str


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy", agent="debug-agent")


@app.get("/dapr/subscribe")
async def subscribe():
    return []
