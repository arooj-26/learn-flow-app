# Opening Files

File handling is a fundamental skill in Python programming. Before you can read from or write to a file, you must first open it. Python provides built-in functions and methods that make file operations straightforward and efficient. Understanding how to properly open files is the first step toward mastering file I/O operations.

## The open() Function

The `open()` function is Python's built-in way to open files. It returns a file object that you can use to read from or write to the file. The basic syntax requires at least one argument: the file path.

```python
# Basic file opening
file = open('example.txt', 'r')
print(f"File name: {file.name}")
print(f"File mode: {file.mode}")
print(f"Is closed: {file.closed}")
file.close()

# Opening with absolute path
file = open('/Users/username/documents/data.txt', 'r')
content = file.read()
file.close()

# Opening with relative path
file = open('../data/input.txt', 'r')
first_line = file.readline()
file.close()
```

## File Object Attributes

Once you open a file, the file object provides several useful attributes that give you information about the file and its current state.

| Attribute | Description | Example |
|-----------|-------------|---------|
| `name` | Returns the name of the file | `file.name` |
| `mode` | Returns the mode in which file was opened | `file.mode` |
| `closed` | Returns True if file is closed | `file.closed` |
| `readable()` | Returns True if file can be read | `file.readable()` |
| `writable()` | Returns True if file can be written | `file.writable()` |

```python
# Exploring file object attributes
file = open('sample.txt', 'r+')

print(f"File name: {file.name}")
print(f"Access mode: {file.mode}")
print(f"Is closed? {file.closed}")
print(f"Is readable? {file.readable()}")
print(f"Is writable? {file.writable()}")

file.close()
print(f"Is closed now? {file.closed}")
```

## Handling File Exceptions

When working with files, many things can go wrong: the file might not exist, you might not have permission to access it, or the disk might be full. Proper exception handling ensures your program doesn't crash unexpectedly.

```python
# Basic exception handling
try:
    file = open('nonexistent.txt', 'r')
    content = file.read()
    file.close()
except FileNotFoundError:
    print("Error: The file does not exist")
except PermissionError:
    print("Error: Permission denied")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# More comprehensive error handling
import os

filename = 'data.txt'
try:
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found")

    file = open(filename, 'r')
    content = file.read()
    print(f"Successfully read {len(content)} characters")
except FileNotFoundError as e:
    print(f"File error: {e}")
except IOError as e:
    print(f"I/O error occurred: {e}")
finally:
    if 'file' in locals() and not file.closed:
        file.close()
        print("File closed in finally block")
```

## The with Statement

The `with` statement automatically handles closing files, even if an exception occurs. This is the recommended way to work with files in Python because it ensures proper resource management.

```python
# Using with statement (recommended)
with open('example.txt', 'r') as file:
    content = file.read()
    print(content)
# File is automatically closed here

# Multiple files with nested with statements
with open('input.txt', 'r') as infile:
    with open('output.txt', 'w') as outfile:
        for line in infile:
            outfile.write(line.upper())

# Multiple files in single with statement (Python 3.1+)
with open('input.txt', 'r') as infile, open('output.txt', 'w') as outfile:
    for line in infile:
        processed = line.strip().upper()
        outfile.write(processed + '\n')

# Exception handling with with statement
try:
    with open('data.txt', 'r') as file:
        content = file.read()
        print(f"File size: {len(content)} bytes")
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Error: {e}")
```

## Binary vs Text Mode

Files can be opened in either text mode (default) or binary mode. Text mode is used for text files and handles encoding automatically, while binary mode is used for non-text files like images or executables.

