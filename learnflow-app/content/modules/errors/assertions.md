# Assertions in Python

Assertions are debugging aids that test conditions during development. They act as internal self-checks for your program, catching bugs early by verifying assumptions about your code's state.

## Basic Assertion Syntax

```python
# assert condition, optional_message
x = 10
assert x > 0, "x must be positive"
print("Assertion passed!")

# Failed assertion raises AssertionError
# assert x < 0, "x must be negative"
# AssertionError: x must be negative
```

## How Assertions Work

An assertion is equivalent to:

```python
# assert condition, message
# is the same as:
if not condition:
    raise AssertionError(message)

# Assertions can be disabled with python -O (optimize mode)
# So NEVER use assertions for data validation in production
```

## Common Assertion Patterns

```python
# Type checking
def process_age(age):
    assert isinstance(age, int), f"Expected int, got {type(age).__name__}"
    assert age >= 0, f"Age cannot be negative: {age}"
    return f"Age: {age}"

print(process_age(25))  # Age: 25

# Preconditions
def divide(a, b):
    assert b != 0, "Divisor cannot be zero"
    return a / b

print(divide(10, 3))  # 3.333...

# Postconditions
def calculate_discount(price, percent):
    assert 0 <= percent <= 100, f"Invalid discount: {percent}%"
    result = price * (1 - percent / 100)
    assert result >= 0, "Discount resulted in negative price"
    return result

print(calculate_discount(100, 20))  # 80.0

# Invariants (conditions that should always be true)
def sort_list(items):
    result = sorted(items)
    assert len(result) == len(items), "Sort changed list length"
    assert all(result[i] <= result[i+1] for i in range(len(result)-1)), "List not sorted"
    return result

print(sort_list([3, 1, 4, 1, 5]))  # [1, 1, 3, 4, 5]
```

## Assertions vs Exceptions

Use the right tool for the right job:

| Scenario | Use |
|----------|-----|
| Bug detection during development | `assert` |
| User input validation | `if` + `raise ValueError` |
| File/network errors | `try/except` |
| API contract enforcement | `raise TypeError/ValueError` |
| Internal state checking | `assert` |

```python
# WRONG: Don't use assert for user input
# assert user_age > 0  # Can be disabled with -O flag!

# RIGHT: Use proper validation
def set_age(age):
    if not isinstance(age, int) or age < 0:
        raise ValueError(f"Invalid age: {age}")
    return age

# RIGHT: Use assert for internal checks
def _internal_process(data):
    assert data is not None, "Internal error: data should not be None"
    # ... process data
```

## Assertion Messages

Good assertion messages help debugging:

```python
# Bad: no context
assert len(items) > 0

# Good: descriptive message
assert len(items) > 0, f"Expected non-empty list, got {len(items)} items"

# Good: include actual values
def merge_lists(a, b):
    assert isinstance(a, list), f"First arg must be list, got {type(a).__name__}"
    assert isinstance(b, list), f"Second arg must be list, got {type(b).__name__}"
    result = a + b
    assert len(result) == len(a) + len(b), \
        f"Merge error: {len(a)} + {len(b)} != {len(result)}"
    return result

print(merge_lists([1, 2], [3, 4]))  # [1, 2, 3, 4]
```

## Assertions in Testing

Assertions are the foundation of unit testing:

```python
# Simple test functions using assert
def test_addition():
    assert 2 + 2 == 4, "Basic addition failed"
    assert -1 + 1 == 0, "Negative addition failed"
    assert 0.1 + 0.2 != 0.3, "Floating point precision"
    print("All addition tests passed!")

test_addition()

# Testing with approximate equality
def approx_equal(a, b, tolerance=1e-9):
    return abs(a - b) < tolerance

assert approx_equal(0.1 + 0.2, 0.3), "Should be approximately equal"
print("Approximate equality works!")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Basic Assertion"
    difficulty: basic
    description: "Write a function that asserts a number is positive, then returns its square root. Test it with 16."
    starter_code: |
      import math

      def safe_sqrt(n):
          # Add assertion and return square root
          pass

      print(safe_sqrt(16))

    expected_output: "4.0"
    hints:
      - "Use assert n >= 0 with a message"
      - "Use math.sqrt() to calculate the square root"
    solution: |
      import math

      def safe_sqrt(n):
          assert n >= 0, f"Cannot take square root of negative number: {n}"
          return math.sqrt(n)

      print(safe_sqrt(16))

  - title: "Assert Type Check"
    difficulty: basic
    description: "Write a function that asserts its input is a string, then returns it uppercased. Test with 'hello'."
    starter_code: |
      def to_upper(text):
          # Assert text is a string, then return uppercased
          pass

      print(to_upper("hello"))

    expected_output: "HELLO"
    hints:
      - "Use isinstance(text, str) in the assertion"
      - "Use .upper() to convert to uppercase"
    solution: |
      def to_upper(text):
          assert isinstance(text, str), f"Expected str, got {type(text).__name__}"
          return text.upper()

      print(to_upper("hello"))

  - title: "Pre and Post Conditions"
    difficulty: intermediate
    description: "Write a function that calculates a percentage. Assert the percentage is between 0-100 (precondition) and the result is non-negative (postcondition). Test with calculate_percentage(200, 25)."
    starter_code: |
      def calculate_percentage(total, percent):
          # Add precondition and postcondition assertions
          pass

      print(calculate_percentage(200, 25))

    expected_output: "50.0"
    hints:
      - "Assert 0 <= percent <= 100 before calculating"
      - "Assert result >= 0 after calculating"
    solution: |
      def calculate_percentage(total, percent):
          assert 0 <= percent <= 100, f"Percent must be 0-100, got {percent}"
          result = total * (percent / 100)
          assert result >= 0, f"Result cannot be negative: {result}"
          return result

      print(calculate_percentage(200, 25))

  - title: "Assertion with Collections"
    difficulty: intermediate
    description: "Write a function that asserts a list has no duplicates, then returns the sorted list. Test with [3, 1, 4, 5, 2]."
    starter_code: |
      def sort_unique(items):
          # Assert no duplicates, return sorted
          pass

      print(sort_unique([3, 1, 4, 5, 2]))

    expected_output: "[1, 2, 3, 4, 5]"
    hints:
      - "Compare len(items) with len(set(items)) to check for duplicates"
      - "Use sorted() to return a sorted copy"
    solution: |
      def sort_unique(items):
          assert len(items) == len(set(items)), f"Duplicate values found in {items}"
          return sorted(items)

      print(sort_unique([3, 1, 4, 5, 2]))

  - title: "Test Suite with Assertions"
    difficulty: advanced
    description: "Write a function 'clamp(value, min_val, max_val)' that restricts a value to a range. Then write 3 test assertions and print 'All tests passed!'."
    starter_code: |
      def clamp(value, min_val, max_val):
          # Return value clamped between min_val and max_val
          pass

      # Write test assertions

    expected_output: "All tests passed!"
    hints:
      - "Use min() and max() or conditional logic to clamp"
      - "Test: below range, in range, above range"
    solution: |
      def clamp(value, min_val, max_val):
          assert min_val <= max_val, "min must be <= max"
          return max(min_val, min(value, max_val))

      assert clamp(5, 0, 10) == 5, "In-range value should stay same"
      assert clamp(-5, 0, 10) == 0, "Below range should clamp to min"
      assert clamp(15, 0, 10) == 10, "Above range should clamp to max"
      print("All tests passed!")

  - title: "Contract-Based Design"
    difficulty: advanced
    description: "Write a Stack class with push and pop methods. Use assertions to enforce: push requires non-None values, pop requires non-empty stack, and stack size is always >= 0. Demonstrate it works."
    starter_code: |
      class Stack:
          def __init__(self):
              self._items = []

          def push(self, item):
              # Assert and push
              pass

          def pop(self):
              # Assert and pop
              pass

          def size(self):
              return len(self._items)

      # Test the stack

    expected_output: |
      Pushed: a, b, c
      Popped: c
      Size: 2
    hints:
      - "Assert item is not None in push"
      - "Assert len(self._items) > 0 in pop"
    solution: |
      class Stack:
          def __init__(self):
              self._items = []

          def push(self, item):
              assert item is not None, "Cannot push None"
              self._items.append(item)
              assert self.size() >= 0

          def pop(self):
              assert len(self._items) > 0, "Cannot pop from empty stack"
              item = self._items.pop()
              assert self.size() >= 0
              return item

          def size(self):
              return len(self._items)

      s = Stack()
      s.push("a")
      s.push("b")
      s.push("c")
      print("Pushed: a, b, c")
      print(f"Popped: {s.pop()}")
      print(f"Size: {s.size()}")
```
<!-- EXERCISE_END -->
