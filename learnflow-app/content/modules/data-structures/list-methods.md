# List Methods

Python lists come with a rich set of built-in methods that allow you to manipulate, search, sort, and transform list data efficiently. Understanding these methods is crucial for writing clean, efficient Python code. This guide explores essential list methods with practical examples and best practices for real-world applications.

## Modifying Lists: Adding and Removing Elements

Lists are mutable, meaning you can change their contents after creation. Python provides several methods to add or remove elements dynamically.

The `append()` method adds a single element to the end of the list, while `extend()` adds multiple elements from an iterable. The `insert()` method allows you to add an element at a specific position.

```python
# Building a task list dynamically
tasks = ["Write report"]
tasks.append("Review code")
tasks.extend(["Send emails", "Update documentation"])
tasks.insert(0, "Morning standup")

print(tasks)
# Output: ['Morning standup', 'Write report', 'Review code', 'Send emails', 'Update documentation']

# Working with numerical data
scores = [85, 92]
scores.append(78)
scores.extend([95, 88, 91])
print(f"All scores: {scores}")
print(f"Average: {sum(scores) / len(scores):.2f}")
```

For removing elements, you have `remove()` (removes first occurrence by value), `pop()` (removes by index and returns the element), and `clear()` (removes all elements).

```python
# Managing a shopping cart
cart = ["apple", "banana", "orange", "banana", "grape"]

# Remove first banana
cart.remove("banana")
print(f"After removing banana: {cart}")

# Remove last item and show what was removed
removed_item = cart.pop()
print(f"Removed: {removed_item}, Cart: {cart}")

# Remove item at index 1
cart.pop(1)
print(f"After removing index 1: {cart}")
```

## Sorting and Reversing Lists

Sorting is a common operation in data processing. Python offers both in-place sorting with `sort()` and non-destructive sorting with the `sorted()` built-in function.

```python
# Sorting student grades
students = [
    ("Alice", 92),
    ("Bob", 85),
    ("Charlie", 95),
    ("Diana", 88)
]

# Sort by grade (second element in tuple)
students.sort(key=lambda x: x[1], reverse=True)
print("Students by grade (highest first):")
for name, grade in students:
    print(f"  {name}: {grade}")

# Sorting strings (case-insensitive)
words = ["Python", "java", "C++", "ruby", "JavaScript"]
words.sort(key=str.lower)
print(f"Sorted words: {words}")

# Reverse a list in-place
numbers = [1, 2, 3, 4, 5]
numbers.reverse()
print(f"Reversed: {numbers}")
```

The `sort()` method has powerful options:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `key` | Function to extract comparison key | `key=len` sorts by length |
| `reverse` | Sort in descending order | `reverse=True` |

## Searching and Counting

Finding elements and counting occurrences are fundamental operations when working with lists.

The `index()` method finds the position of an element, while `count()` tells you how many times an element appears.

```python
# Analyzing survey responses
responses = ["yes", "no", "yes", "yes", "maybe", "no", "yes", "maybe"]

# Count occurrences
yes_count = responses.count("yes")
no_count = responses.count("no")
maybe_count = responses.count("maybe")

print(f"Survey Results:")
print(f"  Yes: {yes_count} ({yes_count/len(responses)*100:.1f}%)")
print(f"  No: {no_count} ({no_count/len(responses)*100:.1f}%)")
print(f"  Maybe: {maybe_count} ({maybe_count/len(responses)*100:.1f}%)")

# Finding positions
data = [10, 20, 30, 40, 30, 50]
first_30 = data.index(30)
print(f"First occurrence of 30 at index: {first_30}")

# Safe searching with error handling
try:
    position = data.index(100)
except ValueError:
    print("Value 100 not found in list")

# Find all occurrences
all_30_positions = [i for i, x in enumerate(data) if x == 30]
print(f"All positions of 30: {all_30_positions}")
```

## Copying and Combining Lists

Understanding how to properly copy lists is crucial to avoid unexpected behavior due to references.

