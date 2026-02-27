# Writing Files

Writing to files is essential for saving program output, logging information, and persisting data. Python provides multiple methods for writing content to files, whether you need to create new files, append to existing ones, or write specific data formats.

## Writing Text to Files

The `write()` method writes a string to a file. Unlike print(), it doesn't automatically add newline characters, giving you complete control over the output format.

```python
# Basic file writing
with open('output.txt', 'w') as file:
    file.write('Hello, World!\n')
    file.write('This is a new line.\n')
    bytes_written = file.write('Python file handling')
    print(f"Bytes written: {bytes_written}")

# Writing multiple lines
lines = ['First line\n', 'Second line\n', 'Third line\n']
with open('multi_line.txt', 'w') as file:
    for line in lines:
        file.write(line)

# Writing with f-strings
name = 'Alice'
age = 30
with open('person.txt', 'w') as file:
    file.write(f'Name: {name}\n')
    file.write(f'Age: {age}\n')
    file.write(f'Year of birth: {2024 - age}\n')
```

## Using writelines()

The `writelines()` method writes a list of strings to a file in a single operation. It's more efficient than writing in a loop, but remember it doesn't add newlines automatically.

```python
# Using writelines()
data = ['Apple\n', 'Banana\n', 'Cherry\n', 'Date\n']
with open('fruits.txt', 'w') as file:
    file.writelines(data)

# Without newlines (need to add them)
items = ['Item 1', 'Item 2', 'Item 3']
with open('items.txt', 'w') as file:
    file.writelines([item + '\n' for item in items])

# Writing from generator
def generate_numbers(n):
    for i in range(1, n + 1):
        yield f'Number: {i}\n'

with open('numbers.txt', 'w') as file:
    file.writelines(generate_numbers(10))

# Efficient large-scale writing
def write_large_dataset(filename, size):
    with open(filename, 'w') as file:
        lines = (f'Record {i}: Data point\n' for i in range(size))
        file.writelines(lines)

write_large_dataset('big_data.txt', 1000)
print("Dataset written successfully")
```

## Appending to Files

Append mode (`'a'`) adds content to the end of an existing file without erasing its current contents. This is perfect for logs and incremental data collection.

```python
# Appending to a file
with open('log.txt', 'a') as file:
    file.write('New log entry\n')
    file.write('Another entry\n')

# Logging with timestamps
from datetime import datetime

def log_message(message, log_file='app.log'):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as file:
        file.write(f'[{timestamp}] {message}\n')

log_message('Application started')
log_message('Processing data')
log_message('Task completed')

# Appending structured data
def add_user(username, email, users_file='users.txt'):
    with open(users_file, 'a') as file:
        file.write(f'{username},{email}\n')

add_user('alice', 'alice@example.com')
add_user('bob', 'bob@example.com')
```

## Write Mode Comparison

Understanding the differences between write modes is crucial for proper file handling. Each mode has specific behaviors and use cases.

| Mode | Description | Creates File | Overwrites | Appends |
|------|-------------|--------------|------------|---------|
| `'w'` | Write mode | Yes | Yes | No |
| `'a'` | Append mode | Yes | No | Yes |
| `'x'` | Exclusive creation | Yes | Error if exists | No |
| `'w+'` | Write and read | Yes | Yes | No |
| `'a+'` | Append and read | Yes | No | Yes |

```python
# Write mode - overwrites existing content
with open('test.txt', 'w') as file:
    file.write('This overwrites everything\n')

# Append mode - adds to existing content
with open('test.txt', 'a') as file:
    file.write('This is appended\n')

# Exclusive mode - fails if file exists
try:
    with open('new_file.txt', 'x') as file:
        file.write('This only works if file is new\n')
    print("File created successfully")
except FileExistsError:
    print("File already exists")

# Read and write mode
with open('data.txt', 'w+') as file:
    file.write('Some data\n')
    file.seek(0)  # Go back to beginning
    content = file.read()
    print(f"Written content: {content}")
```

## Writing Formatted Data

Writing structured data requires careful formatting. Here are patterns for common data structures and formats.

