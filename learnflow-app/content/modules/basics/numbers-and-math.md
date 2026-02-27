# Numbers and Math Operations in Python

Python provides powerful built-in capabilities for working with numbers and performing mathematical operations. Understanding numeric types and math operations is fundamental to data analysis, scientific computing, and general programming.

## Numeric Types

Python has three primary numeric types: integers, floats, and complex numbers.

```python
# Integers - whole numbers
count = 42
temperature = -15
big_number = 1_000_000  # Underscores for readability

# Floats - decimal numbers
price = 19.99
pi = 3.14159
scientific = 2.5e-4  # Scientific notation: 0.00025

# Complex numbers - for advanced math
z = 3 + 4j
real_part = z.real      # 3.0
imaginary_part = z.imag # 4.0
```

## Basic Arithmetic Operations

Python supports all standard mathematical operations with intuitive syntax:

| Operator | Operation | Example | Result |
|----------|-----------|---------|--------|
| `+` | Addition | `10 + 5` | `15` |
| `-` | Subtraction | `10 - 5` | `5` |
| `*` | Multiplication | `10 * 5` | `50` |
| `/` | Division (float) | `10 / 3` | `3.333...` |
| `//` | Floor division | `10 // 3` | `3` |
| `%` | Modulus (remainder) | `10 % 3` | `1` |
| `**` | Exponentiation | `2 ** 3` | `8` |

```python
# Division types
regular_division = 10 / 4    # 2.5 (always returns float)
floor_division = 10 // 4     # 2 (rounds down to integer)
remainder = 10 % 4           # 2 (the remainder)

# Order of operations (PEMDAS)
result = 2 + 3 * 4 ** 2      # 50 (not 400)
result_with_parens = (2 + 3) * 4 ** 2  # 80
```

## Built-in Math Functions

Python includes several built-in functions for common mathematical operations:

```python
# Absolute value
distance = abs(-42)          # 42
diff = abs(10 - 25)          # 15

# Rounding
pi_rounded = round(3.14159, 2)    # 3.14 (2 decimal places)
half = round(2.5)                  # 2 (rounds to nearest even)
half_up = round(3.5)               # 4

# Power and root
squared = pow(5, 2)          # 25
cubed = pow(2, 3)            # 8
square_root = pow(25, 0.5)   # 5.0

# Min and max
smallest = min(5, 2, 9, 1)   # 1
largest = max(5, 2, 9, 1)    # 9
total = sum([1, 2, 3, 4, 5]) # 15
```

## The Math Module

For advanced mathematical operations, Python provides the `math` module:

```python
import math

# Common constants
circle_area = math.pi * (5 ** 2)  # Using pi
euler = math.e                     # Euler's number

# Trigonometric functions (radians)
sine = math.sin(math.pi / 2)      # 1.0
cosine = math.cos(0)               # 1.0
tangent = math.tan(math.pi / 4)   # 1.0

# Logarithms
natural_log = math.log(math.e)    # 1.0
log_base_10 = math.log10(100)     # 2.0
log_base_2 = math.log2(8)         # 3.0

# Advanced functions
ceiling = math.ceil(3.2)          # 4 (round up)
floor = math.floor(3.9)           # 3 (round down)
square_root = math.sqrt(16)       # 4.0
factorial = math.factorial(5)     # 120 (5! = 5*4*3*2*1)

# Practical example: Distance formula
x1, y1 = 0, 0
x2, y2 = 3, 4
distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  # 5.0
```

## Number Precision and Formatting

Working with floating-point numbers requires understanding precision:

```python
# Floating-point precision issues
result = 0.1 + 0.2  # 0.30000000000000004 (not exactly 0.3!)

# Use round() for display
display_result = round(0.1 + 0.2, 2)  # 0.3

# Format strings for controlled output
price = 19.99
formatted = f"${price:.2f}"           # $19.99
scientific = f"{1234567:.2e}"         # 1.23e+06
percentage = f"{0.847:.1%}"           # 84.7%

# For financial calculations, use the decimal module
from decimal import Decimal
price1 = Decimal('19.99')
price2 = Decimal('5.01')
total = price1 + price2  # Decimal('25.00') - exact!
```

## Best Practices for Numeric Operations

1. **Use appropriate types**: Choose integers for counting, floats for measurements
2. **Be aware of division**: Remember `/` always returns float, use `//` for integer division
3. **Handle precision**: Round or format floats for display, use Decimal for money
4. **Avoid magic numbers**: Use named constants for clarity
5. **Check for division by zero**: Validate inputs before dividing

