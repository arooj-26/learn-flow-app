# Reading Files

Reading files is one of the most common operations in programming. Python provides several methods to read file content, each suited for different use cases. Whether you need to read the entire file at once, process it line by line, or read specific chunks, Python has you covered.

## Reading the Entire File

The `read()` method reads the entire content of a file into a single string. This is convenient for small to medium-sized files but can be memory-intensive for large files.

```python
# Read entire file content
with open('story.txt', 'r') as file:
    content = file.read()
    print(content)
    print(f"\nTotal characters: {len(content)}")

# Read with size limit
with open('large_file.txt', 'r') as file:
    # Read only first 100 characters
    partial_content = file.read(100)
    print(partial_content)
    print(f"Read {len(partial_content)} characters")

# Multiple reads from same file
with open('data.txt', 'r') as file:
    first_chunk = file.read(50)
    second_chunk = file.read(50)
    print(f"First chunk: {first_chunk}")
    print(f"Second chunk: {second_chunk}")
```

## Reading Line by Line

The `readline()` method reads a single line from the file, while `readlines()` reads all lines into a list. Line-by-line reading is memory-efficient and perfect for processing large files.

```python
# Reading one line at a time
with open('log.txt', 'r') as file:
    line1 = file.readline()
    line2 = file.readline()
    print(f"First line: {line1.strip()}")
    print(f"Second line: {line2.strip()}")

# Reading all lines into a list
with open('names.txt', 'r') as file:
    all_lines = file.readlines()
    print(f"Total lines: {len(all_lines)}")
    for i, line in enumerate(all_lines, 1):
        print(f"Line {i}: {line.strip()}")

# Processing lines with list comprehension
with open('numbers.txt', 'r') as file:
    numbers = [int(line.strip()) for line in file.readlines()]
    print(f"Sum of numbers: {sum(numbers)}")
```

## Iterating Over Files

Files are iterable objects in Python. You can loop through them directly, which is the most memory-efficient way to process large files since it reads one line at a time.

```python
# Direct iteration (most efficient)
with open('data.txt', 'r') as file:
    for line_number, line in enumerate(file, 1):
        print(f"{line_number}: {line.strip()}")

# Filtering lines while iterating
with open('log.txt', 'r') as file:
    error_lines = [line for line in file if 'ERROR' in line]
    print(f"Found {len(error_lines)} error lines")

# Processing CSV-like data
with open('scores.txt', 'r') as file:
    total_score = 0
    count = 0
    for line in file:
        name, score = line.strip().split(',')
        total_score += int(score)
        count += 1
    average = total_score / count if count > 0 else 0
    print(f"Average score: {average:.2f}")
```

## File Position and Seeking

The file object maintains a current position. You can check the position with `tell()` and change it with `seek()`. This is useful for reading specific parts of a file or re-reading content.

```python
# Checking and using file position
with open('data.txt', 'r') as file:
    print(f"Initial position: {file.tell()}")

    first_10 = file.read(10)
    print(f"After reading 10 chars: {file.tell()}")

    # Go back to beginning
    file.seek(0)
    print(f"After seek(0): {file.tell()}")

    # Read again from beginning
    content = file.read(10)
    print(f"Re-read content: {content}")

# Seeking to specific positions
with open('structured_data.txt', 'r') as file:
    # Read from position 50
    file.seek(50)
    data = file.read(20)
    print(f"Data from position 50: {data}")

    # Seek from current position
    file.seek(10, 1)  # 10 bytes forward from current

    # Seek from end (only in binary mode)
    # file.seek(-10, 2)  # 10 bytes before end

# Practical example: Reading file in chunks
def read_in_chunks(filename, chunk_size=1024):
    with open(filename, 'r') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

for chunk in read_in_chunks('large_file.txt', 100):
    print(f"Processing chunk of {len(chunk)} characters")
```

## Reading Specific File Formats

Different file formats require different reading strategies. Here are some common patterns for reading structured data from text files.

```python
# Reading key-value pairs
def read_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=')
                config[key.strip()] = value.strip()
    return config

config = read_config('settings.conf')
print(f"Configuration: {config}")

# Reading tabular data
def read_table(filename, delimiter='\t'):
    rows = []
    with open(filename, 'r') as file:
        headers = file.readline().strip().split(delimiter)
        for line in file:
            values = line.strip().split(delimiter)
            row_dict = dict(zip(headers, values))
            rows.append(row_dict)
    return rows

data = read_table('data.tsv')
print(f"Read {len(data)} rows")

# Reading multi-line records
def read_records(filename, separator='---'):
    records = []
    current_record = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line == separator:
                if current_record:
                    records.append('\n'.join(current_record))
                    current_record = []
            else:
                current_record.append(line)

        # Don't forget last record
        if current_record:
            records.append('\n'.join(current_record))

    return records

records = read_records('documents.txt')
print(f"Found {len(records)} records")
```

## Handling Different Encodings

Text files can be encoded in various ways. Python defaults to UTF-8, but you might encounter files with different encodings. Proper encoding handling prevents errors and data corruption.

