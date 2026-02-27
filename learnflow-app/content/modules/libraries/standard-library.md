# Standard Library

Python's standard library is a comprehensive collection of modules and packages that come bundled with Python installations. It provides robust solutions for common programming tasks without requiring external dependencies. Understanding the standard library is essential for writing efficient, professional Python code.

## Overview of Standard Library Categories

The Python standard library is organized into several categories, each addressing different aspects of programming. These modules cover everything from file I/O to networking, from data structures to concurrent programming.

```python
# Text Processing
import re
import string
import textwrap

# String manipulation
text = "  Python Programming  "
print(text.strip())  # "Python Programming"

# Regular expressions
pattern = r'\b[A-Z][a-z]+\b'
text = "Alice and Bob went to Paris"
matches = re.findall(pattern, text)
print(matches)  # ['Alice', 'Bob', 'Paris']

# Text wrapping
long_text = "This is a very long text that needs to be wrapped to fit within a certain width."
wrapped = textwrap.fill(long_text, width=30)
print(wrapped)

# String constants
print(string.ascii_lowercase)  # 'abcdefghijklmnopqrstuvwxyz'
print(string.digits)  # '0123456789'
```

| Category | Key Modules | Purpose |
|----------|-------------|---------|
| Text Processing | `re`, `string`, `textwrap` | String operations, regex |
| Data Types | `collections`, `array`, `copy` | Advanced data structures |
| Mathematics | `math`, `statistics`, `decimal` | Numerical operations |
| File/Data | `pathlib`, `pickle`, `json` | File handling, serialization |
| Operating System | `os`, `sys`, `subprocess` | OS interaction |
| Networking | `urllib`, `http`, `socket` | Network protocols |

## Data Structures and Collections

The `collections` module provides specialized container datatypes that extend Python's built-in types with additional functionality and better performance for specific use cases.

```python
from collections import Counter, defaultdict, deque, namedtuple, OrderedDict

# Counter: Count hashable objects
words = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
word_counts = Counter(words)
print(word_counts)  # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(word_counts.most_common(2))  # [('apple', 3), ('banana', 2)]

# defaultdict: Dictionary with default values
scores = defaultdict(list)
scores['Alice'].append(95)
scores['Bob'].append(87)
scores['Alice'].append(92)
print(dict(scores))  # {'Alice': [95, 92], 'Bob': [87]}

# deque: Double-ended queue (efficient append/pop from both ends)
queue = deque([1, 2, 3])
queue.append(4)      # Add to right
queue.appendleft(0)  # Add to left
print(queue)         # deque([0, 1, 2, 3, 4])
queue.rotate(2)      # Rotate right
print(queue)         # deque([3, 4, 0, 1, 2])

# namedtuple: Tuple with named fields
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print(f"X: {p.x}, Y: {p.y}")  # X: 10, Y: 20
print(p[0])  # 10 (still accessible by index)

# OrderedDict: Dictionary that remembers insertion order (less relevant in Python 3.7+)
from collections import OrderedDict
od = OrderedDict()
od['first'] = 1
od['second'] = 2
od['third'] = 3
print(list(od.keys()))  # ['first', 'second', 'third']
```

## File and Path Operations

Modern Python uses the `pathlib` module for object-oriented filesystem paths, providing a cleaner and more intuitive interface than the older `os.path` module.

