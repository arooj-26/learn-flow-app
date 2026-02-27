# Lambda Functions in Python

Lambda functions are small, anonymous functions defined with the `lambda` keyword. They can have any number of arguments but only one expression. Lambda functions are useful for short, simple operations, especially when passing functions as arguments.

## Basic Lambda Syntax

Create simple functions in a single line:

```python
# Regular function
def add(x, y):
    return x + y

# Equivalent lambda function
add_lambda = lambda x, y: x + y

print(add(3, 5))        # 8
print(add_lambda(3, 5)) # 8

# Lambda with single argument
square = lambda x: x ** 2
print(square(5))  # 25

# Lambda with no arguments
get_pi = lambda: 3.14159
print(get_pi())  # 3.14159

# Lambda with multiple arguments
multiply = lambda x, y, z: x * y * z
print(multiply(2, 3, 4))  # 24
```

## Lambda vs Regular Functions

| Feature | Lambda | Regular Function |
|---------|--------|-----------------|
| Syntax | `lambda x: x * 2` | `def f(x): return x * 2` |
| Name | Anonymous | Must have name |
| Statements | Single expression only | Multiple statements |
| Documentation | No docstring | Can have docstring |
| Annotations | Limited | Full type hints |
| Use case | Simple, short operations | Complex logic |

## Lambda with Built-in Functions

Lambda functions shine when used with `map()`, `filter()`, and `sorted()`:

```python
# map() - apply function to each item
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# Convert temperatures from Celsius to Fahrenheit
celsius = [0, 10, 20, 30, 40]
fahrenheit = list(map(lambda c: (c * 9/5) + 32, celsius))
print(fahrenheit)  # [32.0, 50.0, 68.0, 86.0, 104.0]

# filter() - keep items that return True
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]

# Filter strings by length
words = ["cat", "elephant", "dog", "butterfly", "ant"]
long_words = list(filter(lambda w: len(w) > 5, words))
print(long_words)  # ['elephant', 'butterfly']

# sorted() - custom sorting
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78}
]

# Sort by grade
by_grade = sorted(students, key=lambda s: s["grade"])
print(by_grade)
# [{'name': 'Charlie', 'grade': 78}, {'name': 'Alice', 'grade': 85}, {'name': 'Bob', 'grade': 92}]

# Sort by name
by_name = sorted(students, key=lambda s: s["name"])
print(by_name)
```

## Lambda in Data Processing

Real-world examples with data manipulation:

```python
# Processing user data
users = [
    {"id": 1, "name": "Alice", "age": 30, "active": True},
    {"id": 2, "name": "Bob", "age": 25, "active": False},
    {"id": 3, "name": "Charlie", "age": 35, "active": True},
    {"id": 4, "name": "David", "age": 28, "active": True}
]

# Extract names
names = list(map(lambda u: u["name"], users))
print(names)  # ['Alice', 'Bob', 'Charlie', 'David']

# Get active users
active_users = list(filter(lambda u: u["active"], users))
print(f"Active users: {len(active_users)}")  # Active users: 3

# Get users over 30
over_30 = list(filter(lambda u: u["age"] > 30, users))
print(over_30)  # [{'id': 3, 'name': 'Charlie', 'age': 35, 'active': True}]

# Transform data
user_summaries = list(map(
    lambda u: f"{u['name']} ({u['age']} years)",
    users
))
print(user_summaries)
# ['Alice (30 years)', 'Bob (25 years)', 'Charlie (35 years)', 'David (28 years)']

# Processing financial data
transactions = [
    {"amount": 100, "type": "deposit"},
    {"amount": 50, "type": "withdrawal"},
    {"amount": 200, "type": "deposit"},
    {"amount": 75, "type": "withdrawal"}
]

# Calculate total deposits
deposits = filter(lambda t: t["type"] == "deposit", transactions)
total_deposits = sum(map(lambda t: t["amount"], deposits))
print(f"Total deposits: ${total_deposits}")  # Total deposits: $300
```

## Lambda with reduce()

Combine `reduce()` from `functools` with lambda:

```python
from functools import reduce

# Sum all numbers
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda x, y: x + y, numbers)
print(total)  # 15

# Find maximum
maximum = reduce(lambda x, y: x if x > y else y, numbers)
print(maximum)  # 5

# Concatenate strings
words = ["Python", "is", "awesome"]
sentence = reduce(lambda x, y: x + " " + y, words)
print(sentence)  # Python is awesome

# Product of all numbers
product = reduce(lambda x, y: x * y, numbers)
print(product)  # 120

# Real-world: Merge dictionaries
dicts = [
    {"a": 1, "b": 2},
    {"c": 3, "d": 4},
    {"e": 5, "f": 6}
]

merged = reduce(lambda x, y: {**x, **y}, dicts)
print(merged)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
```

## Lambda in Conditional Expressions

Use lambda with ternary operators for conditional logic:

```python
# Absolute value
abs_value = lambda x: x if x >= 0 else -x
print(abs_value(-5))  # 5
print(abs_value(3))   # 3

# Grade assignment
get_grade = lambda score: "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
print(get_grade(95))  # A
print(get_grade(85))  # B
print(get_grade(75))  # C
print(get_grade(65))  # F

# Discount calculator
calculate_discount = lambda price, is_member: price * 0.8 if is_member else price * 0.9
print(calculate_discount(100, True))   # 80.0 (20% member discount)
print(calculate_discount(100, False))  # 90.0 (10% regular discount)

# Max of two numbers
max_of_two = lambda a, b: a if a > b else b
print(max_of_two(10, 5))  # 10
```

## When to Use Lambda (and When Not To)

