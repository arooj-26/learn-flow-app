# Nested Loops in Python

Nested loops are loops placed inside other loops. The inner loop completes all its iterations for each single iteration of the outer loop. They are essential for working with multi-dimensional data, generating patterns, and solving complex algorithmic problems.

## Basic Nested Loop Structure

```python
# The inner loop runs completely for each outer loop iteration
for i in range(3):
    for j in range(4):
        print(f"({i},{j})", end=" ")
    print()  # New line after each row

# Output:
# (0,0) (0,1) (0,2) (0,3)
# (1,0) (1,1) (1,2) (1,3)
# (2,0) (2,1) (2,2) (2,3)
```

The total number of iterations is the product of the ranges: 3 × 4 = 12 iterations.

## Working with 2D Data

Nested loops are natural for processing matrices, grids, and tables:

```python
# Processing a 2D matrix
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Print matrix in grid format
for row in matrix:
    for value in row:
        print(f"{value:3d}", end=" ")
    print()

# Calculate row sums
for i, row in enumerate(matrix):
    row_sum = 0
    for value in row:
        row_sum += value
    print(f"Row {i} sum: {row_sum}")

# Find maximum value and its position
max_val = matrix[0][0]
max_pos = (0, 0)
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        if matrix[i][j] > max_val:
            max_val = matrix[i][j]
            max_pos = (i, j)
print(f"Max value {max_val} at position {max_pos}")
```

## Pattern Generation

Nested loops are commonly used to generate text-based patterns:

```python
# Right triangle
n = 5
for i in range(1, n + 1):
    for j in range(i):
        print("*", end=" ")
    print()
# *
# * *
# * * *
# * * * *
# * * * * *

# Multiplication table
print("   ", end="")
for j in range(1, 6):
    print(f"{j:4d}", end="")
print()
print("   " + "----" * 5)

for i in range(1, 6):
    print(f"{i:2d}|", end="")
    for j in range(1, 6):
        print(f"{i*j:4d}", end="")
    print()
```

## Nested While Loops

While loops can also be nested, useful for dynamic termination conditions:

```python
# Menu system with sub-menus
categories = {"Fruits": ["Apple", "Banana", "Cherry"],
              "Colors": ["Red", "Blue", "Green"]}

for category, items in categories.items():
    print(f"\n{category}:")
    count = 0
    while count < len(items):
        print(f"  {count + 1}. {items[count]}")
        count += 1
```

## Controlling Nested Loops with Break and Continue

`break` and `continue` only affect the innermost loop they're in:

```python
# Break only exits the inner loop
for i in range(3):
    for j in range(5):
        if j == 3:
            break
        print(f"({i},{j})", end=" ")
    print()
# (0,0) (0,1) (0,2)
# (1,0) (1,1) (1,2)
# (2,0) (2,1) (2,2)

# Using a flag to break out of both loops
found = False
for i in range(5):
    for j in range(5):
        if i * j == 12:
            print(f"Found: {i} * {j} = 12")
            found = True
            break
    if found:
        break

# Using else clause with nested loops
for i in range(2, 20):
    for j in range(2, i):
        if i % j == 0:
            break
    else:
        print(f"{i} is prime")
```

## Performance Considerations

Nested loops can become expensive. Understanding time complexity helps:

```python
# O(n^2) - Quadratic time
n = 1000
count = 0
for i in range(n):
    for j in range(n):
        count += 1
# count = 1,000,000

# Optimization: avoid unnecessary inner iterations
# Instead of checking all pairs:
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
# Bad: O(n^2) to find duplicates
duplicates = []
for i in range(len(numbers)):
    for j in range(i + 1, len(numbers)):
        if numbers[i] == numbers[j] and numbers[i] not in duplicates:
            duplicates.append(numbers[i])

# Better: O(n) using a set
seen = set()
duplicates_fast = set()
for num in numbers:
    if num in seen:
        duplicates_fast.add(num)
    seen.add(num)
```

## Real-World Applications

