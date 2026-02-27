# File Paths in Python

Working with file paths correctly is essential for writing portable, cross-platform Python applications. Python's `os.path` and `pathlib` modules provide robust tools for path manipulation.

## Path Basics

File paths differ across operating systems:

```python
# Windows uses backslashes
# C:\Users\alice\documents\file.txt

# Linux/Mac use forward slashes
# /home/alice/documents/file.txt

# Python can handle both, but pathlib is preferred
from pathlib import Path

# Create a path object
p = Path("documents/data/file.txt")
print(p)  # documents/data/file.txt (uses OS-appropriate separator)
```

## The pathlib Module (Modern Approach)

`pathlib` provides an object-oriented interface for filesystem paths:

```python
from pathlib import Path

# Current directory
cwd = Path.cwd()
print(f"Current dir: {cwd}")

# Home directory
home = Path.home()
print(f"Home dir: {home}")

# Building paths with / operator
project = Path.home() / "projects" / "myapp"
config = project / "config" / "settings.json"
print(config)

# Path components
p = Path("/home/alice/documents/report.pdf")
print(p.name)      # report.pdf
print(p.stem)      # report
print(p.suffix)    # .pdf
print(p.parent)    # /home/alice/documents
print(p.parts)     # ('/', 'home', 'alice', 'documents', 'report.pdf')

# Change extension
new_path = p.with_suffix(".txt")
print(new_path)    # /home/alice/documents/report.txt

# Change filename
renamed = p.with_name("summary.pdf")
print(renamed)     # /home/alice/documents/summary.pdf
```

## The os.path Module (Traditional Approach)

```python
import os.path

# Join paths (OS-aware)
path = os.path.join("home", "alice", "file.txt")
print(path)

# Split path into directory and filename
dirname, filename = os.path.split("/home/alice/file.txt")
print(f"Dir: {dirname}, File: {filename}")

# Get file extension
name, ext = os.path.splitext("report.pdf")
print(f"Name: {name}, Extension: {ext}")

# Absolute path
abs_path = os.path.abspath("relative/path.txt")
print(abs_path)

# Check path properties
print(os.path.exists("/tmp"))         # True/False
print(os.path.isfile("script.py"))    # True/False
print(os.path.isdir("/tmp"))          # True/False
print(os.path.getsize("file.txt"))    # File size in bytes
```

## Path Checking and Validation

```python
from pathlib import Path

p = Path("some/path/file.txt")

# Existence checks
print(p.exists())       # Does the path exist?
print(p.is_file())      # Is it a file?
print(p.is_dir())       # Is it a directory?
print(p.is_absolute())  # Is it an absolute path?

# Resolve to absolute path
absolute = p.resolve()
print(absolute)

# Relative paths
base = Path("/home/alice")
full = Path("/home/alice/projects/app/main.py")
relative = full.relative_to(base)
print(relative)  # projects/app/main.py
```

## Directory Operations

```python
from pathlib import Path

# List directory contents
p = Path(".")
for item in p.iterdir():
    kind = "DIR" if item.is_dir() else "FILE"
    print(f"  {kind}: {item.name}")

# Find files by pattern (glob)
for py_file in p.glob("*.py"):
    print(f"Python file: {py_file}")

# Recursive glob
for py_file in p.rglob("*.py"):
    print(f"Found: {py_file}")

# Create directories
new_dir = Path("output/reports/2024")
new_dir.mkdir(parents=True, exist_ok=True)

# Create a file
new_file = new_dir / "report.txt"
new_file.write_text("Hello, World!")
content = new_file.read_text()
print(content)
```

## Cross-Platform Path Handling

```python
from pathlib import Path, PurePosixPath, PureWindowsPath

# PurePath for manipulation without filesystem access
posix = PurePosixPath("/home/alice/file.txt")
windows = PureWindowsPath(r"C:\Users\alice\file.txt")

# Always use Path or os.path.join for portability
# BAD: path = "folder" + "/" + "file.txt"
# GOOD:
path = Path("folder") / "file.txt"

# Normalize paths
import os.path
messy = "folder//subfolder/../subfolder/./file.txt"
clean = os.path.normpath(messy)
print(clean)  # folder/subfolder/file.txt
```

## Best Practices

