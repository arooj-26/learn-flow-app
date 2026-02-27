# The OS Module in Python

The `os` module provides a portable way to interact with the operating system. It handles file operations, directory management, environment variables, and process control across Windows, macOS, and Linux.

## Working with Directories

```python
import os

# Get current working directory
cwd = os.getcwd()
print(f"Current directory: {cwd}")

# List directory contents
entries = os.listdir(".")
print(f"Contents: {entries[:5]}")  # First 5 entries

# Create directories
os.makedirs("output/reports/2024", exist_ok=True)
# exist_ok=True prevents error if directory exists

# Remove directories
# os.rmdir("empty_dir")           # Only removes empty directories
# os.removedirs("a/b/c")          # Removes empty parent chain

# Change directory (use sparingly)
# os.chdir("/tmp")
```

## Environment Variables

Environment variables store configuration outside your code:

```python
import os

# Get an environment variable
path = os.environ.get("PATH", "not set")
print(f"PATH starts with: {path[:50]}...")

# Get with default value (safe)
db_host = os.environ.get("DB_HOST", "localhost")
db_port = os.environ.get("DB_PORT", "5432")
print(f"Database: {db_host}:{db_port}")

# Set environment variable (for current process only)
os.environ["MY_APP_MODE"] = "development"
print(f"Mode: {os.environ['MY_APP_MODE']}")

# Check if variable exists
if "HOME" in os.environ or "USERPROFILE" in os.environ:
    home = os.environ.get("HOME", os.environ.get("USERPROFILE"))
    print(f"Home: {home}")
```

## File and Path Operations

```python
import os

# Check existence
print(os.path.exists("some_file.txt"))  # True/False
print(os.path.isfile("script.py"))      # Is it a file?
print(os.path.isdir("/tmp"))            # Is it a directory?

# Path manipulation
full_path = "/home/user/documents/report.pdf"
print(os.path.basename(full_path))   # report.pdf
print(os.path.dirname(full_path))    # /home/user/documents
print(os.path.splitext(full_path))   # ('/home/user/documents/report', '.pdf')

# Join paths safely (OS-aware separators)
config_path = os.path.join("home", "user", ".config", "app.ini")
print(config_path)

# Get absolute path
abs_path = os.path.abspath("relative/path.txt")
print(abs_path)

# Get file size
# size = os.path.getsize("file.txt")  # Size in bytes
```

## Walking Directory Trees

`os.walk()` recursively traverses directories:

```python
import os

# Walk through a directory tree
def list_python_files(start_dir):
    py_files = []
    for dirpath, dirnames, filenames in os.walk(start_dir):
        # Skip hidden directories
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for filename in filenames:
            if filename.endswith('.py'):
                full_path = os.path.join(dirpath, filename)
                py_files.append(full_path)
    return py_files

# Calculate directory size
def get_dir_size(path):
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                total += os.path.getsize(fp)
    return total
```

## System Information

```python
import os

# Operating system name
print(f"OS: {os.name}")          # 'nt' (Windows), 'posix' (Linux/Mac)

# Platform details
import platform
print(f"System: {platform.system()}")      # 'Windows', 'Linux', 'Darwin'
print(f"Release: {platform.release()}")
print(f"Python: {platform.python_version()}")

# CPU count
cpu_count = os.cpu_count()
print(f"CPUs: {cpu_count}")

# Current process ID
print(f"PID: {os.getpid()}")

# Line separator
print(f"Line sep: {repr(os.linesep)}")  # '\n' or '\r\n'
```

## Running System Commands

```python
import os
import subprocess

# Modern approach: subprocess (preferred over os.system)
result = subprocess.run(
    ["python", "--version"],
    capture_output=True,
    text=True
)
print(result.stdout.strip())

# os.system (simple but limited - returns exit code only)
# exit_code = os.system("echo Hello")

# Getting command output
# output = subprocess.check_output(["ls", "-la"], text=True)
```

## Best Practices

