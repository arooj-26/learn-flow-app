"""Concepts Agent - Explains Python topics with examples.

Topics: Variables, Loops, Lists, Dicts, Functions, OOP, Files, Errors, Libraries
Adapts explanation depth to the student's mastery level.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from src.api.shared.schemas import ConceptRequest, ConceptResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("concepts-agent")

# Topic knowledge base - keyed by topic keyword
TOPIC_EXPLANATIONS: dict[str, dict[str, list]] = {
    "variables": {
        "beginner": {
            "explanation": """# Variables & Types in Python

A **variable** is like a labeled box that stores data.

```python
name = "Alice"    # str - text
age = 15          # int - whole number
grade = 9.5       # float - decimal number
is_student = True # bool - True/False
```

**Rules for variable names:**
- Start with a letter or underscore
- Can contain letters, numbers, underscores
- Case-sensitive (`name` != `Name`)
- No spaces (use `snake_case`)
""",
            "examples": [
                'x = 10\nprint(x)       # 10\nprint(type(x)) # <class \'int\'>',
                'name = "Python"\nprint(len(name))  # 6',
            ],
        },
        "intermediate": {
            "explanation": """# Variables - Deeper Dive

**Type system:** Python is dynamically typed - variables can change type.

```python
x = 10       # int
x = "hello"  # now str - no error!
```

**Multiple assignment:**
```python
a, b, c = 1, 2, 3
x = y = z = 0
a, b = b, a  # swap values!
```

**Type hints (PEP 484):**
```python
age: int = 25
name: str = "Alice"
scores: list[int] = [90, 85, 92]
```
""",
            "examples": [
                "a, b = 5, 10\na, b = b, a\nprint(a, b)  # 10 5",
                "x: int = 42\nprint(f'{x} is {type(x).__name__}')  # 42 is int",
            ],
        },
    },
    "loops": {
        "beginner": {
            "explanation": """# Loops in Python

Loops let you repeat code. Python has two types:

## For Loop
Repeats for each item in a sequence:
```python
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

## While Loop
Repeats while a condition is True:
```python
count = 0
while count < 5:
    print(count)
    count += 1
```
""",
            "examples": [
                "for i in range(1, 6):\n    print(f'{i} x 2 = {i*2}')",
                "total = 0\nfor n in [10, 20, 30]:\n    total += n\nprint(total)  # 60",
            ],
        },
        "intermediate": {
            "explanation": """# Advanced Loops

## enumerate() - get index + value
```python
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
```

## zip() - iterate multiple sequences
```python
names = ["Alice", "Bob"]
scores = [95, 87]
for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

## break and continue
```python
for i in range(10):
    if i == 5: break      # stop loop
    if i % 2 == 0: continue  # skip even
    print(i)  # 1, 3
```

## List comprehensions (loop shortcut)
```python
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
```
""",
            "examples": [
                "pairs = [(x,y) for x in range(3) for y in range(3) if x != y]\nprint(pairs)",
                "matrix = [[1,2],[3,4],[5,6]]\nflat = [n for row in matrix for n in row]\nprint(flat)",
            ],
        },
    },
    "lists": {
        "beginner": {
            "explanation": """# Lists in Python

A **list** is an ordered, changeable collection.

```python
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14]
```

## Accessing elements
```python
print(fruits[0])   # "apple" (first)
print(fruits[-1])  # "cherry" (last)
print(fruits[1:3]) # ["banana", "cherry"] (slice)
```

## Common methods
```python
fruits.append("date")     # add to end
fruits.insert(1, "fig")   # insert at index
fruits.remove("banana")   # remove by value
fruits.pop()              # remove last
fruits.sort()             # sort in place
len(fruits)               # length
```
""",
            "examples": [
                'nums = [3, 1, 4, 1, 5]\nnums.sort()\nprint(nums)  # [1, 1, 3, 4, 5]',
                'words = ["hello", "world"]\nwords.append("python")\nprint(len(words))  # 3',
            ],
        },
        "intermediate": {
            "explanation": """# Lists - Advanced

