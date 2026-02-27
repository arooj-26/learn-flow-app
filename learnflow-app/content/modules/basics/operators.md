# Operators in Python

Operators are special symbols that perform operations on variables and values. Python has several types of operators.

## Arithmetic Operators

Used for mathematical calculations:

```python
a = 10
b = 3

print(a + b)   # Addition: 13
print(a - b)   # Subtraction: 7
print(a * b)   # Multiplication: 30
print(a / b)   # Division: 3.333...
print(a // b)  # Floor division: 3
print(a % b)   # Modulus (remainder): 1
print(a ** b)  # Exponentiation: 1000
```

### Operator Precedence

Python follows mathematical precedence (PEMDAS):
1. Parentheses `()`
2. Exponentiation `**`
3. Multiplication/Division `* / // %`
4. Addition/Subtraction `+ -`

```python
result = 2 + 3 * 4      # 14 (not 20)
result = (2 + 3) * 4    # 20 (parentheses first)
```

## Comparison Operators

Used to compare values, returning `True` or `False`:

```python
x = 5
y = 10

print(x == y)   # Equal: False
print(x != y)   # Not equal: True
print(x < y)    # Less than: True
print(x > y)    # Greater than: False
print(x <= y)   # Less or equal: True
print(x >= y)   # Greater or equal: False
```

## Logical Operators

Used to combine conditional statements:

```python
a = True
b = False

print(a and b)  # Both True? False
print(a or b)   # At least one True? True
print(not a)    # Opposite: False
```

### Truth Table

| A | B | A and B | A or B |
|---|---|---------|--------|
| True | True | True | True |
| True | False | False | True |
| False | True | False | True |
| False | False | False | False |

## Assignment Operators

Shortcuts for modifying variables:

```python
x = 10

x += 5   # Same as: x = x + 5  → 15
x -= 3   # Same as: x = x - 3  → 12
x *= 2   # Same as: x = x * 2  → 24
x /= 4   # Same as: x = x / 4  → 6.0
x //= 2  # Same as: x = x // 2 → 3.0
x %= 2   # Same as: x = x % 2  → 1.0
x **= 3  # Same as: x = x ** 3 → 1.0
```

## Membership Operators

Check if a value exists in a sequence:

```python
fruits = ["apple", "banana", "cherry"]

print("apple" in fruits)     # True
print("grape" in fruits)     # False
print("grape" not in fruits) # True
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Basic Arithmetic"
    difficulty: basic
    description: "Calculate and print the sum, difference, and product of 15 and 4."
    starter_code: |
      a = 15
      b = 4
      # Calculate sum, difference, product

    expected_output: |
      19
      11
      60
    hints:
      - "Use + for addition, - for subtraction, * for multiplication"
    solution: |
      a = 15
      b = 4
      print(a + b)
      print(a - b)
      print(a * b)

  - title: "Division Types"
    difficulty: basic
    description: "Divide 17 by 5 using regular division, floor division, and modulus. Print all three results."
    starter_code: |
      # Calculate different division types
      num = 17
      divisor = 5

    expected_output: |
      3.4
      3
      2
    hints:
      - "/ gives float division"
      - "// gives integer (floor) division"
      - "% gives the remainder"
    solution: |
      num = 17
      divisor = 5
      print(num / divisor)
      print(num // divisor)
      print(num % divisor)

  - title: "Comparison Chain"
    difficulty: intermediate
    description: "Given x=7, check if x is between 5 and 10 (inclusive). Print the result."
    starter_code: |
      x = 7
      # Check if x is between 5 and 10

    expected_output: "True"
    hints:
      - "You can chain comparisons: 5 <= x <= 10"
      - "Or use 'and': x >= 5 and x <= 10"
    solution: |
      x = 7
      print(5 <= x <= 10)

  - title: "Logical Operations"
    difficulty: intermediate
    description: "Given age=20 and has_license=True, check if the person can drive (age >= 18 AND has license)."
    starter_code: |
      age = 20
      has_license = True
      # Check if can drive

    expected_output: "True"
    hints:
      - "Use 'and' to check both conditions"
    solution: |
      age = 20
      has_license = True
      can_drive = age >= 18 and has_license
      print(can_drive)

  - title: "Compound Assignment"
    difficulty: advanced
    description: "Start with x=100. Subtract 25, then multiply by 2, then floor divide by 3. Print the final result."
    starter_code: |
      x = 100
      # Use compound assignment operators

    expected_output: "50"
    hints:
      - "Use -=, *=, //= operators"
    solution: |
      x = 100
      x -= 25
      x *= 2
      x //= 3
      print(x)

  - title: "Complex Expression"
    difficulty: advanced
    description: "Calculate: (2 ** 3 + 4 * 5) // 7. Print the result and explain the order of operations."
    starter_code: |
      # Calculate the expression

    expected_output: "4"
    hints:
      - "Order: exponent first, then multiplication, then addition, then floor division"
      - "2**3=8, 4*5=20, 8+20=28, 28//7=4"
    solution: |
      result = (2 ** 3 + 4 * 5) // 7
      print(result)
```
<!-- EXERCISE_END -->
