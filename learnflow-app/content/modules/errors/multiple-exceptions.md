# Multiple Exceptions

In real-world applications, a single piece of code can fail in multiple ways. Python provides elegant mechanisms to handle different exception types with distinct error-handling logic. Understanding how to manage multiple exceptions effectively is crucial for writing robust, production-ready code that can gracefully handle various error scenarios.

Multiple exception handling allows you to provide specific responses to different types of errors, improving both debugging capabilities and user experience. You can catch multiple exceptions in separate `except` blocks, group them together, or use a combination of both approaches depending on your needs.

## Handling Multiple Exceptions Separately

The most straightforward approach is to use separate `except` blocks for each exception type. This allows you to provide specific handling logic for each error:

```python
def process_data(data, index):
    try:
        value = data[index]
        result = 100 / value
        return f"Result: {result}"
    except IndexError:
        return "Error: Index is out of range"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid data type for division"
    except Exception as e:
        return f"Unexpected error: {type(e).__name__}"

# Test cases
print(process_data([10, 20, 30], 1))      # Result: 5.0
print(process_data([10, 20, 30], 10))     # Index error
print(process_data([10, 0, 30], 1))       # Zero division error
print(process_data([10, "20", 30], 1))    # Type error
```

The order of `except` blocks matters. Python checks them from top to bottom and executes the first matching block. Always place more specific exceptions before more general ones.

## Grouping Multiple Exceptions

When multiple exceptions require the same handling logic, you can group them in a single `except` block using a tuple:

```python
def read_and_parse_file(filename, line_number):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            data = lines[line_number]
            return int(data.strip())
    except (FileNotFoundError, PermissionError) as e:
        print(f"File access error: {e}")
        return None
    except (IndexError, ValueError) as e:
        print(f"Data processing error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__} - {e}")
        return None

# Test cases
result = read_and_parse_file("data.txt", 0)
print(f"Parsed value: {result}")
```

This approach keeps your code clean and maintainable when multiple exception types should trigger the same response.

## Exception Hierarchy and Catching Strategy

Understanding Python's exception hierarchy helps you catch exceptions effectively:

```python
class DataProcessor:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def process_item(self, item):
        try:
            # Attempt to process the item
            if not isinstance(item, (int, float, str)):
                raise TypeError(f"Unsupported type: {type(item).__name__}")

            if isinstance(item, str):
                result = int(item)
            else:
                result = item

            if result < 0:
                raise ValueError("Negative values not allowed")

            return result * 2

        except (TypeError, ValueError) as e:
            # Arithmetic and type errors
            self.errors.append(f"Processing error: {e}")
            return None
        except ArithmeticError as e:
            # Catches ZeroDivisionError, OverflowError, etc.
            self.errors.append(f"Arithmetic error: {e}")
            return None
        except LookupError as e:
            # Catches IndexError, KeyError
            self.errors.append(f"Lookup error: {e}")
            return None
        except Exception as e:
            # Catches anything else
            self.errors.append(f"Unexpected error: {type(e).__name__} - {e}")
            return None

    def process_batch(self, items):
        results = []
        for item in items:
            result = self.process_item(item)
            if result is not None:
                results.append(result)
        return results

# Test
processor = DataProcessor()
data = [5, "10", -3, 15.5, [1, 2], "abc", 20]
results = processor.process_batch(data)

print(f"Results: {results}")
print(f"Errors: {processor.errors}")
```

Python exception hierarchy (partial):

| Base Exception | Common Subclasses | Use Case |
|----------------|-------------------|----------|
| `BaseException` | `Exception`, `KeyboardInterrupt`, `SystemExit` | Root of all exceptions |
| `Exception` | `ArithmeticError`, `LookupError`, `ValueError` | Regular exceptions |
| `ArithmeticError` | `ZeroDivisionError`, `OverflowError` | Math operations |
| `LookupError` | `IndexError`, `KeyError` | Sequence/mapping access |
| `OSError` | `FileNotFoundError`, `PermissionError` | Operating system errors |

## Advanced Multi-Exception Patterns

Here's a comprehensive example demonstrating sophisticated multi-exception handling in a data validation system:

```python
import re
from datetime import datetime

class ValidationError(Exception):
    """Custom base exception for validation errors"""
    pass

class EmailValidationError(ValidationError):
    pass

class AgeValidationError(ValidationError):
    pass

class UserValidator:
    def __init__(self):
        self.validation_results = {
            "valid": [],
            "errors": []
        }

    def validate_user(self, user_data):
        """
        Validate user data with comprehensive error handling.
        Returns True if valid, False otherwise.
        """
        try:
            # Extract and validate required fields
            username = user_data["username"]
            email = user_data["email"]
            age = user_data["age"]
            joined_date = user_data.get("joined_date", None)

            # Username validation
            if not isinstance(username, str) or len(username) < 3:
                raise ValueError("Username must be a string with at least 3 characters")

            # Email validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                raise EmailValidationError(f"Invalid email format: {email}")

            # Age validation
            try:
                age_int = int(age)
                if age_int < 0 or age_int > 150:
                    raise AgeValidationError(f"Age {age_int} is out of valid range (0-150)")
            except (ValueError, TypeError):
                raise AgeValidationError(f"Age must be a valid number, got: {age}")

            # Optional date validation
            if joined_date:
                try:
                    datetime.strptime(joined_date, "%Y-%m-%d")
                except ValueError:
                    raise ValueError(f"Invalid date format: {joined_date}. Expected YYYY-MM-DD")

            # All validations passed
            self.validation_results["valid"].append(username)
            return True

        except KeyError as e:
            error_msg = f"Missing required field: {e}"
            self.validation_results["errors"].append({
                "user": user_data.get("username", "Unknown"),
                "error": error_msg,
                "type": "KeyError"
            })
            return False

        except EmailValidationError as e:
            self.validation_results["errors"].append({
                "user": user_data.get("username", "Unknown"),
                "error": str(e),
                "type": "EmailValidationError"
            })
            return False

        except AgeValidationError as e:
            self.validation_results["errors"].append({
                "user": user_data.get("username", "Unknown"),
                "error": str(e),
                "type": "AgeValidationError"
            })
            return False

        except (ValueError, TypeError) as e:
            self.validation_results["errors"].append({
                "user": user_data.get("username", "Unknown"),
                "error": str(e),
                "type": type(e).__name__
            })
            return False

        except Exception as e:
            self.validation_results["errors"].append({
                "user": user_data.get("username", "Unknown"),
                "error": f"Unexpected error: {e}",
                "type": type(e).__name__
            })
            return False

# Test the validator
validator = UserValidator()

test_users = [
    {"username": "alice", "email": "alice@example.com", "age": 25, "joined_date": "2024-01-15"},
    {"username": "bob", "email": "invalid-email", "age": 30},
    {"username": "charlie", "email": "charlie@test.com", "age": "not_a_number"},
    {"email": "missing@username.com", "age": 28},
    {"username": "diana", "email": "diana@test.com", "age": 200},
]

for user in test_users:
    validator.validate_user(user)

print(f"Valid users: {validator.validation_results['valid']}")
print(f"\nErrors found: {len(validator.validation_results['errors'])}")
for error in validator.validation_results["errors"]:
    print(f"  - {error['user']}: {error['error']} ({error['type']})")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Safe Calculator"
    difficulty: basic
    description: "Create a calculator function that handles multiple types of exceptions when performing basic arithmetic."
    starter_code: |
      def calculate(operation, a, b):
          # Your code here
          pass

      # Test
      print(calculate("add", 10, 5))
      print(calculate("divide", 10, 0))
      print(calculate("multiply", "10", 5))

    expected_output: |
      15
      Error: Cannot divide by zero
      Error: Invalid operand types

    hints:
      - "Handle ZeroDivisionError for division by zero"
      - "Handle TypeError for invalid operand types"
      - "Return descriptive error messages"
    solution: |
      def calculate(operation, a, b):
          try:
              if operation == "add":
                  return a + b
              elif operation == "subtract":
                  return a - b
              elif operation == "multiply":
                  return a * b
              elif operation == "divide":
                  return a / b
              else:
                  return "Unknown operation"
          except ZeroDivisionError:
              return "Error: Cannot divide by zero"
          except TypeError:
              return "Error: Invalid operand types"

      # Test
      print(calculate("add", 10, 5))
      print(calculate("divide", 10, 0))
      print(calculate("multiply", "10", 5))

  - title: "Data Structure Access"
    difficulty: basic
    description: "Write a function that safely accesses nested data structures, handling KeyError and IndexError."
    starter_code: |
      def safe_access(data, key1, key2):
          # Your code here
          pass

      # Test
      data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
      print(safe_access(data, "users", 0))
      print(safe_access(data, "users", 5))
      print(safe_access(data, "missing", 0))

    expected_output: |
      {'name': 'Alice'}
      Error: Index out of range
      Error: Key not found

    hints:
      - "Access data[key1][key2] in a try block"
      - "Catch KeyError for missing dictionary keys"
      - "Catch IndexError for invalid list indices"
    solution: |
      def safe_access(data, key1, key2):
          try:
              return data[key1][key2]
          except KeyError:
              return "Error: Key not found"
          except IndexError:
              return "Error: Index out of range"

      # Test
      data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
      print(safe_access(data, "users", 0))
      print(safe_access(data, "users", 5))
      print(safe_access(data, "missing", 0))

  - title: "File Content Parser"
    difficulty: intermediate
    description: "Create a function that reads a file and parses each line as JSON, handling multiple exception types."
    starter_code: |
      import json

      def parse_json_file(filename):
          # Your code here
          pass

      # Test (assuming test.json exists with mixed valid/invalid JSON lines)
      result = parse_json_file("test.json")
      print(result)

    expected_output: |
      {'parsed': [{'name': 'Alice'}, {'name': 'Bob'}], 'errors': [{'line': 3, 'error': 'JSON decode error'}, {'line': 5, 'error': 'JSON decode error'}], 'file_error': None}

    hints:
      - "Handle FileNotFoundError for missing files"
      - "Handle json.JSONDecodeError for invalid JSON"
      - "Track which lines have errors"
      - "Return a dictionary with parsed data and errors"
    solution: |
      import json

      def parse_json_file(filename):
          result = {"parsed": [], "errors": [], "file_error": None}

          try:
              with open(filename, 'r') as file:
                  for line_num, line in enumerate(file, 1):
                      try:
                          data = json.loads(line.strip())
                          result["parsed"].append(data)
                      except json.JSONDecodeError:
                          result["errors"].append({
                              "line": line_num,
                              "error": "JSON decode error"
                          })
          except FileNotFoundError:
              result["file_error"] = f"File not found: {filename}"
          except PermissionError:
              result["file_error"] = f"Permission denied: {filename}"

          return result

      # Test
      result = parse_json_file("test.json")
      print(result)

  - title: "Type Converter with Statistics"
    difficulty: intermediate
    description: "Build a function that converts values to different types and tracks success/failure statistics for each exception type."
    starter_code: |
      def convert_with_stats(values, target_type):
          # Your code here
          # target_type can be 'int', 'float', or 'bool'
          pass

      # Test
      data = ["123", "45.6", "true", "invalid", "789", None, "12.34"]
      print(convert_with_stats(data, 'int'))

    expected_output: |
      {'converted': [123, 789], 'stats': {'total': 7, 'success': 2, 'ValueError': 3, 'TypeError': 1, 'AttributeError': 1}}

    hints:
      - "Use a dictionary to count each exception type"
      - "Handle ValueError, TypeError, and AttributeError"
      - "Track successful conversions separately"
    solution: |
      def convert_with_stats(values, target_type):
          result = {"converted": [], "stats": {"total": len(values), "success": 0}}

          type_map = {
              'int': int,
              'float': float,
              'bool': bool
          }

          converter = type_map.get(target_type, int)

          for value in values:
              try:
                  converted = converter(value)
                  result["converted"].append(converted)
                  result["stats"]["success"] += 1
              except ValueError:
                  result["stats"]["ValueError"] = result["stats"].get("ValueError", 0) + 1
              except TypeError:
                  result["stats"]["TypeError"] = result["stats"].get("TypeError", 0) + 1
              except AttributeError:
                  result["stats"]["AttributeError"] = result["stats"].get("AttributeError", 0) + 1

          return result

      # Test
      data = ["123", "45.6", "true", "invalid", "789", None, "12.34"]
      print(convert_with_stats(data, 'int'))

  - title: "Database Query Simulator"
    difficulty: advanced
    description: "Create a simulated database query system that handles connection errors, query errors, and data validation errors differently."
    starter_code: |
      class ConnectionError(Exception):
          pass

      class QueryError(Exception):
          pass

      class Database:
          def __init__(self):
              self.connected = False
              self.data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}

          def connect(self, connection_string):
              if "valid" not in connection_string:
                  raise ConnectionError("Invalid connection string")
              self.connected = True

          def query(self, table, id):
              # Your code here
              pass

      # Test
      db = Database()
      print(db.query("users", 1))
      print(db.query("products", 1))
      print(db.query("users", 99))

    expected_output: |
      {'status': 'error', 'message': 'Not connected to database', 'data': None}
      {'status': 'error', 'message': 'Not connected to database', 'data': None}
      {'status': 'error', 'message': 'Not connected to database', 'data': None}

    hints:
      - "Check if connected before querying"
      - "Handle ConnectionError, QueryError, and KeyError separately"
      - "Return a status dictionary with error information"
    solution: |
      class ConnectionError(Exception):
          pass

      class QueryError(Exception):
          pass

      class Database:
          def __init__(self):
              self.connected = False
              self.data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}

          def connect(self, connection_string):
              if "valid" not in connection_string:
                  raise ConnectionError("Invalid connection string")
              self.connected = True

          def query(self, table, id):
              try:
                  if not self.connected:
                      raise ConnectionError("Not connected to database")

                  if table not in self.data:
                      raise QueryError(f"Table '{table}' does not exist")

                  for record in self.data[table]:
                      if record["id"] == id:
                          return {"status": "success", "message": "", "data": record}

                  raise QueryError(f"Record with id {id} not found")

              except ConnectionError as e:
                  return {"status": "error", "message": str(e), "data": None}
              except QueryError as e:
                  return {"status": "error", "message": str(e), "data": None}
              except (KeyError, TypeError) as e:
                  return {"status": "error", "message": f"Data error: {e}", "data": None}

      # Test
      db = Database()
      print(db.query("users", 1))
      print(db.query("products", 1))
      print(db.query("users", 99))

  - title: "Configuration Loader"
    difficulty: advanced
    description: "Build a configuration loader that handles multiple file formats (JSON, invalid syntax) and validates configuration values."
    starter_code: |
      import json

      def load_config(filename, required_keys):
          # Your code here
          # Return: {"status": str, "config": dict, "errors": list}
          pass

      # Test
      print(load_config("config.json", ["host", "port", "timeout"]))

    expected_output: |
      {'status': 'partial', 'config': {'host': 'localhost'}, 'errors': [{'type': 'FileNotFoundError', 'message': 'Configuration file not found'}, {'type': 'ValidationError', 'message': 'Missing required keys: port, timeout'}]}

    hints:
      - "Handle FileNotFoundError, json.JSONDecodeError, and KeyError"
      - "Validate that all required keys exist in the loaded config"
      - "Return partial results when possible"
      - "Track different error types in the errors list"
    solution: |
      import json

      def load_config(filename, required_keys):
          result = {
              "status": "success",
              "config": {},
              "errors": []
          }

          try:
              with open(filename, 'r') as file:
                  try:
                      config = json.load(file)

                      # Validate required keys
                      missing_keys = [key for key in required_keys if key not in config]

                      if missing_keys:
                          result["errors"].append({
                              "type": "ValidationError",
                              "message": f"Missing required keys: {', '.join(missing_keys)}"
                          })
                          result["status"] = "partial"

                      # Extract available keys
                      for key in required_keys:
                          if key in config:
                              result["config"][key] = config[key]

                  except json.JSONDecodeError as e:
                      result["errors"].append({
                          "type": "JSONDecodeError",
                          "message": f"Invalid JSON: {e.msg}"
                      })
                      result["status"] = "failed"

          except FileNotFoundError:
              result["errors"].append({
                  "type": "FileNotFoundError",
                  "message": "Configuration file not found"
              })
              result["status"] = "partial"

              # Try to provide defaults or partial config
              result["config"] = {"host": "localhost"}

          except PermissionError:
              result["errors"].append({
                  "type": "PermissionError",
                  "message": "Permission denied reading config file"
              })
              result["status"] = "failed"

          # Add validation error if we have partial config
          if result["config"] and result["status"] == "partial":
              missing = [k for k in required_keys if k not in result["config"]]
              if missing and not any(e["type"] == "ValidationError" for e in result["errors"]):
                  result["errors"].append({
                      "type": "ValidationError",
                      "message": f"Missing required keys: {', '.join(missing)}"
                  })

          return result

      # Test
      print(load_config("config.json", ["host", "port", "timeout"]))
```
<!-- EXERCISE_END -->
