# Strings in Python

Strings are one of Python's most versatile data types. They are immutable sequences of Unicode characters used to represent text data. Understanding strings deeply is essential for data processing, web development, and virtually every Python application.

## Creating Strings

Python offers multiple ways to create strings, each with specific use cases:

```python
# Single and double quotes
name = 'Alice'
greeting = "Hello, World!"

# Triple quotes for multiline strings
paragraph = """This is a
multiline string that preserves
line breaks and indentation."""

# Raw strings (ignore escape sequences)
path = r"C:\Users\new_folder\test"
print(path)  # C:\Users\new_folder\test

# Byte strings
data = b"Hello"
print(type(data))  # <class 'bytes'>
```

## String Indexing and Slicing

Strings support powerful indexing and slicing operations:

```python
text = "Python Programming"

# Positive indexing (0-based)
print(text[0])    # P
print(text[7])    # P

# Negative indexing (from end)
print(text[-1])   # g
print(text[-4])   # m

# Slicing: [start:stop:step]
print(text[0:6])    # Python
print(text[7:])     # Programming
print(text[:6])     # Python
print(text[::2])    # Pto rgamn
print(text[::-1])   # gnimmargorP nohtyP

# Practical: extract parts of structured data
email = "user@example.com"
username = email[:email.index('@')]
domain = email[email.index('@')+1:]
print(f"{username} at {domain}")  # user at example.com
```

## String Immutability

Strings cannot be modified in place. Any operation that appears to modify a string actually creates a new one:

```python
text = "Hello"
# text[0] = "h"  # TypeError: 'str' object does not support item assignment

# Instead, create a new string
text = "h" + text[1:]
print(text)  # hello

# String interning - Python caches small strings
a = "hello"
b = "hello"
print(a is b)  # True (same object in memory)

# But not for dynamically created strings
c = "hel" + "lo"
d = "hello"
print(c is d)  # True (Python optimizes this)
```

## Escape Sequences

Escape sequences represent special characters within strings:

| Escape | Description | Example |
|--------|-------------|---------|
| `\n` | Newline | `"line1\nline2"` |
| `\t` | Tab | `"col1\tcol2"` |
| `\\` | Backslash | `"path\\file"` |
| `\'` | Single quote | `'it\'s'` |
| `\"` | Double quote | `"say \"hi\""` |
| `\0` | Null character | `"null\0char"` |
| `\u` | Unicode (16-bit) | `"\u0041"` → `A` |
| `\U` | Unicode (32-bit) | `"\U0001F600"` → emoji |

```python
# Practical escape sequences
print("Name:\tAlice\nAge:\t30")
# Name:   Alice
# Age:    30

# Unicode characters
print("\u2764 \u2605 \u266B")  # ❤ ★ ♫

# Raw strings skip escape processing
print(r"No \n newline here")  # No \n newline here
```

## String Formatting

Python provides three main approaches to string formatting:

```python
name = "Alice"
age = 30
score = 95.567

# 1. F-strings (Python 3.6+) - PREFERRED
print(f"Name: {name}, Age: {age}")
print(f"Score: {score:.2f}")        # Score: 95.57
print(f"{'Centered':^20}")          # '      Centered      '
print(f"{age:05d}")                  # 00030
print(f"{1000000:,}")               # 1,000,000

# 2. str.format() method
print("Name: {}, Age: {}".format(name, age))
print("Name: {0}, again {0}".format(name))
print("{name} is {age}".format(name="Bob", age=25))

# 3. % formatting (legacy, but still seen)
print("Name: %s, Age: %d" % (name, age))
print("Score: %.2f%%" % score)

# F-string expressions
items = [1, 2, 3, 4, 5]
print(f"Sum: {sum(items)}")          # Sum: 15
print(f"Even: {[x for x in items if x % 2 == 0]}")  # Even: [2, 4]
```

## String Concatenation and Repetition

```python
# Concatenation
first = "Hello"
second = "World"
result = first + " " + second
print(result)  # Hello World

# Join is more efficient for multiple strings
words = ["Python", "is", "awesome"]
sentence = " ".join(words)
print(sentence)  # Python is awesome

# Repetition
line = "-" * 40
print(line)  # ----------------------------------------

# Building strings efficiently
parts = []
for i in range(5):
    parts.append(f"item_{i}")
result = ", ".join(parts)
print(result)  # item_0, item_1, item_2, item_3, item_4
```

