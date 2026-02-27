# Nested Data Structures in Python

Nested data structures are collections that contain other collections as elements. They are fundamental for representing complex real-world data like JSON APIs, database records, configuration files, and hierarchical information.

## Nested Lists (2D Arrays)

Lists containing other lists create matrix-like structures:

```python
# 2D grid / matrix
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Accessing elements: matrix[row][col]
print(matrix[0][0])  # 1 (top-left)
print(matrix[1][2])  # 6 (row 1, col 2)
print(matrix[2][1])  # 8 (row 2, col 1)

# Iterating through a 2D list
for row in matrix:
    for val in row:
        print(val, end=" ")
    print()

# Modifying nested elements
matrix[1][1] = 99
print(matrix[1])  # [4, 99, 6]

# Creating a matrix dynamically
rows, cols = 3, 4
grid = [[0 for _ in range(cols)] for _ in range(rows)]
```

## Nested Dictionaries

Dictionaries within dictionaries model hierarchical data:

```python
# Student records
students = {
    "alice": {
        "name": "Alice Johnson",
        "age": 22,
        "grades": {"math": 95, "science": 88, "english": 92}
    },
    "bob": {
        "name": "Bob Smith",
        "age": 21,
        "grades": {"math": 78, "science": 85, "english": 90}
    }
}

# Accessing nested values
print(students["alice"]["name"])              # Alice Johnson
print(students["alice"]["grades"]["math"])    # 95

# Safe access with .get()
print(students.get("charlie", {}).get("name", "Not found"))  # Not found

# Modifying nested values
students["alice"]["grades"]["math"] = 97

# Iterating nested dicts
for student_id, info in students.items():
    avg = sum(info["grades"].values()) / len(info["grades"])
    print(f"{info['name']}: Average = {avg:.1f}")
```

## Lists of Dictionaries

The most common pattern for representing collections of records:

```python
# Employee records (like JSON API responses)
employees = [
    {"name": "Alice", "dept": "Engineering", "salary": 95000},
    {"name": "Bob", "dept": "Marketing", "salary": 72000},
    {"name": "Charlie", "dept": "Engineering", "salary": 88000},
    {"name": "Diana", "dept": "Marketing", "salary": 78000}
]

# Filter by department
engineers = [e for e in employees if e["dept"] == "Engineering"]
print(f"Engineers: {len(engineers)}")

# Sort by salary
by_salary = sorted(employees, key=lambda e: e["salary"], reverse=True)
for e in by_salary:
    print(f"  {e['name']}: ${e['salary']:,}")

# Group by department
from collections import defaultdict
by_dept = defaultdict(list)
for e in employees:
    by_dept[e["dept"]].append(e["name"])
print(dict(by_dept))
```

## Dictionaries with List Values

Useful for one-to-many relationships:

```python
# Course enrollments
courses = {
    "Python 101": ["Alice", "Bob", "Charlie"],
    "Data Science": ["Alice", "Diana"],
    "Web Dev": ["Bob", "Charlie", "Diana"]
}

# Find which courses a student is enrolled in
student = "Alice"
enrolled = [course for course, students in courses.items() if student in students]
print(f"{student} is enrolled in: {enrolled}")

# Count enrollments per course
for course, students in courses.items():
    print(f"{course}: {len(students)} students")

# Add a student to a course
courses.setdefault("Machine Learning", []).append("Alice")
```

## Deep Copy vs Shallow Copy

Understanding copy behavior is critical with nested structures:

```python
import copy

original = {"data": [1, 2, 3], "info": {"key": "value"}}

# Shallow copy - nested objects are shared
shallow = original.copy()
shallow["data"].append(4)
print(original["data"])  # [1, 2, 3, 4] - MODIFIED!

# Deep copy - completely independent
original2 = {"data": [1, 2, 3], "info": {"key": "value"}}
deep = copy.deepcopy(original2)
deep["data"].append(4)
print(original2["data"])  # [1, 2, 3] - unchanged
```

## Real-World Example: JSON-like Data Processing

