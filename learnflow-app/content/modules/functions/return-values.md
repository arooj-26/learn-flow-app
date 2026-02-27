# Return Values in Python

Return values allow functions to send data back to the caller, making functions more versatile and reusable. Understanding how to effectively use return statements is essential for writing functional, modular code.

## Basic Return Statements

The `return` statement sends a value back to the function caller:

```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # 8

# Without return, functions return None
def greet(name):
    print(f"Hello, {name}!")

result = greet("Alice")  # Prints: Hello, Alice!
print(result)  # None

# Early return for validation
def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

print(divide(10, 2))  # 5.0
print(divide(10, 0))  # Error: Division by zero
```

## Multiple Return Values

Python functions can return multiple values using tuple packing:

```python
def get_user_info():
    """Return multiple values as a tuple."""
    name = "Alice"
    age = 25
    city = "NYC"
    return name, age, city

# Tuple unpacking
username, user_age, user_city = get_user_info()
print(f"{username}, {user_age}, {user_city}")  # Alice, 25, NYC

# Or receive as tuple
user_data = get_user_info()
print(user_data)  # ('Alice', 25, 'NYC')
print(type(user_data))  # <class 'tuple'>

# Real-world example: Statistics calculator
def calculate_statistics(numbers):
    """Return min, max, mean, and median."""
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    median = sorted_nums[n//2] if n % 2 else (sorted_nums[n//2-1] + sorted_nums[n//2]) / 2

    return {
        'min': min(numbers),
        'max': max(numbers),
        'mean': sum(numbers) / len(numbers),
        'median': median
    }

stats = calculate_statistics([1, 5, 3, 9, 2, 7])
print(f"Min: {stats['min']}, Max: {stats['max']}, Mean: {stats['mean']:.2f}")
# Output: Min: 1, Max: 9, Mean: 4.50
```

## Return Types Comparison

| Return Type | Example | Use Case |
|-------------|---------|----------|
| Single value | `return 42` | Simple calculations |
| Multiple values | `return x, y, z` | Related data points |
| List | `return [1, 2, 3]` | Collection of items |
| Dictionary | `return {'key': 'value'}` | Structured data |
| Boolean | `return True` | Validation/checks |
| None | `return` or no return | Side-effect functions |

## Returning Different Data Types

Functions can return various data structures depending on the use case:

```python
# Returning a list
def get_even_numbers(max_num):
    """Return list of even numbers up to max_num."""
    return [n for n in range(max_num + 1) if n % 2 == 0]

evens = get_even_numbers(10)
print(evens)  # [0, 2, 4, 6, 8, 10]

# Returning a dictionary
def create_person(name, age, occupation):
    """Return a dictionary representing a person."""
    return {
        'name': name,
        'age': age,
        'occupation': occupation,
        'id': hash(name)  # Simple ID generation
    }

person = create_person("Bob", 30, "Engineer")
print(person)  # {'name': 'Bob', 'age': 30, 'occupation': 'Engineer', 'id': ...}

# Returning a set
def get_unique_chars(text):
    """Return set of unique characters in text."""
    return set(text.lower())

unique = get_unique_chars("Hello World")
print(unique)  # {'h', 'e', 'l', 'o', ' ', 'w', 'r', 'd'}

# Returning a function (closure)
def create_multiplier(factor):
    """Return a function that multiplies by factor."""
    def multiply(x):
        return x * factor
    return multiply

times_three = create_multiplier(3)
print(times_three(5))  # 15
print(times_three(10))  # 30
```

## Conditional Returns

Use conditional logic to return different values based on conditions:

```python
def validate_password(password):
    """
    Validate password and return status.
    Returns: (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain a digit"
    return True, "Password is valid"

# Test passwords
passwords = ["weak", "NoDigit", "noUPPER123", "ValidPass123"]
for pwd in passwords:
    is_valid, message = validate_password(pwd)
    print(f"{pwd}: {message}")

# Output:
# weak: Password must be at least 8 characters
# NoDigit: Password must contain a digit
# noUPPER123: Password must contain uppercase letter
# ValidPass123: Password is valid
```

## Return with Complex Logic

Real-world functions often involve complex return logic:

```python
def process_transaction(amount, account_balance, transaction_type):
    """
    Process a financial transaction.
    Returns: (success, new_balance, message)
    """
    if transaction_type == "deposit":
        new_balance = account_balance + amount
        return True, new_balance, f"Deposited ${amount:.2f}"

    elif transaction_type == "withdraw":
        if amount > account_balance:
            return False, account_balance, "Insufficient funds"
        if amount < 0:
            return False, account_balance, "Invalid amount"
        new_balance = account_balance - amount
        return True, new_balance, f"Withdrew ${amount:.2f}"

    else:
        return False, account_balance, "Invalid transaction type"

# Test transactions
balance = 1000.00
success, balance, msg = process_transaction(500, balance, "withdraw")
print(f"{msg} | Balance: ${balance:.2f}")
# Output: Withdrew $500.00 | Balance: $500.00

success, balance, msg = process_transaction(600, balance, "withdraw")
print(f"{msg} | Balance: ${balance:.2f}")
# Output: Insufficient funds | Balance: $500.00
```

