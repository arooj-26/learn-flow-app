# Type Conversion in Python

Type conversion (also called type casting) is the process of converting a value from one data type to another. Python provides both implicit (automatic) and explicit (manual) type conversion, which are essential for data manipulation and ensuring type compatibility.

## Implicit Type Conversion

Python automatically converts data types when needed to prevent data loss:

```python
# Integer + Float = Float (automatic promotion)
result = 5 + 3.2        # 8.2 (int promoted to float)
mixed = 10 * 2.5        # 25.0 (result is float)

# Boolean to Integer (True=1, False=0)
calculation = True + 5   # 6
another = False * 10     # 0

# Automatic type checking
num_int = 42
num_float = 3.14
result = num_int + num_float  # 45.14 (float)
print(type(result))           # <class 'float'>
```

## Explicit Type Conversion Functions

Python provides built-in functions for explicit type conversion:

| Function | Description | Example |
|----------|-------------|---------|
| `int()` | Convert to integer | `int("42")` → `42` |
| `float()` | Convert to float | `float("3.14")` → `3.14` |
| `str()` | Convert to string | `str(42)` → `"42"` |
| `bool()` | Convert to boolean | `bool(1)` → `True` |
| `list()` | Convert to list | `list("abc")` → `['a', 'b', 'c']` |
| `tuple()` | Convert to tuple | `tuple([1, 2])` → `(1, 2)` |
| `set()` | Convert to set | `set([1, 2, 2])` → `{1, 2}` |
| `dict()` | Convert to dictionary | Complex conversion |

## String to Number Conversion

Converting strings to numeric types is common when processing user input or file data:

```python
# String to integer
age_str = "25"
age_int = int(age_str)           # 25
print(type(age_int))             # <class 'int'>

# String to float
price_str = "19.99"
price_float = float(price_str)   # 19.99

# Handling different number formats
hex_str = "FF"
hex_int = int(hex_str, 16)       # 255 (hexadecimal to decimal)
binary_str = "1010"
binary_int = int(binary_str, 2)  # 10 (binary to decimal)
octal_str = "17"
octal_int = int(octal_str, 8)    # 15 (octal to decimal)

# Error handling for invalid conversions
try:
    invalid = int("abc")          # ValueError!
except ValueError as e:
    print(f"Conversion error: {e}")

# Safe conversion with validation
user_input = "42"
if user_input.isdigit():
    number = int(user_input)
else:
    print("Invalid number")
```

## Number to String Conversion

Converting numbers to strings is essential for output formatting and concatenation:

```python
# Basic number to string
age = 25
age_str = str(age)               # "25"
price = 19.99
price_str = str(price)           # "19.99"

# Formatting with f-strings (preferred method)
name = "Alice"
age = 25
message = f"{name} is {age} years old"  # "Alice is 25 years old"

# Number formatting
pi = 3.14159
formatted = f"{pi:.2f}"          # "3.14" (2 decimal places)
percentage = 0.847
percent_str = f"{percentage:.1%}"  # "84.7%"

# Different number bases
number = 255
hex_str = hex(number)            # "0xff"
binary_str = bin(number)         # "0b11111111"
octal_str = oct(number)          # "0o377"

# Remove prefix if needed
hex_clean = hex(number)[2:]      # "ff"
binary_clean = bin(number)[2:]   # "11111111"
```

## Boolean Conversion

Understanding how Python evaluates truthiness is crucial:

```python
# Explicit boolean conversion
bool(1)           # True
bool(0)           # False
bool(42)          # True (any non-zero number)
bool(-5)          # True
bool(0.0)         # False
bool(3.14)        # True

# String to boolean
bool("Hello")     # True (non-empty string)
bool("")          # False (empty string)
bool("False")     # True! (non-empty string, even if it says "False")

# Collection to boolean
bool([1, 2, 3])   # True (non-empty list)
bool([])          # False (empty list)
bool({"key": "value"})  # True (non-empty dict)
bool({})          # False (empty dict)

# None to boolean
bool(None)        # False

# Falsy values in Python
falsy_values = [False, 0, 0.0, "", None, [], {}, set()]
for value in falsy_values:
    print(f"{repr(value):15} is {bool(value)}")
```

## Collection Type Conversions

Converting between different collection types:

```python
# List conversions
string = "hello"
char_list = list(string)         # ['h', 'e', 'l', 'l', 'o']
number_tuple = (1, 2, 3)
number_list = list(number_tuple) # [1, 2, 3]

# Tuple conversions
list_data = [1, 2, 3]
tuple_data = tuple(list_data)    # (1, 2, 3)
string_tuple = tuple("abc")      # ('a', 'b', 'c')

# Set conversions (removes duplicates)
duplicate_list = [1, 2, 2, 3, 3, 3]
unique_set = set(duplicate_list) # {1, 2, 3}
back_to_list = list(unique_set)  # [1, 2, 3] (order not guaranteed)

# Dictionary conversions
pairs = [("a", 1), ("b", 2), ("c", 3)]
dict_from_pairs = dict(pairs)    # {'a': 1, 'b': 2, 'c': 3}
keys = list(dict_from_pairs.keys())    # ['a', 'b', 'c']
values = list(dict_from_pairs.values()) # [1, 2, 3]
```