```python
# Comparing elements across two lists
students = ["Alice", "Bob", "Charlie"]
courses = ["Math", "Science"]

enrollments = []
for student in students:
    for course in courses:
        enrollments.append(f"{student} -> {course}")

for e in enrollments:
    print(e)

# Flattening nested data
nested = [[1, 2], [3, 4, 5], [6]]
flat = []
for sublist in nested:
    for item in sublist:
        flat.append(item)
print(flat)  # [1, 2, 3, 4, 5, 6]

# Equivalent list comprehension
flat_comp = [item for sublist in nested for item in sublist]
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Simple Grid"
    difficulty: basic
    description: "Print a 3x3 grid of asterisks where each row has 3 stars separated by spaces."
    starter_code: |
      # Print a 3x3 grid of asterisks

    expected_output: |
      * * *
      * * *
      * * *
    hints:
      - "Use two nested for loops with range(3)"
      - "Use end=' ' in the inner print and print() for newlines"
    solution: |
      for i in range(3):
          for j in range(3):
              print("*", end=" ")
          print()

  - title: "Row Sums"
    difficulty: basic
    description: "Given a 2D list, print the sum of each row on a separate line."
    starter_code: |
      matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
      # Print the sum of each row

    expected_output: |
      6
      15
      24
    hints:
      - "Loop through each row in the matrix"
      - "Use an inner loop or sum() to add up elements"
    solution: |
      matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
      for row in matrix:
          total = 0
          for val in row:
              total += val
          print(total)

  - title: "Right Triangle Pattern"
    difficulty: intermediate
    description: "Print a right triangle pattern with 5 rows using numbers. Row 1 prints '1', row 2 prints '1 2', and so on."
    starter_code: |
      # Print a number triangle with 5 rows

    expected_output: |
      1
      1 2
      1 2 3
      1 2 3 4
      1 2 3 4 5
    hints:
      - "The outer loop controls which row (1 to 5)"
      - "The inner loop prints numbers from 1 to the current row number"
    solution: |
      for i in range(1, 6):
          for j in range(1, i + 1):
              print(j, end=" " if j < i else "")
          print()

  - title: "Flatten Nested List"
    difficulty: intermediate
    description: "Flatten the nested list [[1, 2], [3, 4, 5], [6, 7]] into a single list and print it."
    starter_code: |
      nested = [[1, 2], [3, 4, 5], [6, 7]]
      # Flatten using nested loops

    expected_output: "[1, 2, 3, 4, 5, 6, 7]"
    hints:
      - "Create an empty result list"
      - "Use nested loops to iterate through sublists and their items"
    solution: |
      nested = [[1, 2], [3, 4, 5], [6, 7]]
      flat = []
      for sublist in nested:
          for item in sublist:
              flat.append(item)
      print(flat)

  - title: "Find Common Elements"
    difficulty: advanced
    description: "Find all common elements between list1 = [1, 3, 5, 7, 9] and list2 = [2, 3, 5, 8, 9] using nested loops. Print the sorted result as a list."
    starter_code: |
      list1 = [1, 3, 5, 7, 9]
      list2 = [2, 3, 5, 8, 9]
      # Find common elements using nested loops

    expected_output: "[3, 5, 9]"
    hints:
      - "Use nested loops to compare each element of list1 with each element of list2"
      - "Append matches to a result list"
    solution: |
      list1 = [1, 3, 5, 7, 9]
      list2 = [2, 3, 5, 8, 9]
      common = []
      for a in list1:
          for b in list2:
              if a == b:
                  common.append(a)
      print(sorted(common))

  - title: "Matrix Transpose"
    difficulty: advanced
    description: "Transpose a 3x3 matrix (swap rows and columns) using nested loops and print each row of the result."
    starter_code: |
      matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
      # Transpose the matrix

    expected_output: |
      [1, 4, 7]
      [2, 5, 8]
      [3, 6, 9]
    hints:
      - "In a transpose, element at (i,j) moves to (j,i)"
      - "Create a new matrix where rows become columns"
    solution: |
      matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
      rows = len(matrix)
      cols = len(matrix[0])
      transposed = []
      for j in range(cols):
          new_row = []
          for i in range(rows):
              new_row.append(matrix[i][j])
          transposed.append(new_row)
      for row in transposed:
          print(row)
```
<!-- EXERCISE_END -->