```python
# Shallow copy vs deep copy
original = [1, 2, [3, 4]]

# Reference (not a copy!)
ref = original
ref[0] = 999
print(f"Original modified: {original}")  # [999, 2, [3, 4]]

# Shallow copy using copy()
original = [1, 2, [3, 4]]
shallow = original.copy()
shallow[0] = 100
shallow[2][0] = 300
print(f"Original: {original}")  # [1, 2, [300, 4]] - nested list affected!
print(f"Shallow: {shallow}")    # [100, 2, [300, 4]]

# Deep copy for nested structures
import copy
original = [1, 2, [3, 4]]
deep = copy.deepcopy(original)
deep[2][0] = 999
print(f"Original: {original}")  # [1, 2, [3, 4]] - unaffected
print(f"Deep: {deep}")          # [1, 2, [999, 4]]

# Combining lists with extend vs concatenation
list1 = [1, 2, 3]
list2 = [4, 5, 6]

# Using extend (modifies in-place)
list1.extend(list2)
print(f"Extended: {list1}")

# Using + operator (creates new list)
list3 = [1, 2, 3]
list4 = list3 + [4, 5, 6]
print(f"Concatenated: {list4}")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Shopping Cart Manager"
    difficulty: basic
    description: "Create a shopping cart manager that adds items, removes items, and displays the cart contents."
    starter_code: |
      cart = []

      # Add three items to the cart
      # Remove the second item
      # Print the final cart

    expected_output: |
      ['milk', 'eggs']
    hints:
      - "Use append() to add items to the cart"
      - "Use pop(index) to remove an item at a specific position"
    solution: |
      cart = []

      # Add three items to the cart
      cart.append("milk")
      cart.append("bread")
      cart.append("eggs")

      # Remove the second item (bread at index 1)
      cart.pop(1)

      # Print the final cart
      print(cart)

  - title: "Count Vowels in Words"
    difficulty: basic
    description: "Given a list of characters, count how many times each vowel appears."
    starter_code: |
      chars = ['a', 'b', 'e', 'c', 'a', 'i', 'o', 'u', 'e', 'a']

      # Count and print occurrences of each vowel (a, e, i, o, u)

    expected_output: |
      a: 3
      e: 2
      i: 1
      o: 1
      u: 1
    hints:
      - "Use the count() method for each vowel"
      - "Loop through the vowels 'aeiou'"
    solution: |
      chars = ['a', 'b', 'e', 'c', 'a', 'i', 'o', 'u', 'e', 'a']

      # Count and print occurrences of each vowel (a, e, i, o, u)
      for vowel in 'aeiou':
          count = chars.count(vowel)
          print(f"{vowel}: {count}")

  - title: "Student Grade Sorter"
    difficulty: intermediate
    description: "Sort a list of student tuples by grade in descending order and display the top 3 students."
    starter_code: |
      students = [("Alice", 85), ("Bob", 92), ("Charlie", 78), ("Diana", 95), ("Eve", 88)]

      # Sort by grade (descending)
      # Display top 3 students

    expected_output: |
      Top 3 Students:
      1. Diana: 95
      2. Bob: 92
      3. Eve: 88
    hints:
      - "Use sort() with a key parameter to sort by the second element"
      - "Use reverse=True for descending order"
      - "Slice the list to get the top 3"
    solution: |
      students = [("Alice", 85), ("Bob", 92), ("Charlie", 78), ("Diana", 95), ("Eve", 88)]

      # Sort by grade (descending)
      students.sort(key=lambda x: x[1], reverse=True)

      # Display top 3 students
      print("Top 3 Students:")
      for i, (name, grade) in enumerate(students[:3], 1):
          print(f"{i}. {name}: {grade}")

  - title: "Remove Duplicates While Preserving Order"
    difficulty: intermediate
    description: "Remove duplicate elements from a list while maintaining the original order of first occurrences."
    starter_code: |
      numbers = [1, 3, 2, 3, 4, 1, 5, 2, 6, 4]

      # Remove duplicates while preserving order
      # Print the result

    expected_output: |
      [1, 3, 2, 4, 5, 6]
    hints:
      - "Use a seen set to track what you've encountered"
      - "Use a loop and append only unseen items"
      - "Check if an item is not in the seen set before adding"
    solution: |
      numbers = [1, 3, 2, 3, 4, 1, 5, 2, 6, 4]

      # Remove duplicates while preserving order
      seen = set()
      result = []
      for num in numbers:
          if num not in seen:
              seen.add(num)
              result.append(num)

      # Print the result
      print(result)

  - title: "Task Priority Queue"
    difficulty: advanced
    description: "Implement a priority task queue that maintains tasks sorted by priority (1=highest) and allows adding, completing, and displaying tasks."
    starter_code: |
      tasks = []

      def add_task(task_name, priority):
          # Add task as tuple (priority, task_name)
          # Keep list sorted by priority
          pass

      def complete_task():
          # Remove and return highest priority task
          pass

      # Test the functions
      add_task("Write report", 2)
      add_task("Fix critical bug", 1)
      add_task("Update docs", 3)
      add_task("Code review", 1)

      print(f"Tasks: {tasks}")
      completed = complete_task()
      print(f"Completed: {completed}")
      print(f"Remaining: {tasks}")

    expected_output: |
      Tasks: [(1, 'Fix critical bug'), (1, 'Code review'), (2, 'Write report'), (3, 'Update docs')]
      Completed: (1, 'Fix critical bug')
      Remaining: [(1, 'Code review'), (2, 'Write report'), (3, 'Update docs')]
    hints:
      - "Store tasks as tuples of (priority, task_name)"
      - "Use insert and sort or use bisect module for efficiency"
      - "Use pop(0) to get the highest priority task"
    solution: |
      tasks = []

      def add_task(task_name, priority):
          # Add task as tuple (priority, task_name)
          tasks.append((priority, task_name))
          # Keep list sorted by priority
          tasks.sort()

      def complete_task():
          # Remove and return highest priority task
          if tasks:
              return tasks.pop(0)
          return None

      # Test the functions
      add_task("Write report", 2)
      add_task("Fix critical bug", 1)
      add_task("Update docs", 3)
      add_task("Code review", 1)

      print(f"Tasks: {tasks}")
      completed = complete_task()
      print(f"Completed: {completed}")
      print(f"Remaining: {tasks}")

  - title: "List Statistics Analyzer"
    difficulty: advanced
    description: "Create a comprehensive statistics analyzer that calculates mean, median, mode, and range from a list of numbers."
    starter_code: |
      def analyze_data(numbers):
          # Calculate mean (average)
          # Calculate median (middle value)
          # Calculate mode (most frequent value)
          # Calculate range (max - min)
          # Return dictionary with all statistics
          pass

      data = [85, 90, 85, 92, 88, 85, 95, 90, 88, 92]
      stats = analyze_data(data)

      for key, value in stats.items():
          print(f"{key}: {value}")

    expected_output: |
      mean: 89.0
      median: 89.0
      mode: 85
      range: 10
    hints:
      - "For median, sort the list and find the middle element"
      - "For mode, use count() to find the most frequent element"
      - "Handle both odd and even length lists for median"
    solution: |
      def analyze_data(numbers):
          # Calculate mean (average)
          mean = sum(numbers) / len(numbers)

          # Calculate median (middle value)
          sorted_nums = sorted(numbers)
          n = len(sorted_nums)
          if n % 2 == 0:
              median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
          else:
              median = sorted_nums[n//2]

          # Calculate mode (most frequent value)
          mode = max(set(numbers), key=numbers.count)

          # Calculate range (max - min)
          range_val = max(numbers) - min(numbers)

          # Return dictionary with all statistics
          return {
              "mean": mean,
              "median": median,
              "mode": mode,
              "range": range_val
          }

      data = [85, 90, 85, 92, 88, 85, 95, 90, 88, 92]
      stats = analyze_data(data)

      for key, value in stats.items():
          print(f"{key}: {value}")
```
<!-- EXERCISE_END -->
