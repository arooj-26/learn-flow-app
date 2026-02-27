# Raising Exceptions

Raising exceptions is a powerful technique that allows you to signal error conditions and enforce business logic in your applications. Rather than allowing invalid states to propagate silently through your code, explicitly raising exceptions makes your code more predictable, easier to debug, and forces calling code to handle error conditions appropriately.

Understanding when and how to raise exceptions is crucial for writing robust Python applications. Well-placed exception raising creates clear contracts between functions, makes error handling explicit, and prevents subtle bugs from occurring due to invalid data or states.

## Basic Exception Raising

The `raise` statement is used to trigger an exception at any point in your code. You can raise built-in exceptions or custom ones:

```python
def divide_positive_numbers(a, b):
    """
    Divides two numbers, but only accepts positive values.
    """
    if a <= 0 or b <= 0:
        raise ValueError("Both numbers must be positive")

    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")

    return a / b

# Test cases
try:
    print(divide_positive_numbers(10, 2))   # Works: 5.0
    print(divide_positive_numbers(-10, 2))  # Raises ValueError
except ValueError as e:
    print(f"Error: {e}")

try:
    print(divide_positive_numbers(10, 0))   # Raises ZeroDivisionError
except ZeroDivisionError as e:
    print(f"Error: {e}")
```

Common built-in exceptions to raise:

| Exception | When to Use | Example |
|-----------|-------------|---------|
| `ValueError` | Invalid value for operation | Non-positive number when positive required |
| `TypeError` | Wrong type provided | String when number expected |
| `KeyError` | Missing dictionary key | Required configuration key not found |
| `IndexError` | Invalid sequence index | Accessing beyond list bounds |
| `RuntimeError` | Generic runtime error | Invalid state for operation |
| `NotImplementedError` | Abstract method not implemented | Subclass must override method |
| `AssertionError` | Assertion failed | Internal invariant violated |

## Re-raising Exceptions

Sometimes you want to catch an exception, perform some action (like logging), and then re-raise it:

```python
import logging

def process_critical_data(data):
    """
    Process data with logging before re-raising exceptions.
    """
    try:
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary")

        if "id" not in data:
            raise KeyError("Missing required field: id")

        # Process the data
        result = data["id"] * 2
        return result

    except (TypeError, KeyError) as e:
        # Log the error
        logging.error(f"Data processing failed: {e}")
        logging.error(f"Problematic data: {data}")

        # Re-raise the same exception
        raise

# Test
try:
    result = process_critical_data({"name": "Alice"})
except KeyError as e:
    print(f"Caught re-raised exception: {e}")
```

You can also raise a different exception while preserving the original:

```python
def convert_config_value(value):
    """Convert configuration value with exception chaining."""
    try:
        return int(value)
    except ValueError as e:
        # Raise a new exception with context from the original
        raise RuntimeError(f"Configuration error: invalid integer value '{value}'") from e

# Test
try:
    result = convert_config_value("abc")
except RuntimeError as e:
    print(f"Error: {e}")
    print(f"Caused by: {e.__cause__}")
```

## Validation and Input Checking

Raising exceptions is excellent for input validation and enforcing preconditions:

```python
class User:
    """User class with validated attributes."""

    def __init__(self, username, email, age):
        self.username = self._validate_username(username)
        self.email = self._validate_email(email)
        self.age = self._validate_age(age)

    def _validate_username(self, username):
        if not isinstance(username, str):
            raise TypeError("Username must be a string")

        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")

        if not username.isalnum():
            raise ValueError("Username must contain only letters and numbers")

        return username

    def _validate_email(self, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string")

        if "@" not in email or "." not in email:
            raise ValueError("Invalid email format")

        return email.lower()

    def _validate_age(self, age):
        if not isinstance(age, (int, float)):
            raise TypeError("Age must be a number")

        age = int(age)

        if age < 0:
            raise ValueError("Age cannot be negative")

        if age > 150:
            raise ValueError("Age seems unrealistic")

        return age

# Test cases
try:
    user1 = User("alice123", "alice@example.com", 25)
    print(f"Created user: {user1.username}")

    user2 = User("ab", "invalid-email", 30)  # Multiple validation errors possible
except (ValueError, TypeError) as e:
    print(f"Validation error: {e}")
```

## Conditional Exception Raising

Raise exceptions based on complex business logic conditions:

