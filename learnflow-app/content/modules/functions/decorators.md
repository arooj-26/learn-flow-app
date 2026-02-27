# Decorators in Python

Decorators are a powerful Python feature that allows you to modify or enhance functions and methods without changing their source code. They use the `@decorator_name` syntax and are essential for implementing cross-cutting concerns like logging, authentication, caching, and timing.

## Basic Decorator Concepts

A decorator is a function that takes another function as input and returns a modified version:

```python
# Simple decorator
def my_decorator(func):
    """Basic decorator wrapper."""
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

# Using decorator with @ syntax
@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Output:
# Before function call
# Hello!
# After function call

# Equivalent to:
def say_goodbye():
    print("Goodbye!")

say_goodbye = my_decorator(say_goodbye)
say_goodbye()
```

## Decorators with Arguments

Handle functions that accept parameters:

```python
def smart_decorator(func):
    """Decorator that handles function arguments."""
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@smart_decorator
def add(a, b):
    return a + b

@smart_decorator
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

result1 = add(5, 3)
# Output:
# Calling add with args=(5, 3), kwargs={}
# add returned 8

result2 = greet("Alice", greeting="Hi")
# Output:
# Calling greet with args=('Alice',), kwargs={'greeting': 'Hi'}
# greet returned Hi, Alice!
```

## Common Decorator Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| Timing | Measure execution time | `@timing_decorator` |
| Logging | Log function calls | `@log_decorator` |
| Authentication | Check permissions | `@require_auth` |
| Caching | Memoization | `@cache_decorator` |
| Validation | Input validation | `@validate_inputs` |
| Retry | Retry on failure | `@retry(times=3)` |

## Practical Decorators

Real-world decorator implementations:

```python
import time
from functools import wraps

# Timing decorator
def timing_decorator(func):
    """Measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    """Simulate slow operation."""
    time.sleep(1)
    return "Done"

slow_function()
# Output: slow_function took 1.0023 seconds

# Logging decorator
def log_decorator(func):
    """Log function calls with arguments."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper

@log_decorator
def multiply(x, y):
    return x * y

multiply(5, 3)
# Output:
# Calling multiply(5, 3)
# multiply returned 15

# Caching/Memoization decorator
def memoize(func):
    """Cache function results."""
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"Cache hit for {args}")
            return cache[args]
        print(f"Cache miss for {args}")
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(5))
# Shows cache hits/misses
```

## Decorators with Parameters

Create decorators that accept configuration:

```python
def repeat(times):
    """Decorator that repeats function execution."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for i in range(times):
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))
# Output: ['Hello, Alice!', 'Hello, Alice!', 'Hello, Alice!']

# Validation decorator with parameters
def validate_range(min_val, max_val):
    """Validate function argument is within range."""
    def decorator(func):
        @wraps(func)
        def wrapper(value):
            if not min_val <= value <= max_val:
                raise ValueError(f"Value must be between {min_val} and {max_val}")
            return func(value)
        return wrapper
    return decorator

@validate_range(0, 100)
def set_percentage(value):
    return f"Percentage set to {value}%"

print(set_percentage(75))  # Percentage set to 75%
# set_percentage(150)  # Raises ValueError

# Retry decorator
def retry(max_attempts=3, delay=1):
    """Retry function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise
                    print(f"Attempt {attempts} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unreliable_function():
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise ConnectionError("Connection failed")
    return "Success!"

# Will retry up to 3 times on failure
```

## Stacking Multiple Decorators

Apply multiple decorators to a single function:

```python
def uppercase_decorator(func):
    """Convert result to uppercase."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper

def exclamation_decorator(func):
    """Add exclamation marks."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"{result}!!!"
    return wrapper

# Stack decorators (applied bottom-up)
@exclamation_decorator
@uppercase_decorator
def greet(name):
    return f"hello, {name}"

print(greet("alice"))  # HELLO, ALICE!!!

# Order matters!
@uppercase_decorator
@exclamation_decorator
def greet2(name):
    return f"hello, {name}"

print(greet2("alice"))  # HELLO, ALICE!!!

# Combining timing and logging
@timing_decorator
@log_decorator
def complex_calculation(x, y):
    time.sleep(0.5)
    return x ** y

complex_calculation(2, 10)
```

