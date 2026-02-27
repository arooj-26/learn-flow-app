# Variables and Data Types in Python

Variables are containers for storing data values. Python is dynamically typed, meaning you don't need to declare variable types explicitly.

## Creating Variables

In Python, you create a variable by assigning a value to it using the `=` operator:

```python
name = "Alice"      # String
age = 25            # Integer
height = 5.9        # Float
is_student = True   # Boolean
```

## Python Data Types

Python has several built-in data types:

| Type | Description | Example |
|------|-------------|---------|
| `str` | Text/strings | `"Hello"`, `'World'` |
| `int` | Whole numbers | `1`, `42`, `-10` |
| `float` | Decimal numbers | `3.14`, `-0.5` |
| `bool` | Boolean values | `True`, `False` |

## Type Checking

You can check the type of any variable using the `type()` function:

```python
x = 10
print(type(x))  # <class 'int'>

y = "hello"
print(type(y))  # <class 'str'>

z = 3.14
print(type(z))  # <class 'float'>
```

## Type Conversion

Python allows you to convert between types:

```python
# String to number
num_str = "42"
num_int = int(num_str)      # Convert to integer: 42
num_float = float(num_str)  # Convert to float: 42.0

# Number to string
age = 25
age_str = str(age)  # Convert to string: "25"

# Float to int (truncates decimal)
pi = 3.14159
pi_int = int(pi)  # 3
```

## Variable Naming Rules

1. Must start with a letter or underscore
2. Can contain letters, numbers, and underscores
3. Case-sensitive (`name` and `Name` are different)
4. Cannot use Python keywords (`if`, `for`, `while`, etc.)

```python
# Valid names
my_name = "Alice"
_private = 42
userName2 = "Bob"

# Invalid names (will cause errors)
# 2name = "Error"    # Can't start with number
# my-name = "Error"  # Can't use hyphens
```

## Multiple Assignment

Python allows assigning multiple variables in one line:

```python
# Assign same value
x = y = z = 0

# Assign different values
a, b, c = 1, 2, 3

# Swap values
x, y = y, x
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Create a Greeting Variable"
    difficulty: basic
    description: "Create a variable called `message` with the value 'Hello, Python!' and print it."
    starter_code: |
      # Create your variable here

    expected_output: "Hello, Python!"
    hints:
      - "Use the = sign to assign a value to a variable"
      - "Use print() to display the value"
    solution: |
      message = "Hello, Python!"
      print(message)

  - title: "Check Variable Types"
    difficulty: basic
    description: "Create three variables: `name` (string 'Alice'), `age` (integer 25), and `height` (float 5.9). Print their types."
    starter_code: |
      # Create variables and print their types

    expected_output: |
      <class 'str'>
      <class 'int'>
      <class 'float'>
    hints:
      - "Use type() function to get the type"
      - "Strings use quotes, integers are whole numbers, floats have decimals"
    solution: |
      name = "Alice"
      age = 25
      height = 5.9
      print(type(name))
      print(type(age))
      print(type(height))

  - title: "Type Conversion"
    difficulty: intermediate
    description: "Convert the string '42' to an integer, add 8 to it, and print the result."
    starter_code: |
      num_str = "42"
      # Convert and calculate

    expected_output: "50"
    hints:
      - "Use int() to convert a string to integer"
      - "After conversion, you can perform arithmetic"
    solution: |
      num_str = "42"
      num_int = int(num_str)
      result = num_int + 8
      print(result)

  - title: "Multiple Assignment"
    difficulty: intermediate
    description: "Use multiple assignment to create variables x=10, y=20, z=30 in one line, then print their sum."
    starter_code: |
      # Use multiple assignment

    expected_output: "60"
    hints:
      - "Syntax: a, b, c = value1, value2, value3"
    solution: |
      x, y, z = 10, 20, 30
      print(x + y + z)

  - title: "F-String Formatting"
    difficulty: advanced
    description: "Create variables `name = 'Python'` and `version = 3.12`. Use an f-string to print 'Welcome to Python version 3.12!'"
    starter_code: |
      name = "Python"
      version = 3.12
      # Use f-string to print

    expected_output: "Welcome to Python version 3.12!"
    hints:
      - "F-strings start with f before the quote"
      - "Put variables inside curly braces: {variable}"
    solution: |
      name = "Python"
      version = 3.12
      print(f"Welcome to {name} version {version}!")

  - title: "Boolean Comparison"
    difficulty: advanced
    description: "Create variables `a = 15` and `b = 10`. Print whether a is greater than b, and whether they are equal."
    starter_code: |
      a = 15
      b = 10
      # Print comparisons

    expected_output: |
      True
      False
    hints:
      - "Use > for greater than comparison"
      - "Use == for equality check"
    solution: |
      a = 15
      b = 10
      print(a > b)
      print(a == b)
```
<!-- EXERCISE_END -->