Good use cases and alternatives:

```python
# GOOD: Short, simple operations with built-in functions
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))

# GOOD: Sorting with simple key
people = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]
sorted_by_age = sorted(people, key=lambda p: p[1])

# GOOD: Event handlers or callbacks (in GUI programming)
# button.onclick = lambda: print("Button clicked!")

# BAD: Complex logic - use regular function
# Don't do this:
complex_lambda = lambda x: x * 2 if x > 0 else x * -1 if x < 0 else 0

# Do this instead:
def process_number(x):
    """Process number with clear logic."""
    if x > 0:
        return x * 2
    elif x < 0:
        return x * -1
    else:
        return 0

# BAD: Lambda that needs a name - just use def
# Don't do this:
calculate_area = lambda length, width: length * width

# Do this instead:
def calculate_area(length, width):
    """Calculate rectangle area."""
    return length * width
```

## Advanced Lambda Patterns

More sophisticated uses of lambda functions:

```python
# Lambda returning lambda (currying)
multiply = lambda x: lambda y: x * y
times_five = multiply(5)
print(times_five(3))  # 15
print(times_five(10)) # 50

# Lambda in dictionary for dispatch table
operations = {
    'add': lambda x, y: x + y,
    'sub': lambda x, y: x - y,
    'mul': lambda x, y: x * y,
    'div': lambda x, y: x / y if y != 0 else "Error"
}

print(operations['add'](10, 5))  # 15
print(operations['mul'](10, 5))  # 50
print(operations['div'](10, 0))  # Error

# Lambda with default arguments
power = lambda base, exp=2: base ** exp
print(power(3))     # 9 (3^2)
print(power(2, 4))  # 16 (2^4)

# Lambda with *args
sum_all = lambda *args: sum(args)
print(sum_all(1, 2, 3, 4, 5))  # 15

# List comprehension vs map with lambda
# These are equivalent:
squares_map = list(map(lambda x: x**2, range(5)))
squares_comp = [x**2 for x in range(5)]
print(squares_map)  # [0, 1, 4, 9, 16]
print(squares_comp) # [0, 1, 4, 9, 16]

# Filter vs list comprehension
# These are equivalent:
evens_filter = list(filter(lambda x: x % 2 == 0, range(10)))
evens_comp = [x for x in range(10) if x % 2 == 0]
print(evens_filter)  # [0, 2, 4, 6, 8]
print(evens_comp)    # [0, 2, 4, 6, 8]
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Basic Lambda"
    difficulty: basic
    description: "Create a lambda function `double` that doubles a number. Test with double(7)."
    starter_code: |
      # Create lambda function

    expected_output: "14"
    hints:
      - "Syntax: lambda x: expression"
      - "Multiply by 2"
    solution: |
      double = lambda x: x * 2
      print(double(7))

  - title: "Lambda with map()"
    difficulty: basic
    description: "Use map() and lambda to square each number in [1, 2, 3, 4, 5]. Print the result as a list."
    starter_code: |
      # Use map with lambda to square numbers

    expected_output: "[1, 4, 9, 16, 25]"
    hints:
      - "map(lambda x: ..., list)"
      - "Convert to list with list()"
    solution: |
      numbers = [1, 2, 3, 4, 5]
      squared = list(map(lambda x: x ** 2, numbers))
      print(squared)

  - title: "Lambda with filter()"
    difficulty: intermediate
    description: "Use filter() and lambda to get numbers greater than 5 from [3, 8, 2, 9, 1, 7, 4]. Print the result as a list."
    starter_code: |
      # Use filter with lambda

    expected_output: "[8, 9, 7]"
    hints:
      - "filter(lambda x: condition, list)"
      - "Condition is x > 5"
    solution: |
      numbers = [3, 8, 2, 9, 1, 7, 4]
      greater_than_five = list(filter(lambda x: x > 5, numbers))
      print(greater_than_five)

  - title: "Lambda with sorted()"
    difficulty: intermediate
    description: "Sort this list of tuples by the second element: [('a', 3), ('b', 1), ('c', 2)]. Use sorted() with lambda key."
    starter_code: |
      # Sort by second element using lambda

    expected_output: "[('b', 1), ('c', 2), ('a', 3)]"
    hints:
      - "sorted(list, key=lambda item: ...)"
      - "Access second element with item[1]"
    solution: |
      items = [('a', 3), ('b', 1), ('c', 2)]
      sorted_items = sorted(items, key=lambda item: item[1])
      print(sorted_items)

  - title: "Lambda with reduce()"
    difficulty: advanced
    description: "Use reduce() from functools with lambda to find the product of all numbers in [2, 3, 4, 5]."
    starter_code: |
      # Use reduce to calculate product

    expected_output: "120"
    hints:
      - "from functools import reduce"
      - "reduce(lambda x, y: x * y, list)"
    solution: |
      from functools import reduce

      numbers = [2, 3, 4, 5]
      product = reduce(lambda x, y: x * y, numbers)
      print(product)

  - title: "Conditional Lambda"
    difficulty: advanced
    description: "Create a lambda `categorize_age` that returns 'minor' if age < 18, 'adult' if 18-65, else 'senior'. Test with ages 15, 30, 70."
    starter_code: |
      # Create conditional lambda

    expected_output: |
      minor
      adult
      senior
    hints:
      - "Use nested ternary: a if cond1 else b if cond2 else c"
      - "Check age ranges in order"
    solution: |
      categorize_age = lambda age: "minor" if age < 18 else "adult" if age <= 65 else "senior"

      print(categorize_age(15))
      print(categorize_age(30))
      print(categorize_age(70))
```
<!-- EXERCISE_END -->
