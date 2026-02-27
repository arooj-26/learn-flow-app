# File Modes

Understanding file modes is crucial for effective file handling in Python. The mode parameter in the `open()` function determines how the file can be accessed and whether it operates in text or binary mode. Choosing the correct mode prevents data loss and ensures your program behaves as expected.

## Basic File Modes

Python supports several file access modes that control whether you can read, write, or both. Each mode has specific behaviors regarding file creation and content preservation.

```python
# Read mode ('r') - default mode
try:
    with open('existing.txt', 'r') as file:
        content = file.read()
        print(f"Read {len(content)} characters")
except FileNotFoundError:
    print("File must exist for read mode")

# Write mode ('w') - creates or overwrites
with open('output.txt', 'w') as file:
    file.write('New content\n')
    print("File created or overwritten")

# Append mode ('a') - creates or appends
with open('log.txt', 'a') as file:
    file.write('New log entry\n')
    print("Content appended")

# Exclusive creation mode ('x')
try:
    with open('unique.txt', 'x') as file:
        file.write('Only created if new\n')
        print("New file created")
except FileExistsError:
    print("File already exists, cannot use 'x' mode")
```

## Text vs Binary Modes

Files can be opened in either text mode (for human-readable text) or binary mode (for any type of data). The mode suffix determines which type is used.

```python
# Text mode (default) - adds 't' or omit
with open('text_file.txt', 'rt') as file:  # or just 'r'
    text_data = file.read()
    print(f"Type: {type(text_data)}")  # str
    print(f"Content: {text_data}")

# Binary mode - adds 'b'
with open('binary_file.bin', 'rb') as file:
    binary_data = file.read()
    print(f"Type: {type(binary_data)}")  # bytes
    print(f"First bytes: {binary_data[:10]}")

# Writing text vs binary
text = "Hello, World!"
binary = text.encode('utf-8')

with open('text.txt', 'w') as file:
    file.write(text)

with open('binary.bin', 'wb') as file:
    file.write(binary)

# Binary mode for images
with open('image.png', 'rb') as file:
    image_data = file.read()
    print(f"Image size: {len(image_data)} bytes")
    print(f"PNG header: {image_data[:8]}")
```

## Combined Read and Write Modes

Some modes allow both reading and writing to the same file. Understanding the difference between them is important for correct file manipulation.

| Mode | Read | Write | Create | Truncate | Position |
|------|------|-------|--------|----------|----------|
| `r+` | Yes | Yes | No | No | Start |
| `w+` | Yes | Yes | Yes | Yes | Start |
| `a+` | Yes | Yes | Yes | No | End |

```python
# Read and write mode ('r+')
with open('data.txt', 'r+') as file:
    # Read existing content
    content = file.read()
    print(f"Original: {content}")

    # Write at current position (end)
    file.write('\nNew line added')

    # Read again from start
    file.seek(0)
    updated = file.read()
    print(f"Updated: {updated}")

# Write and read mode ('w+')
with open('temp.txt', 'w+') as file:
    # File is truncated (emptied)
    file.write('First line\n')
    file.write('Second line\n')

    # Go back to read
    file.seek(0)
    content = file.read()
    print(f"Content: {content}")

# Append and read mode ('a+')
with open('append_read.txt', 'a+') as file:
    # Position starts at end
    file.write('Appended line\n')

    # Need to seek to beginning to read
    file.seek(0)
    all_content = file.read()
    print(f"All content: {all_content}")

# Practical example: Update specific line
def update_line(filename, line_num, new_text):
    with open(filename, 'r+') as file:
        lines = file.readlines()
        if 0 <= line_num < len(lines):
            lines[line_num] = new_text + '\n'
            file.seek(0)
            file.writelines(lines)
            file.truncate()  # Remove extra content
            return True
    return False

update_line('data.txt', 2, 'Updated third line')
```

## Complete Mode Reference

Understanding all available modes and their combinations helps you choose the right one for any situation.

