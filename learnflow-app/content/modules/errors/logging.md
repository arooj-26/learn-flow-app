# Logging in Python

The `logging` module provides a flexible framework for emitting log messages from Python programs. Unlike `print()`, logging supports severity levels, output destinations, formatting, and can be configured without modifying code.

## Why Logging Over Print

```python
# print() limitations:
# - No severity levels
# - Hard to disable in production
# - No timestamps or context
# - Can't redirect easily

# logging advantages:
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Detailed diagnostic info")
logger.info("General operational info")
logger.warning("Something unexpected happened")
logger.error("An error occurred")
logger.critical("System is in a critical state")
```

## Log Levels

Python logging has five standard severity levels:

| Level | Value | Purpose |
|-------|-------|---------|
| `DEBUG` | 10 | Detailed diagnostic information |
| `INFO` | 20 | Confirmation that things work |
| `WARNING` | 30 | Something unexpected (default level) |
| `ERROR` | 40 | A function failed to perform |
| `CRITICAL` | 50 | Program may not continue |

```python
import logging

# Only messages at WARNING or above are shown by default
logging.warning("This will be shown")
logging.info("This will NOT be shown")

# Set level to see all messages
logging.basicConfig(level=logging.DEBUG, force=True)
logging.debug("Now this is visible")
logging.info("And this too")
```

## Configuring Loggers

```python
import logging

# Basic configuration with format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("myapp")
logger.info("Application started")
# 2024-01-15 10:30:00 - myapp - INFO - Application started

# Common format fields
# %(asctime)s    - Human-readable time
# %(name)s       - Logger name
# %(levelname)s  - Level name (DEBUG, INFO, etc.)
# %(message)s    - The log message
# %(filename)s   - Source file name
# %(lineno)d     - Line number
# %(funcName)s   - Function name
```

## Logger Hierarchy

Loggers follow a hierarchy based on their names:

```python
import logging

# Parent logger
app_logger = logging.getLogger("myapp")
app_logger.setLevel(logging.DEBUG)

# Child loggers inherit settings
db_logger = logging.getLogger("myapp.database")
api_logger = logging.getLogger("myapp.api")

# Add handler to parent - children will use it too
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
app_logger.addHandler(handler)

db_logger.info("Connected to database")
# myapp.database - INFO - Connected to database

api_logger.warning("Rate limit approaching")
# myapp.api - WARNING - Rate limit approaching
```

## Handlers and Formatters

Handlers determine where log messages go:

```python
import logging

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_format)

# File handler
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# INFO+ goes to console, DEBUG+ goes to file
logger.debug("Debug details")   # File only
logger.info("User logged in")   # Both console and file
logger.error("Database error")  # Both console and file
```

## Logging Exceptions

```python
import logging

logger = logging.getLogger("myapp")
logging.basicConfig(level=logging.DEBUG)

# Log exception with traceback
try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("Division failed")
    # Logs ERROR level + full traceback

# Or manually include exception info
try:
    int("not_a_number")
except ValueError as e:
    logger.error("Conversion failed: %s", e, exc_info=True)
```

## Practical Logging Patterns

```python
import logging

logging.basicConfig(level=logging.INFO,
                   format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Function entry/exit logging
def process_data(data):
    logger.info("Processing %d items", len(data))
    results = [x * 2 for x in data]
    logger.info("Processing complete: %d results", len(results))
    return results

# Conditional logging
def connect(host, port):
    logger.info("Connecting to %s:%d", host, port)
    if port < 1024:
        logger.warning("Using privileged port %d", port)
    logger.info("Connected successfully")

# Performance logging
import time

def slow_operation():
    start = time.time()
    total = sum(range(1000000))
    elapsed = time.time() - start
    logger.info("Operation took %.3f seconds", elapsed)
    return total
```

## Best Practices

