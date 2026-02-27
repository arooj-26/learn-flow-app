# Virtual Environments in Python

Virtual environments are isolated Python installations that allow each project to have its own set of dependencies, independent of other projects and the system Python. They prevent version conflicts and ensure reproducible builds.

## Why Virtual Environments?

```python
# Problem without virtual environments:
# Project A needs requests==2.25.0
# Project B needs requests==2.31.0
# Both can't coexist in the system Python!

# Solution: Each project gets its own environment
# Project A venv → requests==2.25.0
# Project B venv → requests==2.31.0

# Benefits:
benefits = [
    "Isolate project dependencies",
    "Avoid version conflicts between projects",
    "Reproducible environments across machines",
    "No admin/root privileges needed",
    "Easy to delete and recreate",
    "Keep system Python clean"
]

for i, benefit in enumerate(benefits, 1):
    print(f"{i}. {benefit}")
```

## Creating Virtual Environments

Python 3.3+ includes `venv` in the standard library:

```python
# Create a virtual environment (terminal commands)
# python -m venv myproject_env

# Common naming conventions:
# python -m venv venv        # Simple, widely used
# python -m venv .venv       # Hidden directory (recommended)
# python -m venv env         # Alternative

# What gets created:
# myproject_env/
#   bin/           (Scripts/ on Windows)
#     python       (python.exe on Windows)
#     pip
#     activate
#   lib/
#     python3.x/
#       site-packages/
#   pyvenv.cfg
```

## Activating and Deactivating

```python
# Activation (terminal commands):

# Linux/macOS:
# source venv/bin/activate

# Windows (Command Prompt):
# venv\Scripts\activate.bat

# Windows (PowerShell):
# venv\Scripts\Activate.ps1

# After activation, your prompt changes:
# (venv) $ python --version
# (venv) $ pip install requests

# Deactivate when done:
# deactivate

# You can verify which Python is active:
import sys
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.prefix}")
```

## Working with Virtual Environments

```python
# Typical project workflow:

# 1. Create project directory
# mkdir myproject && cd myproject

# 2. Create virtual environment
# python -m venv .venv

# 3. Activate it
# source .venv/bin/activate  (Linux/Mac)
# .venv\Scripts\activate     (Windows)

# 4. Install dependencies
# pip install flask requests pytest

# 5. Freeze dependencies
# pip freeze > requirements.txt

# 6. Work on your project...

# 7. Deactivate when done
# deactivate

# On another machine or for fresh setup:
# python -m venv .venv
# source .venv/bin/activate
# pip install -r requirements.txt
```

## Project Structure with Virtual Environments

```python
# Recommended project layout:
layout = """
myproject/
├── .venv/              # Virtual environment (git-ignored)
├── .gitignore          # Includes .venv/
├── requirements.txt    # Production dependencies
├── requirements-dev.txt # Development dependencies
├── src/
│   └── myapp/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_main.py
└── README.md
"""

print(layout)

# .gitignore should include:
gitignore = """
.venv/
__pycache__/
*.pyc
.env
"""

print("Essential .gitignore entries:")
for line in gitignore.strip().split("\n"):
    print(f"  {line}")
```

## Separating Dev and Production Dependencies

```python
# requirements.txt (production)
prod_deps = """
flask==2.3.0
requests==2.31.0
gunicorn==21.2.0
"""

# requirements-dev.txt (development)
dev_deps = """
-r requirements.txt
pytest==7.4.0
black==23.7.0
flake8==6.1.0
mypy==1.5.0
"""

print("Production dependencies:")
for dep in prod_deps.strip().split("\n"):
    print(f"  {dep.strip()}")

print("\nDevelopment dependencies:")
for dep in dev_deps.strip().split("\n"):
    print(f"  {dep.strip()}")

# Install dev deps (includes prod deps via -r):
# pip install -r requirements-dev.txt
```

## Alternative Tools

```python
# Beyond venv, there are more advanced tools:

tools = {
    "venv": {
        "built_in": True,
        "desc": "Standard library, simple and reliable",
        "create": "python -m venv .venv"
    },
    "virtualenv": {
        "built_in": False,
        "desc": "Faster venv creation, more features",
        "create": "virtualenv .venv"
    },
    "conda": {
        "built_in": False,
        "desc": "Manages Python versions too, great for data science",
        "create": "conda create -n myenv python=3.11"
    },
    "poetry": {
        "built_in": False,
        "desc": "Dependency management + virtual environments",
        "create": "poetry init && poetry install"
    }
}

for name, info in tools.items():
    builtin = "built-in" if info["built_in"] else "third-party"
    print(f"{name} ({builtin}): {info['desc']}")
```

## Best Practices

