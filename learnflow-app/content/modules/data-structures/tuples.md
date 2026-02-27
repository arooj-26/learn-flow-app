# Tuples

Tuples are immutable sequences in Python, meaning once created, their elements cannot be changed, added, or removed. This immutability makes tuples perfect for representing fixed collections of items, such as coordinates, database records, or function return values. Tuples are faster than lists and can be used as dictionary keys, making them a powerful tool in your Python arsenal.

## Creating and Accessing Tuples

Tuples are created using parentheses `()` or simply by separating values with commas. They can contain elements of different data types.

```python
# Various ways to create tuples
coordinates = (10, 20)
rgb_color = (255, 128, 0)
person = ("Alice", 28, "Engineer")

# Tuple without parentheses (tuple packing)
point = 5, 10, 15

# Single element tuple (note the comma!)
single = (42,)  # This is a tuple
not_tuple = (42)  # This is just an integer

print(f"Coordinates: {coordinates}, Type: {type(coordinates)}")
print(f"Single: {single}, Type: {type(single)}")
print(f"Not tuple: {not_tuple}, Type: {type(not_tuple)}")

# Accessing elements (zero-indexed like lists)
print(f"Person name: {person[0]}")
print(f"Person age: {person[1]}")
print(f"Red value: {rgb_color[0]}")

# Negative indexing
print(f"Last element: {person[-1]}")
print(f"Second to last: {person[-2]}")

# Slicing tuples
numbers = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
print(f"First five: {numbers[:5]}")
print(f"Last three: {numbers[-3:]}")
print(f"Every second: {numbers[::2]}")
```

## Tuple Operations and Methods

While tuples are immutable, they support various operations for accessing and analyzing data. They have only two methods: `count()` and `index()`.

```python
# Tuple concatenation (creates new tuple)
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)
combined = tuple1 + tuple2
print(f"Combined: {combined}")

# Tuple repetition
pattern = ("X", "O")
repeated = pattern * 4
print(f"Repeated pattern: {repeated}")

# count() - count occurrences
grades = (85, 90, 85, 92, 85, 88, 90)
count_85 = grades.count(85)
count_90 = grades.count(90)
print(f"Number of 85s: {count_85}")
print(f"Number of 90s: {count_90}")

# index() - find first occurrence
position = grades.index(92)
print(f"First 92 at index: {position}")

# Membership testing
print(f"Is 90 in grades? {90 in grades}")
print(f"Is 100 in grades? {100 in grades}")

# Length and min/max
print(f"Number of grades: {len(grades)}")
print(f"Highest grade: {max(grades)}")
print(f"Lowest grade: {min(grades)}")
print(f"Average: {sum(grades) / len(grades):.2f}")
```

Common tuple operations:

| Operation | Description | Example |
|-----------|-------------|---------|
| `+` | Concatenation | `(1, 2) + (3, 4)` → `(1, 2, 3, 4)` |
| `*` | Repetition | `(1, 2) * 3` → `(1, 2, 1, 2, 1, 2)` |
| `in` | Membership | `2 in (1, 2, 3)` → `True` |
| `len()` | Length | `len((1, 2, 3))` → `3` |
| `count()` | Count occurrences | `(1, 2, 1).count(1)` → `2` |
| `index()` | Find position | `(1, 2, 3).index(2)` → `1` |

## Tuple Unpacking and Multiple Assignment

Tuple unpacking is one of Python's most elegant features, allowing you to assign multiple variables in a single statement.

```python
# Basic unpacking
person = ("Bob", 30, "Designer")
name, age, job = person
print(f"{name} is {age} years old and works as a {job}")

# Swapping variables (Python magic!)
a, b = 10, 20
print(f"Before swap: a={a}, b={b}")
a, b = b, a
print(f"After swap: a={a}, b={b}")

# Function returning multiple values
def get_statistics(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

data = [85, 92, 78, 95, 88]
minimum, maximum, average = get_statistics(data)
print(f"Min: {minimum}, Max: {maximum}, Avg: {average:.2f}")

# Extended unpacking with *
first, *middle, last = (1, 2, 3, 4, 5, 6)
print(f"First: {first}")
print(f"Middle: {middle}")  # This is a list!
print(f"Last: {last}")

# Unpacking in loops
employees = [
    ("Alice", "Engineering", 95000),
    ("Bob", "Design", 85000),
    ("Charlie", "Marketing", 80000)
]

for name, dept, salary in employees:
    print(f"{name} works in {dept} and earns ${salary:,}")

# Ignoring values with underscore
x, _, z = (10, 20, 30)  # Ignore the middle value
print(f"x={x}, z={z}")
```

## Named Tuples: Tuples with Field Names

Named tuples from the `collections` module provide a way to create tuple subclasses with named fields, making code more readable and self-documenting.

