# Defining Functions in Python

Functions are reusable blocks of code that perform specific tasks. They help organize code, reduce repetition, and make programs easier to maintain.

## Basic Function Definition

Use the `def` keyword to define a function:

```python
def greet():
    print("Hello, World!")

# Call the function
greet()  # Output: Hello, World!
```

## Functions with Parameters

Parameters allow functions to accept input:

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")  # Hello, Alice!
greet("Bob")    # Hello, Bob!
```

### Multiple Parameters

```python
def add(a, b):
    print(a + b)

add(3, 5)  # 8
```

## Return Values

Functions can return values using the `return` statement:

```python
def add(a, b):
    return a + b

result = add(3, 5)
print(result)  # 8
```

### Multiple Return Values

```python
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)

minimum, maximum, total = get_stats([1, 2, 3, 4, 5])
print(minimum, maximum, total)  # 1 5 15
```

## Default Parameters

Provide default values for optional parameters:

```python
def greet(name="World"):
    print(f"Hello, {name}!")

greet()         # Hello, World!
greet("Alice")  # Hello, Alice!

def power(base, exponent=2):
    return base ** exponent

print(power(3))     # 9 (3^2)
print(power(2, 4))  # 16 (2^4)
```

## Keyword Arguments

Call functions using parameter names:

```python
def describe_person(name, age, city):
    print(f"{name} is {age} years old and lives in {city}")

# Using keyword arguments (order doesn't matter)
describe_person(age=25, city="NYC", name="Alice")
```

## *args and **kwargs

Accept variable number of arguments:

```python
# *args - variable positional arguments (tuple)
def add_all(*numbers):
    return sum(numbers)

print(add_all(1, 2, 3, 4))  # 10

# **kwargs - variable keyword arguments (dict)
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="NYC")
```

## Docstrings

Document your functions:

```python
def calculate_area(length, width):
    """
    Calculate the area of a rectangle.

    Parameters:
        length (float): The length of the rectangle
        width (float): The width of the rectangle

    Returns:
        float: The area of the rectangle
    """
    return length * width
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Simple Function"
    difficulty: basic
    description: "Create a function called `say_hello` that prints 'Hello, Python!'. Then call it."
    starter_code: |
      # Define and call your function

    expected_output: "Hello, Python!"
    hints:
      - "Use def keyword to define"
      - "Don't forget the colon after function name"
      - "Call the function after defining it"
    solution: |
      def say_hello():
          print("Hello, Python!")

      say_hello()

  - title: "Function with Parameter"
    difficulty: basic
    description: "Create a function `greet(name)` that prints 'Hello, {name}!'. Call it with 'Alice'."
    starter_code: |
      # Create greeting function

    expected_output: "Hello, Alice!"
    hints:
      - "Put the parameter in parentheses"
      - "Use f-string or concatenation"
    solution: |
      def greet(name):
          print(f"Hello, {name}!")

      greet("Alice")

  - title: "Return Value"
    difficulty: intermediate
    description: "Create a function `multiply(a, b)` that returns the product. Print multiply(4, 5)."
    starter_code: |
      # Create multiply function

    expected_output: "20"
    hints:
      - "Use return statement"
      - "Print the function's return value"
    solution: |
      def multiply(a, b):
          return a * b

      print(multiply(4, 5))

  - title: "Default Parameter"
    difficulty: intermediate
    description: "Create a function `power(base, exp=2)` that returns base raised to exp. Print power(3) and power(2, 4)."
    starter_code: |
      # Create power function with default

    expected_output: |
      9
      16
    hints:
      - "Default parameter: def func(param=default)"
      - "Use ** for exponentiation"
    solution: |
      def power(base, exp=2):
          return base ** exp

      print(power(3))
      print(power(2, 4))

  - title: "Multiple Returns"
    difficulty: advanced
    description: "Create a function `min_max(numbers)` that takes a list and returns both min and max values. Test with [5, 2, 8, 1, 9]."
    starter_code: |
      # Create min_max function

    expected_output: |
      1
      9
    hints:
      - "Return multiple values: return val1, val2"
      - "Use min() and max() built-in functions"
    solution: |
      def min_max(numbers):
          return min(numbers), max(numbers)

      minimum, maximum = min_max([5, 2, 8, 1, 9])
      print(minimum)
      print(maximum)

  - title: "Sum All Arguments"
    difficulty: advanced
    description: "Create a function `sum_all(*args)` that takes any number of arguments and returns their sum. Print sum_all(1, 2, 3, 4, 5)."
    starter_code: |
      # Create sum_all function with *args

    expected_output: "15"
    hints:
      - "*args collects arguments into a tuple"
      - "Use sum() function"
    solution: |
      def sum_all(*args):
          return sum(args)

      print(sum_all(1, 2, 3, 4, 5))
```
<!-- EXERCISE_END -->