1. **Use `pathlib.Path`** for new code - it's more readable and Pythonic
2. **Never hardcode path separators** - use `Path` or `os.path.join()`
3. **Use `exist_ok=True`** with `mkdir()` to avoid errors on existing directories
4. **Resolve relative paths** before comparing them
5. **Use `.rglob()`** for recursive file searches instead of manual recursion

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Path Components"
    difficulty: basic
    description: "Extract and print the filename and extension from the path '/home/user/report.pdf' using pathlib."
    starter_code: |
      from pathlib import Path
      p = Path("/home/user/report.pdf")
      # Print the filename and extension

    expected_output: |
      report.pdf
      .pdf
    hints:
      - "Use .name for the full filename"
      - "Use .suffix for the extension"
    solution: |
      from pathlib import Path
      p = Path("/home/user/report.pdf")
      print(p.name)
      print(p.suffix)

  - title: "Join Paths"
    difficulty: basic
    description: "Build a path from 'home', 'alice', 'documents', 'file.txt' using pathlib and print it."
    starter_code: |
      from pathlib import Path
      # Build the path using / operator

    expected_output: "home/alice/documents/file.txt"
    hints:
      - "Start with Path('home')"
      - "Use the / operator to join parts"
    solution: |
      from pathlib import Path
      p = Path("home") / "alice" / "documents" / "file.txt"
      print(p.as_posix())

  - title: "Change Extension"
    difficulty: intermediate
    description: "Change the extension of 'data/results.csv' to '.json' and print both the original and new path."
    starter_code: |
      from pathlib import Path
      original = Path("data/results.csv")
      # Change extension to .json

    expected_output: |
      data/results.csv
      data/results.json
    hints:
      - "Use .with_suffix() to change the extension"
      - "This returns a new Path object"
    solution: |
      from pathlib import Path
      original = Path("data/results.csv")
      new_path = original.with_suffix(".json")
      print(original.as_posix())
      print(new_path.as_posix())

  - title: "Path Parent Chain"
    difficulty: intermediate
    description: "Print all parent directories of '/home/alice/projects/app/main.py', one per line."
    starter_code: |
      from pathlib import Path
      p = Path("/home/alice/projects/app/main.py")
      # Print all parents

    expected_output: |
      /home/alice/projects/app
      /home/alice/projects
      /home/alice
      /home
      /
    hints:
      - "Use the .parents property which gives all ancestors"
      - "Or use a loop with .parent"
    solution: |
      from pathlib import Path
      p = Path("/home/alice/projects/app/main.py")
      for parent in p.parents:
          print(parent.as_posix())

  - title: "File Organizer Logic"
    difficulty: advanced
    description: "Given a list of filenames, group them by extension and print the result as a dictionary."
    starter_code: |
      from pathlib import Path
      files = ["report.pdf", "data.csv", "notes.txt", "image.pdf", "log.txt", "stats.csv"]
      # Group by extension

    expected_output: "{'.pdf': ['report.pdf', 'image.pdf'], '.csv': ['data.csv', 'stats.csv'], '.txt': ['notes.txt', 'log.txt']}"
    hints:
      - "Use Path(f).suffix to get each file's extension"
      - "Build a dictionary mapping extensions to lists of filenames"
    solution: |
      from pathlib import Path
      files = ["report.pdf", "data.csv", "notes.txt", "image.pdf", "log.txt", "stats.csv"]
      groups = {}
      for f in files:
          ext = Path(f).suffix
          groups.setdefault(ext, []).append(f)
      print(groups)

  - title: "Relative Path Calculator"
    difficulty: advanced
    description: "Calculate and print the relative path from '/home/alice/projects' to '/home/alice/projects/webapp/src/main.py'."
    starter_code: |
      from pathlib import Path
      base = Path("/home/alice/projects")
      target = Path("/home/alice/projects/webapp/src/main.py")
      # Calculate relative path

    expected_output: "webapp/src/main.py"
    hints:
      - "Use .relative_to() method on the target path"
      - "Pass the base path as the argument"
    solution: |
      from pathlib import Path
      base = Path("/home/alice/projects")
      target = Path("/home/alice/projects/webapp/src/main.py")
      relative = target.relative_to(base)
      print(relative.as_posix())
```
<!-- EXERCISE_END -->