## Slicing
```python
nums = [0,1,2,3,4,5,6,7,8,9]
nums[2:7]     # [2,3,4,5,6]
nums[::2]     # [0,2,4,6,8] (every 2nd)
nums[::-1]    # [9,8,7,...,0] (reverse)
```

## List comprehensions
```python
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
```

## Useful functions
```python
nums = [3, 1, 4, 1, 5]
sum(nums)         # 14
min(nums)         # 1
max(nums)         # 5
sorted(nums)      # [1, 1, 3, 4, 5] (new list)
```
""",
            "examples": [
                "matrix = [[1,2,3],[4,5,6]]\ntransposed = [[row[i] for row in matrix] for i in range(3)]\nprint(transposed)",
                "nums = [1,2,2,3,3,3]\nfrom collections import Counter\nprint(Counter(nums))  # Counter({3:3, 2:2, 1:1})",
            ],
        },
    },
    "dicts": {
        "beginner": {
            "explanation": """# Dictionaries in Python

A **dictionary** stores key-value pairs.

```python
student = {
    "name": "Alice",
    "age": 15,
    "grade": "A"
}
```

## Access values
```python
print(student["name"])        # "Alice"
print(student.get("age"))     # 15
print(student.get("x", 0))   # 0 (default)
```

## Modify
```python
student["age"] = 16           # update
student["school"] = "MIT HS"  # add new
del student["grade"]          # delete
```

## Useful methods
```python
student.keys()    # all keys
student.values()  # all values
student.items()   # key-value pairs
```
""",
            "examples": [
                'scores = {"math": 90, "science": 85}\nfor subject, score in scores.items():\n    print(f"{subject}: {score}")',
                'counts = {}\nfor char in "hello":\n    counts[char] = counts.get(char, 0) + 1\nprint(counts)',
            ],
        },
        "intermediate": {
            "explanation": """# Dictionaries - Advanced

## Dict comprehensions
```python
squares = {x: x**2 for x in range(6)}
# {0:0, 1:1, 2:4, 3:9, 4:16, 5:25}
```

## Nested dictionaries
```python
students = {
    "alice": {"grade": "A", "score": 95},
    "bob": {"grade": "B", "score": 85},
}
print(students["alice"]["score"])  # 95
```

## defaultdict & Counter
```python
from collections import defaultdict, Counter
dd = defaultdict(list)
dd["fruits"].append("apple")

words = "the cat sat on the mat".split()
Counter(words)  # Counter({'the': 2, ...})
```
""",
            "examples": [
                "word_lengths = {w: len(w) for w in 'the quick brown fox'.split()}\nprint(word_lengths)",
                "from collections import defaultdict\ngraph = defaultdict(list)\ngraph['a'].append('b')\nprint(dict(graph))",
            ],
        },
    },
    "functions": {
        "beginner": {
            "explanation": """# Functions in Python

A **function** is a reusable block of code.

```python
def greet(name):
    return f"Hello, {name}!"

result = greet("Alice")
print(result)  # Hello, Alice!
```

## Parameters & Return
```python
def add(a, b):
    return a + b

def is_even(n):
    return n % 2 == 0
```

## Default parameters
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Alice")            # "Hello, Alice!"
greet("Bob", "Hi")        # "Hi, Bob!"
```
""",
            "examples": [
                "def factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n-1)\nprint(factorial(5))  # 120",
                "def max_of_three(a, b, c):\n    return max(a, b, c)\nprint(max_of_three(3, 7, 5))  # 7",
            ],
        },
        "intermediate": {
            "explanation": """# Functions - Advanced

## *args and **kwargs
```python
def func(*args, **kwargs):
    print(args)    # tuple of positional
    print(kwargs)  # dict of keyword

func(1, 2, name="Alice")
# (1, 2)
# {'name': 'Alice'}
```

## Lambda functions
```python
square = lambda x: x ** 2
nums = [3, 1, 4]
sorted(nums, key=lambda x: -x)  # [4, 3, 1]
```

## Decorators
```python
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time()-start:.2f}s")
        return result
    return wrapper