```python
# Writing CSV-like data
def write_csv(filename, data, headers):
    with open(filename, 'w') as file:
        # Write header
        file.write(','.join(headers) + '\n')

        # Write rows
        for row in data:
            file.write(','.join(str(item) for item in row) + '\n')

data = [
    ['Alice', 30, 'Engineer'],
    ['Bob', 25, 'Designer'],
    ['Charlie', 35, 'Manager']
]
headers = ['Name', 'Age', 'Role']
write_csv('employees.csv', data, headers)

# Writing key-value configuration
def write_config(filename, config_dict):
    with open(filename, 'w') as file:
        for key, value in config_dict.items():
            file.write(f'{key}={value}\n')

config = {
    'host': 'localhost',
    'port': 8080,
    'debug': True,
    'timeout': 30
}
write_config('settings.conf', config)

# Writing tabular data with alignment
def write_table(filename, data, headers):
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in data:
        for i, item in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(item)))

    with open(filename, 'w') as file:
        # Write header
        header_line = ' | '.join(h.ljust(w) for h, w in zip(headers, col_widths))
        file.write(header_line + '\n')
        file.write('-' * len(header_line) + '\n')

        # Write rows
        for row in data:
            row_line = ' | '.join(str(item).ljust(w) for item, w in zip(row, col_widths))
            file.write(row_line + '\n')

write_table('report.txt', data, headers)

# Writing multi-line records
def write_record(file, record_dict):
    for key, value in record_dict.items():
        file.write(f'{key}: {value}\n')
    file.write('---\n')

records = [
    {'name': 'Product A', 'price': 29.99, 'stock': 100},
    {'name': 'Product B', 'price': 39.99, 'stock': 50}
]

with open('products.txt', 'w') as file:
    for record in records:
        write_record(file, record)
```

## Buffering and Flushing

File writing is buffered by default for efficiency. Understanding buffering helps you control when data is actually written to disk.