## Generator Returns (yield vs return)

While `return` ends function execution, `yield` creates generators:

```python
# Regular return - returns once
def get_squares(n):
    """Return list of squares."""
    return [i**2 for i in range(n)]

squares = get_squares(5)
print(list(squares))  # [0, 1, 4, 9, 16]

# Generator with yield - returns multiple times
def generate_squares(n):
    """Generate squares one at a time."""
    for i in range(n):
        yield i**2

squares_gen = generate_squares(5)
print(next(squares_gen))  # 0
print(next(squares_gen))  # 1
print(list(squares_gen))  # [4, 9, 16]

# Real-world example: File processing
def read_large_file(filename, chunk_size=1024):
    """
    Read file in chunks to save memory.
    Yields chunks instead of returning entire file.
    """
    with open(filename, 'r') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Usage would be:
# for chunk in read_large_file('large_file.txt'):
#     process(chunk)
```

## Type Hints for Return Values

Use type hints to document expected return types:

```python
from typing import Tuple, List, Dict, Optional

def parse_name(full_name: str) -> Tuple[str, str]:
    """Parse full name into first and last name."""
    parts = full_name.split()
    if len(parts) >= 2:
        return parts[0], parts[-1]
    return parts[0], ""

def find_user(user_id: int) -> Optional[Dict[str, any]]:
    """
    Find user by ID.
    Returns user dict if found, None otherwise.
    """
    users = {1: {"name": "Alice", "age": 25}}
    return users.get(user_id)

user = find_user(1)
if user:
    print(f"Found: {user['name']}")
else:
    print("User not found")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Basic Return"
    difficulty: basic
    description: "Create a function `square(n)` that returns the square of n. Print square(7)."
    starter_code: |
      # Create square function

    expected_output: "49"
    hints:
      - "Use return statement"
      - "Square is n * n or n ** 2"
    solution: |
      def square(n):
          return n ** 2

      print(square(7))

  - title: "Return Multiple Values"
    difficulty: basic
    description: "Create a function `split_name(full_name)` that returns first and last name. Test with 'John Doe'."
    starter_code: |
      # Create split_name function

    expected_output: |
      John
      Doe
    hints:
      - "Use split() method"
      - "Return multiple values: return val1, val2"
    solution: |
      def split_name(full_name):
          parts = full_name.split()
          return parts[0], parts[1]

      first, last = split_name("John Doe")
      print(first)
      print(last)

  - title: "Conditional Return"
    difficulty: intermediate
    description: "Create a function `grade_score(score)` that returns 'Pass' if score >= 60, else 'Fail'. Test with 75 and 45."
    starter_code: |
      # Create grade_score function

    expected_output: |
      Pass
      Fail
    hints:
      - "Use if-else statement"
      - "Return different strings based on condition"
    solution: |
      def grade_score(score):
          if score >= 60:
              return "Pass"
          else:
              return "Fail"

      print(grade_score(75))
      print(grade_score(45))

  - title: "Return Dictionary"
    difficulty: intermediate
    description: "Create a function `create_product(name, price, stock)` that returns a dictionary with these keys. Test with 'Laptop', 999.99, 5."
    starter_code: |
      # Create create_product function

    expected_output: "{'name': 'Laptop', 'price': 999.99, 'stock': 5}"
    hints:
      - "Return a dictionary with the three keys"
      - "Use dictionary literal syntax"
    solution: |
      def create_product(name, price, stock):
          return {
              'name': name,
              'price': price,
              'stock': stock
          }

      print(create_product("Laptop", 999.99, 5))

  - title: "Validation with Multiple Returns"
    difficulty: advanced
    description: "Create a function `validate_age(age)` that returns (True, 'Valid') if age is 0-120, else (False, 'Invalid age'). Test with 25 and 150."
    starter_code: |
      # Create validate_age function

    expected_output: |
      True Valid
      False Invalid age
    hints:
      - "Return tuple of (boolean, string)"
      - "Check if 0 <= age <= 120"
    solution: |
      def validate_age(age):
          if 0 <= age <= 120:
              return True, "Valid"
          else:
              return False, "Invalid age"

      valid, msg = validate_age(25)
      print(valid, msg)
      valid, msg = validate_age(150)
      print(valid, msg)

  - title: "Complex Return Logic"
    difficulty: advanced
    description: "Create `calculate_discount(price, customer_type)` that returns (final_price, discount_percent). VIP gets 20%, regular gets 10%, new gets 5%. Test with price=100 and customer_type='VIP'."
    starter_code: |
      # Create calculate_discount function

    expected_output: "80.0 20"
    hints:
      - "Use if-elif-else for customer types"
      - "Calculate final price: price * (1 - discount/100)"
      - "Return both final price and discount percent"
    solution: |
      def calculate_discount(price, customer_type):
          if customer_type == "VIP":
              discount = 20
          elif customer_type == "regular":
              discount = 10
          elif customer_type == "new":
              discount = 5
          else:
              discount = 0

          final_price = price * (1 - discount / 100)
          return final_price, discount

      final, discount = calculate_discount(100, "VIP")
      print(final, discount)
```
<!-- EXERCISE_END -->