```python
# API response structure
api_response = {
    "status": "success",
    "results": [
        {
            "id": 1,
            "title": "Python Basics",
            "tags": ["python", "beginner"],
            "author": {"name": "Alice", "email": "alice@example.com"}
        },
        {
            "id": 2,
            "title": "Advanced Python",
            "tags": ["python", "advanced"],
            "author": {"name": "Bob", "email": "bob@example.com"}
        }
    ],
    "total": 2
}

# Extract all titles
titles = [r["title"] for r in api_response["results"]]
print(titles)  # ['Python Basics', 'Advanced Python']

# Find articles by tag
tag = "advanced"
matching = [r["title"] for r in api_response["results"] if tag in r["tags"]]
print(f"Articles tagged '{tag}': {matching}")

# Build an index by author
by_author = {}
for result in api_response["results"]:
    author = result["author"]["name"]
    by_author.setdefault(author, []).append(result["title"])
print(by_author)
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Access Nested Dictionary"
    difficulty: basic
    description: "Given the nested dictionary, print Alice's math grade."
    starter_code: |
      students = {
          "alice": {"grades": {"math": 95, "science": 88}},
          "bob": {"grades": {"math": 78, "science": 85}}
      }
      # Print Alice's math grade

    expected_output: "95"
    hints:
      - "Chain the keys: dict[key1][key2][key3]"
      - "Access alice, then grades, then math"
    solution: |
      students = {
          "alice": {"grades": {"math": 95, "science": 88}},
          "bob": {"grades": {"math": 78, "science": 85}}
      }
      print(students["alice"]["grades"]["math"])

  - title: "Matrix Diagonal"
    difficulty: basic
    description: "Extract and print the diagonal elements [1, 5, 9] from the 3x3 matrix as a list."
    starter_code: |
      matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
      # Get diagonal elements

    expected_output: "[1, 5, 9]"
    hints:
      - "Diagonal elements have the same row and column index"
      - "matrix[0][0], matrix[1][1], matrix[2][2]"
    solution: |
      matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
      diagonal = [matrix[i][i] for i in range(len(matrix))]
      print(diagonal)

  - title: "Filter Records"
    difficulty: intermediate
    description: "From the list of employees, print the names of those with salary above 80000, one per line."
    starter_code: |
      employees = [
          {"name": "Alice", "salary": 95000},
          {"name": "Bob", "salary": 72000},
          {"name": "Charlie", "salary": 88000}
      ]
      # Print names with salary > 80000

    expected_output: |
      Alice
      Charlie
    hints:
      - "Loop through the list and check each dict's salary"
      - "Use an if condition inside the loop"
    solution: |
      employees = [
          {"name": "Alice", "salary": 95000},
          {"name": "Bob", "salary": 72000},
          {"name": "Charlie", "salary": 88000}
      ]
      for e in employees:
          if e["salary"] > 80000:
              print(e["name"])

  - title: "Group by Key"
    difficulty: intermediate
    description: "Group the people by their city and print the resulting dictionary."
    starter_code: |
      people = [
          {"name": "Alice", "city": "NYC"},
          {"name": "Bob", "city": "LA"},
          {"name": "Charlie", "city": "NYC"},
          {"name": "Diana", "city": "LA"}
      ]
      # Group names by city

    expected_output: "{'NYC': ['Alice', 'Charlie'], 'LA': ['Bob', 'Diana']}"
    hints:
      - "Create an empty dictionary for groups"
      - "Use setdefault() or check if key exists before appending"
    solution: |
      people = [
          {"name": "Alice", "city": "NYC"},
          {"name": "Bob", "city": "LA"},
          {"name": "Charlie", "city": "NYC"},
          {"name": "Diana", "city": "LA"}
      ]
      groups = {}
      for p in people:
          groups.setdefault(p["city"], []).append(p["name"])
      print(groups)

  - title: "Flatten Nested Dict"
    difficulty: advanced
    description: "Calculate and print the average grade across ALL students and ALL subjects."
    starter_code: |
      students = {
          "alice": {"math": 90, "science": 80},
          "bob": {"math": 70, "science": 90}
      }
      # Calculate overall average grade

    expected_output: "82.5"
    hints:
      - "Collect all grades into a single list"
      - "Use nested loops over dict values"
    solution: |
      students = {
          "alice": {"math": 90, "science": 80},
          "bob": {"math": 70, "science": 90}
      }
      all_grades = []
      for grades in students.values():
          for grade in grades.values():
              all_grades.append(grade)
      print(sum(all_grades) / len(all_grades))

  - title: "Inventory Report"
    difficulty: advanced
    description: "Calculate the total inventory value (price * stock) for each category and print the result as a dictionary."
    starter_code: |
      inventory = {
          "electronics": [
              {"name": "Phone", "price": 500, "stock": 10},
              {"name": "Laptop", "price": 1000, "stock": 5}
          ],
          "books": [
              {"name": "Python 101", "price": 30, "stock": 50},
              {"name": "Data Science", "price": 45, "stock": 30}
          ]
      }
      # Calculate total value per category

    expected_output: "{'electronics': 10000, 'books': 2850}"
    hints:
      - "Loop through each category and its items"
      - "Multiply price by stock for each item and sum them"
    solution: |
      inventory = {
          "electronics": [
              {"name": "Phone", "price": 500, "stock": 10},
              {"name": "Laptop", "price": 1000, "stock": 5}
          ],
          "books": [
              {"name": "Python 101", "price": 30, "stock": 50},
              {"name": "Data Science", "price": 45, "stock": 30}
          ]
      }
      totals = {}
      for category, items in inventory.items():
          totals[category] = sum(item["price"] * item["stock"] for item in items)
      print(totals)
```
<!-- EXERCISE_END -->