## Advanced Conversion Techniques

Handling complex conversion scenarios:

```python
# Converting user input safely
def safe_int_input(prompt, default=0):
    """Safely convert user input to integer"""
    user_input = input(prompt)
    try:
        return int(user_input)
    except ValueError:
        return default

# Converting with validation
def convert_to_positive_int(value):
    """Convert to positive integer or raise error"""
    num = int(value)
    if num <= 0:
        raise ValueError("Must be positive")
    return num

# Multiple type conversions
mixed_data = ["42", "3.14", "true", "123"]
integers = [int(float(x)) if '.' in x else int(x)
            for x in mixed_data if x.replace('.', '').isdigit()]
# [42, 3, 123]

# JSON-like string parsing
import json
json_string = '{"name": "Alice", "age": 25}'
data_dict = json.loads(json_string)
# {'name': 'Alice', 'age': 25}

# Converting between numeric types with rounding
float_num = 3.7
int_truncated = int(float_num)   # 3 (truncates)
int_rounded = round(float_num)   # 4 (rounds)
```

## Best Practices for Type Conversion

1. **Validate before converting**: Check if conversion is possible to avoid errors
2. **Use try-except**: Handle conversion errors gracefully
3. **Be explicit**: Don't rely on implicit conversion for clarity
4. **Preserve precision**: Be aware of data loss when converting float to int
5. **Use appropriate methods**: Choose the right conversion function for your needs

```python
# Good: Validate before converting
user_age = "25"
if user_age.isdigit():
    age = int(user_age)
else:
    age = 0  # Default value

# Good: Use try-except for safety
try:
    price = float(input("Enter price: "))
except ValueError:
    print("Invalid price entered")
    price = 0.0

# Good: Be explicit about conversions
total = int(10.5) + int(5.3)  # 15 (explicit truncation)

# Avoid: Implicit conversions that may be unclear
result = 10 / 3  # 3.333... (implicit float conversion)
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "String to Integer"
    difficulty: basic
    description: "Convert the string '100' to an integer, add 50 to it, and print the result."
    starter_code: |
      num_str = "100"
      # Convert and calculate

    expected_output: "150"
    hints:
      - "Use int() to convert string to integer"
      - "Then add 50 to the converted value"
    solution: |
      num_str = "100"
      num_int = int(num_str)
      result = num_int + 50
      print(result)

  - title: "Number to String"
    difficulty: basic
    description: "Create an integer variable `score = 95`. Convert it to a string and concatenate it with the text 'Your score: ' to print 'Your score: 95'."
    starter_code: |
      score = 95
      # Convert and concatenate

    expected_output: "Your score: 95"
    hints:
      - "Use str() to convert the number to string"
      - "Use + or an f-string to combine strings"
    solution: |
      score = 95
      result = "Your score: " + str(score)
      print(result)

  - title: "Float to Integer"
    difficulty: intermediate
    description: "Convert the float 7.8 to an integer (truncating the decimal), then multiply by 3 and print the result."
    starter_code: |
      number = 7.8
      # Convert and calculate

    expected_output: "21"
    hints:
      - "Use int() to truncate the float to an integer"
      - "int() removes the decimal part without rounding"
    solution: |
      number = 7.8
      int_number = int(number)
      result = int_number * 3
      print(result)

  - title: "Truthiness Checker"
    difficulty: intermediate
    description: "Convert these values to boolean and print the result: 0, 'hello', [], 42. Print each on a new line."
    starter_code: |
      # Convert each value to boolean
      values = [0, "hello", [], 42]

    expected_output: |
      False
      True
      False
      True
    hints:
      - "Use bool() to convert each value"
      - "Use a loop or print each separately"
      - "Empty collections and 0 are False, non-empty are True"
    solution: |
      values = [0, "hello", [], 42]
      for value in values:
          print(bool(value))

  - title: "Binary String Converter"
    difficulty: advanced
    description: "Convert the binary string '1010' to a decimal integer, add 5, then convert back to binary (without '0b' prefix). Print the result."
    starter_code: |
      binary_str = "1010"
      # Convert to decimal, add 5, convert back to binary

    expected_output: "1111"
    hints:
      - "Use int(binary_str, 2) to convert binary to decimal"
      - "Use bin() to convert back to binary"
      - "Use slicing [2:] to remove the '0b' prefix"
    solution: |
      binary_str = "1010"
      decimal = int(binary_str, 2)
      result = decimal + 5
      binary_result = bin(result)[2:]
      print(binary_result)

  - title: "Safe User Input Converter"
    difficulty: advanced
    description: "Given user_input = '25.5', safely convert it to a float, multiply by 2, round to 1 decimal place, and print. If conversion fails, print 'Invalid input'."
    starter_code: |
      user_input = "25.5"
      # Safely convert and calculate

    expected_output: "51.0"
    hints:
      - "Use try-except to catch ValueError"
      - "Convert to float, multiply, then use round()"
      - "For invalid input, the except block should print the error message"
    solution: |
      user_input = "25.5"
      try:
          number = float(user_input)
          result = round(number * 2, 1)
          print(result)
      except ValueError:
          print("Invalid input")
```
<!-- EXERCISE_END -->