```python
# Good practice example
TAX_RATE = 0.08  # Named constant
SHIPPING_THRESHOLD = 50

subtotal = 45.99
shipping = 0 if subtotal >= SHIPPING_THRESHOLD else 5.99
tax = subtotal * TAX_RATE
total = round(subtotal + shipping + tax, 2)

print(f"Total: ${total:.2f}")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Calculate Circle Area"
    difficulty: basic
    description: "Given a radius of 5, calculate the area of a circle using the formula: area = π × r². Use 3.14159 for π."
    starter_code: |
      radius = 5
      # Calculate area

    expected_output: "78.53975"
    hints:
      - "Use the ** operator for squaring"
      - "Multiply pi by radius squared"
    solution: |
      radius = 5
      pi = 3.14159
      area = pi * radius ** 2
      print(area)

  - title: "Temperature Converter"
    difficulty: basic
    description: "Convert 100 degrees Fahrenheit to Celsius using the formula: C = (F - 32) × 5/9. Round to 1 decimal place."
    starter_code: |
      fahrenheit = 100
      # Convert to Celsius

    expected_output: "37.8"
    hints:
      - "Follow the order of operations: subtract first, then multiply"
      - "Use round() with 1 as the second argument"
    solution: |
      fahrenheit = 100
      celsius = (fahrenheit - 32) * 5 / 9
      print(round(celsius, 1))

  - title: "Split Bill Calculator"
    difficulty: intermediate
    description: "A restaurant bill of $127.50 needs to be split among 4 people with a 15% tip. Calculate the amount each person pays, rounded to 2 decimal places."
    starter_code: |
      bill = 127.50
      people = 4
      tip_rate = 0.15
      # Calculate per person amount

    expected_output: "36.66"
    hints:
      - "First calculate the total bill including tip"
      - "Then divide by the number of people"
      - "Use round() with 2 decimal places"
    solution: |
      bill = 127.50
      people = 4
      tip_rate = 0.15
      total_with_tip = bill * (1 + tip_rate)
      per_person = total_with_tip / people
      print(round(per_person, 2))

  - title: "Distance Calculator"
    difficulty: intermediate
    description: "Calculate the distance between two points (x1=2, y1=3) and (x2=8, y2=11) using the distance formula: √((x2-x1)² + (y2-y1)²). Round to 2 decimal places."
    starter_code: |
      x1, y1 = 2, 3
      x2, y2 = 8, 11
      # Calculate distance

    expected_output: "10.0"
    hints:
      - "Use ** 0.5 or math.sqrt() for square root"
      - "Square the differences first, then add, then take square root"
    solution: |
      x1, y1 = 2, 3
      x2, y2 = 8, 11
      distance = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
      print(round(distance, 2))

  - title: "Compound Interest Calculator"
    difficulty: advanced
    description: "Calculate the future value of $1000 invested at 5% annual interest compounded monthly for 3 years using: A = P(1 + r/n)^(nt). Print result rounded to 2 decimals."
    starter_code: |
      principal = 1000
      rate = 0.05
      times_compounded = 12
      years = 3
      # Calculate future value

    expected_output: "1161.47"
    hints:
      - "Divide rate by times_compounded to get the periodic rate"
      - "Multiply times_compounded by years for the exponent"
      - "Use ** for exponentiation"
    solution: |
      principal = 1000
      rate = 0.05
      times_compounded = 12
      years = 3
      amount = principal * (1 + rate / times_compounded) ** (times_compounded * years)
      print(round(amount, 2))

  - title: "BMI Calculator"
    difficulty: advanced
    description: "Calculate BMI (Body Mass Index) for weight=70kg and height=1.75m using formula: BMI = weight / height². Determine category: <18.5 'Underweight', 18.5-24.9 'Normal', 25-29.9 'Overweight', ≥30 'Obese'. Print both BMI and category."
    starter_code: |
      weight = 70
      height = 1.75
      # Calculate BMI and determine category

    expected_output: |
      BMI: 22.86
      Category: Normal
    hints:
      - "Square the height using ** 2"
      - "Use if-elif-else to determine the category"
      - "Round BMI to 2 decimal places for display"
    solution: |
      weight = 70
      height = 1.75
      bmi = weight / height ** 2

      if bmi < 18.5:
          category = "Underweight"
      elif bmi < 25:
          category = "Normal"
      elif bmi < 30:
          category = "Overweight"
      else:
          category = "Obese"

      print(f"BMI: {round(bmi, 2)}")
      print(f"Category: {category}")
```
<!-- EXERCISE_END -->
