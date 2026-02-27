# Try & Except

Exception handling is a fundamental concept in Python that allows you to gracefully manage errors and unexpected situations in your code. Instead of letting your program crash when an error occurs, you can catch and handle these exceptions, providing a better user experience and making your applications more robust.

The `try` and `except` blocks form the foundation of Python's exception handling mechanism. Code that might raise an exception is placed in the `try` block, while the code that handles the exception goes in the `except` block. This allows your program to continue running even when errors occur.

## Basic Try-Except Syntax

The most basic form of exception handling uses a `try` block to wrap potentially problematic code and an `except` block to handle any exceptions that occur:

```python
def divide_numbers(a, b):
    try:
        result = a / b
        return result
    except:
        print("An error occurred during division")
        return None

# Test the function
print(divide_numbers(10, 2))   # Output: 5.0
print(divide_numbers(10, 0))   # Output: An error occurred during division, None
```

While the bare `except` clause catches all exceptions, it's generally better to catch specific exceptions to handle different error types appropriately.

## Catching Specific Exceptions

Python provides many built-in exception types. Catching specific exceptions allows you to handle different errors in different ways:

```python
def safe_conversion(value):
    try:
        number = int(value)
        reciprocal = 1 / number
        return reciprocal
    except ValueError:
        print(f"'{value}' cannot be converted to an integer")
        return None
    except ZeroDivisionError:
        print("Cannot calculate reciprocal of zero")
        return None

# Test cases
print(safe_conversion("5"))      # Output: 0.2
print(safe_conversion("abc"))    # ValueError caught
print(safe_conversion("0"))      # ZeroDivisionError caught
```

## Accessing Exception Information

You can access the exception object to get detailed information about what went wrong:

```python
def process_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            return len(content)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"The file '{filename}' was not found")
        return 0
    except PermissionError as e:
        print(f"Error: {e}")
        print(f"No permission to read '{filename}'")
        return 0
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__} - {e}")
        return 0

# Test
length = process_file("nonexistent.txt")
print(f"File length: {length}")
```

Common exception types and their uses:

| Exception Type | When It Occurs | Example |
|---------------|----------------|---------|
| `ValueError` | Invalid value for operation | `int("abc")` |
| `TypeError` | Wrong type for operation | `"string" + 5` |
| `KeyError` | Key not found in dictionary | `my_dict["missing_key"]` |
| `IndexError` | Index out of range | `my_list[100]` |
| `FileNotFoundError` | File doesn't exist | `open("missing.txt")` |
| `ZeroDivisionError` | Division by zero | `10 / 0` |
| `AttributeError` | Attribute doesn't exist | `"string".nonexistent()` |

## Practical Real-World Example

Here's a comprehensive example showing how to build a robust data processing function:

```python
def process_user_data(data_dict):
    """
    Process user data with comprehensive error handling.
    Returns a tuple: (success: bool, result: dict, error_message: str)
    """
    try:
        # Validate required fields
        name = data_dict["name"]
        age = int(data_dict["age"])
        email = data_dict["email"]

        # Validate age range
        if age < 0 or age > 150:
            raise ValueError("Age must be between 0 and 150")

        # Process the data
        processed = {
            "name": name.strip().title(),
            "age": age,
            "email": email.lower().strip(),
            "is_adult": age >= 18
        }

        return True, processed, ""

    except KeyError as e:
        return False, {}, f"Missing required field: {e}"
    except ValueError as e:
        return False, {}, f"Invalid value: {e}"
    except AttributeError as e:
        return False, {}, f"Invalid data type: {e}"
    except Exception as e:
        return False, {}, f"Unexpected error: {type(e).__name__} - {e}"

# Test cases
test_data = [
    {"name": "john doe", "age": "25", "email": "JOHN@EMAIL.COM"},
    {"name": "jane", "age": "invalid"},
    {"age": "30", "email": "test@test.com"},
    {"name": "bob", "age": "-5", "email": "bob@test.com"}
]

for data in test_data:
    success, result, error = process_user_data(data)
    if success:
        print(f"Success: {result}")
    else:
        print(f"Failed: {error}")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Safe Division Calculator"
    difficulty: basic
    description: "Create a function that safely divides two numbers and handles division by zero."
    starter_code: |
      def safe_divide(a, b):
          # Your code here
          pass

      # Test your function
      print(safe_divide(10, 2))
      print(safe_divide(10, 0))

    expected_output: |
      5.0
      Error: Cannot divide by zero
      None

    hints:
      - "Use a try-except block to catch ZeroDivisionError"
      - "Return None when division by zero occurs"
    solution: |
      def safe_divide(a, b):
          try:
              return a / b
          except ZeroDivisionError:
              print("Error: Cannot divide by zero")
              return None

      # Test your function
      print(safe_divide(10, 2))
      print(safe_divide(10, 0))

  - title: "List Element Accessor"
    difficulty: basic
    description: "Write a function that safely accesses a list element by index, handling IndexError."
    starter_code: |
      def get_element(lst, index):
          # Your code here
          pass

      # Test
      my_list = [1, 2, 3, 4, 5]
      print(get_element(my_list, 2))
      print(get_element(my_list, 10))

    expected_output: |
      3
      Index 10 is out of range
      None

    hints:
      - "Catch IndexError when the index is out of range"
      - "Return None for invalid indices"
    solution: |
      def get_element(lst, index):
          try:
              return lst[index]
          except IndexError:
              print(f"Index {index} is out of range")
              return None

      # Test
      my_list = [1, 2, 3, 4, 5]
      print(get_element(my_list, 2))
      print(get_element(my_list, 10))

  - title: "Dictionary Data Extractor"
    difficulty: intermediate
    description: "Create a function that extracts multiple values from a dictionary, handling missing keys gracefully."
    starter_code: |
      def extract_data(data_dict, keys):
          # Your code here
          pass

      # Test
      person = {"name": "Alice", "age": 30, "city": "NYC"}
      print(extract_data(person, ["name", "age", "country"]))

    expected_output: |
      {'name': 'Alice', 'age': 30, 'country': None}

    hints:
      - "Use a try-except block inside a loop for each key"
      - "Set the value to None for missing keys"
    solution: |
      def extract_data(data_dict, keys):
          result = {}
          for key in keys:
              try:
                  result[key] = data_dict[key]
              except KeyError:
                  result[key] = None
          return result

      # Test
      person = {"name": "Alice", "age": 30, "city": "NYC"}
      print(extract_data(person, ["name", "age", "country"]))

  - title: "Type Converter"
    difficulty: intermediate
    description: "Write a function that attempts to convert a list of strings to integers, returning converted values and error information."
    starter_code: |
      def convert_to_integers(string_list):
          # Your code here
          pass

      # Test
      strings = ["123", "456", "abc", "789", "12.5"]
      print(convert_to_integers(strings))

    expected_output: |
      {'converted': [123, 456, 789], 'errors': [{'index': 2, 'value': 'abc', 'error': 'ValueError'}, {'index': 4, 'value': '12.5', 'error': 'ValueError'}]}

    hints:
      - "Loop through the list with enumerate to track indices"
      - "Store successfully converted values and error information separately"
    solution: |
      def convert_to_integers(string_list):
          result = {"converted": [], "errors": []}
          for index, value in enumerate(string_list):
              try:
                  converted = int(value)
                  result["converted"].append(converted)
              except ValueError:
                  result["errors"].append({
                      "index": index,
                      "value": value,
                      "error": "ValueError"
                  })
          return result

      # Test
      strings = ["123", "456", "abc", "789", "12.5"]
      print(convert_to_integers(strings))

  - title: "Robust JSON Parser"
    difficulty: advanced
    description: "Create a function that parses JSON data with comprehensive error handling for multiple exception types."
    starter_code: |
      import json

      def parse_json_safely(json_string):
          # Your code here
          pass

      # Test
      print(parse_json_safely('{"name": "Alice", "age": 30}'))
      print(parse_json_safely('invalid json'))
      print(parse_json_safely(''))

    expected_output: |
      (True, {'name': 'Alice', 'age': 30}, '')
      (False, None, 'JSON decode error: Expecting value: line 1 column 1 (char 0)')
      (False, None, 'JSON decode error: Expecting value: line 1 column 1 (char 0)')

    hints:
      - "Import json module and use json.loads()"
      - "Catch json.JSONDecodeError for invalid JSON"
      - "Return a tuple with success status, data, and error message"
    solution: |
      import json

      def parse_json_safely(json_string):
          try:
              data = json.loads(json_string)
              return True, data, ""
          except json.JSONDecodeError as e:
              return False, None, f"JSON decode error: {e.msg}"
          except TypeError as e:
              return False, None, f"Type error: {e}"
          except Exception as e:
              return False, None, f"Unexpected error: {e}"

      # Test
      print(parse_json_safely('{"name": "Alice", "age": 30}'))
      print(parse_json_safely('invalid json'))
      print(parse_json_safely(''))

  - title: "File Data Processor"
    difficulty: advanced
    description: "Build a function that reads a file, processes each line as a calculation, and handles multiple types of errors."
    starter_code: |
      def process_calculations(filename):
          # Your code here
          # File format: each line contains "num1 operator num2"
          # Example: "10 + 5"
          pass

      # Test (create a test file first)
      # test_calc.txt contents:
      # 10 + 5
      # 20 - 8
      # 15 * 2
      # 10 / 0
      # invalid
      print(process_calculations("test_calc.txt"))

    expected_output: |
      {'results': [15.0, 12.0, 30.0], 'errors': [{'line': 4, 'content': '10 / 0', 'error': 'Division by zero'}, {'line': 5, 'content': 'invalid', 'error': 'Invalid format'}], 'file_error': None}

    hints:
      - "Handle FileNotFoundError for missing files"
      - "Parse each line and use eval() or manual operators"
      - "Catch ZeroDivisionError and ValueError for calculation errors"
      - "Track line numbers for error reporting"
    solution: |
      def process_calculations(filename):
          result = {"results": [], "errors": [], "file_error": None}

          try:
              with open(filename, 'r') as file:
                  for line_num, line in enumerate(file, 1):
                      line = line.strip()
                      try:
                          parts = line.split()
                          if len(parts) != 3:
                              raise ValueError("Invalid format")

                          num1 = float(parts[0])
                          operator = parts[1]
                          num2 = float(parts[2])

                          if operator == '+':
                              res = num1 + num2
                          elif operator == '-':
                              res = num1 - num2
                          elif operator == '*':
                              res = num1 * num2
                          elif operator == '/':
                              if num2 == 0:
                                  raise ZeroDivisionError()
                              res = num1 / num2
                          else:
                              raise ValueError("Invalid operator")

                          result["results"].append(res)

                      except ZeroDivisionError:
                          result["errors"].append({
                              "line": line_num,
                              "content": line,
                              "error": "Division by zero"
                          })
                      except (ValueError, IndexError):
                          result["errors"].append({
                              "line": line_num,
                              "content": line,
                              "error": "Invalid format"
                          })

          except FileNotFoundError:
              result["file_error"] = f"File '{filename}' not found"
          except PermissionError:
              result["file_error"] = f"No permission to read '{filename}'"

          return result

      # Test (create a test file first)
      print(process_calculations("test_calc.txt"))
```
<!-- EXERCISE_END -->
