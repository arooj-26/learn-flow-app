# pip & Packages in Python

pip is Python's package installer, allowing you to install and manage third-party libraries from the Python Package Index (PyPI). Understanding pip is essential for leveraging Python's vast ecosystem of over 400,000 packages.

## What is pip?

pip stands for "pip installs packages." It comes bundled with Python 3.4+ and connects to PyPI (pypi.org):

```python
# Check pip version (run in terminal)
# pip --version
# pip 23.0 from /usr/lib/python3.11/site-packages/pip (python 3.11)

# If pip isn't available, install it:
# python -m ensurepip --upgrade
```

## Installing Packages

```python
# Basic installation (terminal commands)
# pip install requests
# pip install flask
# pip install numpy pandas matplotlib

# Install specific version
# pip install requests==2.28.0
# pip install "requests>=2.25,<3.0"

# Install from requirements file
# pip install -r requirements.txt

# Upgrade a package
# pip install --upgrade requests

# Install in user space (no admin needed)
# pip install --user package_name
```

## Using Installed Packages

```python
# After pip install requests
import requests

# Make an HTTP request
# response = requests.get("https://api.example.com/data")
# print(response.status_code)

# After pip install python-dateutil
from dateutil import parser
date = parser.parse("January 15, 2024 3:30 PM")
print(f"Parsed date: {date}")

# Popular packages and their uses
packages = {
    "requests": "HTTP requests made simple",
    "flask": "Lightweight web framework",
    "pandas": "Data analysis and manipulation",
    "numpy": "Numerical computing",
    "pytest": "Testing framework",
    "black": "Code formatter",
    "pillow": "Image processing",
    "sqlalchemy": "Database toolkit"
}

for pkg, desc in packages.items():
    print(f"  {pkg}: {desc}")
```

## Managing Packages

```python
# List installed packages (terminal commands)
# pip list
# pip list --outdated

# Show package details
# pip show requests
# Name: requests
# Version: 2.28.0
# Summary: Python HTTP for Humans.
# Requires: charset-normalizer, idna, urllib3, certifi

# Uninstall a package
# pip uninstall requests

# Freeze current environment (for reproducibility)
# pip freeze > requirements.txt
# This creates a file like:
# requests==2.28.0
# flask==2.3.0
# numpy==1.24.0
```

## requirements.txt

The standard way to specify project dependencies:

```python
# requirements.txt format:

# Exact version (most reproducible)
# requests==2.28.0

# Minimum version
# requests>=2.25.0

# Version range
# requests>=2.25.0,<3.0.0

# Latest version
# requests

# From git repository
# git+https://github.com/user/repo.git

# Example requirements.txt:
requirements = """
requests==2.31.0
flask>=2.3.0,<3.0
pandas>=2.0
python-dotenv>=1.0
pytest>=7.0
"""

print("Example requirements.txt:")
for line in requirements.strip().split("\n"):
    print(f"  {line.strip()}")
```

## Package Discovery

Finding the right package for your needs:

```python
# Search on PyPI: https://pypi.org
# Common categories:

categories = {
    "Web Frameworks": ["flask", "django", "fastapi"],
    "Data Science": ["pandas", "numpy", "scipy", "scikit-learn"],
    "HTTP Clients": ["requests", "httpx", "aiohttp"],
    "Testing": ["pytest", "unittest", "coverage"],
    "CLI Tools": ["click", "argparse", "typer"],
    "Databases": ["sqlalchemy", "pymongo", "redis"],
    "Async": ["asyncio", "aiohttp", "celery"],
    "DevOps": ["docker", "fabric", "ansible"]
}

for category, pkgs in categories.items():
    print(f"{category}: {', '.join(pkgs)}")
```

## Import Patterns for Packages

```python
# Different import styles
import json                      # Standard library
import requests                  # Third-party
from flask import Flask, jsonify # Specific imports
from pathlib import Path         # Submodule import
import numpy as np               # Import with alias

# Handling optional dependencies
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("pandas not installed - install with: pip install pandas")

# Check what's available
if HAS_PANDAS:
    print("pandas is available!")
else:
    print("Running without pandas")
```

## Best Practices

