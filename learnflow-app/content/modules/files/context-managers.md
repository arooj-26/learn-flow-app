# Context Managers in Python

Context managers provide a clean way to manage resources like files, database connections, and locks. They ensure proper setup and teardown using the `with` statement, even when exceptions occur.

## The with Statement

The `with` statement automatically handles resource cleanup:

```python
# Without context manager (risky)
f = open("data.txt", "r")
try:
    content = f.read()
finally:
    f.close()

# With context manager (clean and safe)
with open("data.txt", "r") as f:
    content = f.read()
# File is automatically closed here, even if an error occurred
```

## How Context Managers Work

Context managers implement two special methods:

```python
# __enter__ is called when entering the with block
# __exit__ is called when leaving the with block (even on error)

class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        print(f"Opening {self.filename}")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing {self.filename}")
        if self.file:
            self.file.close()
        return False  # Don't suppress exceptions

# Usage
with FileManager("test.txt", "w") as f:
    f.write("Hello!")
# Output: Opening test.txt
# Output: Closing test.txt
```

## Multiple Context Managers

You can use multiple context managers in a single `with` statement:

```python
# Copy contents from one file to another
with open("source.txt", "r") as src, open("dest.txt", "w") as dst:
    dst.write(src.read())

# Python 3.10+ allows parentheses for better formatting
with (
    open("source.txt", "r") as src,
    open("dest.txt", "w") as dst,
    open("log.txt", "a") as log
):
    data = src.read()
    dst.write(data)
    log.write(f"Copied {len(data)} characters\n")
```

## The contextlib Module

Python's `contextlib` module provides utilities for creating context managers:

```python
from contextlib import contextmanager

@contextmanager
def managed_file(filename, mode):
    """A simple file context manager using a generator."""
    f = open(filename, mode)
    try:
        yield f  # This is where the with block executes
    finally:
        f.close()

with managed_file("data.txt", "w") as f:
    f.write("Using contextlib!")

# Timer context manager
import time
from contextlib import contextmanager

@contextmanager
def timer(label):
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"{label}: {elapsed:.4f} seconds")

with timer("Processing"):
    total = sum(range(1000000))
```

## Practical Context Manager Patterns

```python
from contextlib import contextmanager

# Temporary directory change
import os

@contextmanager
def change_dir(path):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)

# Database transaction pattern
@contextmanager
def transaction(connection):
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()

# Suppressing specific exceptions
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("temp_file.txt")
# No error even if file doesn't exist
```

## Exception Handling in __exit__

The `__exit__` method receives exception info and can suppress exceptions:

```python
class SafeProcessor:
    def __enter__(self):
        print("Starting processing")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print(f"Handled ValueError: {exc_val}")
            return True  # Suppress the exception
        print("Processing complete")
        return False  # Re-raise any other exceptions

    def process(self, value):
        if value < 0:
            raise ValueError("Negative value")
        return value * 2

with SafeProcessor() as sp:
    result = sp.process(-5)  # ValueError is caught and suppressed
print("Continues normally")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Basic with Statement"
    difficulty: basic
    description: "Demonstrate understanding of context managers by printing 'Entering', 'Inside', and 'Exiting' to show the flow of a with block."
    starter_code: |
      from contextlib import contextmanager

      @contextmanager
      def my_context():
          print("Entering")
          yield
          print("Exiting")

      # Use the context manager

    expected_output: |
      Entering
      Inside
      Exiting
    hints:
      - "Use a with statement with my_context()"
      - "Print 'Inside' within the with block"
    solution: |
      from contextlib import contextmanager

      @contextmanager
      def my_context():
          print("Entering")
          yield
          print("Exiting")

      with my_context():
          print("Inside")

  - title: "Context Manager Return Value"
    difficulty: basic
    description: "Create a context manager that yields a list, use it to append items, then print the list."
    starter_code: |
      from contextlib import contextmanager

      @contextmanager
      def collector():
          items = []
          yield items
          print(f"Collected: {items}")

      # Use the context manager to add 'a', 'b', 'c'

    expected_output: "Collected: ['a', 'b', 'c']"
    hints:
      - "Use 'with collector() as items:' to get the list"
      - "Append items inside the with block"
    solution: |
      from contextlib import contextmanager

      @contextmanager
      def collector():
          items = []
          yield items
          print(f"Collected: {items}")

      with collector() as items:
          items.append('a')
          items.append('b')
          items.append('c')

  - title: "Timer Context Manager"
    difficulty: intermediate
    description: "Create a context manager that measures and prints how long a block takes (use a simulated elapsed time for consistent output)."
    starter_code: |
      from contextlib import contextmanager

      @contextmanager
      def timer(label):
          # Track start, yield, then print elapsed time
          pass

      # Usage:
      # with timer("Task"):
      #     ... do work ...

    expected_output: "Task: done"
    hints:
      - "Use try/finally to ensure the print happens"
      - "yield in the middle of the generator"
    solution: |
      from contextlib import contextmanager

      @contextmanager
      def timer(label):
          try:
              yield
          finally:
              print(f"{label}: done")

      with timer("Task"):
          total = sum(range(100))

  - title: "Class-Based Context Manager"
    difficulty: intermediate
    description: "Create a class-based context manager called Indenter that tracks indentation level. It should print 'Start' on enter and 'End' on exit."
    starter_code: |
      class Indenter:
          # Implement __enter__ and __exit__
          pass

      # with Indenter() as ind:
      #     print("Working...")

    expected_output: |
      Start
      Working...
      End
    hints:
      - "Implement __enter__ returning self and __exit__ for cleanup"
      - "__enter__ prints 'Start', __exit__ prints 'End'"
    solution: |
      class Indenter:
          def __enter__(self):
              print("Start")
              return self

          def __exit__(self, exc_type, exc_val, exc_tb):
              print("End")
              return False

      with Indenter() as ind:
          print("Working...")

  - title: "Exception-Safe Context Manager"
    difficulty: advanced
    description: "Create a context manager that logs both successful and failed operations."
    starter_code: |
      from contextlib import contextmanager

      @contextmanager
      def safe_operation(name):
          # Print start, handle success/failure
          pass

      with safe_operation("save"):
          print("Saving data...")

    expected_output: |
      Starting: save
      Saving data...
      Completed: save
    hints:
      - "Use try/except/else/finally around the yield"
      - "Print different messages for success vs failure"
    solution: |
      from contextlib import contextmanager

      @contextmanager
      def safe_operation(name):
          print(f"Starting: {name}")
          try:
              yield
          except Exception as e:
              print(f"Failed: {name} - {e}")
              raise
          else:
              print(f"Completed: {name}")

      with safe_operation("save"):
          print("Saving data...")

  - title: "Nested Context Managers"
    difficulty: advanced
    description: "Create a context manager that tracks nesting depth and prints indented enter/exit messages."
    starter_code: |
      from contextlib import contextmanager

      depth = 0

      @contextmanager
      def level(name):
          global depth
          # Manage depth and print indented messages
          pass

      # Nest two levels

    expected_output: |
      Entering: outer
        Entering: inner
        Exiting: inner
      Exiting: outer
    hints:
      - "Increment depth on enter, decrement on exit"
      - "Use depth * '  ' for indentation"
    solution: |
      from contextlib import contextmanager

      depth = 0

      @contextmanager
      def level(name):
          global depth
          print("  " * depth + f"Entering: {name}")
          depth += 1
          try:
              yield
          finally:
              depth -= 1
              print("  " * depth + f"Exiting: {name}")

      with level("outer"):
          with level("inner"):
              pass
```
<!-- EXERCISE_END -->