```python
# Demonstration of all modes
modes_info = {
    'r': 'Read only (text), file must exist',
    'rb': 'Read only (binary), file must exist',
    'r+': 'Read and write (text), file must exist',
    'rb+': 'Read and write (binary), file must exist',

    'w': 'Write only (text), creates or truncates',
    'wb': 'Write only (binary), creates or truncates',
    'w+': 'Read and write (text), creates or truncates',
    'wb+': 'Read and write (binary), creates or truncates',

    'a': 'Append (text), creates if needed',
    'ab': 'Append (binary), creates if needed',
    'a+': 'Append and read (text), creates if needed',
    'ab+': 'Append and read (binary), creates if needed',

    'x': 'Exclusive create (text), fails if exists',
    'xb': 'Exclusive create (binary), fails if exists',
    'x+': 'Exclusive create, read/write (text)',
    'xb+': 'Exclusive create, read/write (binary)'
}

for mode, description in modes_info.items():
    print(f"{mode:4} - {description}")

# Testing mode capabilities
def test_mode(mode, filename='test.txt'):
    try:
        with open(filename, mode) as file:
            print(f"\nMode: {mode}")
            print(f"Readable: {file.readable()}")
            print(f"Writable: {file.writable()}")
            print(f"Position: {file.tell()}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Mode {mode} error: {e}")

# Test different modes
for mode in ['r', 'w', 'a', 'r+', 'w+', 'a+']:
    test_mode(mode)
```

## Practical Mode Selection

Choosing the right mode depends on your specific use case. Here are common scenarios and the appropriate modes to use.

```python
# Scenario 1: Reading configuration file
def read_config(filename):
    with open(filename, 'r') as file:
        return file.read()

# Scenario 2: Writing report (overwrite if exists)
def write_report(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

# Scenario 3: Appending to log file
def append_log(filename, message):
    with open(filename, 'a') as file:
        file.write(f"{message}\n")

# Scenario 4: Creating new database file (must not exist)
def create_database(filename):
    try:
        with open(filename, 'x') as file:
            file.write("# Database initialized\n")
        return True
    except FileExistsError:
        return False

# Scenario 5: Updating existing file in place
def update_file(filename, old_text, new_text):
    with open(filename, 'r+') as file:
        content = file.read()
        content = content.replace(old_text, new_text)
        file.seek(0)
        file.write(content)
        file.truncate()

# Scenario 6: Processing binary file (images, etc.)
def process_image(input_file, output_file):
    with open(input_file, 'rb') as infile:
        data = infile.read()
        # Process data here
        processed_data = data  # placeholder

    with open(output_file, 'wb') as outfile:
        outfile.write(processed_data)

# Scenario 7: Read and append (check then add)
def conditional_append(filename, data):
    with open(filename, 'a+') as file:
        file.seek(0)
        content = file.read()
        if data not in content:
            file.write(f"{data}\n")
            return True
    return False
```

## Mode Behavior with File Position

Different modes position the file pointer differently. Understanding this prevents unexpected behavior when reading and writing.

