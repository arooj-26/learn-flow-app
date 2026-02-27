# Parameters and Arguments in Python

Understanding the difference between parameters and arguments is crucial for effective function design. Parameters are the variables defined in the function signature, while arguments are the actual values passed when calling the function. Python offers several powerful ways to work with both.

## Positional vs Keyword Arguments

Positional arguments must be passed in the correct order, while keyword arguments are specified by name:

```python
def create_profile(name, age, city):
    return f"{name}, {age} years old, from {city}"

# Positional arguments - order matters
print(create_profile("Alice", 25, "NYC"))
# Output: Alice, 25 years old, from NYC

# Keyword arguments - order doesn't matter
print(create_profile(city="Boston", name="Bob", age=30))
# Output: Bob, 30 years old, from Boston

# Mixed - positional must come before keyword
print(create_profile("Charlie", age=35, city="LA"))
# Output: Charlie, 35 years old, from LA
```

## Parameter Types Comparison

| Parameter Type | Syntax | Usage | Example |
|----------------|--------|-------|---------|
| Positional | `def func(a, b)` | Order matters | `func(1, 2)` |
| Keyword | `def func(a, b)` | Named arguments | `func(b=2, a=1)` |
| Default | `def func(a=1)` | Optional with default | `func()` or `func(5)` |
| Variable Positional | `def func(*args)` | Any number of args | `func(1, 2, 3, 4)` |
| Variable Keyword | `def func(**kwargs)` | Any number of kwargs | `func(a=1, b=2)` |

## Variable-Length Arguments (*args)

The `*args` parameter allows functions to accept any number of positional arguments:

```python
def calculate_average(*numbers):
    """Calculate average of any number of values."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

print(calculate_average(10, 20, 30))  # 20.0
print(calculate_average(5, 10, 15, 20, 25))  # 15.0

# Real-world example: Logging function
def log_message(level, *messages):
    """Log multiple messages with a severity level."""
    timestamp = "2024-01-01 12:00:00"
    print(f"[{timestamp}] {level}:", " ".join(str(m) for m in messages))

log_message("ERROR", "Database", "connection", "failed")
# Output: [2024-01-01 12:00:00] ERROR: Database connection failed
```

## Variable-Length Keyword Arguments (**kwargs)

The `**kwargs` parameter collects keyword arguments into a dictionary:

```python
def build_user_profile(username, **details):
    """Build a user profile with flexible attributes."""
    profile = {"username": username}
    profile.update(details)
    return profile

user1 = build_user_profile("alice", email="alice@example.com", age=25)
user2 = build_user_profile("bob", email="bob@example.com", role="admin", department="IT")

print(user1)  # {'username': 'alice', 'email': 'alice@example.com', 'age': 25}
print(user2)  # {'username': 'bob', 'email': 'bob@example.com', 'role': 'admin', 'department': 'IT'}

# Real-world example: Database query builder
def query_database(table, **filters):
    """Build a database query with dynamic filters."""
    query = f"SELECT * FROM {table}"
    if filters:
        conditions = [f"{key} = '{value}'" for key, value in filters.items()]
        query += " WHERE " + " AND ".join(conditions)
    return query

print(query_database("users", status="active", role="admin"))
# Output: SELECT * FROM users WHERE status = 'active' AND role = 'admin'
```

## Combining All Parameter Types

When combining different parameter types, they must follow this order:

```python
def advanced_function(pos1, pos2, *args, default1="default", **kwargs):
    """
    Demonstrates all parameter types in correct order:
    1. Positional parameters
    2. *args (variable positional)
    3. Default parameters
    4. **kwargs (variable keyword)
    """
    print(f"Positional: {pos1}, {pos2}")
    print(f"Extra positional (*args): {args}")
    print(f"Default parameter: {default1}")
    print(f"Keyword arguments (**kwargs): {kwargs}")

advanced_function(
    1, 2, 3, 4, 5,
    default1="custom",
    option1="value1",
    option2="value2"
)
# Output:
# Positional: 1, 2
# Extra positional (*args): (3, 4, 5)
# Default parameter: custom
# Keyword arguments (**kwargs): {'option1': 'value1', 'option2': 'value2'}
```

## Argument Unpacking

Use `*` and `**` to unpack sequences and dictionaries as arguments:

```python
def calculate_bmi(weight, height):
    """Calculate Body Mass Index."""
    return weight / (height ** 2)

# Unpacking a list
measurements = [70, 1.75]
bmi = calculate_bmi(*measurements)
print(f"BMI: {bmi:.2f}")  # BMI: 22.86

# Unpacking a dictionary
person_data = {"weight": 70, "height": 1.75}
bmi = calculate_bmi(**person_data)
print(f"BMI: {bmi:.2f}")  # BMI: 22.86

# Real-world example: API request builder
def make_api_request(endpoint, method="GET", **params):
    """Simulate an API request."""
    return f"Request: {method} {endpoint} with params {params}"

# Unpacking configuration
config = {"timeout": 30, "retries": 3, "verify_ssl": True}
result = make_api_request("/api/users", method="POST", **config)
print(result)
# Output: Request: POST /api/users with params {'timeout': 30, 'retries': 3, 'verify_ssl': True}
```

## Positional-Only and Keyword-Only Parameters

Python 3.8+ allows enforcing how arguments can be passed:

```python
def strict_function(pos_only, /, pos_or_kw, *, kw_only):
    """
    - pos_only: Must be positional (before /)
    - pos_or_kw: Can be positional or keyword (between / and *)
    - kw_only: Must be keyword (after *)
    """
    return f"{pos_only}, {pos_or_kw}, {kw_only}"

# Correct usage
print(strict_function(1, 2, kw_only=3))  # 1, 2, 3
print(strict_function(1, pos_or_kw=2, kw_only=3))  # 1, 2, 3

# These would raise errors:
# strict_function(pos_only=1, pos_or_kw=2, kw_only=3)  # Error: pos_only can't be keyword
# strict_function(1, 2, 3)  # Error: kw_only must be keyword

# Real-world example: API endpoint with strict parameters
def create_user(user_id, /, email, *, role="user", notify=True):
    """
    Create a user with strict parameter requirements.
    user_id: positional only (internal ID shouldn't be named in calls)
    email: flexible (can be positional or keyword)
    role, notify: keyword only (clarity in configuration)
    """
    return {
        "id": user_id,
        "email": email,
        "role": role,
        "notify": notify
    }

user = create_user(12345, "user@example.com", role="admin", notify=False)
print(user)
# Output: {'id': 12345, 'email': 'user@example.com', 'role': 'admin', 'notify': False}
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Keyword Arguments Practice"
    difficulty: basic
    description: "Create a function `describe_book(title, author, year)` and call it using keyword arguments in reverse order."
    starter_code: |
      # Define describe_book function and call with keyword arguments

    expected_output: "1984 by George Orwell, published in 1949"
    hints:
      - "Use keyword arguments: func(param2=val2, param1=val1)"
      - "Return a formatted string"
    solution: |
      def describe_book(title, author, year):
          return f"{title} by {author}, published in {year}"

      print(describe_book(year=1949, author="George Orwell", title="1984"))

  - title: "Simple *args Function"
    difficulty: basic
    description: "Create a function `find_max(*numbers)` that returns the maximum value from any number of arguments. Test with find_max(3, 7, 2, 9, 1)."
    starter_code: |
      # Create find_max function with *args

    expected_output: "9"
    hints:
      - "Use *args to accept variable arguments"
      - "Use built-in max() function"
    solution: |
      def find_max(*numbers):
          return max(numbers)

      print(find_max(3, 7, 2, 9, 1))

  - title: "Build Configuration Dictionary"
    difficulty: intermediate
    description: "Create a function `create_config(app_name, **settings)` that returns a dictionary with app_name and all settings. Test with app_name='MyApp' and settings debug=True, port=8000."
    starter_code: |
      # Create create_config function

    expected_output: "{'app_name': 'MyApp', 'debug': True, 'port': 8000}"
    hints:
      - "Start with a dict containing app_name"
      - "Use update() to add kwargs"
    solution: |
      def create_config(app_name, **settings):
          config = {"app_name": app_name}
          config.update(settings)
          return config

      print(create_config("MyApp", debug=True, port=8000))

  - title: "Argument Unpacking"
    difficulty: intermediate
    description: "Create a function `calculate_rectangle(length, width)` that returns area. Create a list [5, 10] and call the function by unpacking the list."
    starter_code: |
      # Create function and unpack list as arguments

    expected_output: "50"
    hints:
      - "Use * to unpack a list: func(*my_list)"
      - "Area = length * width"
    solution: |
      def calculate_rectangle(length, width):
          return length * width

      dimensions = [5, 10]
      print(calculate_rectangle(*dimensions))

  - title: "Combined Parameter Types"
    difficulty: advanced
    description: "Create a function `process_order(order_id, *items, discount=0, **customer_info)` that returns a formatted string with all information. Test with order_id=123, items 'book' and 'pen', discount=10, and customer_info name='Alice' and email='alice@example.com'."
    starter_code: |
      # Create process_order with mixed parameters

    expected_output: |
      Order #123
      Items: book, pen
      Discount: 10%
      Customer: Alice (alice@example.com)
    hints:
      - "Order: positional, *args, default, **kwargs"
      - "Use ', '.join() for items"
    solution: |
      def process_order(order_id, *items, discount=0, **customer_info):
          result = f"Order #{order_id}\n"
          result += f"Items: {', '.join(items)}\n"
          result += f"Discount: {discount}%\n"
          result += f"Customer: {customer_info['name']} ({customer_info['email']})"
          return result

      print(process_order(123, "book", "pen", discount=10, name="Alice", email="alice@example.com"))

  - title: "Flexible Data Processor"
    difficulty: advanced
    description: "Create a function `process_data(data, /, operation='sum', *extra_values, **options)` that processes a list. If operation is 'sum', add extra_values and return total. Support keyword-only parameter 'multiplier' from options (default 1). Test with [1,2,3], 4, 5, multiplier=2."
    starter_code: |
      # Create flexible data processor

    expected_output: "30"
    hints:
      - "data is positional-only (before /)"
      - "Sum list, add extra_values, apply multiplier"
      - "Use options.get('multiplier', 1)"
    solution: |
      def process_data(data, /, operation='sum', *extra_values, **options):
          multiplier = options.get('multiplier', 1)
          if operation == 'sum':
              total = sum(data) + sum(extra_values)
              return total * multiplier
          return 0

      print(process_data([1, 2, 3], 'sum', 4, 5, multiplier=2))
```
<!-- EXERCISE_END -->
