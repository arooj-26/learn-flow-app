# Dictionary Methods

Python dictionaries provide a comprehensive set of methods for manipulating, querying, and transforming key-value data. Mastering these methods enables you to write more efficient and elegant code when working with structured data, configurations, caches, and data transformations. This guide covers essential dictionary methods with practical, real-world examples.

## Accessing and Querying Methods

Dictionary methods provide safe and flexible ways to access data without risking KeyErrors.

The `get()` method is crucial for safe dictionary access, while `setdefault()` combines getting and setting in one operation. The `keys()`, `values()`, and `items()` methods provide views into dictionary data.

```python
# Configuration management example
config = {
    "host": "localhost",
    "port": 8080,
    "debug": True
}

# get() - safe access with defaults
host = config.get("host", "127.0.0.1")
timeout = config.get("timeout", 30)  # Uses default since key doesn't exist
print(f"Host: {host}, Timeout: {timeout}")

# setdefault() - get value or set default if missing
config.setdefault("max_connections", 100)
config.setdefault("port", 3000)  # Doesn't change existing value
print(f"Config: {config}")

# keys(), values(), items() - dictionary views
print(f"Keys: {list(config.keys())}")
print(f"Values: {list(config.values())}")
print(f"Items: {list(config.items())}")

# Dictionary views are dynamic - they reflect changes
original = {"a": 1, "b": 2}
view = original.keys()
print(f"Before: {list(view)}")
original["c"] = 3
print(f"After adding 'c': {list(view)}")

# Practical example: Environment variable handler
import os

class Config:
    def __init__(self):
        self.settings = {}

    def get_setting(self, key, default=None):
        """Get setting from dict, environment, or default"""
        return self.settings.get(key) or os.environ.get(key) or default

    def set_default(self, key, value):
        """Set value only if not already set"""
        return self.settings.setdefault(key, value)

cfg = Config()
cfg.settings["api_url"] = "https://api.example.com"
print(f"API URL: {cfg.get_setting('api_url')}")
print(f"Max retries: {cfg.get_setting('max_retries', 3)}")
```

## Update and Merge Methods

The `update()` method is powerful for merging dictionaries, and Python 3.9+ introduced the merge operators `|` and `|=`.

```python
# Merging user preferences
default_prefs = {
    "theme": "light",
    "language": "en",
    "notifications": True,
    "font_size": 12
}

user_prefs = {
    "theme": "dark",
    "font_size": 14
}

# update() modifies the dictionary in-place
final_prefs = default_prefs.copy()
final_prefs.update(user_prefs)
print(f"Final preferences: {final_prefs}")

# update() can take keyword arguments
settings = {"a": 1, "b": 2}
settings.update(c=3, d=4)
print(f"Settings: {settings}")

# update() with list of tuples
settings.update([("e", 5), ("f", 6)])
print(f"Updated settings: {settings}")

# Python 3.9+: Merge operator |
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}
merged = dict1 | dict2  # Creates new dictionary
print(f"Merged: {merged}")

# In-place merge operator |=
dict1 |= dict2
print(f"Dict1 after |=: {dict1}")

# Practical example: Configuration layers
base_config = {"timeout": 30, "retries": 3, "debug": False}
env_config = {"timeout": 60, "debug": True}
user_config = {"retries": 5}

# Layer configurations: base < env < user
final_config = base_config | env_config | user_config
print(f"Final config: {final_config}")

# Merging with conflict resolution
def merge_with_strategy(dict1, dict2, strategy="overwrite"):
    """Merge with different strategies for conflicts"""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result:
            if strategy == "overwrite":
                result[key] = value
            elif strategy == "keep":
                pass  # Keep original value
            elif strategy == "sum":
                result[key] = result[key] + value
        else:
            result[key] = value
    return result

sales_q1 = {"product_a": 100, "product_b": 150}
sales_q2 = {"product_a": 120, "product_c": 80}

total_sales = merge_with_strategy(sales_q1, sales_q2, strategy="sum")
print(f"Total sales: {total_sales}")
```

