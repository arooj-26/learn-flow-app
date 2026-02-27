# Dictionaries

Dictionaries are Python's implementation of hash tables, providing fast key-value storage and retrieval. They're one of the most versatile and frequently used data structures in Python, perfect for representing structured data, configurations, caches, and mappings. Understanding dictionaries is essential for efficient Python programming and data manipulation.

## Creating and Accessing Dictionaries

Dictionaries store data as key-value pairs enclosed in curly braces `{}`. Keys must be immutable (strings, numbers, tuples), while values can be any Python object.

```python
# Creating dictionaries
student = {
    "name": "Alice",
    "age": 20,
    "major": "Computer Science",
    "gpa": 3.8
}

# Alternative creation methods
empty_dict = {}
also_empty = dict()
from_pairs = dict([("a", 1), ("b", 2), ("c", 3)])

# Using dict comprehension
squares = {x: x**2 for x in range(1, 6)}
print(f"Squares: {squares}")  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Accessing values
print(f"Student name: {student['name']}")
print(f"Student GPA: {student['gpa']}")

# Safe access with get() - returns None if key doesn't exist
email = student.get("email")
print(f"Email: {email}")  # None

# get() with default value
email = student.get("email", "not provided")
print(f"Email: {email}")  # not provided

# Checking if key exists
if "major" in student:
    print(f"Major: {student['major']}")

# KeyError when accessing non-existent key
try:
    phone = student["phone"]
except KeyError:
    print("Phone number not found")
```

## Modifying Dictionaries

Dictionaries are mutable, allowing you to add, update, and remove key-value pairs after creation.

```python
# Starting with a product inventory
inventory = {
    "apple": 50,
    "banana": 30,
    "orange": 40
}

# Adding new items
inventory["grape"] = 25
inventory["mango"] = 15

# Updating existing items
inventory["apple"] = 45  # Sold 5 apples
inventory["banana"] += 20  # Received 20 more bananas

print(f"Updated inventory: {inventory}")

# Using update() to merge dictionaries
new_items = {"watermelon": 10, "pineapple": 8}
inventory.update(new_items)

# Update can also take keyword arguments
inventory.update(apple=40, orange=35)

print(f"After update: {inventory}")

# Removing items
del inventory["mango"]  # Remove specific key

# pop() removes and returns the value
grape_count = inventory.pop("grape")
print(f"Removed {grape_count} grapes")

# pop() with default (doesn't raise error if key missing)
kiwi_count = inventory.pop("kiwi", 0)
print(f"Kiwi count: {kiwi_count}")

# popitem() removes and returns last inserted key-value pair (Python 3.7+)
last_item = inventory.popitem()
print(f"Last item removed: {last_item}")

# clear() removes all items
test_dict = {"a": 1, "b": 2}
test_dict.clear()
print(f"Cleared dict: {test_dict}")  # {}
```

## Iterating Through Dictionaries

Python provides multiple ways to iterate through dictionary keys, values, or key-value pairs.

```python
# Sample data: Student grades
grades = {
    "Alice": 92,
    "Bob": 85,
    "Charlie": 88,
    "Diana": 95,
    "Eve": 90
}

# Iterate over keys (default)
print("Students:")
for student in grades:
    print(f"  {student}")

# Explicit keys() method
for student in grades.keys():
    print(f"  {student}")

# Iterate over values
print("\nGrades:")
for grade in grades.values():
    print(f"  {grade}")

# Iterate over key-value pairs
print("\nStudent grades:")
for student, grade in grades.items():
    print(f"  {student}: {grade}")

# Calculate statistics while iterating
total = 0
highest_grade = 0
top_student = ""

for student, grade in grades.items():
    total += grade
    if grade > highest_grade:
        highest_grade = grade
        top_student = student

average = total / len(grades)
print(f"\nClass average: {average:.2f}")
print(f"Top student: {top_student} ({highest_grade})")

# Dictionary comprehension with filtering
high_performers = {name: grade for name, grade in grades.items() if grade >= 90}
print(f"\nHigh performers (90+): {high_performers}")

# Sorting dictionaries
sorted_by_grade = dict(sorted(grades.items(), key=lambda x: x[1], reverse=True))
print(f"\nSorted by grade: {sorted_by_grade}")
```

## Nested Dictionaries and Complex Structures

Dictionaries can contain other dictionaries, lists, or any Python objects, enabling complex data structures.

