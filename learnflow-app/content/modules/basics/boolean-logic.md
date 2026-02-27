# Boolean Logic in Python

Boolean logic is fundamental to programming, enabling decision-making and flow control. Understanding how Python evaluates truth values and combines logical conditions is essential for writing effective conditional statements.

## Boolean Values and Type

Python has a built-in boolean type with two values: `True` and `False`:

```python
# Boolean literals
is_active = True
is_deleted = False

# Type checking
print(type(True))   # <class 'bool'>
print(type(False))  # <class 'bool'>

# Booleans are subclass of integers
print(int(True))    # 1
print(int(False))   # 0
print(True + True)  # 2 (True treated as 1)
print(True * 5)     # 5

# Creating booleans from comparisons
age = 25
is_adult = age >= 18  # True
is_teen = 13 <= age < 20  # False
```

## Comparison Operators

Comparison operators return boolean values:

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `5 > 3` | `True` |
| `<` | Less than | `5 < 3` | `False` |
| `>=` | Greater than or equal | `5 >= 5` | `True` |
| `<=` | Less than or equal | `3 <= 5` | `True` |

```python
# Numeric comparisons
x = 10
y = 5

print(x > y)       # True
print(x == 10)     # True
print(y != 5)      # False
print(x >= 10)     # True

# String comparisons (lexicographical)
print("apple" < "banana")    # True (alphabetical order)
print("Python" == "python")  # False (case-sensitive)
print("abc" > "ABC")         # True (lowercase > uppercase)

# Chain comparisons (unique to Python!)
age = 25
print(18 <= age < 65)        # True (both conditions checked)
print(0 < x < 100)           # True (elegant range check)

# Comparing different types (be careful!)
print(5 == "5")              # False (different types)
print(5 == 5.0)              # True (numeric equivalence)
```

## Logical Operators

Combine boolean expressions using logical operators:

```python
# AND operator - both must be True
age = 25
has_license = True
can_drive = age >= 18 and has_license  # True

print(True and True)    # True
print(True and False)   # False
print(False and True)   # False
print(False and False)  # False

# OR operator - at least one must be True
is_weekend = False
is_holiday = True
can_relax = is_weekend or is_holiday  # True

print(True or True)     # True
print(True or False)    # True
print(False or True)    # True
print(False or False)   # False

# NOT operator - inverts the boolean
is_raining = False
is_sunny = not is_raining  # True

print(not True)         # False
print(not False)        # True

# Complex combinations
x = 10
y = 5
z = 7
result = (x > y and y < z) or not (x == 10)
# (True and True) or not True
# True or False
# True
```

## Operator Precedence

Understanding the order in which operators are evaluated:

```python
# Precedence (highest to lowest):
# 1. Parentheses ()
# 2. NOT
# 3. AND
# 4. OR

# Examples
result = True or True and False
# Evaluated as: True or (True and False)
# Result: True

result = not True or False
# Evaluated as: (not True) or False
# Result: False

result = True and not False or False
# Evaluated as: True and (not False) or False
# Evaluated as: (True and True) or False
# Result: True

# Best practice: Use parentheses for clarity
result = (True or True) and False  # False
result = True or (True and False)  # True

# Complex example
x = 10
result = (x > 5 and x < 15) or (x == 10 and x != 20)
# (True and True) or (True and True)
# True or True
# True
```

## Truthiness and Falsy Values

Python evaluates all values as either truthy or falsy in boolean contexts:

```python
# Falsy values (evaluate to False)
falsy_values = [
    False,          # Boolean False
    None,           # None type
    0,              # Zero integer
    0.0,            # Zero float
    0j,             # Zero complex
    "",             # Empty string
    [],             # Empty list
    (),             # Empty tuple
    {},             # Empty dict
    set(),          # Empty set
]

for value in falsy_values:
    if not value:
        print(f"{repr(value):15} is falsy")

# Everything else is truthy
truthy_values = [
    True,           # Boolean True
    1,              # Non-zero numbers
    "hello",        # Non-empty strings
    [1, 2],         # Non-empty lists
    {"a": 1},       # Non-empty dicts
]

# Using truthiness in conditions
user_input = input("Enter your name: ")
if user_input:  # Checks if non-empty
    print(f"Hello, {user_input}!")
else:
    print("No name entered")

# Common pattern: Default values
name = user_input or "Guest"  # Use "Guest" if user_input is empty
```

## Short-Circuit Evaluation

Python uses short-circuit evaluation for efficiency:

```python
# AND short-circuits on first False
def expensive_check():
    print("Expensive check running...")
    return True

x = 5
# Second part never executes if first is False
if x > 10 and expensive_check():
    print("Both true")
# Output: Nothing (expensive_check never called)

# OR short-circuits on first True
x = 15
if x > 10 or expensive_check():
    print("At least one true")
# Output: "At least one true" (expensive_check never called)

# Practical use: Avoiding errors
user_list = []
# Safe check: won't try to access [0] if list is empty
if user_list and user_list[0] == "admin":
    print("Admin user")

# Default value pattern
name = None
display_name = name or "Anonymous"  # "Anonymous"

# Guard pattern
def process_user(user):
    if not user or not user.get("active"):
        return  # Early return if conditions not met
    # Process active user...
```