## String Comparison and Membership

```python
# Comparison (lexicographic, based on Unicode values)
print("apple" < "banana")   # True
print("Apple" < "apple")    # True (uppercase < lowercase)
print("abc" == "abc")       # True

# Case-insensitive comparison
s1 = "Hello"
s2 = "hello"
print(s1.lower() == s2.lower())  # True

# Membership testing
text = "Python Programming Language"
print("Python" in text)      # True
print("java" in text)        # False
print("java" not in text)    # True
```

## Best Practices

1. **Use f-strings** for formatting - they're readable and fast
2. **Use `join()`** instead of `+` for concatenating many strings
3. **Use raw strings** for regex patterns and file paths
4. **Use triple quotes** for multiline strings and docstrings
5. **Avoid string concatenation in loops** - build a list and join

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "String Slicing"
    difficulty: basic
    description: "Given the string 'Hello, Python!', extract and print only the word 'Python' using slicing."
    starter_code: |
      text = "Hello, Python!"
      # Extract 'Python' using slicing

    expected_output: "Python"
    hints:
      - "Count the index where 'Python' starts"
      - "Use text[start:end] syntax"
    solution: |
      text = "Hello, Python!"
      print(text[7:13])

  - title: "String Reversal"
    difficulty: basic
    description: "Reverse the string 'Programming' and print it."
    starter_code: |
      word = "Programming"
      # Reverse the string

    expected_output: "gnimmargorP"
    hints:
      - "Use slicing with a negative step"
      - "The syntax is string[::-1]"
    solution: |
      word = "Programming"
      print(word[::-1])

  - title: "Email Parser"
    difficulty: intermediate
    description: "Extract the username and domain from 'developer@company.org' and print them on separate lines."
    starter_code: |
      email = "developer@company.org"
      # Extract username and domain

    expected_output: |
      developer
      company.org
    hints:
      - "Use the index() or find() method to locate '@'"
      - "Use slicing to extract parts before and after '@'"
    solution: |
      email = "developer@company.org"
      at_pos = email.index('@')
      username = email[:at_pos]
      domain = email[at_pos+1:]
      print(username)
      print(domain)

  - title: "Formatted Table Row"
    difficulty: intermediate
    description: "Create a formatted string that displays 'Alice' left-aligned in 15 chars, age 30 right-aligned in 5 chars, and score 95.5 with 1 decimal place in 8 chars. Print the result."
    starter_code: |
      name = "Alice"
      age = 30
      score = 95.5
      # Create formatted output

    expected_output: "Alice              30    95.5"
    hints:
      - "Use f-string format specifiers"
      - "< for left-align, > for right-align"
    solution: |
      name = "Alice"
      age = 30
      score = 95.5
      print(f"{name:<15}{age:>5}{score:>8.1f}")

  - title: "Palindrome Checker"
    difficulty: advanced
    description: "Check if 'A man a plan a canal Panama' is a palindrome (ignoring case and spaces). Print True or False."
    starter_code: |
      text = "A man a plan a canal Panama"
      # Check if palindrome (ignore case and spaces)

    expected_output: "True"
    hints:
      - "Remove spaces and convert to lowercase first"
      - "Compare the cleaned string with its reverse"
    solution: |
      text = "A man a plan a canal Panama"
      cleaned = text.replace(" ", "").lower()
      print(cleaned == cleaned[::-1])

  - title: "String Cipher"
    difficulty: advanced
    description: "Implement a Caesar cipher that shifts each letter in 'hello' by 3 positions forward in the alphabet. Non-letter characters stay unchanged. Print the encrypted result."
    starter_code: |
      message = "hello"
      shift = 3
      # Encrypt using Caesar cipher

    expected_output: "khoor"
    hints:
      - "Use ord() to get character code and chr() to convert back"
      - "Handle wrapping with modulo: (ord(c) - ord('a') + shift) % 26"
    solution: |
      message = "hello"
      shift = 3
      encrypted = ""
      for char in message:
          if char.isalpha():
              base = ord('a') if char.islower() else ord('A')
              encrypted += chr((ord(char) - base + shift) % 26 + base)
          else:
              encrypted += char
      print(encrypted)
```
<!-- EXERCISE_END -->
