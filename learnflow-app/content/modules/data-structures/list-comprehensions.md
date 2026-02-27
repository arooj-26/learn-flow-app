# List Comprehensions

List comprehensions are a powerful and concise way to create lists in Python. They provide an elegant syntax for transforming, filtering, and generating sequences, often replacing multi-line loops with single, readable expressions. Mastering list comprehensions (and their relatives: set and dictionary comprehensions) is a hallmark of Pythonic programming and can significantly improve code clarity and performance.

## Basic List Comprehension Syntax

The basic syntax is `[expression for item in iterable]`, which creates a new list by applying an expression to each item.

```python
# Traditional loop approach
squares_loop = []
for x in range(1, 6):
    squares_loop.append(x ** 2)
print(f"Squares (loop): {squares_loop}")

# List comprehension approach
squares_comp = [x ** 2 for x in range(1, 6)]
print(f"Squares (comprehension): {squares_comp}")

# String transformations
names = ["alice", "bob", "charlie"]
capitalized = [name.capitalize() for name in names]
print(f"Capitalized: {capitalized}")

# More complex expressions
prices = [10.99, 25.50, 8.75, 15.00]
prices_with_tax = [price * 1.08 for price in prices]
formatted_prices = [f"${price:.2f}" for price in prices_with_tax]
print(f"Prices with tax: {formatted_prices}")

# Working with strings
sentence = "Hello World From Python"
words = sentence.split()
word_lengths = [len(word) for word in words]
print(f"Word lengths: {word_lengths}")

# Extracting attributes
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

products = [
    Product("Laptop", 999),
    Product("Mouse", 25),
    Product("Keyboard", 75)
]

# Extract just the names
product_names = [p.name for p in products]
print(f"Product names: {product_names}")

# Extract and transform prices
discounted = [p.price * 0.9 for p in products]
print(f"Discounted prices: {discounted}")
```

## List Comprehensions with Conditions

You can add filtering conditions using `if` clauses to create lists that include only certain elements.

```python
# Filter even numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [x for x in numbers if x % 2 == 0]
odds = [x for x in numbers if x % 2 != 0]
print(f"Evens: {evens}")
print(f"Odds: {odds}")

# Filter and transform
scores = [85, 92, 78, 95, 88, 72, 90]
high_scores = [score for score in scores if score >= 85]
print(f"High scores: {high_scores}")

# Multiple conditions (AND)
passing_high = [score for score in scores if score >= 70 and score <= 90]
print(f"Passing (70-90): {passing_high}")

# Conditional expression (if-else in expression)
# Syntax: [true_value if condition else false_value for item in iterable]
pass_fail = ["Pass" if score >= 70 else "Fail" for score in scores]
print(f"Pass/Fail: {pass_fail}")

# Grade assignment with multiple conditions
def assign_grade(score):
    if score >= 90: return 'A'
    elif score >= 80: return 'B'
    elif score >= 70: return 'C'
    elif score >= 60: return 'D'
    else: return 'F'

grades = [assign_grade(score) for score in scores]
print(f"Grades: {grades}")

# Filter strings by length and content
words = ["apple", "pie", "a", "programming", "elephant", "i"]
long_words = [word for word in words if len(word) > 3]
words_with_e = [word for word in words if 'e' in word]
print(f"Long words: {long_words}")
print(f"Words with 'e': {words_with_e}")

# Real-world example: Processing user data
users = [
    {"name": "Alice", "age": 25, "active": True},
    {"name": "Bob", "age": 17, "active": True},
    {"name": "Charlie", "age": 30, "active": False},
    {"name": "Diana", "age": 22, "active": True}
]

# Get names of active adult users
active_adults = [user["name"] for user in users if user["age"] >= 18 and user["active"]]
print(f"Active adults: {active_adults}")
```

## Nested List Comprehensions

List comprehensions can be nested to work with multi-dimensional data or create complex transformations.

