# Comments and Code Style in Python

Writing clean, readable, and well-documented code is as important as writing functional code. Python has established conventions (PEP 8) that help maintain consistency across projects and make collaboration easier.

## Comments in Python

Comments are used to explain code, make notes, and temporarily disable code execution:

```python
# Single-line comment
# This is a comment explaining the next line
name = "Alice"

# Multi-line comments using multiple # symbols
# This function calculates the area of a rectangle
# Parameters: width and height
# Returns: area as a float
def calculate_area(width, height):
    return width * height

# Inline comments (use sparingly)
price = 19.99  # Price in USD

# Comments for debugging
# print("Debug: value =", x)  # Temporarily disabled

# TODO comments for future work
# TODO: Add input validation
# FIXME: This breaks when input is negative
# HACK: Temporary workaround for API bug
```

## Docstrings

Docstrings are special comments that document modules, classes, and functions:

```python
def calculate_bmi(weight, height):
    """
    Calculate Body Mass Index (BMI).

    Args:
        weight (float): Weight in kilograms
        height (float): Height in meters

    Returns:
        float: BMI value rounded to 2 decimal places

    Example:
        >>> calculate_bmi(70, 1.75)
        22.86
    """
    bmi = weight / (height ** 2)
    return round(bmi, 2)

# Accessing docstrings
print(calculate_bmi.__doc__)

# One-line docstring for simple functions
def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"

# Module-level docstring (at the top of file)
"""
This module provides utility functions for financial calculations.

Contains functions for interest, tax, and currency conversion.
"""
```

## PEP 8 Naming Conventions

Python has established naming conventions that make code more readable:

| Type | Convention | Example |
|------|------------|---------|
| Variables | lowercase_with_underscores | `user_name`, `total_price` |
| Constants | UPPERCASE_WITH_UNDERSCORES | `MAX_SIZE`, `API_KEY` |
| Functions | lowercase_with_underscores | `calculate_total()`, `get_user()` |
| Classes | CapitalizedWords (PascalCase) | `UserAccount`, `ShoppingCart` |
| Modules | lowercase_with_underscores | `data_utils.py`, `user_auth.py` |
| Private | _leading_underscore | `_internal_method()`, `_cache` |

```python
# Good naming examples
user_age = 25                    # Variable
MAX_CONNECTIONS = 100            # Constant
def calculate_total_price():     # Function
    pass

class UserAccount:               # Class
    def __init__(self):
        self._balance = 0        # Private attribute

# Bad naming examples (avoid these)
x = 25                           # Too vague
UserAge = 25                     # Wrong case for variable
def CalculateTotal():            # Wrong case for function
    pass
class user_account:              # Wrong case for class
    pass
```

## Code Formatting and Layout

Proper formatting improves code readability significantly:

```python
# Indentation: Use 4 spaces (not tabs)
def process_data():
    if True:
        print("Properly indented")
        for i in range(5):
            print(i)

# Line length: Maximum 79 characters
# Good: Breaking long lines
user_message = (
    "This is a very long message that "
    "spans multiple lines for better readability"
)

# Function and method arguments
def create_user(
    username,
    email,
    age,
    is_active=True
):
    pass

# Blank lines
# Two blank lines before top-level functions and classes
# One blank line between methods in a class

class Example:
    def method_one(self):
        pass

    def method_two(self):
        pass


def another_function():
    pass

# Whitespace in expressions
# Good
x = 5
y = x + 1
result = calculate(x, y)

# Bad (too much or too little whitespace)
x=5
y = x+1
result=calculate( x,y )

# Operator spacing
# Good
i = i + 1
submitted += 1
x = x * 2 - 1
hypot2 = x * x + y * y
c = (a + b) * (a - b)

# Bad
i=i+1
submitted +=1
x = x*2 - 1
```

## Import Statements

Organizing imports properly keeps code clean and maintainable:

```python
# Import order (per PEP 8):
# 1. Standard library imports
import os
import sys
from datetime import datetime

# 2. Related third-party imports
import numpy as np
import pandas as pd
from flask import Flask, render_template

# 3. Local application imports
from .utils import helper_function
from .models import User

# Good import practices
import math                    # Good: Import module
from math import sqrt, pi     # Good: Specific imports

# Avoid
from math import *            # Bad: Wildcard imports

# Aliasing for long names
import matplotlib.pyplot as plt
import pandas as pd

# Multiple imports on separate lines
import sys
import os

# Not recommended
import sys, os
```

## Best Practices for Code Style

Following these practices makes your code professional and maintainable:

```python
# 1. Write self-documenting code
# Good: Clear variable names
user_age_in_years = 25
is_email_verified = True

# Bad: Unclear abbreviations
uaiy = 25
iev = True

# 2. Use meaningful function names
# Good
def calculate_compound_interest(principal, rate, time):
    return principal * (1 + rate) ** time

# Bad
def calc(p, r, t):
    return p * (1 + r) ** t

# 3. Keep functions focused (Single Responsibility)
# Good: Each function does one thing
def validate_email(email):
    return "@" in email and "." in email

def send_email(to, subject, body):
    # Send email logic
    pass

# Bad: Function doing too much
def validate_and_send_email(email, subject, body):
    if "@" in email:  # Validation
        pass  # Sending logic
    return True

# 4. Use list comprehensions for simple transformations
# Good
squares = [x ** 2 for x in range(10)]

# Also good for readability when complex
squares = []
for x in range(10):
    squares.append(x ** 2)

# 5. Consistent quote style
name = "Alice"      # Double quotes
message = "She said, 'Hello!'"  # Single quotes inside double
```

