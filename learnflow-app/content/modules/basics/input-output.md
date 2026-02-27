# Input and Output in Python

Input and output (I/O) operations are fundamental to creating interactive programs. Python provides simple yet powerful built-in functions for reading user input and displaying output, along with advanced formatting capabilities for professional-looking results.

## Basic Output with print()

The `print()` function is the primary way to display output in Python:

```python
# Simple printing
print("Hello, World!")

# Printing variables
name = "Alice"
age = 25
print(name)
print(age)

# Printing multiple values
print("Name:", name, "Age:", age)
# Output: Name: Alice Age: 25

# Print separator (default is space)
print("apple", "banana", "orange", sep=", ")
# Output: apple, banana, orange

print(2025, 2, 9, sep="-")
# Output: 2025-2-9

# Print ending (default is newline)
print("Loading", end="...")
print("Done!")
# Output: Loading...Done!

# Print to file
with open("output.txt", "w") as f:
    print("Hello, File!", file=f)
```

## String Formatting Methods

Python offers several ways to format strings for output:

```python
# Old style: % formatting (legacy)
name = "Alice"
age = 25
message = "My name is %s and I'm %d years old" % (name, age)
print(message)

# .format() method
message = "My name is {} and I'm {} years old".format(name, age)
print(message)

# Named placeholders
message = "My name is {n} and I'm {a} years old".format(n=name, a=age)
print(message)

# Positional arguments
message = "{1} is {0} years old".format(age, name)
print(message)  # "Alice is 25 years old"
```

## F-Strings (Modern and Preferred)

F-strings (formatted string literals) are the most readable and efficient:

```python
# Basic f-string
name = "Alice"
age = 25
print(f"My name is {name} and I'm {age} years old")

# Expressions in f-strings
x = 10
y = 5
print(f"The sum of {x} and {y} is {x + y}")
# Output: The sum of 10 and 5 is 15

# Calling functions in f-strings
def greet(name):
    return f"Hello, {name}!"

print(f"{greet('Bob')}")
# Output: Hello, Bob!

# Number formatting
pi = 3.14159
print(f"Pi: {pi:.2f}")           # 2 decimal places: "Pi: 3.14"
print(f"Pi: {pi:.4f}")           # 4 decimal places: "Pi: 3.1416"

# Width and alignment
name = "Alice"
print(f"{name:>10}")             # Right align: "     Alice"
print(f"{name:<10}")             # Left align: "Alice     "
print(f"{name:^10}")             # Center: "  Alice   "

# Number formatting
price = 1234.56
print(f"${price:,.2f}")          # Thousands separator: "$1,234.56"
print(f"{price:.2e}")            # Scientific: "1.23e+03"

# Percentage
ratio = 0.847
print(f"{ratio:.1%}")            # Percentage: "84.7%"

# Binary, octal, hex
num = 255
print(f"Binary: {num:b}")        # "Binary: 11111111"
print(f"Octal: {num:o}")         # "Octal: 377"
print(f"Hex: {num:x}")           # "Hex: ff"
```

## Reading User Input

The `input()` function reads user input as a string:

```python
# Basic input
name = input("What is your name? ")
print(f"Hello, {name}!")

# Input always returns a string
age_str = input("Enter your age: ")
print(type(age_str))  # <class 'str'>

# Convert input to numbers
age = int(input("Enter your age: "))
price = float(input("Enter price: "))

# Multiple inputs on one line
data = input("Enter name and age (separated by space): ")
name, age = data.split()
age = int(age)

# Safe input with validation
while True:
    try:
        age = int(input("Enter your age: "))
        if 0 <= age <= 120:
            break
        else:
            print("Age must be between 0 and 120")
    except ValueError:
        print("Please enter a valid number")

print(f"Your age is {age}")
```

## Advanced Input Handling

Techniques for robust input processing:

```python
# Strip whitespace from input
name = input("Enter your name: ").strip()

# Case normalization
email = input("Enter email: ").strip().lower()

# Default values
name = input("Enter name (or press Enter for 'Guest'): ").strip()
name = name or "Guest"  # Use "Guest" if empty

# Yes/No input
def get_yes_no(prompt):
    """Get yes/no input from user"""
    while True:
        response = input(prompt + " (yes/no): ").strip().lower()
        if response in ("yes", "y"):
            return True
        elif response in ("no", "n"):
            return False
        else:
            print("Please enter yes or no")

# Multiple choice input
def get_choice(prompt, options):
    """Get choice from list of options"""
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    while True:
        try:
            choice = int(input("Enter choice number: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")

# Usage
favorite = get_choice(
    "What's your favorite fruit?",
    ["Apple", "Banana", "Orange", "Grape"]
)
print(f"You chose: {favorite}")
```

## Formatted Tables and Reports

Creating professional-looking output:

```python
# Simple table
print(f"{'Name':<10} {'Age':>5} {'City':<15}")
print("-" * 32)
print(f"{'Alice':<10} {25:>5} {'New York':<15}")
print(f"{'Bob':<10} {30:>5} {'Los Angeles':<15}")

# Output:
# Name       Age   City
# --------------------------------
# Alice       25   New York
# Bob         30   Los Angeles

# Receipt formatting
items = [
    ("Coffee", 3, 4.50),
    ("Sandwich", 2, 7.99),
    ("Cookie", 5, 2.50),
]

print("=" * 40)
print(f"{'Item':<15} {'Qty':>5} {'Price':>8} {'Total':>10}")
print("-" * 40)

subtotal = 0
for item, qty, price in items:
    total = qty * price
    subtotal += total
    print(f"{item:<15} {qty:>5} ${price:>7.2f} ${total:>9.2f}")

tax = subtotal * 0.08
grand_total = subtotal + tax

print("-" * 40)
print(f"{'Subtotal:':<30} ${subtotal:>9.2f}")
print(f"{'Tax (8%):':<30} ${tax:>9.2f}")
print("=" * 40)
print(f"{'TOTAL:':<30} ${grand_total:>9.2f}")
print("=" * 40)
```

