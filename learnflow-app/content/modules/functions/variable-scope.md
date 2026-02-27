# Variable Scope in Python

Variable scope determines where in your code a variable can be accessed. Understanding scope is crucial for writing bug-free code and avoiding naming conflicts. Python follows the LEGB rule: Local, Enclosing, Global, and Built-in.

## Local Scope

Variables defined inside a function are local to that function:

```python
def calculate_total():
    price = 100  # Local variable
    tax = 0.08   # Local variable
    total = price * (1 + tax)
    return total

result = calculate_total()
print(result)  # 108.0

# This would cause an error:
# print(price)  # NameError: name 'price' is not defined

# Each function call has its own local scope
def greet(name):
    message = f"Hello, {name}!"  # Local to this function call
    return message

print(greet("Alice"))  # Hello, Alice!
print(greet("Bob"))    # Hello, Bob!
# message is not accessible here
```

## Global Scope

Variables defined at the top level are global:

```python
# Global variables
app_name = "LearnFlow"
version = "1.0.0"

def get_app_info():
    """Functions can read global variables."""
    return f"{app_name} v{version}"

print(get_app_info())  # LearnFlow v1.0.0

# Attempting to modify global variable locally creates a new local variable
counter = 0

def increment_wrong():
    counter = counter + 1  # UnboundLocalError!
    return counter

# This will cause an error:
# increment_wrong()

# Use global keyword to modify global variables
counter = 0

def increment_correct():
    global counter
    counter = counter + 1
    return counter

print(increment_correct())  # 1
print(increment_correct())  # 2
print(counter)  # 2
```

## LEGB Rule Overview

| Scope | Description | Example | Priority |
|-------|-------------|---------|----------|
| Local | Inside current function | `def f(): x = 1` | 1 (Highest) |
| Enclosing | Inside enclosing function | `def outer(): x = 1; def inner(): ...` | 2 |
| Global | Module level | `x = 1` (top level) | 3 |
| Built-in | Python built-ins | `print`, `len`, `str` | 4 (Lowest) |

## Enclosing Scope (Closures)

Functions defined inside other functions can access the enclosing function's variables:

```python
def outer_function(x):
    """Outer function with enclosing scope."""

    def inner_function(y):
        """Inner function accessing enclosing scope."""
        return x + y  # x is from enclosing scope

    return inner_function

# Create a closure
add_five = outer_function(5)
print(add_five(3))  # 8
print(add_five(10))  # 15

# Real-world example: Creating configured functions
def create_multiplier(factor):
    """Factory function creating multipliers."""

    def multiply(number):
        return number * factor  # factor from enclosing scope

    return multiply

times_two = create_multiplier(2)
times_ten = create_multiplier(10)

print(times_two(5))   # 10
print(times_ten(5))   # 50

# Multiple levels of nesting
def level_one():
    x = "Level 1"

    def level_two():
        y = "Level 2"

        def level_three():
            z = "Level 3"
            # Can access x, y, and z
            return f"{x}, {y}, {z}"

        return level_three()

    return level_two()

print(level_one())  # Level 1, Level 2, Level 3
```

## The nonlocal Keyword

Use `nonlocal` to modify variables in enclosing scope:

```python
def counter_function():
    """Create a counter using nonlocal."""
    count = 0

    def increment():
        nonlocal count  # Modify enclosing scope variable
        count += 1
        return count

    def decrement():
        nonlocal count
        count -= 1
        return count

    def get_count():
        return count  # Just reading, no nonlocal needed

    return increment, decrement, get_count

# Use the counter
inc, dec, get = counter_function()
print(inc())  # 1
print(inc())  # 2
print(inc())  # 3
print(dec())  # 2
print(get())  # 2

# Real-world example: Bank account with closure
def create_account(initial_balance):
    """Create account with encapsulated balance."""
    balance = initial_balance

    def deposit(amount):
        nonlocal balance
        if amount > 0:
            balance += amount
            return f"Deposited ${amount}. New balance: ${balance}"
        return "Invalid amount"

    def withdraw(amount):
        nonlocal balance
        if 0 < amount <= balance:
            balance -= amount
            return f"Withdrew ${amount}. New balance: ${balance}"
        return "Invalid amount or insufficient funds"

    def get_balance():
        return f"Current balance: ${balance}"

    return {
        'deposit': deposit,
        'withdraw': withdraw,
        'balance': get_balance
    }

account = create_account(1000)
print(account['balance']())      # Current balance: $1000
print(account['deposit'](500))   # Deposited $500. New balance: $1500
print(account['withdraw'](300))  # Withdrew $300. New balance: $1200
```

## Scope Visualization Example

Demonstrating how Python resolves variables:

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(f"Local x: {x}")

    inner()
    print(f"Enclosing x: {x}")

outer()
print(f"Global x: {x}")

# Output:
# Local x: local
# Enclosing x: enclosing
# Global x: global

# Without local assignment, looks up in enclosing/global
y = "global y"

def outer_2():
    y = "enclosing y"

    def inner_2():
        # No local y, so uses enclosing y
        print(f"Inside inner: {y}")

    inner_2()
    print(f"Inside outer: {y}")

outer_2()
print(f"In global: {y}")

# Output:
# Inside inner: enclosing y
# Inside outer: enclosing y
# In global: global y
```

## Common Scope Pitfalls

Avoid these common mistakes:

```python
# Pitfall 1: Loop variables leaking
for i in range(3):
    x = i * 2

print(x)  # 4 - x still exists! (in Python 2, i would also leak)

# Pitfall 2: Late binding in closures
def create_functions():
    """Common closure mistake."""
    functions = []
    for i in range(3):
        functions.append(lambda: i)  # All refer to same i!
    return functions