```python
# Text mode (default)
with open('document.txt', 'r') as file:
    text_content = file.read()
    print(f"Type: {type(text_content)}")  # str

# Binary mode
with open('image.png', 'rb') as file:
    binary_content = file.read()
    print(f"Type: {type(binary_content)}")  # bytes
    print(f"First 10 bytes: {binary_content[:10]}")

# Text mode with specific encoding
with open('unicode.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    print(content)

# Binary write mode
data = bytes([0x89, 0x50, 0x4E, 0x47])  # PNG header
with open('test.png', 'wb') as file:
    file.write(data)
    print(f"Wrote {len(data)} bytes")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Open and Inspect a File"
    difficulty: basic
    description: "Open a file in read mode and print its attributes (name, mode, and whether it's readable)."
    starter_code: |
      # Open 'sample.txt' in read mode
      # Print the file name, mode, and readable status
      # Close the file

    expected_output: |
      File name: sample.txt
      Mode: r
      Readable: True
    hints:
      - "Use the open() function with 'r' mode"
      - "Access file.name, file.mode, and file.readable()"
      - "Don't forget to close the file"
    solution: |
      file = open('sample.txt', 'r')
      print(f"File name: {file.name}")
      print(f"Mode: {file.mode}")
      print(f"Readable: {file.readable()}")
      file.close()

  - title: "Using the with Statement"
    difficulty: basic
    description: "Open a file using the with statement and print a confirmation message."
    starter_code: |
      # Use with statement to open 'data.txt' in read mode
      # Print 'File opened successfully'
      # Print 'File closed automatically' after the with block

    expected_output: |
      File opened successfully
      File closed automatically
    hints:
      - "Use 'with open() as file:' syntax"
      - "The file closes automatically after the with block"
    solution: |
      with open('data.txt', 'r') as file:
          print("File opened successfully")
      print("File closed automatically")

  - title: "Exception Handling for Missing Files"
    difficulty: intermediate
    description: "Try to open a non-existent file and handle the FileNotFoundError exception appropriately."
    starter_code: |
      # Try to open 'nonexistent.txt'
      # Handle FileNotFoundError
      # Print appropriate error message

    expected_output: |
      Error: The file 'nonexistent.txt' was not found
    hints:
      - "Use try-except block"
      - "Catch FileNotFoundError specifically"
      - "Print a user-friendly error message"
    solution: |
      try:
          file = open('nonexistent.txt', 'r')
          content = file.read()
          file.close()
      except FileNotFoundError:
          print("Error: The file 'nonexistent.txt' was not found")

  - title: "Multiple File Operations"
    difficulty: intermediate
    description: "Simulate opening two files simultaneously using a single with statement and print their names."
    starter_code: |
      # Open 'input.txt' and 'output.txt' in a single with statement
      # Print both file names
      # Use read mode for input, write mode for output

    expected_output: |
      Input file: input.txt
      Output file: output.txt
    hints:
      - "Use comma to separate multiple file opens in with statement"
      - "Different files can have different modes"
    solution: |
      with open('input.txt', 'r') as infile, open('output.txt', 'w') as outfile:
          print(f"Input file: {infile.name}")
          print(f"Output file: {outfile.name}")

  - title: "File Mode Detective"
    difficulty: advanced
    description: "Create a function that opens a file and returns a dictionary with all file object attributes and methods availability."
    starter_code: |
      def file_inspector(filename, mode):
          # Open file with given mode
          # Create dictionary with name, mode, closed, readable, writable
          # Close file and return dictionary
          pass

      # Test with 'test.txt' in 'r+' mode

    expected_output: |
      {'name': 'test.txt', 'mode': 'r+', 'closed': True, 'readable': True, 'writable': True}
    hints:
      - "Open the file with the specified mode"
      - "Call readable() and writable() methods"
      - "Close the file before returning"
    solution: |
      def file_inspector(filename, mode):
          file = open(filename, mode)
          info = {
              'name': file.name,
              'mode': file.mode,
              'closed': False,
              'readable': file.readable(),
              'writable': file.writable()
          }
          file.close()
          info['closed'] = True
          return info

      result = file_inspector('test.txt', 'r+')
      print(result)

  - title: "Robust File Opener with Fallback"
    difficulty: advanced
    description: "Create a context manager function that tries to open a file, and if it fails, creates the file and returns it."
    starter_code: |
      def safe_file_open(filename, mode='r'):
          # Try to open file
          # If FileNotFoundError and mode is 'r', create file then open
          # Use try-except and return file object
          pass

      # Simulate usage

    expected_output: |
      Attempting to open: data.txt
      File not found, creating new file
      File opened successfully in mode: r
    hints:
      - "Use try-except for FileNotFoundError"
      - "If file doesn't exist and mode is 'r', create it first with 'w'"
      - "Then open it in the requested mode"
    solution: |
      def safe_file_open(filename, mode='r'):
          print(f"Attempting to open: {filename}")
          try:
              file = open(filename, mode)
              print(f"File opened successfully in mode: {mode}")
              return file
          except FileNotFoundError:
              if mode == 'r':
                  print("File not found, creating new file")
                  with open(filename, 'w') as f:
                      pass
                  file = open(filename, mode)
                  print(f"File opened successfully in mode: {mode}")
                  return file
              raise

      file = safe_file_open('data.txt', 'r')
      file.close()
```
<!-- EXERCISE_END -->