@timer
def slow_func():
    import time; time.sleep(1)
```
""",
            "examples": [
                "add = lambda a, b: a + b\nprint(add(3, 4))  # 7",
                "def apply(func, lst):\n    return [func(x) for x in lst]\nprint(apply(lambda x: x**2, [1,2,3]))  # [1,4,9]",
            ],
        },
    },
    "oop": {
        "beginner": {
            "explanation": """# Object-Oriented Programming (OOP)

**Classes** are blueprints for creating objects.

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        return f"{self.name} says Woof!"

my_dog = Dog("Rex", "Labrador")
print(my_dog.bark())  # Rex says Woof!
```

## Key concepts:
- **Class**: Blueprint (template)
- **Object**: Instance of a class
- **`__init__`**: Constructor (runs when creating object)
- **`self`**: Reference to the current object
- **Method**: Function inside a class
""",
            "examples": [
                'class Circle:\n    def __init__(self, radius):\n        self.radius = radius\n    def area(self):\n        return 3.14159 * self.radius ** 2\nc = Circle(5)\nprint(f"Area: {c.area():.2f}")',
                'class Student:\n    def __init__(self, name):\n        self.name = name\n        self.grades = []\n    def add_grade(self, grade):\n        self.grades.append(grade)\n    def average(self):\n        return sum(self.grades)/len(self.grades) if self.grades else 0\ns = Student("Alice")\ns.add_grade(90)\ns.add_grade(85)\nprint(s.average())',
            ],
        },
        "intermediate": {
            "explanation": """# OOP - Inheritance & Polymorphism

## Inheritance
```python
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"
```

## super()
```python
class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade
```

## Class vs Instance methods
```python
class MyClass:
    count = 0  # class variable

    def __init__(self):
        MyClass.count += 1

    @classmethod
    def get_count(cls):
        return cls.count

    @staticmethod
    def utility():
        return "I don't need self or cls"
```
""",
            "examples": [
                "class Shape:\n    def area(self): raise NotImplementedError\nclass Rect(Shape):\n    def __init__(self,w,h): self.w,self.h=w,h\n    def area(self): return self.w*self.h\nclass Circle(Shape):\n    def __init__(self,r): self.r=r\n    def area(self): return 3.14*self.r**2\nfor s in [Rect(3,4),Circle(5)]:\n    print(f'{type(s).__name__}: {s.area()}')",
            ],
        },
    },
    "files": {
        "beginner": {
            "explanation": """# File Handling in Python

## Reading files
```python
# Best practice: use 'with' statement
with open("data.txt", "r") as f:
    content = f.read()        # entire file as string
    # or
    lines = f.readlines()     # list of lines
    # or
    for line in f:             # line by line
        print(line.strip())
```

## Writing files
```python
with open("output.txt", "w") as f:
    f.write("Hello, World!\\n")
    f.write("Line 2\\n")

# Append mode
with open("log.txt", "a") as f:
    f.write("New entry\\n")
```

**File modes:** `r` (read), `w` (write), `a` (append), `r+` (read+write)
""",
            "examples": [
                "# Count lines in a file\nwith open('example.txt','w') as f:\n    f.write('line1\\nline2\\nline3')\nwith open('example.txt') as f:\n    count = sum(1 for _ in f)\nprint(f'Lines: {count}')",
            ],
        },
    },
    "errors": {
        "beginner": {
            "explanation": """# Error Handling in Python

## try/except
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

## Common exceptions
- `SyntaxError` - Invalid Python code
- `NameError` - Variable not defined
- `TypeError` - Wrong type for operation
- `ValueError` - Right type, wrong value
- `IndexError` - List index out of range
- `KeyError` - Dict key not found
- `FileNotFoundError` - File doesn't exist

