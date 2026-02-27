# Lists in Python

Lists are ordered, mutable collections that can hold items of different types. They are one of the most versatile data structures in Python.

## Creating Lists

```python
# Empty list
empty = []
empty = list()

# List with items
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# List from range
nums = list(range(1, 6))  # [1, 2, 3, 4, 5]

# List from string
chars = list("hello")  # ['h', 'e', 'l', 'l', 'o']
```

## Accessing Elements

```python
fruits = ["apple", "banana", "cherry", "date"]

# Positive indexing (from start)
print(fruits[0])   # apple (first)
print(fruits[1])   # banana (second)

# Negative indexing (from end)
print(fruits[-1])  # date (last)
print(fruits[-2])  # cherry (second to last)
```

## List Slicing

Extract portions of a list:

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(numbers[2:5])    # [2, 3, 4] (index 2 to 4)
print(numbers[:4])     # [0, 1, 2, 3] (start to index 3)
print(numbers[6:])     # [6, 7, 8, 9] (index 6 to end)
print(numbers[::2])    # [0, 2, 4, 6, 8] (every 2nd element)
print(numbers[::-1])   # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] (reversed)
```

## List Methods

### Adding Elements
```python
fruits = ["apple", "banana"]

fruits.append("cherry")      # Add to end: ["apple", "banana", "cherry"]
fruits.insert(1, "orange")   # Insert at index: ["apple", "orange", "banana", "cherry"]
fruits.extend(["grape", "kiwi"])  # Add multiple: [..., "grape", "kiwi"]
```

### Removing Elements
```python
fruits = ["apple", "banana", "cherry", "banana"]

fruits.remove("banana")  # Remove first occurrence
popped = fruits.pop()    # Remove and return last item
popped = fruits.pop(0)   # Remove and return item at index
fruits.clear()           # Remove all items
```

### Other Methods
```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

numbers.sort()           # Sort in place: [1, 1, 2, 3, 4, 5, 6, 9]
numbers.reverse()        # Reverse in place
count = numbers.count(1) # Count occurrences: 2
index = numbers.index(4) # Find index of value
length = len(numbers)    # Get length: 8
```

## List Comprehension

Concise way to create lists:

```python
# Basic comprehension
squares = [x**2 for x in range(1, 6)]  # [1, 4, 9, 16, 25]

# With condition
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# With transformation
upper = [s.upper() for s in ["a", "b", "c"]]  # ["A", "B", "C"]
```

## Copying Lists

```python
original = [1, 2, 3]

# Shallow copy methods
copy1 = original.copy()
copy2 = list(original)
copy3 = original[:]

# Note: assignment creates a reference, not a copy!
reference = original  # Both point to same list
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Create and Access"
    difficulty: basic
    description: "Create a list `numbers = [10, 20, 30, 40, 50]`. Print the first element, last element, and middle element."
    starter_code: |
      # Create list and print elements

    expected_output: |
      10
      50
      30
    hints:
      - "First element: list[0]"
      - "Last element: list[-1]"
      - "Middle element: list[2] (index 2 for 5 elements)"
    solution: |
      numbers = [10, 20, 30, 40, 50]
      print(numbers[0])
      print(numbers[-1])
      print(numbers[2])

  - title: "List Modification"
    difficulty: basic
    description: "Start with `fruits = ['apple', 'banana']`. Add 'cherry' to the end, then insert 'orange' at the beginning. Print the final list."
    starter_code: |
      fruits = ['apple', 'banana']
      # Add cherry and insert orange

    expected_output: "['orange', 'apple', 'banana', 'cherry']"
    hints:
      - "Use append() to add to end"
      - "Use insert(0, item) to add at beginning"
    solution: |
      fruits = ['apple', 'banana']
      fruits.append('cherry')
      fruits.insert(0, 'orange')
      print(fruits)

  - title: "List Slicing"
    difficulty: intermediate
    description: "Given `numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`, print: first 5 elements, last 3 elements, and every other element."
    starter_code: |
      numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      # Use slicing

    expected_output: |
      [1, 2, 3, 4, 5]
      [8, 9, 10]
      [1, 3, 5, 7, 9]
    hints:
      - "First 5: numbers[:5]"
      - "Last 3: numbers[-3:]"
      - "Every other: numbers[::2]"
    solution: |
      numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      print(numbers[:5])
      print(numbers[-3:])
      print(numbers[::2])

  - title: "Find and Remove"
    difficulty: intermediate
    description: "Given `items = ['a', 'b', 'c', 'b', 'd']`, remove all occurrences of 'b' and print the result."
    starter_code: |
      items = ['a', 'b', 'c', 'b', 'd']
      # Remove all 'b' values

    expected_output: "['a', 'c', 'd']"
    hints:
      - "Use a while loop with 'in' check"
      - "Or use list comprehension to filter"
    solution: |
      items = ['a', 'b', 'c', 'b', 'd']
      items = [x for x in items if x != 'b']
      print(items)

  - title: "List Comprehension - Squares"
    difficulty: advanced
    description: "Use list comprehension to create a list of squares of numbers 1-10. Print the result."
    starter_code: |
      # Create squares using list comprehension

    expected_output: "[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]"
    hints:
      - "Syntax: [expression for item in range]"
      - "Square: x**2 or x*x"
    solution: |
      squares = [x**2 for x in range(1, 11)]
      print(squares)

  - title: "Filter and Transform"
    difficulty: advanced
    description: "Given `numbers = [-5, -2, 0, 3, 7, -1, 4]`, create a new list containing only positive numbers, doubled. Print the result."
    starter_code: |
      numbers = [-5, -2, 0, 3, 7, -1, 4]
      # Filter positive and double them

    expected_output: "[6, 14, 8]"
    hints:
      - "Combine condition and transformation in comprehension"
      - "Syntax: [expr for x in list if condition]"
    solution: |
      numbers = [-5, -2, 0, 3, 7, -1, 4]
      result = [x * 2 for x in numbers if x > 0]
      print(result)
```
<!-- EXERCISE_END -->