1. **Use `__name__`** as the logger name for automatic hierarchy
2. **Never use print()** for production logging
3. **Use lazy formatting** (`logger.info("Value: %s", val)` not `logger.info(f"Value: {val}")`)
4. **Set appropriate levels** - DEBUG for dev, WARNING for production
5. **Use `logger.exception()`** inside except blocks for automatic tracebacks

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Basic Logging"
    difficulty: basic
    description: "Set up basic logging with INFO level and log three messages: an info, a warning, and an error."
    starter_code: |
      import logging
      # Configure and log messages

    expected_output: |
      INFO:root:Application started
      WARNING:root:Low disk space
      ERROR:root:Connection failed
    hints:
      - "Use logging.basicConfig(level=logging.INFO)"
      - "Use logging.info(), logging.warning(), logging.error()"
    solution: |
      import logging
      logging.basicConfig(level=logging.INFO, force=True)
      logging.info("Application started")
      logging.warning("Low disk space")
      logging.error("Connection failed")

  - title: "Named Logger"
    difficulty: basic
    description: "Create a named logger called 'myapp' and log an info message 'Hello from myapp'."
    starter_code: |
      import logging
      # Create named logger and log a message

    expected_output: "INFO:myapp:Hello from myapp"
    hints:
      - "Use logging.getLogger('myapp')"
      - "Set the level with basicConfig or logger.setLevel()"
    solution: |
      import logging
      logging.basicConfig(level=logging.INFO, force=True)
      logger = logging.getLogger("myapp")
      logger.info("Hello from myapp")

  - title: "Formatted Logging"
    difficulty: intermediate
    description: "Configure logging with a custom format showing level and message separated by ' | '. Log an info and warning message."
    starter_code: |
      import logging
      # Configure with custom format

    expected_output: |
      INFO | Server started
      WARNING | High memory usage
    hints:
      - "Use format='%(levelname)s | %(message)s' in basicConfig"
    solution: |
      import logging
      logging.basicConfig(
          level=logging.INFO,
          format='%(levelname)s | %(message)s',
          force=True
      )
      logging.info("Server started")
      logging.warning("High memory usage")

  - title: "Log with Variables"
    difficulty: intermediate
    description: "Log a message that includes the user name and action using lazy formatting (% style)."
    starter_code: |
      import logging
      logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s', force=True)
      logger = logging.getLogger()

      user = "Alice"
      action = "login"
      # Log using lazy formatting

    expected_output: "INFO:User Alice performed login"
    hints:
      - "Use logger.info('User %s performed %s', user, action)"
      - "This is the recommended way - avoids string formatting if level is disabled"
    solution: |
      import logging
      logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s', force=True)
      logger = logging.getLogger()

      user = "Alice"
      action = "login"
      logger.info("User %s performed %s", user, action)

  - title: "Exception Logging"
    difficulty: advanced
    description: "Write a function that attempts to convert a string to int, logs the exception if it fails, and returns a default value. Test with 'abc'."
    starter_code: |
      import logging
      logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s', force=True)
      logger = logging.getLogger()

      def safe_int(value, default=0):
          # Try to convert, log error on failure
          pass

      result = safe_int("abc", default=-1)
      print(f"Result: {result}")

    expected_output: |
      ERROR:Failed to convert 'abc' to int
      Result: -1
    hints:
      - "Use try/except ValueError"
      - "Use logger.error() in the except block"
    solution: |
      import logging
      logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s', force=True)
      logger = logging.getLogger()

      def safe_int(value, default=0):
          try:
              return int(value)
          except ValueError:
              logger.error("Failed to convert '%s' to int", value)
              return default

      result = safe_int("abc", default=-1)
      print(f"Result: {result}")

  - title: "Multi-Level Logger"
    difficulty: advanced
    description: "Create a function that processes items and logs at different levels: DEBUG for each item, INFO for summary, WARNING if list is empty."
    starter_code: |
      import logging
      logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s', force=True)
      logger = logging.getLogger()

      def process_items(items):
          # Log appropriately based on input
          pass

      process_items([10, 20, 30])

    expected_output: |
      DEBUG:Processing item: 10
      DEBUG:Processing item: 20
      DEBUG:Processing item: 30
      INFO:Processed 3 items, total: 60
    hints:
      - "Use logger.debug() for each item in the loop"
      - "Use logger.info() for the summary after processing"
      - "Use logger.warning() if the list is empty"
    solution: |
      import logging
      logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s', force=True)
      logger = logging.getLogger()

      def process_items(items):
          if not items:
              logger.warning("Empty list provided")
              return
          total = 0
          for item in items:
              logger.debug("Processing item: %s", item)
              total += item
          logger.info("Processed %d items, total: %d", len(items), total)

      process_items([10, 20, 30])
```
<!-- EXERCISE_END -->
