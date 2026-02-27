# Importing Modules

Python's module system is one of its most powerful features, enabling code reusability and organization. Modules are Python files containing functions, classes, and variables that can be imported and used in other programs. Understanding how to properly import and use modules is fundamental to writing clean, maintainable Python code.

## Understanding Import Mechanisms

Python provides several ways to import modules, each suited for different scenarios. The basic `import` statement loads an entire module, making all its contents available through the module's namespace.

```python
# Basic import
import math
print(math.pi)  # 3.141592653589793
print(math.sqrt(16))  # 4.0

# Import with alias
import datetime as dt
now = dt.datetime.now()
print(now.year)

# Import multiple modules
import os, sys, json
print(os.name)  # 'posix' or 'nt'
```

The module search path follows a specific order: first the current directory, then directories in the `PYTHONPATH` environment variable, and finally the standard library directories. You can inspect this path using `sys.path`.

## From Import Statements

The `from` keyword allows you to import specific items from a module, reducing namespace pollution and making code more explicit about what it uses.

```python
# Import specific items
from math import pi, sqrt, pow
print(pi)  # 3.141592653589793
print(sqrt(25))  # 5.0

# Import with aliases
from datetime import datetime as dt, timedelta as td
meeting = dt(2024, 6, 15, 14, 30)
duration = td(hours=2)
end_time = meeting + duration

# Import all (not recommended)
from random import *
print(randint(1, 10))  # Works but pollutes namespace

# Better: explicit imports
from random import randint, choice, shuffle
numbers = [1, 2, 3, 4, 5]
shuffle(numbers)
print(numbers)
```

| Import Style | Use Case | Namespace Impact |
|--------------|----------|------------------|
| `import module` | Full module access | Clean, prefixed |
| `from module import item` | Specific items | Direct access |
| `import module as alias` | Shorter names | Custom prefix |
| `from module import *` | Avoid | Pollutes namespace |

## Creating and Importing Custom Modules

Creating your own modules is as simple as writing a Python file. Any `.py` file can be imported as a module by other Python scripts in the same directory or in the Python path.

```python
# File: mymath.py
"""Custom math utilities module."""

PI = 3.14159

def circle_area(radius):
    """Calculate the area of a circle."""
    return PI * radius ** 2

def circle_circumference(radius):
    """Calculate the circumference of a circle."""
    return 2 * PI * radius

class Calculator:
    """Simple calculator class."""

    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

# File: main.py
import mymath
from mymath import circle_area, Calculator

# Using the module
area = circle_area(5)
print(f"Area: {area}")

calc = Calculator()
result = calc.multiply(4, 7)
print(f"Result: {result}")

# Access module-level constant
print(f"PI value: {mymath.PI}")
```

## Advanced Import Techniques

Python offers advanced import features for more complex scenarios, including conditional imports, dynamic imports, and relative imports for packages.

```python
# Conditional imports for compatibility
try:
    import ujson as json  # Faster JSON library
except ImportError:
    import json  # Fallback to standard library

# Dynamic imports with importlib
import importlib

module_name = "math"
math_module = importlib.import_module(module_name)
print(math_module.sqrt(16))  # 4.0

# Lazy imports (only when needed)
def process_data():
    import pandas as pd  # Only imported if function is called
    df = pd.DataFrame({'A': [1, 2, 3]})
    return df

# Relative imports (in packages)
# From within a package:
# from . import sibling_module
# from .. import parent_module
# from .subpackage import module

# Checking if module is main script
if __name__ == "__main__":
    print("This script is being run directly")
else:
    print("This script has been imported")

# Import everything from a module programmatically
import sys
module = sys.modules[__name__]
for attr_name in dir(module):
    if not attr_name.startswith('_'):
        attr = getattr(module, attr_name)
        print(f"{attr_name}: {type(attr)}")
```

## Module Attributes and Introspection

Every module has built-in attributes that provide metadata and allow for introspection. Understanding these attributes helps debug import issues and understand module structure.