## Code Review Checklist

When reviewing your code, check for these elements:

```python
# Checklist example
"""
Code Style Checklist:
✓ Meaningful variable and function names
✓ Consistent naming conventions (PEP 8)
✓ Proper indentation (4 spaces)
✓ Comments explain why, not what
✓ Docstrings for all public functions
✓ Line length under 79 characters
✓ Proper whitespace around operators
✓ Imports organized correctly
✓ No unnecessary comments
✓ Code is DRY (Don't Repeat Yourself)
"""

# Example of well-styled code
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30


def fetch_user_data(user_id, timeout=DEFAULT_TIMEOUT):
    """
    Fetch user data from the API.

    Args:
        user_id (int): The unique user identifier
        timeout (int): Request timeout in seconds

    Returns:
        dict: User data or None if not found

    Raises:
        ConnectionError: If API is unreachable
    """
    for attempt in range(MAX_RETRIES):
        try:
            # API call logic here
            return {"id": user_id, "name": "Alice"}
        except ConnectionError as e:
            if attempt == MAX_RETRIES - 1:
                raise
            continue

    return None
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Add Comments"
    difficulty: basic
    description: "Add a single-line comment above the variable explaining that 'price' stores the product price in USD, then print the price."
    starter_code: |
      price = 29.99
      print(price)

    expected_output: "29.99"
    hints:
      - "Start the comment line with #"
      - "Write the comment above the variable assignment"
    solution: |
      # Price of the product in USD
      price = 29.99
      print(price)

  - title: "Fix Variable Naming"
    difficulty: basic
    description: "Rename the variable 'x' to follow PEP 8 conventions (should be 'user_age'), then print it."
    starter_code: |
      x = 25
      # Rename and print

    expected_output: "25"
    hints:
      - "Use lowercase with underscores for variable names"
      - "The name should describe what it stores"
    solution: |
      user_age = 25
      print(user_age)

  - title: "Add Function Docstring"
    difficulty: intermediate
    description: "Add a docstring to the function that describes what it does, its parameter, and return value. Then call it with 5 and print the result."
    starter_code: |
      def square(n):
          return n ** 2

      # Add docstring above, then call function

    expected_output: "25"
    hints:
      - "Docstring goes right after the def line, enclosed in triple quotes"
      - "Describe what the function does, its parameter, and return value"
    solution: |
      def square(n):
          """
          Calculate the square of a number.

          Args:
              n (int/float): The number to square

          Returns:
              int/float: The square of n
          """
          return n ** 2

      result = square(5)
      print(result)

  - title: "Format Import Statements"
    difficulty: intermediate
    description: "Organize these imports according to PEP 8: separate standard library from third-party, one per line. Then print 'Imports organized'."
    starter_code: |
      import math, os
      from pandas import DataFrame
      import sys
      # Organize imports properly

    expected_output: "Imports organized"
    hints:
      - "Standard library imports (math, os, sys) come first"
      - "Third-party imports (pandas) come after"
      - "Use separate lines for each import"
    solution: |
      import math
      import os
      import sys

      from pandas import DataFrame

      print("Imports organized")

  - title: "Create Well-Named Constants"
    difficulty: advanced
    description: "Create two constants following PEP 8: MAX_USERS (100) and DEFAULT_TIMEOUT (30). Calculate and print their sum."
    starter_code: |
      # Create constants and calculate sum

    expected_output: "130"
    hints:
      - "Constants use UPPERCASE_WITH_UNDERSCORES"
      - "Define them at the top of your code"
      - "Add them together and print"
    solution: |
      MAX_USERS = 100
      DEFAULT_TIMEOUT = 30

      total = MAX_USERS + DEFAULT_TIMEOUT
      print(total)

  - title: "Complete Code Style Refactor"
    difficulty: advanced
    description: "Refactor this code: fix naming (x→user_count, y→total_price), add docstring, add comments, improve spacing. Call the function with 5 and 10.99."
    starter_code: |
      def calc(x,y):
          return x*y
      # Refactor and call

    expected_output: "54.95"
    hints:
      - "Rename parameters to be descriptive"
      - "Add proper spacing around operators"
      - "Add a docstring explaining the function"
      - "Add a comment explaining what the function calculates"
    solution: |
      def calculate_total_price(user_count, price_per_user):
          """
          Calculate total price for multiple users.

          Args:
              user_count (int): Number of users
              price_per_user (float): Price per user

          Returns:
              float: Total price
          """
          # Calculate total by multiplying count and price
          return user_count * price_per_user

      result = calculate_total_price(5, 10.99)
      print(result)
```
<!-- EXERCISE_END -->
