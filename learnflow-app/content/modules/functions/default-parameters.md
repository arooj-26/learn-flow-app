# Default Parameters in Python

Default parameters provide fallback values when arguments are not supplied, making functions more flexible and easier to use. They enable you to create versatile functions with sensible defaults while allowing customization when needed.

## Basic Default Parameters

Define default values in the function signature:

```python
def greet(name="Guest"):
    """Greet user with optional name."""
    return f"Hello, {name}!"

print(greet())  # Hello, Guest!
print(greet("Alice"))  # Hello, Alice!

# Multiple default parameters
def create_user(username, role="user", active=True):
    """Create user with default role and status."""
    return {
        "username": username,
        "role": role,
        "active": active
    }

print(create_user("alice"))
# {'username': 'alice', 'role': 'user', 'active': True}

print(create_user("bob", role="admin"))
# {'username': 'bob', 'role': 'admin', 'active': True}

print(create_user("charlie", role="moderator", active=False))
# {'username': 'charlie', 'role': 'moderator', 'active': False}
```

## Default Parameters Best Practices

| Practice | Good Example | Bad Example | Why |
|----------|--------------|-------------|-----|
| Order | `def f(required, optional=1)` | `def f(optional=1, required)` | Required params first |
| Immutable defaults | `def f(x, lst=None)` | `def f(x, lst=[])` | Mutable defaults persist |
| Clear naming | `def connect(timeout=30)` | `def connect(t=30)` | Clarity over brevity |
| Sensible values | `def log(level="INFO")` | `def log(level="DEBUG")` | Most common use case |

## Mutable Default Arguments Pitfall

Never use mutable objects as default parameters:

```python
# WRONG: Mutable default argument
def add_item_wrong(item, items=[]):
    """BAD: List is shared across calls!"""
    items.append(item)
    return items

# The same list is reused!
print(add_item_wrong("apple"))  # ['apple']
print(add_item_wrong("banana"))  # ['apple', 'banana'] - unexpected!

# CORRECT: Use None and create new list
def add_item_correct(item, items=None):
    """GOOD: New list created each time."""
    if items is None:
        items = []
    items.append(item)
    return items

print(add_item_correct("apple"))  # ['apple']
print(add_item_correct("banana"))  # ['banana'] - correct!

# Real-world example: Configuration management
def create_config(app_name, settings=None):
    """Create application configuration."""
    if settings is None:
        settings = {}

    # Default settings
    config = {
        "app_name": app_name,
        "debug": False,
        "port": 8000,
        "host": "localhost"
    }

    # Override with custom settings
    config.update(settings)
    return config

print(create_config("MyApp"))
# {'app_name': 'MyApp', 'debug': False, 'port': 8000, 'host': 'localhost'}

print(create_config("MyApp", {"debug": True, "port": 3000}))
# {'app_name': 'MyApp', 'debug': True, 'port': 3000, 'host': 'localhost'}
```

## Default Parameters with Type Hints

Combine default parameters with type hints for clear documentation:

```python
from typing import Optional, List, Dict

def fetch_data(
    url: str,
    timeout: int = 30,
    retries: int = 3,
    headers: Optional[Dict[str, str]] = None
) -> Dict:
    """
    Fetch data from URL with configurable options.

    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds (default: 30)
        retries: Number of retry attempts (default: 3)
        headers: Optional HTTP headers

    Returns:
        Response data as dictionary
    """
    if headers is None:
        headers = {"User-Agent": "Python App"}

    return {
        "url": url,
        "timeout": timeout,
        "retries": retries,
        "headers": headers
    }

# Using defaults
response = fetch_data("https://api.example.com/data")
print(response)

# Custom parameters
response = fetch_data(
    "https://api.example.com/data",
    timeout=60,
    headers={"Authorization": "Bearer token"}
)
print(response)
```

## Default Parameters in Real-World Scenarios

Common patterns using default parameters effectively:

```python
# Database connection with defaults
def connect_database(
    host="localhost",
    port=5432,
    database="mydb",
    username="admin",
    password=None,
    ssl=True
):
    """Connect to database with sensible defaults."""
    if password is None:
        raise ValueError("Password is required")

    connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    ssl_mode = "require" if ssl else "disable"

    return {
        "connection_string": connection_string,
        "ssl_mode": ssl_mode
    }

# Minimal usage
db = connect_database(password="secret123")
print(db)

# Custom configuration
db = connect_database(
    host="prod-db.example.com",
    port=5433,
    database="production",
    password="secret123",
    ssl=True
)
print(db)

# Logging function with severity levels
def log(message, level="INFO", timestamp=None, to_file=False):
    """
    Log message with configurable options.

    Args:
        message: The message to log
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        timestamp: Custom timestamp (None = current time)
        to_file: Whether to write to file
    """
    from datetime import datetime

    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] {level}: {message}"

    print(log_entry)

    if to_file:
        # In real implementation, write to file
        return f"Written to file: {log_entry}"

    return log_entry

# Simple usage
log("Application started")

# Detailed usage
log("Database error", level="ERROR", to_file=True)
```

## Default Parameters with *args and **kwargs

Combine default parameters with variable arguments:

```python
def create_report(title, *sections, format="pdf", include_toc=True, **metadata):
    """
    Create a report with flexible structure.

    Args:
        title: Report title (required)
        *sections: Variable number of section names
        format: Output format (default: pdf)
        include_toc: Include table of contents (default: True)
        **metadata: Additional metadata fields
    """
    report = {
        "title": title,
        "sections": sections,
        "format": format,
        "include_toc": include_toc,
        "metadata": metadata
    }
    return report

# Minimal report
report1 = create_report("Monthly Report")
print(report1)

# Full featured report
report2 = create_report(
    "Annual Report",
    "Introduction",
    "Analysis",
    "Conclusion",
    format="html",
    include_toc=True,
    author="John Doe",
    date="2024-01-01",
    version="1.0"
)
print(report2)
```

## Dynamic Default Values

Use function calls or expressions for dynamic defaults:

```python
from datetime import datetime
import random

def create_event(name, event_id=None, created_at=None):
    """Create event with auto-generated defaults."""
    if event_id is None:
        event_id = random.randint(10000, 99999)

    if created_at is None:
        created_at = datetime.now().isoformat()

    return {
        "name": name,
        "id": event_id,
        "created_at": created_at
    }

# Auto-generated values
event1 = create_event("Conference")
print(event1)

# Custom values
event2 = create_event("Workshop", event_id=12345, created_at="2024-01-01T10:00:00")
print(event2)

# Factory pattern with defaults
def create_vehicle(vehicle_type="car", color="black", year=2024):
    """Vehicle factory with defaults."""
    return {
        "type": vehicle_type,
        "color": color,
        "year": year,
        "id": f"{vehicle_type}_{random.randint(1000, 9999)}"
    }

car = create_vehicle()
truck = create_vehicle(vehicle_type="truck", color="red")
bike = create_vehicle(vehicle_type="motorcycle", year=2023)

print(car)
print(truck)
print(bike)
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Simple Default Parameter"
    difficulty: basic
    description: "Create a function `power(base, exponent=2)` that returns base raised to exponent. Test power(5) and power(2, 3)."
    starter_code: |
      # Create power function with default exponent

    expected_output: |
      25
      8
    hints:
      - "Default parameter: def func(param=default)"
      - "Use ** operator for exponentiation"
    solution: |
      def power(base, exponent=2):
          return base ** exponent

      print(power(5))
      print(power(2, 3))

  - title: "Multiple Defaults"
    difficulty: basic
    description: "Create a function `format_name(first, last, title='Mr.')` that returns formatted name. Test with ('John', 'Doe') and ('Jane', 'Smith', 'Dr.')."
    starter_code: |
      # Create format_name function

    expected_output: |
      Mr. John Doe
      Dr. Jane Smith
    hints:
      - "Return formatted string with title"
      - "Use f-string for formatting"
    solution: |
      def format_name(first, last, title="Mr."):
          return f"{title} {first} {last}"

      print(format_name("John", "Doe"))
      print(format_name("Jane", "Smith", "Dr."))

  - title: "Mutable Default Fix"
    difficulty: intermediate
    description: "Create a function `add_student(name, courses=None)` that adds name to a courses list. If courses is None, create new list. Test by calling twice with different names."
    starter_code: |
      # Create add_student with proper default handling

    expected_output: |
      ['Alice']
      ['Bob']
    hints:
      - "Use None as default, not []"
      - "Check if courses is None, then create new list"
    solution: |
      def add_student(name, courses=None):
          if courses is None:
              courses = []
          courses.append(name)
          return courses

      print(add_student("Alice"))
      print(add_student("Bob"))

  - title: "Configuration Builder"
    difficulty: intermediate
    description: "Create `build_server_config(name, host='localhost', port=8000, debug=False)` that returns a dict. Test with just name='MyServer' and with custom port=3000, debug=True."
    starter_code: |
      # Create build_server_config function

    expected_output: |
      {'name': 'MyServer', 'host': 'localhost', 'port': 8000, 'debug': False}
      {'name': 'MyServer', 'host': 'localhost', 'port': 3000, 'debug': True}
    hints:
      - "Return dictionary with all parameters"
      - "Use keyword arguments when calling"
    solution: |
      def build_server_config(name, host="localhost", port=8000, debug=False):
          return {
              "name": name,
              "host": host,
              "port": port,
              "debug": debug
          }

      print(build_server_config("MyServer"))
      print(build_server_config("MyServer", port=3000, debug=True))

  - title: "API Request Builder"
    difficulty: advanced
    description: "Create `api_request(endpoint, method='GET', timeout=30, headers=None)` that returns a dict. If headers is None, use {'Content-Type': 'application/json'}. Test with endpoint='/users' using defaults and with method='POST', custom headers."
    starter_code: |
      # Create api_request function

    expected_output: |
      {'endpoint': '/users', 'method': 'GET', 'timeout': 30, 'headers': {'Content-Type': 'application/json'}}
      {'endpoint': '/users', 'method': 'POST', 'timeout': 30, 'headers': {'Authorization': 'Bearer token'}}
    hints:
      - "Check if headers is None"
      - "Set default headers dict"
      - "Return dict with all config"
    solution: |
      def api_request(endpoint, method="GET", timeout=30, headers=None):
          if headers is None:
              headers = {"Content-Type": "application/json"}
          return {
              "endpoint": endpoint,
              "method": method,
              "timeout": timeout,
              "headers": headers
          }

      print(api_request("/users"))
      print(api_request("/users", method="POST", headers={"Authorization": "Bearer token"}))

  - title: "Email Sender with Defaults"
    difficulty: advanced
    description: "Create `send_email(to, subject, body, cc=None, bcc=None, priority='normal')` that returns a dict with all params. If cc/bcc are None, use empty lists. Test with minimal args and with cc=['admin@example.com'], priority='high'."
    starter_code: |
      # Create send_email function

    expected_output: |
      {'to': 'user@example.com', 'subject': 'Hello', 'body': 'Message', 'cc': [], 'bcc': [], 'priority': 'normal'}
      {'to': 'user@example.com', 'subject': 'Hello', 'body': 'Message', 'cc': ['admin@example.com'], 'bcc': [], 'priority': 'high'}
    hints:
      - "Use None for mutable defaults (cc, bcc)"
      - "Create empty lists if None"
      - "Return dict with all fields"
    solution: |
      def send_email(to, subject, body, cc=None, bcc=None, priority="normal"):
          if cc is None:
              cc = []
          if bcc is None:
              bcc = []
          return {
              "to": to,
              "subject": subject,
              "body": body,
              "cc": cc,
              "bcc": bcc,
              "priority": priority
          }

      print(send_email("user@example.com", "Hello", "Message"))
      print(send_email("user@example.com", "Hello", "Message", cc=["admin@example.com"], priority="high"))
```
<!-- EXERCISE_END -->
