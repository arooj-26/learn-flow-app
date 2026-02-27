# String Methods in Python

Strings are one of the most commonly used data types in Python. The built-in string methods provide powerful tools for text manipulation, formatting, and analysis. Mastering these methods is essential for effective text processing.

## Case Conversion Methods

Python provides several methods to change the case of strings:

```python
text = "Hello, World!"

# Convert to different cases
uppercase = text.upper()         # "HELLO, WORLD!"
lowercase = text.lower()         # "hello, world!"
titlecase = text.title()         # "Hello, World!"
swapcase = text.swapcase()       # "hELLO, wORLD!"
capitalize = text.capitalize()   # "Hello, world!"

# Real-world example: Normalizing user input
user_email = "   User@EXAMPLE.com   "
normalized = user_email.strip().lower()  # "user@example.com"
```

## String Search and Check Methods

These methods help you find and validate content within strings:

```python
sentence = "Python programming is fun and powerful"

# Search methods
starts = sentence.startswith("Python")      # True
ends = sentence.endswith("powerful")        # True
contains = "fun" in sentence                # True
position = sentence.find("programming")     # 7 (index of first occurrence)
not_found = sentence.find("Java")           # -1 (not found)
count = sentence.count("a")                 # 3

# Check methods
is_alpha = "hello".isalpha()               # True (only letters)
is_digit = "12345".isdigit()               # True (only digits)
is_alnum = "hello123".isalnum()            # True (letters and digits)
is_space = "   ".isspace()                 # True (only whitespace)
is_upper = "HELLO".isupper()               # True
is_lower = "hello".islower()               # True

# Practical example: Email validation
email = "user@example.com"
has_at = "@" in email
has_dot = "." in email
is_valid = has_at and has_dot and not email.isspace()
```

## String Modification Methods

Methods that return modified versions of strings:

```python
text = "  Hello, World!  "

# Whitespace removal
stripped = text.strip()          # "Hello, World!"
left_strip = text.lstrip()       # "Hello, World!  "
right_strip = text.rstrip()      # "  Hello, World!"

# Replacement
replaced = text.replace("World", "Python")     # "  Hello, Python!  "
multi_replace = "banana".replace("a", "o", 2)  # "bonona" (max 2 replacements)

# Padding and alignment
centered = "Hello".center(11)         # "   Hello   "
left_aligned = "Hello".ljust(10)      # "Hello     "
right_aligned = "Hello".rjust(10)     # "     Hello"
zero_padded = "42".zfill(5)           # "00042"

# Real-world example: Formatting table columns
name = "Alice"
score = "95"
print(f"{name.ljust(10)} {score.rjust(5)}")  # "Alice           95"
```

## String Splitting and Joining

Essential methods for parsing and constructing strings:

```python
# Splitting strings
csv_data = "apple,banana,orange"
fruits = csv_data.split(",")           # ['apple', 'banana', 'orange']

sentence = "Hello world from Python"
words = sentence.split()               # ['Hello', 'world', 'from', 'Python']
words_limited = sentence.split(" ", 2) # ['Hello', 'world', 'from Python']

# Splitting lines
multiline = "Line 1\nLine 2\nLine 3"
lines = multiline.splitlines()         # ['Line 1', 'Line 2', 'Line 3']

# Joining strings
fruits = ["apple", "banana", "orange"]
csv = ", ".join(fruits)                # "apple, banana, orange"
path = "/".join(["home", "user", "documents"])  # "home/user/documents"

# Partition and rpartition
email = "user@example.com"
username, at, domain = email.partition("@")  # ('user', '@', 'example.com')

url = "https://www.example.com/page"
base, sep, path = url.rpartition("/")  # ('https://www.example.com', '/', 'page')
```

## Advanced String Methods

More specialized methods for complex string operations:

```python
# Expandtabs and translate
tabbed = "Name\tAge\tCity"
expanded = tabbed.expandtabs(4)        # "Name    Age    City"

# String translation (character mapping)
translation_table = str.maketrans("aeiou", "12345")
encoded = "hello world".translate(translation_table)  # "h2ll4 w4rld"

# Remove prefix/suffix (Python 3.9+)
url = "https://example.com"
without_protocol = url.removeprefix("https://")  # "example.com"

filename = "document.pdf"
without_ext = filename.removesuffix(".pdf")      # "document"

# Format method
template = "Hello, {name}! You are {age} years old."
message = template.format(name="Alice", age=25)
# "Hello, Alice! You are 25 years old."

# F-strings (modern and preferred)
name, age = "Bob", 30
message = f"Hello, {name}! You are {age} years old."
```