```python
import math
import os

# Module attributes
print(math.__name__)      # 'math'
print(math.__file__)      # Path to module file (None for built-ins)
print(math.__doc__[:50])  # First 50 chars of docstring

# List all module contents
print(dir(math))  # All attributes and methods

# Filter for public items (no underscore prefix)
public_items = [item for item in dir(math) if not item.startswith('_')]
print(f"Public items: {len(public_items)}")

# Check if attribute exists
if hasattr(math, 'sqrt'):
    sqrt_func = getattr(math, 'sqrt')
    print(sqrt_func(16))  # 4.0

# Module path information
import sys
print("Python path:")
for path in sys.path:
    print(f"  {path}")

# Reload a module (useful during development)
import importlib
importlib.reload(math)  # Reloads the module

# Get module documentation
help(os.path)  # Display full documentation
```

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `__name__` | Module name | `'math'` |
| `__file__` | File path | `'/usr/lib/python3.9/math.py'` |
| `__doc__` | Documentation | Module docstring |
| `__dict__` | Namespace | Module's symbol table |
| `__package__` | Package name | For package modules |

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Import Math Operations"
    difficulty: basic
    description: "Import specific functions from the math module and use them to calculate the volume of a sphere. Formula: (4/3) * π * r³"
    starter_code: |
      # Import pi and pow from math module


      radius = 5
      # Calculate volume: (4/3) * pi * r^3
      volume =
      print(f"Volume of sphere with radius {radius}: {volume:.2f}")
    expected_output: |
      Volume of sphere with radius 5: 523.60
    hints:
      - "Use 'from math import pi, pow'"
      - "Formula: (4/3) * pi * pow(radius, 3)"
    solution: |
      # Import pi and pow from math module
      from math import pi, pow

      radius = 5
      # Calculate volume: (4/3) * pi * r^3
      volume = (4/3) * pi * pow(radius, 3)
      print(f"Volume of sphere with radius {radius}: {volume:.2f}")

  - title: "Module Aliases"
    difficulty: basic
    description: "Import the datetime module with an alias and create a function that returns the number of days until a future date."
    starter_code: |
      # Import datetime as dt


      def days_until(year, month, day):
          # Get today's date
          today =
          # Create future date
          future =
          # Calculate difference
          delta =
          return delta.days

      result = days_until(2024, 12, 31)
      print(f"Days until end of year: {result}")
    expected_output: |
      Days until end of year: 326
    hints:
      - "Use 'import datetime as dt'"
      - "Use dt.date.today() for today"
      - "Create future date with dt.date(year, month, day)"
    solution: |
      # Import datetime as dt
      import datetime as dt

      def days_until(year, month, day):
          # Get today's date
          today = dt.date.today()
          # Create future date
          future = dt.date(year, month, day)
          # Calculate difference
          delta = future - today
          return delta.days

      result = days_until(2024, 12, 31)
      print(f"Days until end of year: {result}")

  - title: "Custom Module Creation"
    difficulty: intermediate
    description: "Create a custom string utilities module (as a class) with methods for reversing, capitalizing each word, and counting vowels. Import and use it."
    starter_code: |
      # Define the StringUtils class
      class StringUtils:
          @staticmethod
          def reverse(text):
              # Reverse the string


          @staticmethod
          def capitalize_words(text):
              # Capitalize each word


          @staticmethod
          def count_vowels(text):
              # Count vowels (a, e, i, o, u)


      # Use the utilities
      utils = StringUtils()
      text = "python programming"
      print(f"Reversed: {utils.reverse(text)}")
      print(f"Capitalized: {utils.capitalize_words(text)}")
      print(f"Vowels: {utils.count_vowels(text)}")
    expected_output: |
      Reversed: gnimmargorp nohtyp
      Capitalized: Python Programming
      Vowels: 5
    hints:
      - "Use slicing [::-1] to reverse"
      - "Use title() method for capitalization"
      - "Count vowels with a loop or sum with generator"
    solution: |
      # Define the StringUtils class
      class StringUtils:
          @staticmethod
          def reverse(text):
              # Reverse the string
              return text[::-1]

          @staticmethod
          def capitalize_words(text):
              # Capitalize each word
              return text.title()

          @staticmethod
          def count_vowels(text):
              # Count vowels (a, e, i, o, u)
              vowels = 'aeiouAEIOU'
              return sum(1 for char in text if char in vowels)

      # Use the utilities
      utils = StringUtils()
      text = "python programming"
      print(f"Reversed: {utils.reverse(text)}")
      print(f"Capitalized: {utils.capitalize_words(text)}")
      print(f"Vowels: {utils.count_vowels(text)}")

  - title: "Selective Imports"
    difficulty: intermediate
    description: "Import only the necessary functions from random and collections modules to create a function that returns the most common element from a shuffled list."
    starter_code: |
      # Import shuffle from random and Counter from collections


      def most_common_shuffled(items):
          # Shuffle the list

          # Count occurrences

          # Return most common element and its count


      data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
      element, count = most_common_shuffled(data)
      print(f"Most common: {element} (appears {count} times)")
      print(f"Shuffled list: {data}")
    expected_output: |
      Most common: 4 (appears 4 times)
      Shuffled list: [3, 4, 2, 4, 1, 3, 4, 2, 3, 4]
    hints:
      - "Use 'from random import shuffle'"
      - "Use 'from collections import Counter'"
      - "Counter.most_common(1) returns a list with the top element"
    solution: |
      # Import shuffle from random and Counter from collections
      from random import shuffle
      from collections import Counter

      def most_common_shuffled(items):
          # Shuffle the list
          shuffle(items)
          # Count occurrences
          counter = Counter(items)
          # Return most common element and its count
          element, count = counter.most_common(1)[0]
          return element, count

      data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
      element, count = most_common_shuffled(data)
      print(f"Most common: {element} (appears {count} times)")
      print(f"Shuffled list: {data}")

  - title: "Dynamic Module Import"
    difficulty: advanced
    description: "Create a function that dynamically imports a module by name and calls a specified function from it with arguments. Include error handling."
    starter_code: |
      import importlib

      def dynamic_function_call(module_name, function_name, *args):
          try:
              # Import module dynamically

              # Get function from module

              # Call function with arguments

          except ImportError:
              return f"Error: Module '{module_name}' not found"
          except AttributeError:
              return f"Error: Function '{function_name}' not found in module"
          except Exception as e:
              return f"Error: {str(e)}"

      # Test cases
      result1 = dynamic_function_call('math', 'sqrt', 16)
      result2 = dynamic_function_call('os.path', 'join', 'home', 'user', 'file.txt')
      result3 = dynamic_function_call('fake_module', 'fake_func', 1)

      print(f"sqrt(16) = {result1}")
      print(f"path join = {result2}")
      print(result3)
    expected_output: |
      sqrt(16) = 4.0
      path join = home\user\file.txt
      Error: Module 'fake_module' not found
    hints:
      - "Use importlib.import_module(module_name)"
      - "Use getattr(module, function_name) to get the function"
      - "Call the function with *args"
    solution: |
      import importlib

      def dynamic_function_call(module_name, function_name, *args):
          try:
              # Import module dynamically
              module = importlib.import_module(module_name)
              # Get function from module
              func = getattr(module, function_name)
              # Call function with arguments
              result = func(*args)
              return result
          except ImportError:
              return f"Error: Module '{module_name}' not found"
          except AttributeError:
              return f"Error: Function '{function_name}' not found in module"
          except Exception as e:
              return f"Error: {str(e)}"

      # Test cases
      result1 = dynamic_function_call('math', 'sqrt', 16)
      result2 = dynamic_function_call('os.path', 'join', 'home', 'user', 'file.txt')
      result3 = dynamic_function_call('fake_module', 'fake_func', 1)

      print(f"sqrt(16) = {result1}")
      print(f"path join = {result2}")
      print(result3)

  - title: "Module Introspection Tool"
    difficulty: advanced
    description: "Create a module analyzer that imports a module and returns statistics about it: number of functions, classes, constants, and a list of public callable items."
    starter_code: |
      import types

      def analyze_module(module_name):
          try:
              # Import the module
              module = __import__(module_name)

              stats = {
                  'functions': 0,
                  'classes': 0,
                  'constants': 0,
                  'public_callables': []
              }

              # Iterate through module attributes
              for name in dir(module):
                  # Skip private attributes


                  attr = getattr(module, name)

                  # Count functions

                  # Count classes

                  # Count constants (uppercase names that aren't callable)


              return stats
          except ImportError:
              return None

      # Analyze the math module
      result = analyze_module('math')
      if result:
          print(f"Functions: {result['functions']}")
          print(f"Classes: {result['classes']}")
          print(f"Constants: {result['constants']}")
          print(f"Public callables: {result['public_callables'][:5]}")
    expected_output: |
      Functions: 44
      Classes: 0
      Constants: 5
      Public callables: ['acos', 'acosh', 'asin', 'asinh', 'atan']
    hints:
      - "Skip names starting with '_'"
      - "Use isinstance(attr, types.FunctionType) for functions"
      - "Use isinstance(attr, type) for classes"
      - "Constants are uppercase and not callable"
    solution: |
      import types

      def analyze_module(module_name):
          try:
              # Import the module
              module = __import__(module_name)

              stats = {
                  'functions': 0,
                  'classes': 0,
                  'constants': 0,
                  'public_callables': []
              }

              # Iterate through module attributes
              for name in dir(module):
                  # Skip private attributes
                  if name.startswith('_'):
                      continue

                  attr = getattr(module, name)

                  # Count functions
                  if isinstance(attr, types.BuiltinFunctionType) or isinstance(attr, types.FunctionType):
                      stats['functions'] += 1
                      stats['public_callables'].append(name)
                  # Count classes
                  elif isinstance(attr, type):
                      stats['classes'] += 1
                  # Count constants (uppercase names that aren't callable)
                  elif name.isupper() and not callable(attr):
                      stats['constants'] += 1

              return stats
          except ImportError:
              return None

      # Analyze the math module
      result = analyze_module('math')
      if result:
          print(f"Functions: {result['functions']}")
          print(f"Classes: {result['classes']}")
          print(f"Constants: {result['constants']}")
          print(f"Public callables: {result['public_callables'][:5]}")
```
<!-- EXERCISE_END -->