```python
# Default buffering
with open('buffered.txt', 'w') as file:
    file.write('This is buffered\n')
    # Data might not be on disk yet
    file.flush()  # Force write to disk
    file.write('This too\n')
    # Automatically flushed when file closes

# Unbuffered writing (binary mode)
with open('unbuffered.bin', 'wb', buffering=0) as file:
    file.write(b'Immediately written\n')

# Line buffering (text mode)
with open('line_buffered.txt', 'w', buffering=1) as file:
    file.write('Line 1\n')  # Flushed immediately
    file.write('Line 2\n')  # Flushed immediately

# Custom buffer size
with open('custom_buffer.txt', 'w', buffering=8192) as file:
    for i in range(1000):
        file.write(f'Line {i}\n')

# Real-time logging with flush
import time

with open('realtime.log', 'w') as file:
    for i in range(5):
        file.write(f'Event {i} at {time.time()}\n')
        file.flush()  # Ensure immediate write
        time.sleep(1)
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Write Simple Text"
    difficulty: basic
    description: "Simulate writing three lines of text to a file and print confirmation."
    starter_code: |
      # Simulate writing to a file by storing in a list
      file_content = []

      # Add three lines to file_content
      # Print number of lines written

    expected_output: |
      Line 1
      Line 2
      Line 3
      Wrote 3 lines
    hints:
      - "Append strings to the file_content list"
      - "Print each line and the total count"
    solution: |
      file_content = []

      file_content.append('Line 1')
      file_content.append('Line 2')
      file_content.append('Line 3')

      for line in file_content:
          print(line)
      print(f"Wrote {len(file_content)} lines")

  - title: "Write List with writelines()"
    difficulty: basic
    description: "Simulate using writelines() to write a list of items."
    starter_code: |
      items = ['Apple', 'Banana', 'Cherry', 'Date']

      # Simulate writelines by creating output with newlines
      # Print the result

    expected_output: |
      Apple
      Banana
      Cherry
      Date
    hints:
      - "Add newline to each item"
      - "Print each item on separate line"
    solution: |
      items = ['Apple', 'Banana', 'Cherry', 'Date']

      output = [item + '\n' for item in items]
      for line in output:
          print(line.strip())

  - title: "Append Log Entries"
    difficulty: intermediate
    description: "Simulate appending log entries with timestamps to a log file."
    starter_code: |
      # Simulate existing log
      log = ['[2024-01-01 10:00:00] App started\n']

      # Add two new log entries with timestamps
      # Print all log entries

    expected_output: |
      [2024-01-01 10:00:00] App started
      [2024-01-01 10:05:00] Processing data
      [2024-01-01 10:10:00] Task completed
    hints:
      - "Append new entries to the log list"
      - "Format with timestamp in brackets"
      - "Print all entries"
    solution: |
      log = ['[2024-01-01 10:00:00] App started\n']

      log.append('[2024-01-01 10:05:00] Processing data\n')
      log.append('[2024-01-01 10:10:00] Task completed\n')

      for entry in log:
          print(entry.strip())

  - title: "Write CSV Format"
    difficulty: intermediate
    description: "Create a function to format data as CSV and print the output."
    starter_code: |
      def create_csv_output(headers, data):
          # Format headers and data rows as CSV
          # Return list of lines
          pass

      headers = ['Name', 'Age', 'City']
      data = [['Alice', 30, 'NYC'], ['Bob', 25, 'LA']]

    expected_output: |
      Name,Age,City
      Alice,30,NYC
      Bob,25,LA
    hints:
      - "Use ','.join() to combine items"
      - "Process headers first, then each data row"
      - "Convert all values to strings"
    solution: |
      def create_csv_output(headers, data):
          lines = []
          lines.append(','.join(headers))
          for row in data:
              lines.append(','.join(str(item) for item in row))
          return lines

      headers = ['Name', 'Age', 'City']
      data = [['Alice', 30, 'NYC'], ['Bob', 25, 'LA']]

      output = create_csv_output(headers, data)
      for line in output:
          print(line)

  - title: "Write Configuration File"
    difficulty: advanced
    description: "Create a function that formats a dictionary as a configuration file with sections and comments."
    starter_code: |
      def write_config_format(config):
          # Format config dict with sections
          # Add comment header
          # Return list of formatted lines
          pass

      config = {
          'server': {'host': 'localhost', 'port': 8080},
          'database': {'name': 'mydb', 'user': 'admin'}
      }

    expected_output: |
      # Configuration File

      [server]
      host=localhost
      port=8080

      [database]
      name=mydb
      user=admin
    hints:
      - "Start with a comment line"
      - "Each section starts with [section_name]"
      - "Write key=value pairs for each section"
      - "Add blank line between sections"
    solution: |
      def write_config_format(config):
          lines = ['# Configuration File', '']
          for section, values in config.items():
              lines.append(f'[{section}]')
              for key, value in values.items():
                  lines.append(f'{key}={value}')
              lines.append('')
          return lines

      config = {
          'server': {'host': 'localhost', 'port': 8080},
          'database': {'name': 'mydb', 'user': 'admin'}
      }

      output = write_config_format(config)
      for line in output:
          print(line)

  - title: "Format Aligned Table"
    difficulty: advanced
    description: "Create a function that formats data as an aligned table with headers and separators."
    starter_code: |
      def format_table(headers, data):
          # Calculate column widths
          # Create aligned table with separators
          # Return formatted lines
          pass

      headers = ['Name', 'Score', 'Grade']
      data = [['Alice', 95, 'A'], ['Bob', 87, 'B'], ['Charlie', 92, 'A']]

    expected_output: |
      Name    | Score | Grade
      --------+-------+------
      Alice   | 95    | A
      Bob     | 87    | B
      Charlie | 92    | A
    hints:
      - "Calculate max width for each column"
      - "Use ljust() to pad strings"
      - "Create separator line with dashes and plus signs"
    solution: |
      def format_table(headers, data):
          lines = []
          col_widths = [len(h) for h in headers]

          for row in data:
              for i, item in enumerate(row):
                  col_widths[i] = max(col_widths[i], len(str(item)))

          header_line = ' | '.join(h.ljust(w) for h, w in zip(headers, col_widths))
          lines.append(header_line)

          separator = '+'.join('-' * (w + 2) for w in col_widths)
          lines.append(separator)

          for row in data:
              row_line = ' | '.join(str(item).ljust(w) for item, w in zip(row, col_widths))
              lines.append(row_line)

          return lines

      headers = ['Name', 'Score', 'Grade']
      data = [['Alice', 95, 'A'], ['Bob', 87, 'B'], ['Charlie', 92, 'A']]

      output = format_table(headers, data)
      for line in output:
          print(line)
```
<!-- EXERCISE_END -->
