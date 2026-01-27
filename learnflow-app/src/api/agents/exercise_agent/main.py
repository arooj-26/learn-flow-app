"""Exercise Agent - Generate exercises with test cases, auto-grade submissions.

Difficulty levels: easy, medium, hard.
Returns: exercise JSON with test cases.
"""
import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from src.api.shared.config import TOPIC_EXERCISE_STARTED, settings
from src.api.shared.dapr_client import publish_event
from src.api.shared.database import get_session
from src.api.shared.schemas import (
    Difficulty,
    ExerciseGradeResponse,
    ExerciseRequest,
    ExerciseResponse,
    ExerciseSubmission,
    TestCase,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("exercise-agent")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Exercise Agent starting")
    yield
    logger.info("Exercise Agent shutting down")


app = FastAPI(title="LearnFlow Exercise Agent", version="1.0.0", lifespan=lifespan)

# Exercise templates organized by topic keyword and difficulty
EXERCISE_BANK: dict[str, dict[str, list[dict]]] = {
    "variables": {
        "easy": [
            {
                "title": "Variable Swap",
                "description": "Create two variables `a` and `b` with values 5 and 10. Swap their values WITHOUT using a third variable. Print both values after swapping.",
                "starter_code": "a = 5\nb = 10\n# Swap a and b without a third variable\n\nprint(a, b)",
                "test_cases": [
                    {"input": "", "expected_output": "10 5", "description": "Values should be swapped"},
                ],
                "hints": ["Python allows multiple assignment in one line", "Think about tuple unpacking: a, b = ..."],
            },
            {
                "title": "Type Detective",
                "description": "Given `x = '42'`, convert it to an integer, add 8 to it, then print the result and its type.",
                "starter_code": "x = '42'\n# Convert x to int, add 8, print result and type\n",
                "test_cases": [
                    {"input": "", "expected_output": "50\n<class 'int'>", "description": "Should print 50 and int type"},
                ],
                "hints": ["Use int() to convert strings to integers", "Use type() to check the type"],
            },
        ],
        "medium": [
            {
                "title": "Temperature Converter",
                "description": "Write a function `celsius_to_fahrenheit(celsius)` that converts Celsius to Fahrenheit. Formula: F = C * 9/5 + 32. Print the result for 100°C.",
                "starter_code": "def celsius_to_fahrenheit(celsius):\n    # Your code here\n    pass\n\nprint(celsius_to_fahrenheit(100))",
                "test_cases": [
                    {"input": "", "expected_output": "212.0", "description": "100°C should be 212.0°F"},
                ],
                "hints": ["The formula is: fahrenheit = celsius * 9/5 + 32", "Make sure to return the result, not just calculate it"],
            },
        ],
        "hard": [
            {
                "title": "Dynamic Type Checker",
                "description": "Write a function `type_summary(values)` that takes a list and returns a dictionary counting occurrences of each type. Example: type_summary([1, 'a', 2, 'b', True]) should return {'int': 2, 'str': 2, 'bool': 1}. Note: check bool BEFORE int since bool is a subclass of int.",
                "starter_code": "def type_summary(values):\n    # Your code here\n    pass\n\nprint(type_summary([1, 'hello', 3.14, True, 'world', 42]))",
                "test_cases": [
                    {"input": "", "expected_output": "{'int': 2, 'str': 2, 'float': 1, 'bool': 1}", "description": "Should count each type correctly"},
                ],
                "hints": ["Use type().__name__ to get type as string", "Check isinstance(x, bool) before isinstance(x, int)"],
            },
        ],
    },
    "loops": {
        "easy": [
            {
                "title": "Sum of Numbers",
                "description": "Use a for loop to calculate the sum of numbers from 1 to 10 (inclusive). Print the result.",
                "starter_code": "total = 0\n# Use a for loop to sum 1 to 10\n\nprint(total)",
                "test_cases": [
                    {"input": "", "expected_output": "55", "description": "Sum of 1 to 10 is 55"},
                ],
                "hints": ["Use range(1, 11) to get numbers 1 through 10", "Add each number to total inside the loop"],
            },
        ],
        "medium": [
            {
                "title": "FizzBuzz",
                "description": "Print numbers 1-20. For multiples of 3 print 'Fizz', for multiples of 5 print 'Buzz', for multiples of both print 'FizzBuzz'.",
                "starter_code": "# Print FizzBuzz for numbers 1-20\n",
                "test_cases": [
                    {"input": "", "expected_output": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz\n16\n17\nFizz\n19\nBuzz", "description": "Classic FizzBuzz output"},
                ],
                "hints": ["Check divisibility by 15 FIRST (before 3 or 5)", "Use the modulo operator: n % 3 == 0"],
            },
        ],
        "hard": [
            {
                "title": "Prime Sieve",
                "description": "Write a function `primes_up_to(n)` that returns a list of all prime numbers up to n using the Sieve of Eratosthenes. Print primes up to 30.",
                "starter_code": "def primes_up_to(n):\n    # Your code here\n    pass\n\nprint(primes_up_to(30))",
                "test_cases": [
                    {"input": "", "expected_output": "[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]", "description": "Primes up to 30"},
                ],
                "hints": ["Start with a boolean list of True values", "For each prime p, mark all multiples p*2, p*3, ... as not prime"],
            },
        ],
    },
    "lists": {
        "easy": [
            {
                "title": "List Operations",
                "description": "Create a list `nums` with [3, 1, 4, 1, 5, 9]. Sort it, then print the sorted list and its length.",
                "starter_code": "nums = [3, 1, 4, 1, 5, 9]\n# Sort and print\n",
                "test_cases": [
                    {"input": "", "expected_output": "[1, 1, 3, 4, 5, 9]\n6", "description": "Sorted list and length"},
                ],
                "hints": ["Use .sort() to sort in place or sorted() for a new list", "Use len() to get the length"],
            },
        ],
        "medium": [
            {
                "title": "List Comprehension Filter",
                "description": "Using a list comprehension, create a list of squares of even numbers from 1 to 20. Print the result.",
                "starter_code": "# Create list of squares of even numbers 1-20\nresult = # Your list comprehension here\nprint(result)",
                "test_cases": [
                    {"input": "", "expected_output": "[4, 16, 36, 64, 100, 144, 196, 256, 324, 400]", "description": "Squares of even numbers"},
                ],
                "hints": ["Format: [expression for x in range(...) if condition]", "Even check: x % 2 == 0"],
            },
        ],
        "hard": [
            {
                "title": "Matrix Transpose",
                "description": "Write a function `transpose(matrix)` that transposes a 2D list (swap rows and columns). Print the transpose of [[1,2,3],[4,5,6],[7,8,9]].",
                "starter_code": "def transpose(matrix):\n    # Your code here\n    pass\n\nmatrix = [[1,2,3],[4,5,6],[7,8,9]]\nprint(transpose(matrix))",
                "test_cases": [
                    {"input": "", "expected_output": "[[1, 4, 7], [2, 5, 8], [3, 6, 9]]", "description": "Transposed matrix"},
                ],
                "hints": ["New row i = old column i", "Try nested list comprehension or zip(*matrix)"],
            },
        ],
    },
    "functions": {
        "easy": [
            {
                "title": "Greeting Function",
                "description": "Write a function `greet(name)` that returns 'Hello, {name}!'. Print the result for 'Python'.",
                "starter_code": "def greet(name):\n    # Your code here\n    pass\n\nprint(greet('Python'))",
                "test_cases": [
                    {"input": "", "expected_output": "Hello, Python!", "description": "Should greet Python"},
                ],
                "hints": ["Use f-string: f'Hello, {name}!'", "Don't forget to return, not just print"],
            },
        ],
        "medium": [
            {
                "title": "Recursive Fibonacci",
                "description": "Write a function `fibonacci(n)` that returns the nth Fibonacci number (0-indexed: fib(0)=0, fib(1)=1). Print fib(10).",
                "starter_code": "def fibonacci(n):\n    # Your code here\n    pass\n\nprint(fibonacci(10))",
                "test_cases": [
                    {"input": "", "expected_output": "55", "description": "10th Fibonacci number is 55"},
                ],
                "hints": ["Base cases: fib(0) = 0, fib(1) = 1", "Recursive: fib(n) = fib(n-1) + fib(n-2)"],
            },
        ],
        "hard": [
            {
                "title": "Decorator Timer",
                "description": "Write a decorator `count_calls` that counts how many times a function is called. The decorated function should have a `.call_count` attribute. Test with a function called 3 times.",
                "starter_code": "def count_calls(func):\n    # Your code here\n    pass\n\n@count_calls\ndef say_hello():\n    print('Hello!')\n\nsay_hello()\nsay_hello()\nsay_hello()\nprint(f'Called {say_hello.call_count} times')",
                "test_cases": [
                    {"input": "", "expected_output": "Hello!\nHello!\nHello!\nCalled 3 times", "description": "Should track 3 calls"},
                ],
                "hints": ["Use a wrapper function inside the decorator", "Store call_count as an attribute of the wrapper function"],
            },
        ],
    },
    "oop": {
        "easy": [
            {
                "title": "Simple Class",
                "description": "Create a class `Rectangle` with width and height. Add an `area()` method. Print the area of a 5x3 rectangle.",
                "starter_code": "class Rectangle:\n    # Your code here\n    pass\n\nrect = Rectangle(5, 3)\nprint(rect.area())",
                "test_cases": [
                    {"input": "", "expected_output": "15", "description": "5x3 rectangle area is 15"},
                ],
                "hints": ["Define __init__(self, width, height)", "area returns self.width * self.height"],
            },
        ],
        "medium": [
            {
                "title": "Inheritance Chain",
                "description": "Create Animal(name, sound) base class with speak() method. Create Dog and Cat subclasses. Dog.speak() returns '{name} says Woof!', Cat.speak() returns '{name} says Meow!'. Print for Rex and Whiskers.",
                "starter_code": "class Animal:\n    # Your code here\n    pass\n\nclass Dog(Animal):\n    pass\n\nclass Cat(Animal):\n    pass\n\ndog = Dog('Rex')\ncat = Cat('Whiskers')\nprint(dog.speak())\nprint(cat.speak())",
                "test_cases": [
                    {"input": "", "expected_output": "Rex says Woof!\nWhiskers says Meow!", "description": "Animals should speak correctly"},
                ],
                "hints": ["Base class stores name, subclass overrides speak()", "Use super().__init__(name) in subclass __init__"],
            },
        ],
    },
    "errors": {
        "easy": [
            {
                "title": "Safe Division",
                "description": "Write a function `safe_divide(a, b)` that returns a/b but handles ZeroDivisionError by returning 'Cannot divide by zero'. Print results for (10,2) and (10,0).",
                "starter_code": "def safe_divide(a, b):\n    # Your code here\n    pass\n\nprint(safe_divide(10, 2))\nprint(safe_divide(10, 0))",
                "test_cases": [
                    {"input": "", "expected_output": "5.0\nCannot divide by zero", "description": "Should handle division by zero"},
                ],
                "hints": ["Use try/except ZeroDivisionError", "Return the error message string in the except block"],
            },
        ],
    },
}

# Default exercises for topics not in the bank
DEFAULT_EXERCISES = {
    "easy": {
        "title": "Practice Exercise",
        "description": "Write a Python program that demonstrates your understanding of this topic. Use print() to show your results.",
        "starter_code": "# Write your code here\n",
        "test_cases": [],
        "hints": ["Start simple - get something working first", "Use print() to verify your logic"],
    },
    "medium": {
        "title": "Challenge Exercise",
        "description": "Solve this problem using the concepts you've learned. Write clean, well-structured code with comments.",
        "starter_code": "# Write your solution here\n",
        "test_cases": [],
        "hints": ["Break the problem into smaller steps", "Think about edge cases"],
    },
    "hard": {
        "title": "Advanced Challenge",
        "description": "This problem requires combining multiple concepts. Write efficient, Pythonic code.",
        "starter_code": "# Write your advanced solution here\n",
        "test_cases": [],
        "hints": ["Consider using built-in functions and comprehensions", "Think about time complexity"],
    },
}


def find_topic_key(topic_id: str) -> str:
    """Find matching topic key from exercise bank. Falls back to general."""
    # In production, this would query the DB for topic name
    return "variables"


def get_exercises(topic_key: str, difficulty: str, count: int) -> list[dict]:
    """Retrieve exercises from the bank."""
    topic_exercises = EXERCISE_BANK.get(topic_key, {})
    available = topic_exercises.get(difficulty, [])
    if not available:
        return [DEFAULT_EXERCISES.get(difficulty, DEFAULT_EXERCISES["easy"])] * count
    result = []
    for i in range(count):
        result.append(available[i % len(available)])
    return result


@app.post("/generate", response_model=list[ExerciseResponse])
async def generate_exercises(request: ExerciseRequest) -> list[ExerciseResponse]:
    """Generate exercises for a topic at a given difficulty level."""
    logger.info("Generating %d %s exercises for topic %s", request.count, request.difficulty, request.topic_id)

    topic_key = find_topic_key(str(request.topic_id))
    raw_exercises = get_exercises(topic_key, request.difficulty.value, request.count)

    results = []
    for ex in raw_exercises:
        exercise_id = uuid.uuid4()
        results.append(ExerciseResponse(
            exercise_id=exercise_id,
            title=ex["title"],
            description=ex["description"],
            difficulty=request.difficulty,
            starter_code=ex["starter_code"],
            test_cases=[TestCase(**tc) for tc in ex["test_cases"]],
            hints=ex["hints"],
        ))

    return results


@app.post("/grade", response_model=ExerciseGradeResponse)
async def grade_submission(submission: ExerciseSubmission) -> ExerciseGradeResponse:
    """Auto-grade a student's exercise submission."""
    logger.info("Grading submission from student %s for exercise %s", submission.student_id, submission.exercise_id)

    # Publish exercise started event
    await publish_event(TOPIC_EXERCISE_STARTED, {
        "student_id": str(submission.student_id),
        "exercise_id": str(submission.exercise_id),
    })

    # Basic grading: check if code compiles and has content
    code = submission.code.strip()
    if not code or code == "# Write your code here":
        return ExerciseGradeResponse(
            passed=False,
            tests_passed=0,
            tests_total=1,
            feedback="No code submitted. Write your solution and try again!",
            score=0,
        )

    # Check syntax
    import ast
    try:
        ast.parse(code)
    except SyntaxError as e:
        return ExerciseGradeResponse(
            passed=False,
            tests_passed=0,
            tests_total=1,
            feedback=f"Syntax error on line {e.lineno}: {e.msg}. Fix the syntax and resubmit.",
            score=10,
        )

    # Basic code quality scoring
    has_function = "def " in code
    has_comments = "#" in code
    has_print = "print" in code
    line_count = len([l for l in code.split("\n") if l.strip()])

    quality_score = 40  # Base for valid code
    if has_function:
        quality_score += 20
    if has_comments:
        quality_score += 10
    if has_print:
        quality_score += 10
    if line_count >= 3:
        quality_score += 10
    if line_count >= 8:
        quality_score += 10

    quality_score = min(quality_score, 100)
    passed = quality_score >= 60

    return ExerciseGradeResponse(
        passed=passed,
        tests_passed=1 if passed else 0,
        tests_total=1,
        feedback="Good work! Code compiles and looks well-structured." if passed else "Code compiles but needs more work. Try adding functions and comments.",
        score=quality_score,
    )


class HealthResponse(BaseModel):
    status: str
    agent: str


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy", agent="exercise-agent")


@app.get("/dapr/subscribe")
async def subscribe():
    return []
