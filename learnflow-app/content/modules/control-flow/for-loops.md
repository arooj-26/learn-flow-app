# For Loops in Python

For loops are used to iterate over sequences like lists, strings, tuples, or ranges. They execute a block of code for each item in the sequence.

## Basic For Loop

```python
# Iterating over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
# Output:
# apple
# banana
# cherry
```

## Using range()

The `range()` function generates a sequence of numbers:

```python
# range(stop) - 0 to stop-1
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# range(start, stop) - start to stop-1
for i in range(2, 6):
    print(i)  # 2, 3, 4, 5

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Counting backwards
for i in range(5, 0, -1):
    print(i)  # 5, 4, 3, 2, 1
```

## Iterating Over Strings

Strings are sequences of characters:

```python
word = "Python"
for letter in word:
    print(letter)
# P, y, t, h, o, n
```

## enumerate() Function

Get both index and value while iterating:

```python
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry
```

## Nested Loops

Loops inside loops:

```python
for i in range(3):
    for j in range(3):
        print(f"({i}, {j})", end=" ")
    print()  # New line
# (0, 0) (0, 1) (0, 2)
# (1, 0) (1, 1) (1, 2)
# (2, 0) (2, 1) (2, 2)
```

## Loop with else

The `else` block executes when the loop completes normally (without break):

```python
for i in range(5):
    print(i)
else:
    print("Loop completed!")
```

## Common Patterns

### Sum of Numbers
```python
total = 0
for num in range(1, 11):
    total += num
print(total)  # 55
```

### Finding Maximum
```python
numbers = [3, 7, 2, 9, 1]
maximum = numbers[0]
for num in numbers:
    if num > maximum:
        maximum = num
print(maximum)  # 9
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Print Numbers 1-5"
    difficulty: basic
    description: "Use a for loop to print numbers from 1 to 5, each on a new line."
    starter_code: |
      # Print numbers 1 to 5

    expected_output: |
      1
      2
      3
      4
      5
    hints:
      - "Use range(1, 6) to get numbers 1 through 5"
      - "Remember: range(start, stop) excludes stop"
    solution: |
      for i in range(1, 6):
          print(i)

  - title: "Sum of Range"
    difficulty: basic
    description: "Calculate and print the sum of numbers from 1 to 10 using a for loop."
    starter_code: |
      total = 0
      # Add numbers 1-10 to total

    expected_output: "55"
    hints:
      - "Use += to add each number to total"
      - "range(1, 11) gives you 1 through 10"
    solution: |
      total = 0
      for i in range(1, 11):
          total += i
      print(total)

  - title: "Print List Items"
    difficulty: intermediate
    description: "Given the list `colors = ['red', 'green', 'blue']`, print each color in uppercase."
    starter_code: |
      colors = ['red', 'green', 'blue']
      # Print each color in uppercase

    expected_output: |
      RED
      GREEN
      BLUE
    hints:
      - "Use .upper() method on strings"
      - "Iterate directly over the list"
    solution: |
      colors = ['red', 'green', 'blue']
      for color in colors:
          print(color.upper())

  - title: "Even Numbers"
    difficulty: intermediate
    description: "Print all even numbers from 2 to 20 (inclusive)."
    starter_code: |
      # Print even numbers 2-20

    expected_output: |
      2
      4
      6
      8
      10
      12
      14
      16
      18
      20
    hints:
      - "Use range(start, stop, step) with step=2"
      - "Or use range and check if num % 2 == 0"
    solution: |
      for i in range(2, 21, 2):
          print(i)

  - title: "Multiplication Table"
    difficulty: advanced
    description: "Print the multiplication table for 7 (7x1 through 7x10), showing '7 x 1 = 7' format."
    starter_code: |
      # Print 7's multiplication table

    expected_output: |
      7 x 1 = 7
      7 x 2 = 14
      7 x 3 = 21
      7 x 4 = 28
      7 x 5 = 35
      7 x 6 = 42
      7 x 7 = 49
      7 x 8 = 56
      7 x 9 = 63
      7 x 10 = 70
    hints:
      - "Use f-string for formatting"
      - "range(1, 11) gives 1-10"
    solution: |
      for i in range(1, 11):
          print(f"7 x {i} = {7 * i}")

  - title: "Triangle Pattern"
    difficulty: advanced
    description: "Print a right triangle pattern with 5 rows using asterisks (*)."
    starter_code: |
      # Print:
      # *
      # **
      # ***
      # ****
      # *****

    expected_output: |
      *
      **
      ***
      ****
      *****
    hints:
      - "Use string multiplication: '*' * n"
      - "Or use nested loops"
    solution: |
      for i in range(1, 6):
          print('*' * i)
```
<!-- EXERCISE_END -->