## Boolean Functions and Methods

Common boolean-returning functions and methods:

```python
# String methods
text = "Hello123"
print(text.isalpha())      # False (contains numbers)
print(text.isdigit())      # False (contains letters)
print(text.isalnum())      # True (only letters and numbers)
print(text.startswith("H")) # True
print(text.endswith("23"))  # True

# Membership testing
fruits = ["apple", "banana", "orange"]
print("apple" in fruits)    # True
print("grape" in fruits)    # False
print("grape" not in fruits) # True

# Identity testing
x = [1, 2, 3]
y = [1, 2, 3]
z = x

print(x == y)    # True (same content)
print(x is y)    # False (different objects)
print(x is z)    # True (same object)
print(x is not y) # True

# Type checking
value = 42
print(isinstance(value, int))     # True
print(isinstance(value, str))     # False
print(isinstance(value, (int, float)))  # True (check multiple types)
```

## Practical Boolean Patterns

Real-world applications of boolean logic:

```python
# Validation patterns
def is_valid_email(email):
    """Check if email has basic valid format"""
    return (
        email and
        "@" in email and
        "." in email and
        not email.startswith("@") and
        not email.endswith("@")
    )

# Range checking
def is_valid_age(age):
    """Check if age is in valid range"""
    return 0 <= age <= 120

# Permission checking
def can_edit_post(user, post):
    """Check if user can edit post"""
    is_author = user.id == post.author_id
    is_admin = user.role == "admin"
    return is_author or is_admin

# Complex eligibility checking
def is_eligible_for_loan(age, income, credit_score):
    """Check loan eligibility"""
    is_adult = age >= 18
    has_income = income >= 30000
    has_good_credit = credit_score >= 650

    return is_adult and has_income and has_good_credit

# Feature flags
DEBUG_MODE = True
ENABLE_LOGGING = True
SEND_EMAILS = False

if DEBUG_MODE and ENABLE_LOGGING:
    print("Debug log: Processing user data")

if not SEND_EMAILS:
    print("Email sending disabled")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Basic Comparison"
    difficulty: basic
    description: "Create two variables: x = 10 and y = 20. Print whether x is less than y."
    starter_code: |
      x = 10
      y = 20
      # Compare and print

    expected_output: "True"
    hints:
      - "Use the < operator for less than comparison"
      - "The result will be a boolean value"
    solution: |
      x = 10
      y = 20
      print(x < y)

  - title: "Logical AND"
    difficulty: basic
    description: "Check if age (25) is greater than 18 AND less than 65. Print the result."
    starter_code: |
      age = 25
      # Use AND operator

    expected_output: "True"
    hints:
      - "Use the 'and' keyword to combine conditions"
      - "Both conditions must be True for the result to be True"
    solution: |
      age = 25
      result = age > 18 and age < 65
      print(result)

  - title: "String Membership"
    difficulty: intermediate
    description: "Check if the word 'Python' is in the sentence 'I love Python programming' and print the result."
    starter_code: |
      sentence = "I love Python programming"
      # Check membership

    expected_output: "True"
    hints:
      - "Use the 'in' keyword to check membership"
      - "String matching is case-sensitive"
    solution: |
      sentence = "I love Python programming"
      result = "Python" in sentence
      print(result)

  - title: "Truthiness Check"
    difficulty: intermediate
    description: "Create a variable empty_list = []. Use a boolean check to print 'List is empty' if the list is empty, otherwise print 'List has items'."
    starter_code: |
      empty_list = []
      # Check and print message

    expected_output: "List is empty"
    hints:
      - "Empty lists are falsy in Python"
      - "Use 'if not empty_list:' to check for emptiness"
    solution: |
      empty_list = []
      if not empty_list:
          print("List is empty")
      else:
          print("List has items")

  - title: "Complex Boolean Logic"
    difficulty: advanced
    description: "A user can access a resource if they are: (admin OR owner) AND account is active. Given is_admin=False, is_owner=True, is_active=True, print the access result."
    starter_code: |
      is_admin = False
      is_owner = True
      is_active = True
      # Calculate access

    expected_output: "True"
    hints:
      - "First evaluate (is_admin or is_owner)"
      - "Then AND that result with is_active"
      - "Use parentheses to control evaluation order"
    solution: |
      is_admin = False
      is_owner = True
      is_active = True
      can_access = (is_admin or is_owner) and is_active
      print(can_access)

  - title: "Age Validator"
    difficulty: advanced
    description: "Create a function is_valid_age(age) that returns True if age is between 0 and 120 (inclusive), False otherwise. Test with age=25 and age=150."
    starter_code: |
      def is_valid_age(age):
          # Return validation result
          pass

      # Test the function

    expected_output: |
      True
      False
    hints:
      - "Use chained comparison: 0 <= age <= 120"
      - "Return the result directly"
      - "Test with both valid and invalid ages"
    solution: |
      def is_valid_age(age):
          return 0 <= age <= 120

      print(is_valid_age(25))
      print(is_valid_age(150))
```
<!-- EXERCISE_END -->
