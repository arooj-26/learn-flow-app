# Debugging Techniques in Python

Debugging is the systematic process of finding and fixing errors in your code. Python provides powerful built-in tools and techniques that help you identify issues quickly and efficiently.

## Print Debugging

The simplest debugging technique - strategically placing print statements:

```python
def calculate_average(numbers):
    print(f"DEBUG: Input = {numbers}")        # Check input
    total = sum(numbers)
    print(f"DEBUG: Total = {total}")           # Check intermediate value
    count = len(numbers)
    print(f"DEBUG: Count = {count}")           # Check intermediate value
    average = total / count
    print(f"DEBUG: Average = {average}")       # Check result
    return average

result = calculate_average([10, 20, 30, 40])
print(f"Result: {result}")

# Better approach: use a debug flag
DEBUG = True

def debug_print(*args, **kwargs):
    if DEBUG:
        print("DEBUG:", *args, **kwargs)
```

## Using the pdb Debugger

Python's built-in debugger lets you step through code interactively:

```python
import pdb

def find_bug(data):
    result = []
    for item in data:
        # Set a breakpoint
        # pdb.set_trace()  # Uncomment to debug
        processed = item * 2
        if processed > 10:
            result.append(processed)
    return result

# Python 3.7+ built-in breakpoint
def process_data(items):
    total = 0
    for i, item in enumerate(items):
        # breakpoint()  # Uncomment to debug
        total += item
    return total

# Common pdb commands:
# n (next)     - Execute next line
# s (step)     - Step into function
# c (continue) - Continue execution
# p variable   - Print variable value
# l (list)     - Show current code
# q (quit)     - Quit debugger
# h (help)     - Show help
```

## Type and Value Inspection

```python
# Inspecting objects
data = {"name": "Alice", "scores": [90, 85, 92]}

print(type(data))           # <class 'dict'>
print(isinstance(data, dict))  # True
print(dir(data))            # List all methods

# Checking variable details
x = 42
print(f"Value: {x}")
print(f"Type: {type(x)}")
print(f"ID: {id(x)}")
print(f"Size: {x.__sizeof__()} bytes")

# Using vars() for object attributes
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Alice", 30)
print(vars(p))  # {'name': 'Alice', 'age': 30}
```

## Traceback Analysis

Understanding tracebacks is crucial for debugging:

```python
# Reading a traceback (bottom-up)
def function_c():
    return 1 / 0

def function_b():
    return function_c()

def function_a():
    return function_b()

# When function_a() is called, you get:
# Traceback (most recent call last):
#   File "script.py", line 10, in <module>
#     function_a()
#   File "script.py", line 8, in function_a
#     return function_b()
#   File "script.py", line 5, in function_b
#     return function_c()
#   File "script.py", line 2, in function_c
#     return 1 / 0
# ZeroDivisionError: division by zero

# Getting traceback programmatically
import traceback

try:
    function_a()
except ZeroDivisionError:
    error_info = traceback.format_exc()
    print("Caught error:")
    print(error_info)
```

## Common Bug Patterns

```python
# 1. Off-by-one errors
items = [10, 20, 30, 40, 50]
# Bug: range(len(items) + 1) causes IndexError
# Fix: range(len(items))
for i in range(len(items)):
    print(items[i], end=" ")
print()

# 2. Mutable default arguments
def append_to(item, target=None):  # CORRECT
    if target is None:
        target = []
    target.append(item)
    return target

# NOT: def append_to(item, target=[])  # Bug: shared list!

# 3. Variable scope confusion
total = 0
def add_to_total(value):
    global total  # Must declare global to modify
    total += value
    return total

print(add_to_total(5))  # 5

# 4. Comparison vs assignment
x = 5
# if x = 5:   # SyntaxError - assignment not comparison
if x == 5:    # Correct - comparison
    print("x is 5")
```

## Debugging with repr() vs str()

```python
# str() is for human readability
# repr() is for debugging (shows exact representation)

text = "Hello\tWorld"
print(str(text))   # Hello	World  (tab is rendered)
print(repr(text))  # 'Hello\tWorld'  (shows escape character)

# Useful for spotting hidden characters
data = "hello "  # trailing space
print(f"str: '{str(data)}'")    # str: 'hello '
print(f"repr: {repr(data)}")    # repr: 'hello '

# In f-strings, use !r for repr
name = "Alice\n"
print(f"Name is {name!r}")  # Name is 'Alice\n'
```

## Systematic Debugging Process

1. **Reproduce** the bug consistently
2. **Isolate** - find the smallest input that causes the bug
3. **Inspect** - check variable values at key points
4. **Hypothesize** - form a theory about the cause
5. **Test** - verify your hypothesis
6. **Fix** and verify the fix doesn't break anything else