```python
# Mode 'r+' - position at start
with open('test.txt', 'r+') as file:
    print(f"Initial position: {file.tell()}")  # 0
    file.write('OVERWRITE')
    print(f"After write: {file.tell()}")

    file.seek(0)
    print(f"Content: {file.read()}")

# Mode 'w+' - truncates and position at start
with open('test.txt', 'w+') as file:
    print(f"Initial position: {file.tell()}")  # 0 (file empty)
    file.write('New content')

    file.seek(0)
    print(f"Content: {file.read()}")

# Mode 'a+' - position at end
with open('test.txt', 'a+') as file:
    print(f"Initial position: {file.tell()}")  # at end
    file.write(' appended')

    file.seek(0)  # Must seek to read from start
    print(f"Content: {file.read()}")

# Demonstrating position behavior
def demonstrate_position(mode, initial_content='12345'):
    # Setup: create file with initial content
    with open('demo.txt', 'w') as f:
        f.write(initial_content)

    # Test mode
    with open('demo.txt', mode) as file:
        pos = file.tell()
        print(f"Mode {mode}: initial position = {pos}")

        if file.readable():
            file.seek(0)
            content = file.read(10)
            print(f"  Content: {content}")

for mode in ['r', 'r+', 'w+', 'a', 'a+']:
    demonstrate_position(mode)
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Identify Correct Mode"
    difficulty: basic
    description: "Given different scenarios, print the correct file mode to use."
    starter_code: |
      # Print the correct mode for each scenario
      scenarios = [
          "Read an existing text file",
          "Create a new file and write to it",
          "Add entries to an existing log file"
      ]

      # Print mode for each scenario

    expected_output: |
      Read an existing text file: r
      Create a new file and write to it: w
      Add entries to an existing log file: a
    hints:
      - "r for reading existing files"
      - "w for writing/creating files"
      - "a for appending to files"
    solution: |
      scenarios = [
          "Read an existing text file",
          "Create a new file and write to it",
          "Add entries to an existing log file"
      ]

      modes = ['r', 'w', 'a']

      for scenario, mode in zip(scenarios, modes):
          print(f"{scenario}: {mode}")

  - title: "Text vs Binary Mode"
    difficulty: basic
    description: "Determine whether to use text or binary mode for different file types."
    starter_code: |
      files = [
          ('document.txt', 'text'),
          ('image.png', 'binary'),
          ('data.json', 'text'),
          ('video.mp4', 'binary')
      ]

      # Print correct mode (rt or rb) for each file

    expected_output: |
      document.txt: rt
      image.png: rb
      data.json: rt
      video.mp4: rb
    hints:
      - "Text files use 'rt' or 'r'"
      - "Binary files (images, videos) use 'rb'"
    solution: |
      files = [
          ('document.txt', 'text'),
          ('image.png', 'binary'),
          ('data.json', 'text'),
          ('video.mp4', 'binary')
      ]

      for filename, file_type in files:
          mode = 'rt' if file_type == 'text' else 'rb'
          print(f"{filename}: {mode}")

  - title: "Mode Capability Checker"
    difficulty: intermediate
    description: "Create a function that returns the capabilities of a given file mode."
    starter_code: |
      def check_mode_capabilities(mode):
          # Return dict with readable, writable, creates_file, truncates
          pass

      # Test with modes: 'r', 'w', 'a', 'r+'

    expected_output: |
      r: readable=True, writable=False, creates=False, truncates=False
      w: readable=False, writable=True, creates=True, truncates=True
      a: readable=False, writable=True, creates=True, truncates=False
      r+: readable=True, writable=True, creates=False, truncates=False
    hints:
      - "Check what each mode allows"
      - "r only reads, w creates and overwrites, a appends"
      - "r+ allows both read and write"
    solution: |
      def check_mode_capabilities(mode):
          capabilities = {
              'r': {'readable': True, 'writable': False, 'creates': False, 'truncates': False},
              'w': {'readable': False, 'writable': True, 'creates': True, 'truncates': True},
              'a': {'readable': False, 'writable': True, 'creates': True, 'truncates': False},
              'r+': {'readable': True, 'writable': True, 'creates': False, 'truncates': False}
          }
          return capabilities.get(mode, {})

      for mode in ['r', 'w', 'a', 'r+']:
          caps = check_mode_capabilities(mode)
          print(f"{mode}: readable={caps['readable']}, writable={caps['writable']}, creates={caps['creates']}, truncates={caps['truncates']}")

  - title: "Choose Mode for Task"
    difficulty: intermediate
    description: "Create a function that recommends the best file mode for a given task description."
    starter_code: |
      def recommend_mode(task):
          # Return recommended mode based on task
          pass

      tasks = [
          "read configuration",
          "write new report",
          "add log entry",
          "update existing data"
      ]

    expected_output: |
      read configuration: r
      write new report: w
      add log entry: a
      update existing data: r+
    hints:
      - "Reading only needs 'r'"
      - "Writing new file needs 'w'"
      - "Adding to file needs 'a'"
      - "Updating needs 'r+'"
    solution: |
      def recommend_mode(task):
          if 'read' in task.lower():
              return 'r'
          elif 'write new' in task.lower() or 'write' in task.lower():
              return 'w'
          elif 'add' in task.lower() or 'append' in task.lower():
              return 'a'
          elif 'update' in task.lower():
              return 'r+'
          return 'r'

      tasks = [
          "read configuration",
          "write new report",
          "add log entry",
          "update existing data"
      ]

      for task in tasks:
          mode = recommend_mode(task)
          print(f"{task}: {mode}")

  - title: "Mode Behavior Simulator"
    difficulty: advanced
    description: "Simulate the behavior of different file modes on a virtual file system."
    starter_code: |
      class VirtualFile:
          def __init__(self):
              self.content = "original content"
              self.exists = True

          def simulate_mode(self, mode):
              # Simulate what happens with this mode
              # Return status message
              pass

      vfile = VirtualFile()

    expected_output: |
      Mode r: Can read, position=0, content='original content'
      Mode w: Truncated, can write, content=''
      Mode a: Can append, position=16, content='original content'
      Mode r+: Can read/write, position=0, content='original content'
    hints:
      - "r mode: read only, position at start"
      - "w mode: truncates file"
      - "a mode: position at end"
      - "r+ mode: read/write, position at start"
    solution: |
      class VirtualFile:
          def __init__(self):
              self.content = "original content"
              self.exists = True

          def simulate_mode(self, mode):
              if mode == 'r':
                  return f"Can read, position=0, content='{self.content}'"
              elif mode == 'w':
                  return f"Truncated, can write, content=''"
              elif mode == 'a':
                  pos = len(self.content)
                  return f"Can append, position={pos}, content='{self.content}'"
              elif mode == 'r+':
                  return f"Can read/write, position=0, content='{self.content}'"

      vfile = VirtualFile()

      for mode in ['r', 'w', 'a', 'r+']:
          result = vfile.simulate_mode(mode)
          print(f"Mode {mode}: {result}")

  - title: "Safe Mode Selector"
    difficulty: advanced
    description: "Create a function that selects the safest file mode based on requirements and file existence."
    starter_code: |
      def safe_mode_selector(file_exists, need_read, need_write, preserve_content):
          # Return safest mode based on parameters
          # Consider all safety implications
          pass

      scenarios = [
          (True, True, False, True),   # exists, read only, preserve
          (False, False, True, False), # new file, write only
          (True, True, True, True),    # exists, read/write, preserve
          (False, True, True, False)   # new file, read/write
      ]

    expected_output: |
      Scenario (True, True, False, True): r
      Scenario (False, False, True, False): w
      Scenario (True, True, True, True): r+
      Scenario (False, True, True, False): w+
    hints:
      - "If read only and file exists: use 'r'"
      - "If write only and don't preserve: use 'w'"
      - "If read/write and preserve: use 'r+'"
      - "If read/write and new file: use 'w+'"
    solution: |
      def safe_mode_selector(file_exists, need_read, need_write, preserve_content):
          if need_read and not need_write:
              return 'r' if file_exists else None
          elif need_write and not need_read:
              return 'w'
          elif need_read and need_write:
              if preserve_content and file_exists:
                  return 'r+'
              else:
                  return 'w+'
          return 'r'

      scenarios = [
          (True, True, False, True),
          (False, False, True, False),
          (True, True, True, True),
          (False, True, True, False)
      ]

      for scenario in scenarios:
          mode = safe_mode_selector(*scenario)
          print(f"Scenario {scenario}: {mode}")
```
<!-- EXERCISE_END -->