## Best Practices for String Methods

1. **Strings are immutable**: Methods return new strings, they don't modify the original
2. **Chain methods wisely**: Multiple operations can be chained but readability matters
3. **Use f-strings**: For string formatting, prefer f-strings over .format() or %
4. **Validate inputs**: Always check string content before processing
5. **Consider performance**: For large-scale text processing, use appropriate tools

```python
# Good: Clear and readable
user_input = "  HELLO  "
cleaned = user_input.strip().lower()

# Better: With validation
if user_input and isinstance(user_input, str):
    cleaned = user_input.strip().lower()
else:
    cleaned = ""

# Method chaining example
text = "  Python Programming  "
result = text.strip().lower().replace(" ", "-")  # "python-programming"

# Remember: Strings are immutable
original = "Hello"
modified = original.upper()
print(original)  # Still "Hello"
print(modified)  # "HELLO"
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Username Validator"
    difficulty: basic
    description: "Create a variable `username = 'Alice123'`. Check if it's alphanumeric and print True or False."
    starter_code: |
      username = "Alice123"
      # Check if alphanumeric

    expected_output: "True"
    hints:
      - "Use the .isalnum() method"
      - "This checks if all characters are letters or numbers"
    solution: |
      username = "Alice123"
      print(username.isalnum())

  - title: "Title Case Converter"
    difficulty: basic
    description: "Convert the string 'python programming is fun' to title case and print it."
    starter_code: |
      text = "python programming is fun"
      # Convert to title case

    expected_output: "Python Programming Is Fun"
    hints:
      - "Use the .title() method"
      - "It capitalizes the first letter of each word"
    solution: |
      text = "python programming is fun"
      print(text.title())

  - title: "Email Extractor"
    difficulty: intermediate
    description: "Given the email 'john.doe@example.com', extract and print just the username part (before the @)."
    starter_code: |
      email = "john.doe@example.com"
      # Extract username

    expected_output: "john.doe"
    hints:
      - "Use the .split() method with '@' as delimiter"
      - "Take the first element [0] from the result"
    solution: |
      email = "john.doe@example.com"
      username = email.split("@")[0]
      print(username)

  - title: "Word Counter"
    difficulty: intermediate
    description: "Count how many times the word 'python' appears in the text 'Python is great. I love python. Python rocks!' (case-insensitive)."
    starter_code: |
      text = "Python is great. I love python. Python rocks!"
      # Count occurrences of 'python'

    expected_output: "3"
    hints:
      - "Convert the text to lowercase first for case-insensitive matching"
      - "Use the .count() method"
    solution: |
      text = "Python is great. I love python. Python rocks!"
      count = text.lower().count("python")
      print(count)

  - title: "URL Slug Generator"
    difficulty: advanced
    description: "Convert the title 'My First Blog Post!' into a URL slug: lowercase, spaces to hyphens, remove exclamation marks. Expected: 'my-first-blog-post'"
    starter_code: |
      title = "My First Blog Post!"
      # Create URL slug

    expected_output: "my-first-blog-post"
    hints:
      - "Use .lower() to make it lowercase"
      - "Use .replace() to change spaces to hyphens"
      - "Use .replace() again to remove exclamation marks"
    solution: |
      title = "My First Blog Post!"
      slug = title.lower().replace(" ", "-").replace("!", "")
      print(slug)

  - title: "CSV Parser"
    difficulty: advanced
    description: "Parse the CSV data 'Alice,25,Engineer' into a formatted string: 'Name: Alice, Age: 25, Job: Engineer'."
    starter_code: |
      csv_data = "Alice,25,Engineer"
      # Parse and format

    expected_output: "Name: Alice, Age: 25, Job: Engineer"
    hints:
      - "Use .split(',') to break the CSV into parts"
      - "Assign the parts to variables: name, age, job"
      - "Use an f-string to format the output"
    solution: |
      csv_data = "Alice,25,Engineer"
      parts = csv_data.split(",")
      name, age, job = parts[0], parts[1], parts[2]
      result = f"Name: {name}, Age: {age}, Job: {job}"
      print(result)
```
<!-- EXERCISE_END -->