```python
from collections import namedtuple

# Define a named tuple type
Point = namedtuple('Point', ['x', 'y'])
Person = namedtuple('Person', ['name', 'age', 'city'])

# Create instances
p1 = Point(10, 20)
p2 = Point(x=30, y=40)

# Access by name (more readable!)
print(f"Point 1: x={p1.x}, y={p1.y}")
print(f"Point 2: x={p2.x}, y={p2.y}")

# Still works like regular tuples
print(f"Point by index: {p1[0]}, {p1[1]}")

# Real-world example: Managing employee records
Employee = namedtuple('Employee', ['id', 'name', 'department', 'salary'])

employees = [
    Employee(101, "Alice", "Engineering", 95000),
    Employee(102, "Bob", "Design", 85000),
    Employee(103, "Charlie", "Marketing", 80000)
]

# More readable code
for emp in employees:
    if emp.salary > 82000:
        print(f"{emp.name} ({emp.department}): ${emp.salary:,}")

# Named tuples are immutable but can be "updated" with _replace
updated_alice = employees[0]._replace(salary=100000)
print(f"Updated: {updated_alice}")

# Convert to dictionary
emp_dict = employees[0]._asdict()
print(f"As dict: {emp_dict}")

# Using named tuples for function returns
Rectangle = namedtuple('Rectangle', ['width', 'height', 'area', 'perimeter'])

def analyze_rectangle(width, height):
    area = width * height
    perimeter = 2 * (width + height)
    return Rectangle(width, height, area, perimeter)

rect = analyze_rectangle(5, 10)
print(f"Rectangle: {rect.width}x{rect.height}")
print(f"Area: {rect.area}, Perimeter: {rect.perimeter}")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "RGB Color Manager"
    difficulty: basic
    description: "Create RGB color tuples and calculate their brightness using the formula: (R + G + B) / 3."
    starter_code: |
      red = (255, 0, 0)
      green = (0, 255, 0)
      blue = (0, 0, 255)

      # Calculate and print brightness for each color
      # Format: "Color (R, G, B): brightness"

    expected_output: |
      Color (255, 0, 0): 85.0
      Color (0, 255, 0): 85.0
      Color (0, 0, 255): 85.0
    hints:
      - "Access tuple elements by index: color[0], color[1], color[2]"
      - "Calculate brightness as (R + G + B) / 3"
      - "Use sum(color) to add all elements"
    solution: |
      red = (255, 0, 0)
      green = (0, 255, 0)
      blue = (0, 0, 255)

      # Calculate and print brightness for each color
      for color in [red, green, blue]:
          brightness = sum(color) / 3
          print(f"Color {color}: {brightness}")

  - title: "Tuple Unpacking Practice"
    difficulty: basic
    description: "Use tuple unpacking to swap the values of three variables in a circular manner (a→b, b→c, c→a)."
    starter_code: |
      a, b, c = 1, 2, 3
      print(f"Before: a={a}, b={b}, c={c}")

      # Perform circular swap using tuple unpacking

      print(f"After: a={a}, b={b}, c={c}")

    expected_output: |
      Before: a=1, b=2, c=3
      After: a=3, b=1, c=2
    hints:
      - "Use tuple packing and unpacking: a, b, c = new_a, new_b, new_c"
      - "For circular swap: a gets c's value, b gets a's value, c gets b's value"
    solution: |
      a, b, c = 1, 2, 3
      print(f"Before: a={a}, b={b}, c={c}")

      # Perform circular swap using tuple unpacking
      a, b, c = c, a, b

      print(f"After: a={a}, b={b}, c={c}")

  - title: "Student Record Analyzer"
    difficulty: intermediate
    description: "Given a list of student tuples (name, math, science, english), calculate and display each student's average score."
    starter_code: |
      students = [
          ("Alice", 85, 90, 88),
          ("Bob", 78, 82, 80),
          ("Charlie", 92, 95, 89)
      ]

      # Calculate and display each student's average
      # Format: "Name: average"

    expected_output: |
      Alice: 87.67
      Bob: 80.00
      Charlie: 92.00
    hints:
      - "Unpack the tuple in the loop: name, math, science, english"
      - "Calculate average of the three scores"
      - "Use :.2f for formatting to 2 decimal places"
    solution: |
      students = [
          ("Alice", 85, 90, 88),
          ("Bob", 78, 82, 80),
          ("Charlie", 92, 95, 89)
      ]

      # Calculate and display each student's average
      for name, math, science, english in students:
          average = (math + science + english) / 3
          print(f"{name}: {average:.2f}")

  - title: "Coordinate Distance Calculator"
    difficulty: intermediate
    description: "Calculate the Euclidean distance between two 3D points using tuples. Distance = sqrt((x2-x1)² + (y2-y1)² + (z2-z1)²)"
    starter_code: |
      import math

      point1 = (0, 0, 0)
      point2 = (3, 4, 0)

      # Calculate Euclidean distance
      # Print the result rounded to 2 decimal places

    expected_output: |
      Distance: 5.00
    hints:
      - "Unpack the tuples: x1, y1, z1 = point1"
      - "Use math.sqrt() for square root"
      - "Formula: sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)"
    solution: |
      import math

      point1 = (0, 0, 0)
      point2 = (3, 4, 0)

      # Calculate Euclidean distance
      x1, y1, z1 = point1
      x2, y2, z2 = point2
      distance = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

      # Print the result rounded to 2 decimal places
      print(f"Distance: {distance:.2f}")

  - title: "Named Tuple Database"
    difficulty: advanced
    description: "Create a Product named tuple and implement functions to filter products by price range and find the most expensive product."
    starter_code: |
      from collections import namedtuple

      Product = namedtuple('Product', ['id', 'name', 'price', 'category'])

      products = [
          Product(1, "Laptop", 1200, "Electronics"),
          Product(2, "Mouse", 25, "Electronics"),
          Product(3, "Desk", 300, "Furniture"),
          Product(4, "Chair", 150, "Furniture"),
          Product(5, "Monitor", 400, "Electronics")
      ]

      def filter_by_price(products, min_price, max_price):
          # Return list of products within price range
          pass

      def most_expensive(products):
          # Return the most expensive product
          pass

      # Test the functions
      affordable = filter_by_price(products, 0, 300)
      print(f"Affordable products: {len(affordable)}")
      for p in affordable:
          print(f"  {p.name}: ${p.price}")

      expensive = most_expensive(products)
      print(f"Most expensive: {expensive.name} (${expensive.price})")

    expected_output: |
      Affordable products: 3
        Mouse: $25
        Desk: $300
        Chair: $150
      Most expensive: Laptop ($1200)
    hints:
      - "Use list comprehension with filtering condition"
      - "For most expensive, use max() with key parameter"
      - "Access named tuple fields using dot notation"
    solution: |
      from collections import namedtuple

      Product = namedtuple('Product', ['id', 'name', 'price', 'category'])

      products = [
          Product(1, "Laptop", 1200, "Electronics"),
          Product(2, "Mouse", 25, "Electronics"),
          Product(3, "Desk", 300, "Furniture"),
          Product(4, "Chair", 150, "Furniture"),
          Product(5, "Monitor", 400, "Electronics")
      ]

      def filter_by_price(products, min_price, max_price):
          # Return list of products within price range
          return [p for p in products if min_price <= p.price <= max_price]

      def most_expensive(products):
          # Return the most expensive product
          return max(products, key=lambda p: p.price)

      # Test the functions
      affordable = filter_by_price(products, 0, 300)
      print(f"Affordable products: {len(affordable)}")
      for p in affordable:
          print(f"  {p.name}: ${p.price}")

      expensive = most_expensive(products)
      print(f"Most expensive: {expensive.name} (${expensive.price})")

  - title: "Time Series Data Processor"
    difficulty: advanced
    description: "Process time series data stored as tuples (timestamp, value) to find the maximum value, minimum value, and calculate the moving average of the last 3 readings."
    starter_code: |
      readings = [
          (1, 20.5),
          (2, 21.0),
          (3, 19.8),
          (4, 22.3),
          (5, 23.1),
          (6, 22.8),
          (7, 24.0)
      ]

      def analyze_readings(data):
          # Extract all values
          # Find max and min
          # Calculate moving average of last 3 values
          # Return tuple of (max_val, min_val, moving_avg)
          pass

      max_val, min_val, moving_avg = analyze_readings(readings)
      print(f"Max: {max_val}")
      print(f"Min: {min_val}")
      print(f"Moving Avg (last 3): {moving_avg:.2f}")

    expected_output: |
      Max: 24.0
      Min: 19.8
      Moving Avg (last 3): 23.27
    hints:
      - "Unpack tuples to extract values: [value for timestamp, value in data]"
      - "Use max() and min() on the values list"
      - "For moving average, slice the last 3 values and calculate their mean"
    solution: |
      readings = [
          (1, 20.5),
          (2, 21.0),
          (3, 19.8),
          (4, 22.3),
          (5, 23.1),
          (6, 22.8),
          (7, 24.0)
      ]

      def analyze_readings(data):
          # Extract all values
          values = [value for timestamp, value in data]

          # Find max and min
          max_val = max(values)
          min_val = min(values)

          # Calculate moving average of last 3 values
          last_three = values[-3:]
          moving_avg = sum(last_three) / len(last_three)

          # Return tuple of (max_val, min_val, moving_avg)
          return max_val, min_val, moving_avg

      max_val, min_val, moving_avg = analyze_readings(readings)
      print(f"Max: {max_val}")
      print(f"Min: {min_val}")
      print(f"Moving Avg (last 3): {moving_avg:.2f}")
```
<!-- EXERCISE_END -->