1. **Always use virtual environments** to isolate project dependencies
2. **Pin exact versions** in production (`==`) for reproducibility
3. **Use `requirements.txt`** to document all dependencies
4. **Separate dev dependencies** from production ones
5. **Regularly update** packages to get security fixes
6. **Check package health** on PyPI before installing (downloads, maintenance, etc.)

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Check Installed Packages"
    difficulty: basic
    description: "Use the pkg_resources module to check if 'json' (standard library) is importable and print the result."
    starter_code: |
      # Check if json module is available
      try:
          import json
          print(f"json is available: version info = {json.__name__}")
      except ImportError:
          print("json is not available")

    expected_output: "json is available: version info = json"
    hints:
      - "Standard library modules are always available"
      - "Use __name__ attribute to verify"
    solution: |
      try:
          import json
          print(f"json is available: version info = {json.__name__}")
      except ImportError:
          print("json is not available")

  - title: "Requirements Parser"
    difficulty: basic
    description: "Parse a requirements string and print each package name (without version specifiers)."
    starter_code: |
      requirements = """requests==2.31.0
      flask>=2.3.0
      pandas>=2.0,<3.0
      numpy"""

      # Print just the package names

    expected_output: |
      requests
      flask
      pandas
      numpy
    hints:
      - "Split by lines, then split each line on '>' or '='"
      - "Use a loop to process each requirement"
    solution: |
      requirements = """requests==2.31.0
      flask>=2.3.0
      pandas>=2.0,<3.0
      numpy"""

      for line in requirements.strip().split("\n"):
          line = line.strip()
          for sep in [">=", "==", "<", ">"]:
              line = line.split(sep)[0]
          print(line)

  - title: "Dependency Checker"
    difficulty: intermediate
    description: "Write a function that checks if modules are importable and prints the status of each."
    starter_code: |
      modules = ["json", "os", "sys", "fake_module_xyz"]

      def check_modules(module_list):
          # Check each module and print status
          pass

      check_modules(modules)

    expected_output: |
      json: available
      os: available
      sys: available
      fake_module_xyz: NOT available
    hints:
      - "Use importlib.import_module() or try/except with __import__"
      - "Catch ImportError for missing modules"
    solution: |
      modules = ["json", "os", "sys", "fake_module_xyz"]

      def check_modules(module_list):
          for mod in module_list:
              try:
                  __import__(mod)
                  print(f"{mod}: available")
              except ImportError:
                  print(f"{mod}: NOT available")

      check_modules(modules)

  - title: "Version Comparator"
    difficulty: intermediate
    description: "Write a function that compares two version strings (like '2.3.1' and '2.4.0') and prints which is newer."
    starter_code: |
      def compare_versions(v1, v2):
          # Compare version strings
          pass

      compare_versions("2.3.1", "2.4.0")
      compare_versions("3.0.0", "2.9.9")
      compare_versions("1.0.0", "1.0.0")

    expected_output: |
      2.4.0 is newer than 2.3.1
      3.0.0 is newer than 2.9.9
      1.0.0 and 1.0.0 are equal
    hints:
      - "Split version strings by '.' and compare each part as integers"
      - "Use tuple comparison for easy ordering"
    solution: |
      def compare_versions(v1, v2):
          parts1 = tuple(int(x) for x in v1.split("."))
          parts2 = tuple(int(x) for x in v2.split("."))
          if parts1 > parts2:
              print(f"{v1} is newer than {v2}")
          elif parts1 < parts2:
              print(f"{v2} is newer than {v1}")
          else:
              print(f"{v1} and {v2} are equal")

      compare_versions("2.3.1", "2.4.0")
      compare_versions("3.0.0", "2.9.9")
      compare_versions("1.0.0", "1.0.0")

  - title: "Requirements Generator"
    difficulty: advanced
    description: "Write a function that takes a dict of packages with versions and generates a formatted requirements.txt string."
    starter_code: |
      packages = {
          "requests": "2.31.0",
          "flask": "2.3.0",
          "pandas": "2.1.0",
          "pytest": "7.4.0"
      }

      def generate_requirements(pkgs):
          # Generate requirements.txt content
          pass

      print(generate_requirements(packages))

    expected_output: |
      flask==2.3.0
      pandas==2.1.0
      pytest==7.4.0
      requests==2.31.0
    hints:
      - "Sort packages alphabetically"
      - "Format each as 'package==version'"
    solution: |
      packages = {
          "requests": "2.31.0",
          "flask": "2.3.0",
          "pandas": "2.1.0",
          "pytest": "7.4.0"
      }

      def generate_requirements(pkgs):
          lines = []
          for name in sorted(pkgs):
              lines.append(f"{name}=={pkgs[name]}")
          return "\n".join(lines)

      print(generate_requirements(packages))

  - title: "Package Dependency Tree"
    difficulty: advanced
    description: "Simulate a dependency tree: given packages and their dependencies, print a tree showing what each package requires."
    starter_code: |
      deps = {
          "flask": ["werkzeug", "jinja2", "click"],
          "requests": ["urllib3", "certifi"],
          "werkzeug": [],
          "jinja2": [],
          "click": [],
          "urllib3": [],
          "certifi": []
      }

      def print_tree(packages, deps):
          # Print dependency tree
          pass

      print_tree(["flask", "requests"], deps)

    expected_output: |
      flask
        werkzeug
        jinja2
        click
      requests
        urllib3
        certifi
    hints:
      - "Loop through top-level packages"
      - "For each, print its name then indented dependencies"
    solution: |
      deps = {
          "flask": ["werkzeug", "jinja2", "click"],
          "requests": ["urllib3", "certifi"],
          "werkzeug": [],
          "jinja2": [],
          "click": [],
          "urllib3": [],
          "certifi": []
      }

      def print_tree(packages, deps):
          for pkg in packages:
              print(pkg)
              for dep in deps.get(pkg, []):
                  print(f"  {dep}")

      print_tree(["flask", "requests"], deps)
```
<!-- EXERCISE_END -->