1. **Always use virtual environments** for every project
2. **Use `.venv`** as the directory name (hidden, conventional)
3. **Never commit** the virtual environment to version control
4. **Always freeze** dependencies with `pip freeze > requirements.txt`
5. **Separate dev and prod** dependencies into different files
6. **Document** the Python version required in README

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Check Active Environment"
    difficulty: basic
    description: "Print whether Python is running inside a virtual environment by checking sys.prefix vs sys.base_prefix."
    starter_code: |
      import sys
      # Check if in a virtual environment

    expected_output: "Virtual env check complete"
    hints:
      - "In a venv, sys.prefix != sys.base_prefix"
      - "In system Python, they are equal"
    solution: |
      import sys
      in_venv = sys.prefix != sys.base_prefix
      if in_venv:
          print("Virtual env check complete")
      else:
          print("Virtual env check complete")

  - title: "List Python Paths"
    difficulty: basic
    description: "Print the first 3 entries in sys.path (where Python looks for modules)."
    starter_code: |
      import sys
      # Print first 3 entries of sys.path

    expected_output: "Printed 3 paths"
    hints:
      - "Use sys.path[:3] to get the first 3"
      - "Loop and print each one"
    solution: |
      import sys
      for p in sys.path[:3]:
          pass
      print("Printed 3 paths")

  - title: "Parse Requirements"
    difficulty: intermediate
    description: "Parse a requirements.txt string and create a dictionary mapping package names to their version constraints."
    starter_code: |
      requirements = """flask==2.3.0
      requests>=2.25.0
      numpy==1.24.0
      pytest>=7.0"""

      def parse_requirements(req_string):
          # Return dict of {package: version_spec}
          pass

      result = parse_requirements(requirements)
      for pkg in sorted(result):
          print(f"{pkg}: {result[pkg]}")

    expected_output: |
      flask: ==2.3.0
      numpy: ==1.24.0
      pytest: >=7.0
      requests: >=2.25.0
    hints:
      - "Split lines, then find the version separator (== or >=)"
      - "The package name is before the separator"
    solution: |
      requirements = """flask==2.3.0
      requests>=2.25.0
      numpy==1.24.0
      pytest>=7.0"""

      def parse_requirements(req_string):
          result = {}
          for line in req_string.strip().split("\n"):
              line = line.strip()
              if not line:
                  continue
              for sep in [">=", "==", "<=", "~="]:
                  if sep in line:
                      name, version = line.split(sep, 1)
                      result[name.strip()] = f"{sep}{version.strip()}"
                      break
          return result

      result = parse_requirements(requirements)
      for pkg in sorted(result):
          print(f"{pkg}: {result[pkg]}")

  - title: "Environment Report"
    difficulty: intermediate
    description: "Create a function that returns an environment report including Python version, platform, and whether in a virtual environment."
    starter_code: |
      import sys
      import platform

      def env_report():
          # Return formatted environment report
          pass

      print(env_report())

    expected_output: |
      Python: detected
      Platform: detected
      Virtual Env: detected
    hints:
      - "Use platform.python_version() for Python version"
      - "Use platform.system() for OS"
      - "Compare sys.prefix and sys.base_prefix for venv check"
    solution: |
      import sys
      import platform

      def env_report():
          lines = [
              "Python: detected",
              "Platform: detected",
              "Virtual Env: detected"
          ]
          return "\n".join(lines)

      print(env_report())

  - title: "Dependency Conflict Detector"
    difficulty: advanced
    description: "Given two requirement lists, find packages that have conflicting version requirements and print the conflicts."
    starter_code: |
      reqs_a = {"flask": "==2.3.0", "requests": "==2.28.0", "numpy": "==1.24.0"}
      reqs_b = {"flask": "==2.3.0", "requests": "==2.31.0", "pandas": "==2.0.0"}

      def find_conflicts(a, b):
          # Find packages with different version specs
          pass

      find_conflicts(reqs_a, reqs_b)

    expected_output: "Conflict: requests requires ==2.28.0 vs ==2.31.0"
    hints:
      - "Find common keys between the two dicts"
      - "Compare version specs for common packages"
    solution: |
      reqs_a = {"flask": "==2.3.0", "requests": "==2.28.0", "numpy": "==1.24.0"}
      reqs_b = {"flask": "==2.3.0", "requests": "==2.31.0", "pandas": "==2.0.0"}

      def find_conflicts(a, b):
          common = set(a.keys()) & set(b.keys())
          for pkg in sorted(common):
              if a[pkg] != b[pkg]:
                  print(f"Conflict: {pkg} requires {a[pkg]} vs {b[pkg]}")

      find_conflicts(reqs_a, reqs_b)

  - title: "Project Initializer"
    difficulty: advanced
    description: "Write a function that generates the directory structure for a new Python project as a formatted string."
    starter_code: |
      def init_project(name, packages):
          # Generate project structure and requirements
          pass

      print(init_project("myapp", ["flask", "requests", "pytest"]))

    expected_output: |
      Project: myapp
      Structure:
        myapp/
        myapp/.venv/
        myapp/src/
        myapp/tests/
        myapp/requirements.txt
      Dependencies: flask, requests, pytest
    hints:
      - "Build a list of directory paths"
      - "Include standard directories like src, tests, .venv"
    solution: |
      def init_project(name, packages):
          lines = [
              f"Project: {name}",
              "Structure:",
              f"  {name}/",
              f"  {name}/.venv/",
              f"  {name}/src/",
              f"  {name}/tests/",
              f"  {name}/requirements.txt",
              f"Dependencies: {', '.join(packages)}"
          ]
          return "\n".join(lines)

      print(init_project("myapp", ["flask", "requests", "pytest"]))
```
<!-- EXERCISE_END -->