```python
# Flatten a 2D list
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Flatten to 1D list
flat = [num for row in matrix for num in row]
print(f"Flattened: {flat}")

# Create multiplication table
mult_table = [[i * j for j in range(1, 6)] for i in range(1, 6)]
print("Multiplication table:")
for row in mult_table:
    print(row)

# Transpose a matrix
transposed = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
print(f"Transposed: {transposed}")

# Working with nested data structures
students = [
    {"name": "Alice", "grades": [85, 90, 92]},
    {"name": "Bob", "grades": [78, 82, 80]},
    {"name": "Charlie", "grades": [95, 93, 97]}
]

# Get all grades as flat list
all_grades = [grade for student in students for grade in student["grades"]]
print(f"All grades: {all_grades}")

# Calculate average for each student
averages = [(student["name"], sum(student["grades"]) / len(student["grades"]))
            for student in students]
print(f"Averages: {averages}")

# Coordinates: all combinations of x and y
x_coords = [1, 2, 3]
y_coords = [4, 5, 6]
coordinates = [(x, y) for x in x_coords for y in y_coords]
print(f"Coordinates: {coordinates}")

# Filtered nested comprehension
coordinates_sum_even = [(x, y) for x in x_coords for y in y_coords if (x + y) % 2 == 0]
print(f"Coordinates (sum even): {coordinates_sum_even}")
```

## Set and Dictionary Comprehensions

Python also supports comprehensions for sets and dictionaries, using similar syntax.

```python
# Set comprehension - automatically removes duplicates
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squares = {x ** 2 for x in numbers}
print(f"Unique squares: {unique_squares}")

# Filter into set
text = "Hello World"
vowels = {char.lower() for char in text if char.lower() in 'aeiou'}
print(f"Vowels in text: {vowels}")

# Dictionary comprehension
# Syntax: {key: value for item in iterable}
squares_dict = {x: x ** 2 for x in range(1, 6)}
print(f"Squares dict: {squares_dict}")

# Invert a dictionary (swap keys and values)
original = {"a": 1, "b": 2, "c": 3}
inverted = {value: key for key, value in original.items()}
print(f"Inverted: {inverted}")

# Filter dictionary
prices = {"apple": 0.5, "banana": 0.3, "orange": 0.6, "grape": 2.0}
expensive = {item: price for item, price in prices.items() if price > 0.5}
print(f"Expensive items: {expensive}")

# Transform dictionary values
doubled_prices = {item: price * 2 for item, price in prices.items()}
print(f"Doubled prices: {doubled_prices}")

# Create dictionary from two lists
keys = ["name", "age", "city"]
values = ["Alice", 25, "New York"]
person = {k: v for k, v in zip(keys, values)}
print(f"Person: {person}")

# Real-world example: Word frequency counter
text = "the quick brown fox jumps over the lazy dog the fox"
word_freq = {word: text.split().count(word) for word in set(text.split())}
print(f"Word frequency: {word_freq}")

# Nested dictionary comprehension
students = ["Alice", "Bob", "Charlie"]
subjects = ["Math", "Science", "English"]
grade_book = {
    student: {subject: 0 for subject in subjects}
    for student in students
}
print(f"Grade book structure: {grade_book}")

# Generator expression (similar but returns generator, not list)
# Uses () instead of []
gen = (x ** 2 for x in range(1000000))  # Doesn't create list immediately
print(f"Generator: {gen}")
print(f"First value: {next(gen)}")  # Computed on demand
```

Performance and readability comparison:

| Pattern | Traditional Loop | List Comprehension | Performance |
|---------|-----------------|-------------------|-------------|
| Simple map | 5 lines | 1 line | ~10% faster |
| Filter | 4-5 lines | 1 line | ~15% faster |
| Map + Filter | 6-8 lines | 1 line | ~20% faster |
| Nested loops | 8+ lines | 1-2 lines | Similar |

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Square Even Numbers"
    difficulty: basic
    description: "Create a list of squares of even numbers from 1 to 10 using a list comprehension."
    starter_code: |
      # Create list of squares of even numbers from 1 to 10
      # Print the result

    expected_output: |
      [4, 16, 36, 64, 100]
    hints:
      - "Use range(1, 11) to get numbers 1 to 10"
      - "Filter for even numbers with if x % 2 == 0"
      - "Square each number with x ** 2"
    solution: |
      # Create list of squares of even numbers from 1 to 10
      result = [x ** 2 for x in range(1, 11) if x % 2 == 0]

      # Print the result
      print(result)

  - title: "String Length Filter"
    difficulty: basic
    description: "Extract words longer than 4 characters from a sentence and convert them to uppercase."
    starter_code: |
      sentence = "the quick brown fox jumps over the lazy dog"

      # Extract words longer than 4 chars and convert to uppercase
      # Print the result

    expected_output: |
      ['QUICK', 'BROWN', 'JUMPS']
    hints:
      - "Use sentence.split() to get words"
      - "Filter with if len(word) > 4"
      - "Use word.upper() to convert to uppercase"
    solution: |
      sentence = "the quick brown fox jumps over the lazy dog"

      # Extract words longer than 4 chars and convert to uppercase
      result = [word.upper() for word in sentence.split() if len(word) > 4]

      # Print the result
      print(result)

  - title: "Temperature Converter"
    difficulty: intermediate
    description: "Convert a list of Celsius temperatures to Fahrenheit, rounding to 1 decimal place. Formula: F = C * 9/5 + 32"
    starter_code: |
      celsius = [0, 10, 20, 30, 37, 100]

      # Convert to Fahrenheit and round to 1 decimal
      # Print the result

    expected_output: |
      [32.0, 50.0, 68.0, 86.0, 98.6, 212.0]
    hints:
      - "Use formula: c * 9/5 + 32"
      - "Use round(value, 1) for 1 decimal place"
    solution: |
      celsius = [0, 10, 20, 30, 37, 100]

      # Convert to Fahrenheit and round to 1 decimal
      fahrenheit = [round(c * 9/5 + 32, 1) for c in celsius]

      # Print the result
      print(fahrenheit)

  - title: "Nested List Flattener with Filter"
    difficulty: intermediate
    description: "Flatten a 2D list and keep only numbers greater than 5."
    starter_code: |
      matrix = [
          [1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12]
      ]

      # Flatten and keep only numbers > 5
      # Print the result

    expected_output: |
      [6, 7, 8, 9, 10, 11, 12]
    hints:
      - "Use nested comprehension: for row in matrix for num in row"
      - "Add condition if num > 5"
    solution: |
      matrix = [
          [1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12]
      ]

      # Flatten and keep only numbers > 5
      result = [num for row in matrix for num in row if num > 5]

      # Print the result
      print(result)

  - title: "Dictionary from Lists with Condition"
    difficulty: advanced
    description: "Create a dictionary from two lists (names and scores) but only include students who scored 80 or above."
    starter_code: |
      names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
      scores = [92, 78, 85, 95, 72]

      # Create dict of {name: score} for scores >= 80
      # Print the result

    expected_output: |
      {'Alice': 92, 'Charlie': 85, 'Diana': 95}
    hints:
      - "Use zip(names, scores) to pair them"
      - "Use dictionary comprehension: {name: score for ...}"
      - "Add condition if score >= 80"
    solution: |
      names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
      scores = [92, 78, 85, 95, 72]

      # Create dict of {name: score} for scores >= 80
      result = {name: score for name, score in zip(names, scores) if score >= 80}

      # Print the result
      print(result)

  - title: "Prime Number Generator"
    difficulty: advanced
    description: "Generate a list of prime numbers between 2 and 50 using list comprehension."
    starter_code: |
      # Generate list of prime numbers from 2 to 50
      # A prime has no divisors except 1 and itself
      # Hint: use nested comprehension to check divisibility

    expected_output: |
      [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    hints:
      - "A number n is prime if no number from 2 to n-1 divides it evenly"
      - "Use all() with a generator to check divisibility"
      - "Filter: if all(n % i != 0 for i in range(2, n))"
    solution: |
      # Generate list of prime numbers from 2 to 50
      primes = [n for n in range(2, 51) if all(n % i != 0 for i in range(2, n))]
      print(primes)
```
<!-- EXERCISE_END -->