## Removal Methods

Python provides several methods to remove items from dictionaries, each with different behaviors and use cases.

```python
# pop() - remove and return value
user_data = {
    "username": "alice",
    "email": "alice@example.com",
    "temp_token": "abc123",
    "session_id": "xyz789"
}

# Remove and use the value
token = user_data.pop("temp_token")
print(f"Removed token: {token}")
print(f"User data: {user_data}")

# pop() with default (doesn't raise KeyError)
api_key = user_data.pop("api_key", None)
print(f"API key: {api_key}")  # None

# popitem() - remove and return last inserted item (LIFO in Python 3.7+)
cache = {"page1": "data1", "page2": "data2", "page3": "data3"}
last_item = cache.popitem()
print(f"Removed: {last_item}")
print(f"Cache: {cache}")

# clear() - remove all items
temp_data = {"a": 1, "b": 2, "c": 3}
temp_data.clear()
print(f"Cleared: {temp_data}")  # {}

# del statement (not a method, but commonly used)
data = {"x": 10, "y": 20, "z": 30}
del data["y"]
print(f"After del: {data}")

# Practical example: LRU Cache implementation (simplified)
class SimpleCache:
    def __init__(self, max_size=3):
        self.cache = {}
        self.max_size = max_size

    def get(self, key):
        if key in self.cache:
            # Move to end (most recently used)
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        return None

    def put(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.max_size:
            # Remove least recently used (first item)
            self.cache.pop(next(iter(self.cache)))
        self.cache[key] = value

    def __repr__(self):
        return str(self.cache)

cache = SimpleCache(max_size=3)
cache.put("a", 1)
cache.put("b", 2)
cache.put("c", 3)
print(f"Cache: {cache}")
cache.put("d", 4)  # Evicts "a"
print(f"After adding 'd': {cache}")
cache.get("b")  # Move "b" to end
cache.put("e", 5)  # Evicts "c" (not "b")
print(f"After adding 'e': {cache}")
```

## Copying and View Methods

Understanding shallow vs. deep copying is crucial when working with nested dictionaries.

```python
import copy

# copy() - shallow copy
original = {
    "name": "Alice",
    "scores": [85, 90, 92],
    "metadata": {"created": "2024-01-01"}
}

# Shallow copy
shallow = original.copy()
shallow["name"] = "Bob"  # Doesn't affect original
shallow["scores"].append(95)  # DOES affect original!
shallow["metadata"]["created"] = "2024-02-01"  # DOES affect original!

print(f"Original: {original}")
print(f"Shallow: {shallow}")

# Deep copy for nested structures
original2 = {
    "name": "Charlie",
    "scores": [88, 92],
    "metadata": {"created": "2024-01-01"}
}

deep = copy.deepcopy(original2)
deep["scores"].append(95)
deep["metadata"]["created"] = "2024-03-01"

print(f"\nOriginal2: {original2}")  # Unchanged
print(f"Deep: {deep}")

# fromkeys() - create dict from sequence of keys
keys = ["a", "b", "c"]
default_dict = dict.fromkeys(keys, 0)
print(f"Default dict: {default_dict}")

# Warning: fromkeys with mutable default
keys = ["x", "y", "z"]
bad_dict = dict.fromkeys(keys, [])  # Same list object for all!
bad_dict["x"].append(1)
print(f"Bad dict: {bad_dict}")  # All keys have [1]!

# Correct way: use dict comprehension
good_dict = {key: [] for key in keys}
good_dict["x"].append(1)
print(f"Good dict: {good_dict}")  # Only 'x' has [1]

# Practical example: Initialize student records
students = ["Alice", "Bob", "Charlie"]
grades = {name: {"assignments": [], "exams": [], "final": None} for name in students}
print(f"Grade book: {grades}")
```

Dictionary methods summary:

| Method | Returns | Modifies Dict | Description |
|--------|---------|---------------|-------------|
| `get(key, default)` | Value or default | No | Safe access |
| `setdefault(key, default)` | Value | Yes | Get or set default |
| `update(other)` | None | Yes | Merge dictionaries |
| `pop(key, default)` | Value | Yes | Remove and return |
| `popitem()` | (key, value) | Yes | Remove last item |
| `clear()` | None | Yes | Remove all items |
| `copy()` | New dict | No | Shallow copy |
| `keys()` | View | No | All keys |
| `values()` | View | No | All values |
| `items()` | View | No | All pairs |
| `fromkeys(seq, value)` | New dict | No | Create from keys |

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Safe Configuration Reader"
    difficulty: basic
    description: "Use get() method to safely read configuration values with appropriate defaults."
    starter_code: |
      config = {
          "host": "localhost",
          "port": 8080
      }

      # Get host, port, and timeout (default 30)
      # Print each value

    expected_output: |
      host: localhost
      port: 8080
      timeout: 30
    hints:
      - "Use get() with a default value for missing keys"
      - "Timeout key doesn't exist, so it should use the default"
    solution: |
      config = {
          "host": "localhost",
          "port": 8080
      }

      # Get host, port, and timeout (default 30)
      host = config.get("host")
      port = config.get("port")
      timeout = config.get("timeout", 30)

      # Print each value
      print(f"host: {host}")
      print(f"port: {port}")
      print(f"timeout: {timeout}")

  - title: "Initialize Default Values"
    difficulty: basic
    description: "Use setdefault() to ensure all required configuration keys exist with default values."
    starter_code: |
      config = {"debug": True}

      # Use setdefault to add: host='localhost', port=8080, timeout=30
      # Debug should remain True
      # Print the final config

    expected_output: |
      {'debug': True, 'host': 'localhost', 'port': 8080, 'timeout': 30}
    hints:
      - "Use setdefault() for each key"
      - "setdefault() won't change existing values"
    solution: |
      config = {"debug": True}

      # Use setdefault to add: host='localhost', port=8080, timeout=30
      config.setdefault("host", "localhost")
      config.setdefault("port", 8080)
      config.setdefault("timeout", 30)

      # Print the final config
      print(config)

  - title: "Merge User Preferences"
    difficulty: intermediate
    description: "Merge default preferences with user preferences, where user preferences override defaults."
    starter_code: |
      defaults = {
          "theme": "light",
          "notifications": True,
          "language": "en",
          "font_size": 12
      }

      user_prefs = {
          "theme": "dark",
          "font_size": 16
      }

      # Merge user_prefs into a copy of defaults
      # Print the final preferences

    expected_output: |
      {'theme': 'dark', 'notifications': True, 'language': 'en', 'font_size': 16}
    hints:
      - "Create a copy of defaults first"
      - "Use update() to merge user preferences"
    solution: |
      defaults = {
          "theme": "light",
          "notifications": True,
          "language": "en",
          "font_size": 12
      }

      user_prefs = {
          "theme": "dark",
          "font_size": 16
      }

      # Merge user_prefs into a copy of defaults
      final = defaults.copy()
      final.update(user_prefs)

      # Print the final preferences
      print(final)

  - title: "Clean Expired Sessions"
    difficulty: intermediate
    description: "Remove all sessions that have expired (is_expired=True) using pop() in a loop."
    starter_code: |
      sessions = {
          "session1": {"user": "alice", "is_expired": False},
          "session2": {"user": "bob", "is_expired": True},
          "session3": {"user": "charlie", "is_expired": True},
          "session4": {"user": "diana", "is_expired": False}
      }

      # Remove expired sessions
      # Print remaining sessions

    expected_output: |
      {'session1': {'user': 'alice', 'is_expired': False}, 'session4': {'user': 'diana', 'is_expired': False}}
    hints:
      - "Create a list of expired session IDs first"
      - "Then use pop() to remove each one"
      - "Don't modify dictionary while iterating over it directly"
    solution: |
      sessions = {
          "session1": {"user": "alice", "is_expired": False},
          "session2": {"user": "bob", "is_expired": True},
          "session3": {"user": "charlie", "is_expired": True},
          "session4": {"user": "diana", "is_expired": False}
      }

      # Remove expired sessions
      expired = [sid for sid, data in sessions.items() if data["is_expired"]]
      for sid in expired:
          sessions.pop(sid)

      # Print remaining sessions
      print(sessions)

  - title: "Dictionary Aggregator"
    difficulty: advanced
    description: "Aggregate sales data from multiple sources, summing values for matching keys."
    starter_code: |
      source1 = {"apple": 100, "banana": 50, "orange": 75}
      source2 = {"banana": 30, "orange": 25, "grape": 40}
      source3 = {"apple": 50, "grape": 20, "mango": 60}

      def aggregate_sales(*sources):
          # Combine all sources, summing values for matching keys
          # Return the aggregated dictionary
          pass

      total = aggregate_sales(source1, source2, source3)
      for product, quantity in sorted(total.items()):
          print(f"{product}: {quantity}")

    expected_output: |
      apple: 150
      banana: 80
      grape: 60
      mango: 60
      orange: 100
    hints:
      - "Start with an empty result dictionary"
      - "Iterate through each source dictionary"
      - "Use get() with default 0 to add values"
    solution: |
      source1 = {"apple": 100, "banana": 50, "orange": 75}
      source2 = {"banana": 30, "orange": 25, "grape": 40}
      source3 = {"apple": 50, "grape": 20, "mango": 60}

      def aggregate_sales(*sources):
          # Combine all sources, summing values for matching keys
          result = {}
          for source in sources:
              for product, quantity in source.items():
                  result[product] = result.get(product, 0) + quantity
          return result

      total = aggregate_sales(source1, source2, source3)
      for product, quantity in sorted(total.items()):
          print(f"{product}: {quantity}")

  - title: "Deep Copy Validator"
    difficulty: advanced
    description: "Demonstrate the difference between shallow and deep copy by modifying nested structures."
    starter_code: |
      import copy

      original = {
          "name": "Project X",
          "members": ["Alice", "Bob"],
          "config": {"version": 1, "active": True}
      }

      # Create shallow and deep copies
      # Modify nested structures in each copy
      # Show that shallow copy affects original, deep copy doesn't

      def test_copies():
          pass

      test_copies()

    expected_output: |
      Original after shallow: {'name': 'Project X', 'members': ['Alice', 'Bob', 'Charlie'], 'config': {'version': 2, 'active': True}}
      Original after deep: {'name': 'Project X', 'members': ['Alice', 'Bob', 'Charlie'], 'config': {'version': 2, 'active': True}}
      Shallow: {'name': 'Project Y', 'members': ['Alice', 'Bob', 'Charlie'], 'config': {'version': 2, 'active': True}}
      Deep: {'name': 'Project Z', 'members': ['Alice', 'Bob', 'Charlie', 'Diana'], 'config': {'version': 3, 'active': False}}
    hints:
      - "Use .copy() for shallow copy and copy.deepcopy() for deep copy"
      - "Modify nested list and dict in both copies"
      - "Observe which changes affect the original"
    solution: |
      import copy

      original = {
          "name": "Project X",
          "members": ["Alice", "Bob"],
          "config": {"version": 1, "active": True}
      }

      def test_copies():
          # Create shallow and deep copies
          shallow = original.copy()

          # Modify shallow copy
          shallow["name"] = "Project Y"
          shallow["members"].append("Charlie")
          shallow["config"]["version"] = 2

          print(f"Original after shallow: {original}")

          # Create deep copy
          deep = copy.deepcopy(original)

          # Modify deep copy
          deep["name"] = "Project Z"
          deep["members"].append("Diana")
          deep["config"]["version"] = 3
          deep["config"]["active"] = False

          print(f"Original after deep: {original}")
          print(f"Shallow: {shallow}")
          print(f"Deep: {deep}")

      test_copies()
```
<!-- EXERCISE_END -->