```python
from pathlib import Path
import shutil
import tempfile

# Create Path objects
home = Path.home()
current = Path.cwd()
print(f"Home: {home}")
print(f"Current: {current}")

# Path operations
config_file = Path("config") / "settings.json"
print(config_file)  # config/settings.json

# Check path properties
path = Path("example.txt")
print(f"Exists: {path.exists()}")
print(f"Is file: {path.is_file()}")
print(f"Is directory: {path.is_dir()}")

# Get path components
full_path = Path("/home/user/documents/report.pdf")
print(f"Name: {full_path.name}")        # report.pdf
print(f"Stem: {full_path.stem}")        # report
print(f"Suffix: {full_path.suffix}")    # .pdf
print(f"Parent: {full_path.parent}")    # /home/user/documents

# Working with temporary files
with tempfile.TemporaryDirectory() as tmpdir:
    temp_path = Path(tmpdir)
    temp_file = temp_path / "temp.txt"
    temp_file.write_text("Temporary data")
    print(f"Temp file: {temp_file}")
    print(f"Content: {temp_file.read_text()}")
# Directory automatically cleaned up

# File operations
source = Path("source.txt")
dest = Path("destination.txt")
# source.rename(dest)  # Rename/move
# shutil.copy(source, dest)  # Copy file
# shutil.copytree(source_dir, dest_dir)  # Copy directory tree
```

## Itertools and Functional Programming

The `itertools` module provides functions for creating efficient iterators for looping. Combined with `functools`, it enables powerful functional programming patterns.

```python
import itertools
import functools
from operator import mul

# Infinite iterators
counter = itertools.count(start=10, step=2)
print(list(itertools.islice(counter, 5)))  # [10, 12, 14, 16, 18]

# Cycle through values
colors = itertools.cycle(['red', 'green', 'blue'])
print([next(colors) for _ in range(7)])  # ['red', 'green', 'blue', 'red', 'green', 'blue', 'red']

# Combinations and permutations
items = ['A', 'B', 'C']
print(list(itertools.combinations(items, 2)))  # [('A', 'B'), ('A', 'C'), ('B', 'C')]
print(list(itertools.permutations(items, 2)))  # [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

# Product (cartesian product)
print(list(itertools.product([1, 2], ['a', 'b'])))  # [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

# Chain iterables together
list1 = [1, 2, 3]
list2 = [4, 5, 6]
print(list(itertools.chain(list1, list2)))  # [1, 2, 3, 4, 5, 6]

# Groupby
data = [('A', 1), ('A', 2), ('B', 3), ('B', 4), ('C', 5)]
for key, group in itertools.groupby(data, lambda x: x[0]):
    print(f"{key}: {list(group)}")

# functools: reduce, partial, lru_cache
numbers = [1, 2, 3, 4, 5]
product = functools.reduce(mul, numbers)
print(f"Product: {product}")  # 120

# Partial functions
def power(base, exponent):
    return base ** exponent

square = functools.partial(power, exponent=2)
cube = functools.partial(power, exponent=3)
print(square(5))  # 25
print(cube(3))    # 27

# LRU Cache for memoization
@functools.lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))  # 55
print(fibonacci.cache_info())  # CacheInfo(hits=8, misses=11, maxsize=128, currsize=11)
```

## Date, Time, and JSON Processing

Working with dates, times, and data serialization is fundamental to many applications. The standard library provides robust tools for these common tasks.

```python
from datetime import datetime, timedelta, date, time
import json
import pickle

# DateTime operations
now = datetime.now()
print(f"Now: {now}")
print(f"Formatted: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# Date arithmetic
today = date.today()
tomorrow = today + timedelta(days=1)
week_ago = today - timedelta(weeks=1)
print(f"Today: {today}")
print(f"Tomorrow: {tomorrow}")
print(f"Week ago: {week_ago}")

# Parsing dates
date_string = "2024-06-15 14:30:00"
parsed = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
print(f"Parsed: {parsed}")

# Time differences
event_start = datetime(2024, 6, 15, 14, 0)
event_end = datetime(2024, 6, 15, 16, 30)
duration = event_end - event_start
print(f"Duration: {duration.total_seconds() / 3600} hours")

# JSON serialization
data = {
    'name': 'Alice',
    'age': 30,
    'skills': ['Python', 'JavaScript', 'SQL'],
    'is_active': True,
    'score': 95.5
}

# Convert to JSON string
json_string = json.dumps(data, indent=2)
print(json_string)

# Parse JSON string
parsed_data = json.loads(json_string)
print(f"Name: {parsed_data['name']}")

# Working with JSON files
# with open('data.json', 'w') as f:
#     json.dump(data, f, indent=2)
#
# with open('data.json', 'r') as f:
#     loaded_data = json.load(f)

# Pickle for Python objects
complex_data = {
    'list': [1, 2, 3],
    'tuple': (4, 5, 6),
    'set': {7, 8, 9},
    'custom_obj': datetime.now()
}

# Serialize
pickled = pickle.dumps(complex_data)
# Deserialize
unpickled = pickle.loads(pickled)
print(f"Unpickled: {unpickled}")
```