## Class-Based Decorators

Use classes to create decorators with state:

```python
class CountCalls:
    """Decorator that counts function calls."""

    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count} of {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    print("Hello!")

say_hello()  # Call 1 of say_hello
say_hello()  # Call 2 of say_hello
say_hello()  # Call 3 of say_hello

# Class decorator with parameters
class RateLimit:
    """Rate limit function calls."""

    def __init__(self, max_calls, time_window):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls outside time window
            self.calls = [call for call in self.calls
                         if now - call < self.time_window]

            if len(self.calls) >= self.max_calls:
                raise Exception(f"Rate limit exceeded: {self.max_calls} calls per {self.time_window}s")

            self.calls.append(now)
            return func(*args, **kwargs)
        return wrapper

@RateLimit(max_calls=3, time_window=10)
def api_call():
    return "API response"

# Can call 3 times, then rate limited for 10 seconds
```

## Built-in Decorators

Python provides several useful built-in decorators:

```python
# @property - Create managed attributes
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        """Get radius."""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Set radius with validation."""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        """Calculate area (read-only)."""
        return 3.14159 * self._radius ** 2

circle = Circle(5)
print(circle.radius)  # 5
print(circle.area)    # 78.53975
circle.radius = 10
print(circle.area)    # 314.159

# @staticmethod and @classmethod
class MathOperations:
    class_variable = "Math Utils"

    @staticmethod
    def add(x, y):
        """Static method - no access to instance or class."""
        return x + y

    @classmethod
    def multiply(cls, x, y):
        """Class method - access to class."""
        print(f"Called from {cls.class_variable}")
        return x * y

print(MathOperations.add(5, 3))        # 8
print(MathOperations.multiply(5, 3))   # Called from Math Utils, then 15

# @wraps from functools - preserve function metadata
from functools import wraps

def my_decorator(func):
    @wraps(func)  # Preserves func.__name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def documented_function():
    """This is the docstring."""
    pass

print(documented_function.__name__)  # documented_function (not 'wrapper')
print(documented_function.__doc__)   # This is the docstring.
```

## Advanced Decorator Patterns

Sophisticated decorator use cases:

```python
# Context-aware decorator
def require_permission(permission):
    """Check if user has permission."""
    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            if permission not in user.get('permissions', []):
                raise PermissionError(f"User lacks {permission} permission")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

@require_permission('admin')
def delete_user(user, target_id):
    return f"User {target_id} deleted"

admin_user = {'name': 'Admin', 'permissions': ['admin', 'user']}
regular_user = {'name': 'User', 'permissions': ['user']}

delete_user(admin_user, 123)  # Works
# delete_user(regular_user, 123)  # Raises PermissionError

# Decorator that modifies function signature
def inject_db(func):
    """Inject database connection."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # In real code, create actual DB connection
        db_connection = "DatabaseConnection"
        return func(*args, db=db_connection, **kwargs)
    return wrapper

@inject_db
def get_user(user_id, db):
    return f"Fetching user {user_id} from {db}"

print(get_user(123))  # db parameter injected automatically
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Basic Decorator"
    difficulty: basic
    description: "Create a decorator `print_call` that prints 'Calling function' before execution and 'Function called' after. Apply it to a function that prints 'Hello'."
    starter_code: |
      # Create decorator and apply it

    expected_output: |
      Calling function
      Hello
      Function called
    hints:
      - "Decorator takes func as parameter"
      - "Create wrapper function inside"
      - "Call func() between print statements"
    solution: |
      def print_call(func):
          def wrapper():
              print("Calling function")
              func()
              print("Function called")
          return wrapper

      @print_call
      def say_hello():
          print("Hello")

      say_hello()

  - title: "Decorator with Arguments"
    difficulty: basic
    description: "Create a decorator `print_args` that prints the arguments passed to a function. Apply to a function add(a, b) that returns a + b. Test with add(5, 3)."
    starter_code: |
      # Create decorator with *args, **kwargs

    expected_output: |
      Arguments: (5, 3) {}
      8
    hints:
      - "Use *args and **kwargs in wrapper"
      - "Print args and kwargs"
      - "Return func(*args, **kwargs)"
    solution: |
      def print_args(func):
          def wrapper(*args, **kwargs):
              print(f"Arguments: {args} {kwargs}")
              return func(*args, **kwargs)
          return wrapper

      @print_args
      def add(a, b):
          return a + b

      print(add(5, 3))

  - title: "Timing Decorator"
    difficulty: intermediate
    description: "Create a `timer` decorator that measures and prints execution time. Apply to a function that sleeps for 0.1 seconds using time.sleep(0.1)."
    starter_code: |
      # Create timing decorator
      import time

    expected_output: "Execution time:"
    hints:
      - "Import time module"
      - "Record time.time() before and after"
      - "Print the difference"
    solution: |
      import time

      def timer(func):
          def wrapper(*args, **kwargs):
              start = time.time()
              result = func(*args, **kwargs)
              end = time.time()
              print(f"Execution time: {end - start:.4f} seconds")
              return result
          return wrapper

      @timer
      def slow_function():
          time.sleep(0.1)
          return "Done"

      slow_function()

  - title: "Repeat Decorator"
    difficulty: intermediate
    description: "Create a decorator `repeat(n)` that executes a function n times. Apply @repeat(3) to a function that prints 'Hello'. Test it."
    starter_code: |
      # Create parameterized repeat decorator

    expected_output: |
      Hello
      Hello
      Hello
    hints:
      - "Outer function takes n parameter"
      - "Inner function is the actual decorator"
      - "Wrapper loops n times"
    solution: |
      def repeat(n):
          def decorator(func):
              def wrapper(*args, **kwargs):
                  for _ in range(n):
                      func(*args, **kwargs)
              return wrapper
          return decorator

      @repeat(3)
      def say_hello():
          print("Hello")

      say_hello()

  - title: "Memoization Decorator"
    difficulty: advanced
    description: "Create a `memoize` decorator that caches function results. Apply it to a recursive fibonacci function. Test with fibonacci(10) and observe cache behavior."
    starter_code: |
      # Create memoization decorator

    expected_output: "55"
    hints:
      - "Create cache dict inside decorator"
      - "Check if args in cache"
      - "Store and return cached results"
    solution: |
      def memoize(func):
          cache = {}
          def wrapper(*args):
              if args not in cache:
                  cache[args] = func(*args)
              return cache[args]
          return wrapper

      @memoize
      def fibonacci(n):
          if n <= 1:
              return n
          return fibonacci(n - 1) + fibonacci(n - 2)

      print(fibonacci(10))

  - title: "Validation Decorator"
    difficulty: advanced
    description: "Create a decorator `validate_positive` that checks if all arguments are positive numbers. Raise ValueError if not. Apply to a function multiply(a, b). Test with valid and invalid inputs."
    starter_code: |
      # Create validation decorator

    expected_output: "20"
    hints:
      - "Loop through args in wrapper"
      - "Check if each arg > 0"
      - "Raise ValueError if not positive"
    solution: |
      def validate_positive(func):
          def wrapper(*args, **kwargs):
              for arg in args:
                  if not isinstance(arg, (int, float)) or arg <= 0:
                      raise ValueError("All arguments must be positive numbers")
              return func(*args, **kwargs)
          return wrapper

      @validate_positive
      def multiply(a, b):
          return a * b

      print(multiply(4, 5))
      # multiply(-1, 5)  # Would raise ValueError
```
<!-- EXERCISE_END -->