funcs = create_functions()
print([f() for f in funcs])  # [2, 2, 2] - all return 2!

# Fix: Use default argument to capture value
def create_functions_fixed():
    """Correct way using default argument."""
    functions = []
    for i in range(3):
        functions.append(lambda x=i: x)  # Capture current value
    return functions

funcs = create_functions_fixed()
print([f() for f in funcs])  # [0, 1, 2] - correct!

# Pitfall 3: Shadowing built-ins
def bad_function():
    list = [1, 2, 3]  # Shadows built-in list()
    # Now list() function is not accessible in this scope
    return list

# Better: Use descriptive names
def good_function():
    numbers = [1, 2, 3]
    return numbers
```

## Practical Scope Applications

Real-world examples using scope effectively:

```python
# Configuration management with closures
def create_config():
    """Encapsulate configuration."""
    _config = {
        'debug': False,
        'max_connections': 10,
        'timeout': 30
    }

    def get(key, default=None):
        return _config.get(key, default)

    def set(key, value):
        nonlocal _config
        _config[key] = value

    def reset():
        nonlocal _config
        _config = {
            'debug': False,
            'max_connections': 10,
            'timeout': 30
        }

    return {'get': get, 'set': set, 'reset': reset}

config = create_config()
print(config['get']('debug'))  # False
config['set']('debug', True)
print(config['get']('debug'))  # True

# Rate limiter using closure
def create_rate_limiter(max_calls, time_window):
    """Create a rate limiter."""
    calls = []

    def is_allowed():
        nonlocal calls
        import time
        now = time.time()

        # Remove old calls outside time window
        calls = [call for call in calls if now - call < time_window]

        if len(calls) < max_calls:
            calls.append(now)
            return True
        return False

    return is_allowed

# Allow 3 calls per 60 seconds
limiter = create_rate_limiter(3, 60)

for i in range(5):
    if limiter():
        print(f"Request {i+1}: Allowed")
    else:
        print(f"Request {i+1}: Rate limited")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Local vs Global"
    difficulty: basic
    description: "Create a global variable `count = 0` and a function `show_count()` that prints it. Call the function."
    starter_code: |
      # Create global variable and function

    expected_output: "0"
    hints:
      - "Define count at top level"
      - "Functions can read global variables without global keyword"
    solution: |
      count = 0

      def show_count():
          print(count)

      show_count()

  - title: "Using global Keyword"
    difficulty: basic
    description: "Create a global `total = 0` and function `add_to_total(n)` that adds n to total using global keyword. Call with add_to_total(5) twice and print total."
    starter_code: |
      # Create global variable and function with global keyword

    expected_output: "10"
    hints:
      - "Use global keyword to modify global variable"
      - "global total inside the function"
    solution: |
      total = 0

      def add_to_total(n):
          global total
          total += n

      add_to_total(5)
      add_to_total(5)
      print(total)

  - title: "Simple Closure"
    difficulty: intermediate
    description: "Create a function `make_adder(x)` that returns a function that adds x to its argument. Create `add_ten = make_adder(10)` and print add_ten(5)."
    starter_code: |
      # Create closure function

    expected_output: "15"
    hints:
      - "Return an inner function"
      - "Inner function uses x from outer scope"
    solution: |
      def make_adder(x):
          def add(y):
              return x + y
          return add

      add_ten = make_adder(10)
      print(add_ten(5))

  - title: "nonlocal Keyword"
    difficulty: intermediate
    description: "Create `create_counter()` that returns an inner function `increment()`. The inner function increments a counter variable using nonlocal and returns it. Test by calling it 3 times."
    starter_code: |
      # Create counter with nonlocal

    expected_output: |
      1
      2
      3
    hints:
      - "Define counter = 0 in outer function"
      - "Use nonlocal counter in inner function"
      - "Increment and return counter"
    solution: |
      def create_counter():
          counter = 0
          def increment():
              nonlocal counter
              counter += 1
              return counter
          return increment

      count = create_counter()
      print(count())
      print(count())
      print(count())

  - title: "LEGB Rule Practice"
    difficulty: advanced
    description: "Create a global `x = 'global'`. Create `outer()` with `x = 'enclosing'` and inner function `inner()` with `x = 'local'`. Inner should print all three x values by accessing each scope appropriately."
    starter_code: |
      # Demonstrate LEGB with multiple scopes

    expected_output: |
      local
      enclosing
      global
    hints:
      - "Local x is just x"
      - "Pass enclosing x as parameter to inner"
      - "Use globals()['x'] for global x or pass it in"
    solution: |
      x = "global"

      def outer():
          x = "enclosing"
          def inner():
              x = "local"
              print(x)
              print(outer_x)
              print(global_x)
          outer_x = x
          global_x = globals()['x']
          inner()

      outer()

  - title: "Encapsulated Counter Object"
    difficulty: advanced
    description: "Create `create_counter(start=0)` that returns a dict with three functions: 'inc' (increment), 'dec' (decrement), 'get' (get value). Use nonlocal to manage state. Test by incrementing twice, decrementing once, then getting value."
    starter_code: |
      # Create encapsulated counter

    expected_output: "1"
    hints:
      - "Define count = start in outer function"
      - "Each function uses nonlocal count"
      - "Return dict with three functions"
    solution: |
      def create_counter(start=0):
          count = start

          def inc():
              nonlocal count
              count += 1

          def dec():
              nonlocal count
              count -= 1

          def get():
              return count

          return {'inc': inc, 'dec': dec, 'get': get}

      counter = create_counter()
      counter['inc']()
      counter['inc']()
      counter['dec']()
      print(counter['get']())
```
<!-- EXERCISE_END -->