```python
# Example: Binary search debugging
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        # Debug: print state at each step
        print(f"  Searching: left={left}, right={right}, mid={mid}, arr[mid]={arr[mid]}")

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

arr = [1, 3, 5, 7, 9, 11, 13]
print(f"Found at index: {binary_search(arr, 7)}")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Find the Bug"
    difficulty: basic
    description: "The function below has a bug. Fix it so it correctly calculates the average of a list of numbers."
    starter_code: |
      def average(numbers):
          total = 0
          for n in numbers:
              total += n
          return total / len(numbers) + 1  # Bug is here

      print(average([10, 20, 30]))

    expected_output: "20.0"
    hints:
      - "Check the return statement carefully"
      - "The + 1 is causing an off-by-one in the result"
    solution: |
      def average(numbers):
          total = 0
          for n in numbers:
              total += n
          return total / len(numbers)

      print(average([10, 20, 30]))

  - title: "Debug with Print"
    difficulty: basic
    description: "Add a debug print to show the intermediate sum, then print the final result of summing [5, 10, 15]."
    starter_code: |
      def debug_sum(numbers):
          total = 0
          for n in numbers:
              total += n
              # Add debug print here
          return total

      result = debug_sum([5, 10, 15])
      print(f"Final: {result}")

    expected_output: |
      Running total: 5
      Running total: 15
      Running total: 30
      Final: 30
    hints:
      - "Print the running total inside the loop"
      - "Use an f-string to show the current total"
    solution: |
      def debug_sum(numbers):
          total = 0
          for n in numbers:
              total += n
              print(f"Running total: {total}")
          return total

      result = debug_sum([5, 10, 15])
      print(f"Final: {result}")

  - title: "Fix the Index Error"
    difficulty: intermediate
    description: "The function has an off-by-one bug. Fix it to correctly pair adjacent elements."
    starter_code: |
      def pair_adjacent(items):
          pairs = []
          for i in range(len(items)):
              pairs.append((items[i], items[i + 1]))
          return pairs

      print(pair_adjacent([1, 2, 3, 4]))

    expected_output: "[(1, 2), (2, 3), (3, 4)]"
    hints:
      - "The loop goes one element too far when accessing items[i + 1]"
      - "Change range to len(items) - 1"
    solution: |
      def pair_adjacent(items):
          pairs = []
          for i in range(len(items) - 1):
              pairs.append((items[i], items[i + 1]))
          return pairs

      print(pair_adjacent([1, 2, 3, 4]))

  - title: "Type Inspection"
    difficulty: intermediate
    description: "Write a function that prints the type and repr of each argument, then returns them joined as a string."
    starter_code: |
      def inspect_and_join(*args):
          # Print type and repr of each arg, then join as strings
          pass

      print(inspect_and_join("hello", 42, True))

    expected_output: |
      Arg 0: type=str, repr='hello'
      Arg 1: type=int, repr=42
      Arg 2: type=bool, repr=True
      hello 42 True
    hints:
      - "Use type(arg).__name__ to get the type name"
      - "Use repr(arg) to get the repr string"
    solution: |
      def inspect_and_join(*args):
          for i, arg in enumerate(args):
              print(f"Arg {i}: type={type(arg).__name__}, repr={repr(arg)}")
          return " ".join(str(a) for a in args)

      print(inspect_and_join("hello", 42, True))

  - title: "Fix the Mutable Default"
    difficulty: advanced
    description: "The function has a mutable default argument bug. Fix it so each call gets a fresh list."
    starter_code: |
      def add_item(item, items=[]):
          items.append(item)
          return items

      list1 = add_item("a")
      list2 = add_item("b")
      print(list1)
      print(list2)

    expected_output: |
      ['a']
      ['b']
    hints:
      - "Default mutable arguments are shared across calls"
      - "Use None as default and create a new list inside the function"
    solution: |
      def add_item(item, items=None):
          if items is None:
              items = []
          items.append(item)
          return items

      list1 = add_item("a")
      list2 = add_item("b")
      print(list1)
      print(list2)

  - title: "Trace Function Calls"
    difficulty: advanced
    description: "Write a decorator that prints function name, arguments, and return value for debugging. Apply it to an add function."
    starter_code: |
      def debug_trace(func):
          # Create a debugging decorator
          pass

      @debug_trace
      def add(a, b):
          return a + b

      result = add(3, 7)
      print(f"Got: {result}")

    expected_output: |
      CALL: add(3, 7)
      RETURN: add -> 10
      Got: 10
    hints:
      - "The decorator should print args before calling the function"
      - "Capture the return value, print it, then return it"
    solution: |
      def debug_trace(func):
          def wrapper(*args, **kwargs):
              args_str = ", ".join(repr(a) for a in args)
              print(f"CALL: {func.__name__}({args_str})")
              result = func(*args, **kwargs)
              print(f"RETURN: {func.__name__} -> {result}")
              return result
          return wrapper

      @debug_trace
      def add(a, b):
          return a + b

      result = add(3, 7)
      print(f"Got: {result}")
```
<!-- EXERCISE_END -->