```python
# Reading UTF-8 file (default)
with open('unicode.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    print(content)

# Reading file with different encoding
with open('latin1.txt', 'r', encoding='latin-1') as file:
    content = file.read()
    print(content)

# Handling encoding errors
with open('mixed_encoding.txt', 'r', encoding='utf-8', errors='ignore') as file:
    content = file.read()
    print("Invalid characters ignored")

# Using errors='replace'
with open('problematic.txt', 'r', encoding='utf-8', errors='replace') as file:
    content = file.read()
    print("Invalid characters replaced with �")

# Detecting encoding (requires chardet library)
def safe_read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Fallback to latin-1
        with open(filename, 'r', encoding='latin-1') as file:
            return file.read()

content = safe_read_file('unknown_encoding.txt')
print(f"Successfully read {len(content)} characters")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Read and Count Words"
    difficulty: basic
    description: "Read a file and count the total number of words in it."
    starter_code: |
      # Simulate file content
      content = "Hello world\nThis is a test file\nPython is great"

      # Count total words

    expected_output: |
      Total words: 9
    hints:
      - "Use split() to separate words"
      - "Count words in each line"
      - "Sum up the counts"
    solution: |
      content = "Hello world\nThis is a test file\nPython is great"

      words = content.split()
      print(f"Total words: {len(words)}")

  - title: "Read First N Lines"
    difficulty: basic
    description: "Read and print the first 3 lines from a simulated file content."
    starter_code: |
      # Simulate file content
      lines = ["Line 1\n", "Line 2\n", "Line 3\n", "Line 4\n", "Line 5\n"]

      # Print first 3 lines

    expected_output: |
      Line 1
      Line 2
      Line 3
    hints:
      - "Use list slicing [:3]"
      - "Remember to strip newline characters"
    solution: |
      lines = ["Line 1\n", "Line 2\n", "Line 3\n", "Line 4\n", "Line 5\n"]

      for line in lines[:3]:
          print(line.strip())

  - title: "Search for Keyword"
    difficulty: intermediate
    description: "Read through simulated file content and find all lines containing a specific keyword."
    starter_code: |
      # Simulate log file content
      logs = [
          "INFO: Application started\n",
          "ERROR: Connection failed\n",
          "INFO: Processing data\n",
          "ERROR: File not found\n",
          "INFO: Task completed\n"
      ]

      # Find all lines with 'ERROR' and print with line numbers

    expected_output: |
      Line 2: ERROR: Connection failed
      Line 4: ERROR: File not found
      Found 2 error lines
    hints:
      - "Use enumerate() to get line numbers"
      - "Check if 'ERROR' is in the line"
      - "Keep a counter for matches"
    solution: |
      logs = [
          "INFO: Application started\n",
          "ERROR: Connection failed\n",
          "INFO: Processing data\n",
          "ERROR: File not found\n",
          "INFO: Task completed\n"
      ]

      error_count = 0
      for line_num, line in enumerate(logs, 1):
          if 'ERROR' in line:
              print(f"Line {line_num}: {line.strip()}")
              error_count += 1

      print(f"Found {error_count} error lines")

  - title: "Parse Configuration File"
    difficulty: intermediate
    description: "Parse a simulated configuration file with key=value pairs and return a dictionary."
    starter_code: |
      # Simulate config file content
      config_lines = [
          "host=localhost\n",
          "port=8080\n",
          "# This is a comment\n",
          "debug=true\n",
          "timeout=30\n"
      ]

      # Parse into dictionary, skip comments

    expected_output: |
      {'host': 'localhost', 'port': '8080', 'debug': 'true', 'timeout': '30'}
    hints:
      - "Skip lines starting with #"
      - "Split each line by '='"
      - "Strip whitespace from keys and values"
    solution: |
      config_lines = [
          "host=localhost\n",
          "port=8080\n",
          "# This is a comment\n",
          "debug=true\n",
          "timeout=30\n"
      ]

      config = {}
      for line in config_lines:
          line = line.strip()
          if line and not line.startswith('#'):
              key, value = line.split('=')
              config[key.strip()] = value.strip()

      print(config)

  - title: "Calculate Statistics from Data"
    difficulty: advanced
    description: "Read simulated CSV-like data and calculate statistics (min, max, average)."
    starter_code: |
      # Simulate CSV data: name,score
      data_lines = [
          "name,score\n",
          "Alice,85\n",
          "Bob,92\n",
          "Charlie,78\n",
          "Diana,95\n",
          "Eve,88\n"
      ]

      # Calculate min, max, average scores

    expected_output: |
      Minimum score: 78
      Maximum score: 95
      Average score: 87.60
      Total students: 5
    hints:
      - "Skip the header line"
      - "Split each line by comma"
      - "Extract the score and convert to int"
      - "Use min(), max(), and sum() functions"
    solution: |
      data_lines = [
          "name,score\n",
          "Alice,85\n",
          "Bob,92\n",
          "Charlie,78\n",
          "Diana,95\n",
          "Eve,88\n"
      ]

      scores = []
      for line in data_lines[1:]:  # Skip header
          parts = line.strip().split(',')
          score = int(parts[1])
          scores.append(score)

      print(f"Minimum score: {min(scores)}")
      print(f"Maximum score: {max(scores)}")
      print(f"Average score: {sum(scores) / len(scores):.2f}")
      print(f"Total students: {len(scores)}")

  - title: "Read File in Chunks with Generator"
    difficulty: advanced
    description: "Create a generator function that yields chunks of text from simulated file content."
    starter_code: |
      def read_chunks(content, chunk_size=10):
          # Yield chunks of specified size from content
          # Use a generator
          pass

      # Test with sample content
      text = "This is a long piece of text that needs to be processed in chunks."

    expected_output: |
      Chunk 1: This is a
      Chunk 2: long piece
      Chunk 3:  of text t
      Chunk 4: hat needs
      Chunk 5: to be proc
      Chunk 6: essed in c
      Chunk 7: hunks.
    hints:
      - "Use a while loop with an index"
      - "Yield slices of the content"
      - "Stop when index exceeds content length"
    solution: |
      def read_chunks(content, chunk_size=10):
          index = 0
          while index < len(content):
              yield content[index:index + chunk_size]
              index += chunk_size

      text = "This is a long piece of text that needs to be processed in chunks."

      for i, chunk in enumerate(read_chunks(text, 10), 1):
          print(f"Chunk {i}: {chunk}")
```
<!-- EXERCISE_END -->