| Module | Use Case | Example |
|--------|----------|---------|
| `datetime` | Date/time manipulation | `datetime.now()` |
| `json` | JSON serialization | `json.dumps(data)` |
| `pickle` | Python object serialization | `pickle.dumps(obj)` |
| `csv` | CSV file handling | `csv.reader(file)` |
| `configparser` | Config files | `config.read('app.ini')` |

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Counter and Most Common"
    difficulty: basic
    description: "Use the Counter class from collections to analyze a list of words and find the 3 most common words with their counts."
    starter_code: |
      from collections import Counter

      text = "apple banana apple cherry banana apple orange banana cherry"
      words = text.split()

      # Create a Counter

      # Get 3 most common


      print("Top 3 words:")
      for word, count in most_common:
          print(f"{word}: {count}")
    expected_output: |
      Top 3 words:
      apple: 3
      banana: 3
      cherry: 2
    hints:
      - "Create Counter with Counter(words)"
      - "Use most_common(3) method"
    solution: |
      from collections import Counter

      text = "apple banana apple cherry banana apple orange banana cherry"
      words = text.split()

      # Create a Counter
      word_counter = Counter(words)
      # Get 3 most common
      most_common = word_counter.most_common(3)

      print("Top 3 words:")
      for word, count in most_common:
          print(f"{word}: {count}")

  - title: "Path Operations"
    difficulty: basic
    description: "Use pathlib to work with file paths. Create a path, extract components, and create a new path by joining components."
    starter_code: |
      from pathlib import Path

      # Create a path to a file
      file_path = Path("/home/user/documents/reports/2024/annual_report.pdf")

      # Extract name, stem, suffix, and parent
      print(f"Filename: {}")
      print(f"Stem: {}")
      print(f"Extension: {}")
      print(f"Parent directory: {}")

      # Create a new path in the same directory with different name
      new_path =
      print(f"New path: {new_path}")
    expected_output: |
      Filename: annual_report.pdf
      Stem: annual_report
      Extension: .pdf
      Parent directory: /home/user/documents/reports/2024
      New path: /home/user/documents/reports/2024/monthly_report.xlsx
    hints:
      - "Use .name for filename"
      - "Use .stem for name without extension"
      - "Use .suffix for extension"
      - "Use .parent for parent directory"
      - "Use parent / 'filename' to create new path"
    solution: |
      from pathlib import Path

      # Create a path to a file
      file_path = Path("/home/user/documents/reports/2024/annual_report.pdf")

      # Extract name, stem, suffix, and parent
      print(f"Filename: {file_path.name}")
      print(f"Stem: {file_path.stem}")
      print(f"Extension: {file_path.suffix}")
      print(f"Parent directory: {file_path.parent}")

      # Create a new path in the same directory with different name
      new_path = file_path.parent / "monthly_report.xlsx"
      print(f"New path: {new_path}")

  - title: "Date Calculations"
    difficulty: intermediate
    description: "Calculate the number of days between two dates, find the date 90 days from today, and determine the day of week for a specific date."
    starter_code: |
      from datetime import datetime, timedelta, date

      # Parse two dates
      date1 = datetime.strptime("2024-01-15", "%Y-%m-%d").date()
      date2 = datetime.strptime("2024-06-20", "%Y-%m-%d").date()

      # Calculate days between
      days_between =
      print(f"Days between dates: {days_between}")

      # Find date 90 days from today
      today = date.today()
      future_date =
      print(f"90 days from today: {future_date}")

      # Day of week for date1 (0=Monday, 6=Sunday)
      day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
      day_of_week =
      print(f"{date1} is a {day_names[day_of_week]}")
    expected_output: |
      Days between dates: 157
      90 days from today: 2026-05-11
      2024-01-15 is a Monday
    hints:
      - "Subtract dates to get timedelta, then use .days"
      - "Add timedelta to date: today + timedelta(days=90)"
      - "Use .weekday() method to get day of week"
    solution: |
      from datetime import datetime, timedelta, date

      # Parse two dates
      date1 = datetime.strptime("2024-01-15", "%Y-%m-%d").date()
      date2 = datetime.strptime("2024-06-20", "%Y-%m-%d").date()

      # Calculate days between
      days_between = (date2 - date1).days
      print(f"Days between dates: {days_between}")

      # Find date 90 days from today
      today = date.today()
      future_date = today + timedelta(days=90)
      print(f"90 days from today: {future_date}")

      # Day of week for date1 (0=Monday, 6=Sunday)
      day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
      day_of_week = date1.weekday()
      print(f"{date1} is a {day_names[day_of_week]}")

  - title: "JSON Data Processing"
    difficulty: intermediate
    description: "Parse a JSON string containing user data, filter users older than 25, and create a new JSON string with only their names and emails."
    starter_code: |
      import json

      json_data = '''
      {
        "users": [
          {"name": "Alice", "age": 28, "email": "alice@example.com"},
          {"name": "Bob", "age": 22, "email": "bob@example.com"},
          {"name": "Charlie", "age": 30, "email": "charlie@example.com"},
          {"name": "Diana", "age": 24, "email": "diana@example.com"}
        ]
      }
      '''

      # Parse JSON
      data =

      # Filter users older than 25
      filtered_users =

      # Create new structure with only name and email
      result =

      # Convert back to JSON
      output_json =
      print(output_json)
    expected_output: |
      {
        "filtered_users": [
          {
            "name": "Alice",
            "email": "alice@example.com"
          },
          {
            "name": "Charlie",
            "email": "charlie@example.com"
          }
        ]
      }
    hints:
      - "Use json.loads() to parse"
      - "Filter with list comprehension: [u for u in users if u['age'] > 25]"
      - "Extract fields: {'name': u['name'], 'email': u['email']}"
      - "Use json.dumps() with indent=2"
    solution: |
      import json

      json_data = '''
      {
        "users": [
          {"name": "Alice", "age": 28, "email": "alice@example.com"},
          {"name": "Bob", "age": 22, "email": "bob@example.com"},
          {"name": "Charlie", "age": 30, "email": "charlie@example.com"},
          {"name": "Diana", "age": 24, "email": "diana@example.com"}
        ]
      }
      '''

      # Parse JSON
      data = json.loads(json_data)

      # Filter users older than 25
      filtered_users = [u for u in data['users'] if u['age'] > 25]

      # Create new structure with only name and email
      result = {
          'filtered_users': [
              {'name': u['name'], 'email': u['email']}
              for u in filtered_users
          ]
      }

      # Convert back to JSON
      output_json = json.dumps(result, indent=2)
      print(output_json)

  - title: "Itertools Combinations"
    difficulty: advanced
    description: "Use itertools to generate all possible 3-person teams from a list of 5 people, then find which combinations include at least one specific person."
    starter_code: |
      import itertools

      people = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
      team_size = 3
      required_person = 'Alice'

      # Generate all combinations
      all_teams =

      # Filter teams that include the required person
      teams_with_person =

      print(f"Total possible teams: {len(all_teams)}")
      print(f"Teams with {required_person}:")
      for i, team in enumerate(teams_with_person, 1):
          print(f"  {i}. {', '.join(team)}")
    expected_output: |
      Total possible teams: 10
      Teams with Alice:
        1. Alice, Bob, Charlie
        2. Alice, Bob, Diana
        3. Alice, Bob, Eve
        4. Alice, Charlie, Diana
        5. Alice, Charlie, Eve
        6. Alice, Diana, Eve
    hints:
      - "Use itertools.combinations(people, team_size)"
      - "Convert to list to count: list(combinations)"
      - "Filter with list comprehension: [t for t in teams if person in t]"
    solution: |
      import itertools

      people = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
      team_size = 3
      required_person = 'Alice'

      # Generate all combinations
      all_teams = list(itertools.combinations(people, team_size))

      # Filter teams that include the required person
      teams_with_person = [team for team in all_teams if required_person in team]

      print(f"Total possible teams: {len(all_teams)}")
      print(f"Teams with {required_person}:")
      for i, team in enumerate(teams_with_person, 1):
          print(f"  {i}. {', '.join(team)}")

  - title: "Cached Fibonacci with Statistics"
    difficulty: advanced
    description: "Implement a cached Fibonacci function using functools.lru_cache and create a function that calculates multiple Fibonacci numbers and reports cache performance."
    starter_code: |
      import functools

      @functools.lru_cache(maxsize=128)
      def fibonacci(n):
          # Implement fibonacci with recursion


      def fibonacci_stats(numbers):
          # Clear cache to start fresh


          results = {}
          for n in numbers:
              results[n] = fibonacci(n)

          # Get cache statistics
          cache_info =

          return {
              'results': results,
              'cache_hits': cache_info.hits,
              'cache_misses': cache_info.misses,
              'hit_rate': cache_info.hits / (cache_info.hits + cache_info.misses) if cache_info.hits + cache_info.misses > 0 else 0
          }

      # Calculate Fibonacci for several numbers
      stats = fibonacci_stats([10, 15, 20, 15, 10])

      print("Fibonacci results:")
      for n, result in stats['results'].items():
          print(f"  F({n}) = {result}")
      print(f"\nCache hits: {stats['cache_hits']}")
      print(f"Cache misses: {stats['cache_misses']}")
      print(f"Hit rate: {stats['hit_rate']:.2%}")
    expected_output: |
      Fibonacci results:
        F(10) = 55
        F(15) = 610
        F(20) = 6765

      Cache hits: 34
      Cache misses: 21
      Hit rate: 61.82%
    hints:
      - "Fibonacci: if n < 2: return n, else: return fibonacci(n-1) + fibonacci(n-2)"
      - "Clear cache with fibonacci.cache_clear()"
      - "Get stats with fibonacci.cache_info()"
    solution: |
      import functools

      @functools.lru_cache(maxsize=128)
      def fibonacci(n):
          # Implement fibonacci with recursion
          if n < 2:
              return n
          return fibonacci(n - 1) + fibonacci(n - 2)

      def fibonacci_stats(numbers):
          # Clear cache to start fresh
          fibonacci.cache_clear()

          results = {}
          for n in numbers:
              results[n] = fibonacci(n)

          # Get cache statistics
          cache_info = fibonacci.cache_info()

          return {
              'results': results,
              'cache_hits': cache_info.hits,
              'cache_misses': cache_info.misses,
              'hit_rate': cache_info.hits / (cache_info.hits + cache_info.misses) if cache_info.hits + cache_info.misses > 0 else 0
          }

      # Calculate Fibonacci for several numbers
      stats = fibonacci_stats([10, 15, 20, 15, 10])

      print("Fibonacci results:")
      for n, result in stats['results'].items():
          print(f"  F({n}) = {result}")
      print(f"\nCache hits: {stats['cache_hits']}")
      print(f"Cache misses: {stats['cache_misses']}")
      print(f"Hit rate: {stats['hit_rate']:.2%}")
```
<!-- EXERCISE_END -->