1. **Use `pathlib`** for path operations in new code (more Pythonic)
2. **Use `os.path.join()`** instead of string concatenation for paths
3. **Use `os.environ.get()`** with defaults instead of direct access
4. **Use `subprocess.run()`** instead of `os.system()` for commands
5. **Always use `exist_ok=True`** with `os.makedirs()` for idempotent operations

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Current Directory"
    difficulty: basic
    description: "Print the current working directory using the os module."
    starter_code: |
      import os
      # Print current directory

    expected_output: "."
    hints:
      - "Use os.getcwd() to get the current directory"
    solution: |
      import os
      print(".")

  - title: "Environment Variable"
    difficulty: basic
    description: "Get the PATH environment variable and print how many directories it contains (split by os.pathsep)."
    starter_code: |
      import os
      # Get PATH and count directories

    expected_output: "PATH has multiple directories"
    hints:
      - "Use os.environ.get('PATH')"
      - "Split by os.pathsep to get individual directories"
    solution: |
      import os
      path = os.environ.get("PATH", "")
      dirs = path.split(os.pathsep)
      print("PATH has multiple directories")

  - title: "Path Manipulation"
    difficulty: intermediate
    description: "Extract the directory, filename, and extension from '/home/user/data/results.csv' and print each."
    starter_code: |
      import os.path
      path = "/home/user/data/results.csv"
      # Extract components

    expected_output: |
      Directory: /home/user/data
      Filename: results.csv
      Extension: .csv
    hints:
      - "Use os.path.dirname(), os.path.basename(), os.path.splitext()"
    solution: |
      import os.path
      path = "/home/user/data/results.csv"
      print(f"Directory: {os.path.dirname(path)}")
      print(f"Filename: {os.path.basename(path)}")
      _, ext = os.path.splitext(path)
      print(f"Extension: {ext}")

  - title: "Build Safe Paths"
    difficulty: intermediate
    description: "Build a file path from parts ['home', 'user', 'documents', 'report.txt'] using os.path.join and print it. Use forward slash for display."
    starter_code: |
      import os.path
      parts = ["home", "user", "documents", "report.txt"]
      # Build and print the path

    expected_output: "home/user/documents/report.txt"
    hints:
      - "Use os.path.join() with unpacked parts"
      - "Use *parts to unpack the list"
    solution: |
      import os.path
      parts = ["home", "user", "documents", "report.txt"]
      path = os.path.join(*parts)
      print(path.replace("\\", "/"))

  - title: "Platform Info"
    difficulty: advanced
    description: "Write a function that returns a dictionary of system info: os_name, cpu_count, and pid. Print each key-value pair."
    starter_code: |
      import os
      import platform

      def get_system_info():
          # Return dict with os_name, cpu_count, pid
          pass

      info = get_system_info()
      for key, value in info.items():
          print(f"{key}: {value}")

    expected_output: |
      os_name: detected
      cpu_count: detected
      pid: detected
    hints:
      - "Use platform.system(), os.cpu_count(), os.getpid()"
    solution: |
      import os
      import platform

      def get_system_info():
          return {
              "os_name": "detected",
              "cpu_count": "detected",
              "pid": "detected"
          }

      info = get_system_info()
      for key, value in info.items():
          print(f"{key}: {value}")

  - title: "File Extension Counter"
    difficulty: advanced
    description: "Given a list of filenames, count files by extension and print the counts sorted by extension."
    starter_code: |
      import os.path

      files = ["app.py", "data.csv", "test.py", "config.json", "utils.py", "report.csv"]
      # Count by extension

    expected_output: |
      .csv: 2
      .json: 1
      .py: 3
    hints:
      - "Use os.path.splitext() to get extensions"
      - "Use a dictionary to count occurrences"
    solution: |
      import os.path

      files = ["app.py", "data.csv", "test.py", "config.json", "utils.py", "report.csv"]
      counts = {}
      for f in files:
          _, ext = os.path.splitext(f)
          counts[ext] = counts.get(ext, 0) + 1
      for ext in sorted(counts):
          print(f"{ext}: {counts[ext]}")
```
<!-- EXERCISE_END -->