## Multiple except blocks
```python
try:
    num = int(input("Enter number: "))
    result = 100 / num
except ValueError:
    print("Not a valid number")
except ZeroDivisionError:
    print("Cannot divide by zero")
```
""",
            "examples": [
                'try:\n    nums = [1,2,3]\n    print(nums[10])\nexcept IndexError as e:\n    print(f"Error: {e}")',
                'def safe_divide(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return None\nprint(safe_divide(10, 0))  # None',
            ],
        },
    },
    "libraries": {
        "beginner": {
            "explanation": """# Python Libraries

## Importing
```python
import math
from random import randint
from datetime import datetime as dt
```

## Standard Library Highlights
```python
import math
math.sqrt(16)     # 4.0
math.pi           # 3.14159...

import random
random.randint(1, 10)    # random int 1-10
random.choice(["a","b"]) # random pick

from datetime import datetime
now = datetime.now()
print(now.strftime("%Y-%m-%d"))

import os
os.getcwd()       # current directory
os.listdir(".")   # list files
```
""",
            "examples": [
                "import math\nprint(f'pi = {math.pi:.4f}')\nprint(f'sqrt(144) = {math.sqrt(144)}')\nprint(f'factorial(5) = {math.factorial(5)}')",
                "import random\nnums = list(range(1, 11))\nrandom.shuffle(nums)\nprint(nums[:5])  # 5 random numbers",
            ],
        },
    },
}


def get_mastery_tier(mastery: int) -> str:
    """Convert mastery percentage to tier name."""
    if mastery <= 40:
        return "beginner"
    return "intermediate"


def find_topic(query: str) -> str | None:
    """Match query to a known topic."""
    query_lower = query.lower()
    for key in TOPIC_EXPLANATIONS:
        if key in query_lower:
            return key

    # Keyword synonyms
    synonyms = {
        "variables": ["variable", "var", "type", "int", "str", "float", "bool", "string"],
        "loops": ["loop", "for", "while", "iterate", "iteration", "range", "repeat"],
        "lists": ["list", "array", "append", "sort", "slice", "index"],
        "dicts": ["dict", "dictionary", "key", "value", "mapping", "hash"],
        "functions": ["function", "def", "return", "parameter", "argument", "lambda", "recursion"],
        "oop": ["class", "object", "inherit", "method", "self", "constructor", "__init__", "polymorphism"],
        "files": ["file", "open", "read", "write", "csv", "json", "io"],
        "errors": ["error", "exception", "try", "except", "raise", "finally", "handling"],
        "libraries": ["library", "import", "module", "package", "pip", "install", "math", "random"],
    }

    for topic, keywords in synonyms.items():
        if any(kw in query_lower for kw in keywords):
            return topic

    return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Concepts Agent starting with %d topics", len(TOPIC_EXPLANATIONS))
    yield
    logger.info("Concepts Agent shutting down")


app = FastAPI(
    title="LearnFlow Concepts Agent",
    version="1.0.0",
    lifespan=lifespan,
)


@app.post("/explain", response_model=ConceptResponse)
async def explain(request: ConceptRequest) -> ConceptResponse:
    """Explain a Python topic adapted to student mastery level."""
    topic_key = find_topic(request.topic)
    if not topic_key or topic_key not in TOPIC_EXPLANATIONS:
        # Fallback generic response
        return ConceptResponse(
            topic=request.topic,
            explanation=f"# {request.topic}\n\nThis topic covers important Python concepts. "
            "Try asking about: variables, loops, lists, dicts, functions, OOP, files, errors, or libraries.",
            examples=[],
            difficulty_adapted="beginner",
        )

    tier = get_mastery_tier(request.mastery_level or 0)
    topic_data = TOPIC_EXPLANATIONS[topic_key]

    # Fall back to beginner if tier not available
    if tier not in topic_data:
        tier = "beginner"

    content = topic_data[tier]

    return ConceptResponse(
        topic=topic_key,
        explanation=content["explanation"],
        examples=content.get("examples", []),
        difficulty_adapted=tier,
    )


class HealthResponse(BaseModel):
    status: str
    agent: str


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy", agent="concepts-agent")


@app.get("/dapr/subscribe")
async def subscribe():
    return []