## Best Practices for I/O

Guidelines for effective input and output:

```python
# 1. Always validate user input
def get_positive_number(prompt):
    """Get a positive number from user"""
    while True:
        try:
            num = float(input(prompt))
            if num > 0:
                return num
            print("Number must be positive")
        except ValueError:
            print("Please enter a valid number")

# 2. Provide clear prompts
# Good
age = input("Enter your age (0-120): ")

# Bad
age = input("Age? ")

# 3. Use f-strings for readability
name = "Alice"
score = 95

# Good
print(f"{name} scored {score} points")

# Less readable
print("%s scored %d points" % (name, score))

# 4. Format numbers appropriately
price = 1234.567
print(f"Price: ${price:,.2f}")  # Price: $1,234.57

# 5. Handle errors gracefully
try:
    value = int(input("Enter a number: "))
except ValueError:
    print("Invalid input. Using default value of 0")
    value = 0

# 6. Use meaningful separators
print("Name", "Age", "City", sep=" | ")
# Output: Name | Age | City
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Simple Greeting"
    difficulty: basic
    description: "Use input() to ask for the user's name, then print 'Hello, [name]!' using an f-string. For testing, assume input is 'Alice'."
    starter_code: |
      # Get name and print greeting
      name = "Alice"  # Simulated input

    expected_output: "Hello, Alice!"
    hints:
      - "In real code, use: name = input('Enter your name: ')"
      - "Use an f-string with curly braces for the variable"
    solution: |
      name = "Alice"  # In real code: name = input("Enter your name: ")
      print(f"Hello, {name}!")

  - title: "Print with Separator"
    difficulty: basic
    description: "Print the words 'apple', 'banana', and 'orange' separated by ' - ' using the sep parameter."
    starter_code: |
      # Print with custom separator

    expected_output: "apple - banana - orange"
    hints:
      - "Use print() with multiple arguments"
      - "Use the sep parameter to set the separator"
    solution: |
      print("apple", "banana", "orange", sep=" - ")

  - title: "Number Formatting"
    difficulty: intermediate
    description: "Given price = 1234.567, print it formatted as currency with 2 decimal places and thousands separator: '$1,234.57'"
    starter_code: |
      price = 1234.567
      # Format and print

    expected_output: "$1,234.57"
    hints:
      - "Use an f-string with format specifiers"
      - "Format: {price:,.2f} gives thousands separator and 2 decimals"
    solution: |
      price = 1234.567
      print(f"${price:,.2f}")

  - title: "Calculate with Input"
    difficulty: intermediate
    description: "Simulate getting two numbers (10 and 5) as input, convert them to integers, add them, and print 'The sum is: 15'. Use simulated input for testing."
    starter_code: |
      # Simulated input
      num1_str = "10"
      num2_str = "5"
      # Convert, calculate, and print

    expected_output: "The sum is: 15"
    hints:
      - "Use int() to convert strings to integers"
      - "Add the converted numbers"
      - "Use an f-string for the output"
    solution: |
      num1_str = "10"
      num2_str = "5"
      num1 = int(num1_str)
      num2 = int(num2_str)
      total = num1 + num2
      print(f"The sum is: {total}")

  - title: "Formatted Table Row"
    difficulty: advanced
    description: "Print a table row with name 'Alice' (left-aligned, width 10), age 25 (right-aligned, width 5), and city 'Boston' (left-aligned, width 12)."
    starter_code: |
      name = "Alice"
      age = 25
      city = "Boston"
      # Print formatted row

    expected_output: "Alice          25 Boston      "
    hints:
      - "Use f-string with alignment: {name:<10} for left align"
      - "Use {age:>5} for right align"
      - "Combine all in one print statement"
    solution: |
      name = "Alice"
      age = 25
      city = "Boston"
      print(f"{name:<10} {age:>5} {city:<12}")

  - title: "Receipt Calculator"
    difficulty: advanced
    description: "Calculate a receipt: item price $29.99, quantity 3. Print: 'Subtotal: $89.97', 'Tax (10%): $9.00', 'Total: $98.97'. Format all with 2 decimals."
    starter_code: |
      price = 29.99
      quantity = 3
      tax_rate = 0.10
      # Calculate and print receipt

    expected_output: |
      Subtotal: $89.97
      Tax (10%): $9.00
      Total: $98.97
    hints:
      - "Calculate subtotal = price * quantity"
      - "Calculate tax = subtotal * tax_rate"
      - "Calculate total = subtotal + tax"
      - "Use f-strings with :.2f for 2 decimal places"
    solution: |
      price = 29.99
      quantity = 3
      tax_rate = 0.10

      subtotal = price * quantity
      tax = subtotal * tax_rate
      total = subtotal + tax

      print(f"Subtotal: ${subtotal:.2f}")
      print(f"Tax (10%): ${tax:.2f}")
      print(f"Total: ${total:.2f}")
```
<!-- EXERCISE_END -->