```python
class BankAccount:
    """Bank account with transaction validation."""

    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance
        self.is_active = True
        self.daily_withdrawal_limit = 1000
        self.daily_withdrawn = 0

    def withdraw(self, amount):
        """
        Withdraw money with comprehensive validation.
        """
        # Check account status
        if not self.is_active:
            raise RuntimeError("Account is inactive")

        # Validate amount
        if not isinstance(amount, (int, float)):
            raise TypeError(f"Amount must be a number, got {type(amount).__name__}")

        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        # Check balance
        if amount > self.balance:
            raise ValueError(
                f"Insufficient funds. Balance: ${self.balance:.2f}, "
                f"Requested: ${amount:.2f}"
            )

        # Check daily limit
        if self.daily_withdrawn + amount > self.daily_withdrawal_limit:
            remaining = self.daily_withdrawal_limit - self.daily_withdrawn
            raise ValueError(
                f"Daily withdrawal limit exceeded. "
                f"Limit: ${self.daily_withdrawal_limit}, "
                f"Already withdrawn: ${self.daily_withdrawn:.2f}, "
                f"Remaining: ${remaining:.2f}"
            )

        # All checks passed, process withdrawal
        self.balance -= amount
        self.daily_withdrawn += amount
        return self.balance

    def deposit(self, amount):
        """Deposit money with validation."""
        if not self.is_active:
            raise RuntimeError("Account is inactive")

        if not isinstance(amount, (int, float)):
            raise TypeError(f"Amount must be a number, got {type(amount).__name__}")

        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self.balance += amount
        return self.balance

# Test the account
account = BankAccount("12345", balance=500)

try:
    print(f"Balance: ${account.balance}")
    account.withdraw(200)
    print(f"After withdrawal: ${account.balance}")
    account.withdraw(400)  # Will raise ValueError
except ValueError as e:
    print(f"Transaction failed: {e}")

try:
    account.withdraw("100")  # Will raise TypeError
except TypeError as e:
    print(f"Invalid input: {e}")
```

## Defensive Programming with Assertions vs Exceptions

Understanding when to use `raise` vs `assert`:

```python
def process_user_data(user_data, admin_mode=False):
    """
    Demonstrates difference between assertions and exceptions.

    Assertions: Check internal invariants (can be disabled with -O flag)
    Exceptions: Check external conditions (always active)
    """

    # Use exceptions for external input validation
    if not isinstance(user_data, dict):
        raise TypeError("user_data must be a dictionary")

    if "user_id" not in user_data:
        raise ValueError("user_id is required")

    # Use assertions for internal consistency checks
    assert isinstance(admin_mode, bool), "admin_mode must be boolean"
    assert hasattr(user_data, "get"), "user_data must support .get() method"

    # Process data
    user_id = user_data["user_id"]

    # Exception for business logic violation
    if user_id < 0:
        raise ValueError(f"Invalid user_id: {user_id}")

    # Assertion for programmer error (this should never happen)
    assert user_id is not None, "user_id became None unexpectedly"

    return {"processed": True, "user_id": user_id}

# When to use each:
# - raise Exception: External errors, validation, business rules
# - assert: Internal checks, debugging, invariants

try:
    # Valid call
    result = process_user_data({"user_id": 123})
    print(f"Result: {result}")

    # Invalid call - will raise ValueError
    result = process_user_data({"user_id": -1})
except ValueError as e:
    print(f"Business rule violation: {e}")
```

Comparison table:

| Feature | `raise Exception` | `assert` |
|---------|-------------------|----------|
| Purpose | Handle expected errors | Check programmer assumptions |
| Production | Always active | Can be disabled with `-O` |
| Use for | Input validation, business rules | Internal invariants, debugging |
| Performance | Always checked | Can be optimized away |
| Error type | Any exception | Always AssertionError |

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Temperature Validator"
    difficulty: basic
    description: "Create a function that validates temperature values and raises ValueError for invalid ranges."
    starter_code: |
      def validate_temperature(temp, unit):
          # Your code here
          # Celsius: -273.15 to 1000
          # Fahrenheit: -459.67 to 1832
          pass

      # Test
      print(validate_temperature(25, "C"))
      print(validate_temperature(-300, "C"))

    expected_output: |
      25
      Error: Temperature -300 C is below absolute zero (-273.15 C)

    hints:
      - "Check if temperature is below absolute zero for each unit"
      - "Raise ValueError with descriptive message"
      - "Return the temperature if valid"
    solution: |
      def validate_temperature(temp, unit):
          if unit == "C":
              if temp < -273.15:
                  raise ValueError(f"Temperature {temp} C is below absolute zero (-273.15 C)")
              if temp > 1000:
                  raise ValueError(f"Temperature {temp} C is above maximum (1000 C)")
          elif unit == "F":
              if temp < -459.67:
                  raise ValueError(f"Temperature {temp} F is below absolute zero (-459.67 F)")
              if temp > 1832:
                  raise ValueError(f"Temperature {temp} F is above maximum (1832 F)")
          else:
              raise ValueError(f"Unknown unit: {unit}")
          return temp

      # Test
      print(validate_temperature(25, "C"))
      try:
          print(validate_temperature(-300, "C"))
      except ValueError as e:
          print(f"Error: {e}")

  - title: "List Index Validator"
    difficulty: basic
    description: "Write a function that raises IndexError with helpful messages when accessing invalid list indices."
    starter_code: |
      def safe_get(lst, index):
          # Your code here
          pass

      # Test
      my_list = [10, 20, 30, 40, 50]
      print(safe_get(my_list, 2))
      print(safe_get(my_list, 10))

    expected_output: |
      30
      Error: Index 10 is out of range (list size: 5)

    hints:
      - "Check if index is negative or >= length"
      - "Raise IndexError with list size information"
      - "Return the element if index is valid"
    solution: |
      def safe_get(lst, index):
          if index < 0 or index >= len(lst):
              raise IndexError(f"Index {index} is out of range (list size: {len(lst)})")
          return lst[index]

      # Test
      my_list = [10, 20, 30, 40, 50]
      print(safe_get(my_list, 2))
      try:
          print(safe_get(my_list, 10))
      except IndexError as e:
          print(f"Error: {e}")

  - title: "Password Validator"
    difficulty: intermediate
    description: "Create a password validator that raises specific ValueErrors for different validation failures."
    starter_code: |
      def validate_password(password):
          # Your code here
          # Rules: min 8 chars, at least 1 digit, 1 uppercase, 1 lowercase
          pass

      # Test
      print(validate_password("SecurePass123"))
      print(validate_password("weak"))
      print(validate_password("nouppercase123"))

    expected_output: |
      Password is valid
      Error: Password must be at least 8 characters long
      Error: Password must contain at least one uppercase letter

    hints:
      - "Check length first"
      - "Use any() with generator expressions for character checks"
      - "Raise ValueError for each validation failure"
      - "Return success message if all checks pass"
    solution: |
      def validate_password(password):
          if len(password) < 8:
              raise ValueError("Password must be at least 8 characters long")

          if not any(c.isdigit() for c in password):
              raise ValueError("Password must contain at least one digit")

          if not any(c.isupper() for c in password):
              raise ValueError("Password must contain at least one uppercase letter")

          if not any(c.islower() for c in password):
              raise ValueError("Password must contain at least one lowercase letter")

          return "Password is valid"

      # Test
      print(validate_password("SecurePass123"))
      try:
          print(validate_password("weak"))
      except ValueError as e:
          print(f"Error: {e}")

      try:
          print(validate_password("nouppercase123"))
      except ValueError as e:
          print(f"Error: {e}")

  - title: "Configuration Validator"
    difficulty: intermediate
    description: "Build a configuration validator that raises different exceptions for missing keys, wrong types, and invalid values."
    starter_code: |
      def validate_config(config):
          # Your code here
          # Required keys: host (str), port (int 1-65535), timeout (int > 0)
          pass

      # Test
      print(validate_config({"host": "localhost", "port": 8080, "timeout": 30}))
      print(validate_config({"host": "localhost", "port": 8080}))
      print(validate_config({"host": "localhost", "port": "8080", "timeout": 30}))

    expected_output: |
      Configuration is valid
      Error: Missing required key: timeout
      Error: port must be an integer, got str

    hints:
      - "Check for missing keys and raise KeyError"
      - "Check types and raise TypeError"
      - "Check value ranges and raise ValueError"
    solution: |
      def validate_config(config):
          required_keys = ["host", "port", "timeout"]

          # Check for missing keys
          for key in required_keys:
              if key not in config:
                  raise KeyError(f"Missing required key: {key}")

          # Type validation
          if not isinstance(config["host"], str):
              raise TypeError(f"host must be a string, got {type(config['host']).__name__}")

          if not isinstance(config["port"], int):
              raise TypeError(f"port must be an integer, got {type(config['port']).__name__}")

          if not isinstance(config["timeout"], (int, float)):
              raise TypeError(f"timeout must be a number, got {type(config['timeout']).__name__}")

          # Value validation
          if config["port"] < 1 or config["port"] > 65535:
              raise ValueError(f"port must be between 1 and 65535, got {config['port']}")

          if config["timeout"] <= 0:
              raise ValueError(f"timeout must be positive, got {config['timeout']}")

          return "Configuration is valid"

      # Test
      print(validate_config({"host": "localhost", "port": 8080, "timeout": 30}))
      try:
          print(validate_config({"host": "localhost", "port": 8080}))
      except KeyError as e:
          print(f"Error: {e}")

      try:
          print(validate_config({"host": "localhost", "port": "8080", "timeout": 30}))
      except TypeError as e:
          print(f"Error: {e}")

  - title: "State Machine Validator"
    difficulty: advanced
    description: "Create a state machine that raises RuntimeError for invalid state transitions."
    starter_code: |
      class StateMachine:
          def __init__(self):
              self.state = "idle"
              self.valid_transitions = {
                  "idle": ["running"],
                  "running": ["paused", "stopped"],
                  "paused": ["running", "stopped"],
                  "stopped": ["idle"]
              }

          def transition(self, new_state):
              # Your code here
              pass

          def get_state(self):
              return self.state

      # Test
      sm = StateMachine()
      print(sm.get_state())
      sm.transition("running")
      print(sm.get_state())
      sm.transition("idle")

    expected_output: |
      idle
      running
      Error: Invalid transition from running to idle

    hints:
      - "Check if new_state is in valid_transitions[self.state]"
      - "Raise RuntimeError for invalid transitions"
      - "Update self.state if transition is valid"
    solution: |
      class StateMachine:
          def __init__(self):
              self.state = "idle"
              self.valid_transitions = {
                  "idle": ["running"],
                  "running": ["paused", "stopped"],
                  "paused": ["running", "stopped"],
                  "stopped": ["idle"]
              }

          def transition(self, new_state):
              if new_state not in self.valid_transitions.get(self.state, []):
                  raise RuntimeError(f"Invalid transition from {self.state} to {new_state}")
              self.state = new_state

          def get_state(self):
              return self.state

      # Test
      sm = StateMachine()
      print(sm.get_state())
      sm.transition("running")
      print(sm.get_state())
      try:
          sm.transition("idle")
      except RuntimeError as e:
          print(f"Error: {e}")

  - title: "Data Pipeline with Chained Exceptions"
    difficulty: advanced
    description: "Build a data pipeline that processes data through multiple stages, raising chained exceptions with context."
    starter_code: |
      def extract_data(source):
          # Simulates data extraction
          if source == "invalid":
              raise ValueError("Invalid data source")
          return {"raw_data": [1, 2, 3, "invalid", 5]}

      def transform_data(data):
          # Your code here
          # Transform raw_data to integers, raise chained exception on failure
          pass

      def load_data(data):
          # Your code here
          # Validate and load data, raise chained exception on failure
          pass

      def run_pipeline(source):
          # Your code here
          # Run all stages, chain exceptions
          pass

      # Test
      run_pipeline("valid")
      run_pipeline("invalid")

    expected_output: |
      Pipeline succeeded: {'transformed': [1, 2, 3, 5]}
      Pipeline failed at stage extract: Invalid data source
      Caused by: ValueError

    hints:
      - "Catch exceptions at each stage"
      - "Use 'raise NewException() from original_exception' for chaining"
      - "Include stage information in exception messages"
    solution: |
      def extract_data(source):
          if source == "invalid":
              raise ValueError("Invalid data source")
          return {"raw_data": [1, 2, 3, "invalid", 5]}

      def transform_data(data):
          try:
              transformed = []
              for item in data["raw_data"]:
                  if isinstance(item, int):
                      transformed.append(item)
                  elif isinstance(item, str) and item.isdigit():
                      transformed.append(int(item))
                  else:
                      raise ValueError(f"Cannot transform item: {item}")
              return {"transformed": transformed}
          except (ValueError, KeyError) as e:
              raise RuntimeError("Transformation failed") from e

      def load_data(data):
          try:
              if "transformed" not in data:
                  raise KeyError("Missing transformed data")
              if len(data["transformed"]) == 0:
                  raise ValueError("No data to load")
              return {"status": "loaded", "count": len(data["transformed"])}
          except (ValueError, KeyError) as e:
              raise RuntimeError("Load failed") from e

      def run_pipeline(source):
          try:
              raw = extract_data(source)
              transformed = transform_data(raw)
              loaded = load_data(transformed)
              print(f"Pipeline succeeded: {transformed}")
          except ValueError as e:
              print(f"Pipeline failed at stage extract: {e}")
              if e.__cause__:
                  print(f"Caused by: {type(e.__cause__).__name__}")
          except RuntimeError as e:
              print(f"Pipeline failed: {e}")
              if e.__cause__:
                  print(f"Caused by: {type(e.__cause__).__name__}: {e.__cause__}")

      # Test
      run_pipeline("valid")
      run_pipeline("invalid")
```
<!-- EXERCISE_END -->