```python
# Company employee database
company = {
    "employees": {
        "E001": {
            "name": "Alice Johnson",
            "position": "Senior Developer",
            "department": "Engineering",
            "salary": 95000,
            "skills": ["Python", "JavaScript", "Docker"]
        },
        "E002": {
            "name": "Bob Smith",
            "position": "Designer",
            "department": "Design",
            "salary": 80000,
            "skills": ["Figma", "Photoshop", "CSS"]
        },
        "E003": {
            "name": "Charlie Brown",
            "position": "Product Manager",
            "department": "Product",
            "salary": 100000,
            "skills": ["Agile", "JIRA", "Roadmapping"]
        }
    },
    "departments": {
        "Engineering": {"budget": 500000, "headcount": 15},
        "Design": {"budget": 200000, "headcount": 5},
        "Product": {"budget": 300000, "headcount": 8}
    }
}

# Accessing nested data
alice = company["employees"]["E001"]
print(f"Employee: {alice['name']}")
print(f"Position: {alice['position']}")
print(f"Skills: {', '.join(alice['skills'])}")

# Iterating through nested structure
print("\nAll employees:")
for emp_id, emp_data in company["employees"].items():
    print(f"{emp_id}: {emp_data['name']} - {emp_data['position']}")

# Finding employees by department
def get_employees_by_department(company, dept_name):
    return {
        emp_id: emp_data
        for emp_id, emp_data in company["employees"].items()
        if emp_data["department"] == dept_name
    }

engineers = get_employees_by_department(company, "Engineering")
print(f"\nEngineering team: {list(engineers.keys())}")

# Calculate total salary by department
dept_salaries = {}
for emp_data in company["employees"].values():
    dept = emp_data["department"]
    salary = emp_data["salary"]
    dept_salaries[dept] = dept_salaries.get(dept, 0) + salary

print("\nSalary by department:")
for dept, total in dept_salaries.items():
    print(f"  {dept}: ${total:,}")

# Safe nested access with get()
marketing_budget = company.get("departments", {}).get("Marketing", {}).get("budget", 0)
print(f"\nMarketing budget: ${marketing_budget}")  # 0 (doesn't exist)
```

Dictionary operations comparison:

| Operation | Time Complexity | Description |
|-----------|----------------|-------------|
| `dict[key]` | O(1) | Direct access |
| `key in dict` | O(1) | Membership test |
| `dict.get(key)` | O(1) | Safe access |
| `dict.items()` | O(n) | Get all pairs |
| `dict.update()` | O(n) | Merge dictionaries |
| `del dict[key]` | O(1) | Remove item |

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Student Grade Book"
    difficulty: basic
    description: "Create a grade book dictionary and calculate the average grade for all students."
    starter_code: |
      grades = {
          "Alice": 92,
          "Bob": 85,
          "Charlie": 88,
          "Diana": 95
      }

      # Calculate and print the average grade

    expected_output: |
      Average grade: 90.0
    hints:
      - "Use values() to get all grades"
      - "Calculate sum of values divided by number of students"
      - "Use len() to count students"
    solution: |
      grades = {
          "Alice": 92,
          "Bob": 85,
          "Charlie": 88,
          "Diana": 95
      }

      # Calculate and print the average grade
      average = sum(grades.values()) / len(grades)
      print(f"Average grade: {average}")

  - title: "Inventory Update"
    difficulty: basic
    description: "Update inventory quantities after sales and restocking, then display the final inventory."
    starter_code: |
      inventory = {"apple": 50, "banana": 30, "orange": 40}

      # Sell 10 apples
      # Restock 25 bananas
      # Add new item: grape with 20 units
      # Print final inventory

    expected_output: |
      {'apple': 40, 'banana': 55, 'orange': 40, 'grape': 20}
    hints:
      - "Use subtraction to decrease inventory"
      - "Use addition to increase inventory"
      - "Assign new key-value pair to add item"
    solution: |
      inventory = {"apple": 50, "banana": 30, "orange": 40}

      # Sell 10 apples
      inventory["apple"] -= 10

      # Restock 25 bananas
      inventory["banana"] += 25

      # Add new item: grape with 20 units
      inventory["grape"] = 20

      # Print final inventory
      print(inventory)

  - title: "Word Frequency Counter"
    difficulty: intermediate
    description: "Count the frequency of each word in a sentence and display words that appear more than once."
    starter_code: |
      sentence = "the quick brown fox jumps over the lazy dog the fox"

      # Count word frequencies
      # Display words that appear more than once
      # Format: "word: count"

    expected_output: |
      the: 3
      fox: 2
    hints:
      - "Split the sentence into words using split()"
      - "Use a dictionary to count occurrences"
      - "Use get() with default value 0 for counting"
      - "Filter words with count > 1"
    solution: |
      sentence = "the quick brown fox jumps over the lazy dog the fox"

      # Count word frequencies
      words = sentence.split()
      freq = {}
      for word in words:
          freq[word] = freq.get(word, 0) + 1

      # Display words that appear more than once
      for word, count in freq.items():
          if count > 1:
              print(f"{word}: {count}")

  - title: "Contact Merger"
    difficulty: intermediate
    description: "Merge two contact dictionaries. If a contact exists in both, keep the one from the second dictionary."
    starter_code: |
      contacts1 = {
          "Alice": "alice@email.com",
          "Bob": "bob@email.com",
          "Charlie": "charlie@email.com"
      }

      contacts2 = {
          "Bob": "bob.smith@email.com",
          "Diana": "diana@email.com"
      }

      # Merge contacts2 into contacts1
      # Print the merged result

    expected_output: |
      {'Alice': 'alice@email.com', 'Bob': 'bob.smith@email.com', 'Charlie': 'charlie@email.com', 'Diana': 'diana@email.com'}
    hints:
      - "Use the update() method to merge dictionaries"
      - "The second dictionary's values will overwrite the first"
    solution: |
      contacts1 = {
          "Alice": "alice@email.com",
          "Bob": "bob@email.com",
          "Charlie": "charlie@email.com"
      }

      contacts2 = {
          "Bob": "bob.smith@email.com",
          "Diana": "diana@email.com"
      }

      # Merge contacts2 into contacts1
      contacts1.update(contacts2)

      # Print the merged result
      print(contacts1)

  - title: "Shopping Cart Total Calculator"
    difficulty: advanced
    description: "Given a cart dictionary with product quantities and a price dictionary, calculate the total cost."
    starter_code: |
      cart = {
          "apple": 5,
          "banana": 3,
          "orange": 2,
          "grape": 1
      }

      prices = {
          "apple": 0.5,
          "banana": 0.3,
          "orange": 0.6,
          "grape": 2.0,
          "mango": 1.5
      }

      # Calculate total cost
      # Format: "Item: quantity x $price = $subtotal" for each item
      # Then print "Total: $amount"

    expected_output: |
      apple: 5 x $0.5 = $2.5
      banana: 3 x $0.3 = $0.9
      orange: 2 x $0.6 = $1.2
      grape: 1 x $2.0 = $2.0
      Total: $6.6
    hints:
      - "Iterate through cart items"
      - "Look up price for each item"
      - "Calculate subtotal as quantity * price"
      - "Sum all subtotals for the total"
    solution: |
      cart = {
          "apple": 5,
          "banana": 3,
          "orange": 2,
          "grape": 1
      }

      prices = {
          "apple": 0.5,
          "banana": 0.3,
          "orange": 0.6,
          "grape": 2.0,
          "mango": 1.5
      }

      # Calculate total cost
      total = 0
      for item, quantity in cart.items():
          price = prices[item]
          subtotal = quantity * price
          print(f"{item}: {quantity} x ${price} = ${subtotal}")
          total += subtotal

      print(f"Total: ${total}")

  - title: "Nested Student Database Query"
    difficulty: advanced
    description: "Query a nested student database to find all students with GPA above 3.5 and display their information."
    starter_code: |
      students = {
          "S001": {"name": "Alice", "gpa": 3.8, "major": "CS"},
          "S002": {"name": "Bob", "gpa": 3.2, "major": "Math"},
          "S003": {"name": "Charlie", "gpa": 3.9, "major": "CS"},
          "S004": {"name": "Diana", "gpa": 3.6, "major": "Physics"}
      }

      # Find and display students with GPA > 3.5
      # Format: "ID: Name (Major) - GPA"
      # Then print count of high performers

    expected_output: |
      High Performers:
      S001: Alice (CS) - 3.8
      S003: Charlie (CS) - 3.9
      S004: Diana (Physics) - 3.6
      Total: 3 students
    hints:
      - "Iterate through students.items()"
      - "Check if gpa > 3.5"
      - "Keep count of matching students"
      - "Access nested values using student_data['gpa']"
    solution: |
      students = {
          "S001": {"name": "Alice", "gpa": 3.8, "major": "CS"},
          "S002": {"name": "Bob", "gpa": 3.2, "major": "Math"},
          "S003": {"name": "Charlie", "gpa": 3.9, "major": "CS"},
          "S004": {"name": "Diana", "gpa": 3.6, "major": "Physics"}
      }

      # Find and display students with GPA > 3.5
      print("High Performers:")
      count = 0
      for student_id, student_data in students.items():
          if student_data["gpa"] > 3.5:
              print(f"{student_id}: {student_data['name']} ({student_data['major']}) - {student_data['gpa']}")
              count += 1

      print(f"Total: {count} students")
```
<!-- EXERCISE_END -->
