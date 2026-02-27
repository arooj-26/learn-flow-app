# JSON Files

JSON (JavaScript Object Notation) is a lightweight data interchange format that's easy for humans to read and write, and easy for machines to parse and generate. Python's `json` module provides a simple interface for working with JSON data, making it ideal for configuration files, API responses, and data storage.

## Reading JSON Files

The `json.load()` function reads JSON from a file, while `json.loads()` parses JSON from a string. Both convert JSON data into Python objects (dictionaries, lists, etc.).

```python
import json

# Reading JSON from file
with open('config.json', 'r') as file:
    data = json.load(file)
    print(f"Type: {type(data)}")
    print(f"Data: {data}")

# Accessing JSON data
with open('user.json', 'r') as file:
    user = json.load(file)
    print(f"Name: {user['name']}")
    print(f"Email: {user['email']}")
    print(f"Age: {user.get('age', 'Not specified')}")

# Reading JSON string
json_string = '{"name": "Alice", "age": 30, "active": true}'
data = json.loads(json_string)
print(f"Parsed: {data}")

# Handling nested JSON
nested_json = '''
{
    "company": "TechCorp",
    "employees": [
        {"name": "Alice", "role": "Engineer"},
        {"name": "Bob", "role": "Designer"}
    ],
    "location": {
        "city": "San Francisco",
        "state": "CA"
    }
}
'''

data = json.loads(nested_json)
print(f"Company: {data['company']}")
print(f"First employee: {data['employees'][0]['name']}")
print(f"City: {data['location']['city']}")

# Safe JSON reading with error handling
def read_json_safe(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return None

data = read_json_safe('config.json')
if data:
    print(f"Successfully loaded: {data}")
```

## Writing JSON Files

The `json.dump()` function writes JSON to a file, while `json.dumps()` converts Python objects to JSON strings. Both handle Python data types automatically.

```python
import json

# Writing JSON to file
data = {
    'name': 'Alice',
    'age': 30,
    'email': 'alice@example.com',
    'active': True
}

with open('user.json', 'w') as file:
    json.dump(data, file)

# Writing with formatting (indentation)
with open('user_formatted.json', 'w') as file:
    json.dump(data, file, indent=4)

# Writing complex structures
company_data = {
    'company': 'TechCorp',
    'employees': [
        {'name': 'Alice', 'role': 'Engineer', 'salary': 120000},
        {'name': 'Bob', 'role': 'Designer', 'salary': 100000}
    ],
    'founded': 2020,
    'active': True
}

with open('company.json', 'w') as file:
    json.dump(company_data, file, indent=2)

# Converting to JSON string
json_string = json.dumps(data, indent=2)
print(json_string)

# Writing with sorted keys
with open('sorted.json', 'w') as file:
    json.dump(data, file, indent=2, sort_keys=True)

# Appending to JSON array
def append_to_json_array(filename, new_item):
    # Read existing data
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Append new item
    data.append(new_item)

    # Write back
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)

new_employee = {'name': 'Charlie', 'role': 'Manager'}
append_to_json_array('employees.json', new_employee)
```

## JSON Data Type Mapping

Understanding how Python types map to JSON types is crucial for working with JSON data effectively.

| Python Type | JSON Type | Example |
|-------------|-----------|---------|
| dict | object | `{"key": "value"}` |
| list, tuple | array | `[1, 2, 3]` |
| str | string | `"text"` |
| int, float | number | `42`, `3.14` |
| True | true | `true` |
| False | false | `false` |
| None | null | `null` |

```python
import json

# Demonstrating type conversions
python_data = {
    'string': 'Hello',
    'integer': 42,
    'float': 3.14,
    'boolean_true': True,
    'boolean_false': False,
    'null_value': None,
    'list': [1, 2, 3],
    'tuple': (4, 5, 6),  # Becomes array
    'nested_dict': {'key': 'value'}
}

json_string = json.dumps(python_data, indent=2)
print(json_string)

# Note: tuples become arrays
data = {'items': (1, 2, 3)}
json_str = json.dumps(data)
parsed = json.loads(json_str)
print(f"Original type: {type(data['items'])}")  # tuple
print(f"Parsed type: {type(parsed['items'])}")   # list

# Handling non-serializable types
from datetime import datetime

# This will fail
# data = {'timestamp': datetime.now()}
# json.dumps(data)  # TypeError

# Custom serialization
def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

data = {'timestamp': datetime.now()}
json_string = json.dumps(data, default=json_serial)
print(json_string)

# Custom deserialization
def parse_datetime(dct):
    for key, value in dct.items():
        try:
            dct[key] = datetime.fromisoformat(value)
        except (ValueError, AttributeError):
            pass
    return dct

parsed = json.loads(json_string, object_hook=parse_datetime)
print(f"Parsed timestamp: {parsed['timestamp']}")
```

## Advanced JSON Operations

JSON files often require advanced operations like merging, filtering, and updating specific fields while preserving structure.

```python
import json
from copy import deepcopy

# Merging JSON objects
def merge_json(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

        # Merge dictionaries (data2 overwrites data1)
        merged = {**data1, **data2}

        with open(output_file, 'w') as out:
            json.dump(merged, out, indent=2)

# Deep merging nested dictionaries
def deep_merge(dict1, dict2):
    result = deepcopy(dict1)
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result

config1 = {'database': {'host': 'localhost', 'port': 5432}}
config2 = {'database': {'user': 'admin'}, 'debug': True}
merged = deep_merge(config1, config2)
print(json.dumps(merged, indent=2))

# Filtering JSON data
def filter_json(filename, condition):
    with open(filename, 'r') as file:
        data = json.load(file)

        if isinstance(data, list):
            filtered = [item for item in data if condition(item)]
            return filtered
        return data

# Filter employees with salary > 100000
high_earners = filter_json('employees.json',
                           lambda emp: emp.get('salary', 0) > 100000)

# Updating specific fields
def update_json_field(filename, path, value):
    with open(filename, 'r') as file:
        data = json.load(file)

    # Navigate path (e.g., ['company', 'location', 'city'])
    current = data
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = value

    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)

# Update city in nested structure
update_json_field('company.json', ['location', 'city'], 'New York')

# Searching in JSON
def search_json(data, search_key, search_value):
    results = []

    def search_recursive(obj, path=''):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                if key == search_key and value == search_value:
                    results.append({'path': new_path, 'value': value})
                search_recursive(value, new_path)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                search_recursive(item, f"{path}[{i}]")

    search_recursive(data)
    return results

with open('company.json', 'r') as file:
    data = json.load(file)
    matches = search_json(data, 'role', 'Engineer')
    for match in matches:
        print(f"Found at {match['path']}: {match['value']}")
```

## JSON Schema Validation

While Python doesn't have built-in JSON schema validation, you can implement basic validation to ensure data integrity.

```python
import json

# Simple validation function
def validate_json_structure(data, schema):
    """
    Validate JSON data against a simple schema.
    Schema example: {'name': str, 'age': int, 'email': str}
    """
    for key, expected_type in schema.items():
        if key not in data:
            return False, f"Missing required field: {key}"
        if not isinstance(data[key], expected_type):
            return False, f"Field {key} should be {expected_type.__name__}"
    return True, "Valid"

# Define schema
user_schema = {
    'name': str,
    'age': int,
    'email': str,
    'active': bool
}

# Validate data
user_data = {
    'name': 'Alice',
    'age': 30,
    'email': 'alice@example.com',
    'active': True
}

is_valid, message = validate_json_structure(user_data, user_schema)
print(f"Validation: {message}")

# Advanced validation with nested structures
def validate_nested(data, schema):
    if isinstance(schema, dict):
        if not isinstance(data, dict):
            return False, f"Expected dict, got {type(data)}"
        for key, value_schema in schema.items():
            if key not in data:
                return False, f"Missing key: {key}"
            valid, msg = validate_nested(data[key], value_schema)
            if not valid:
                return False, f"{key}: {msg}"
        return True, "Valid"
    elif isinstance(schema, list):
        if not isinstance(data, list):
            return False, f"Expected list, got {type(data)}"
        if len(schema) > 0:
            for item in data:
                valid, msg = validate_nested(item, schema[0])
                if not valid:
                    return False, msg
        return True, "Valid"
    else:
        if not isinstance(data, schema):
            return False, f"Expected {schema}, got {type(data)}"
        return True, "Valid"

# Nested schema example
company_schema = {
    'company': str,
    'employees': [
        {
            'name': str,
            'role': str,
            'salary': int
        }
    ]
}

is_valid, message = validate_nested(company_data, company_schema)
print(f"Nested validation: {message}")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Parse JSON String"
    difficulty: basic
    description: "Parse a JSON string and extract specific values."
    starter_code: |
      import json

      json_str = '{"name": "Alice", "age": 30, "city": "NYC"}'

      # Parse and print name and city

    expected_output: |
      Name: Alice
      City: NYC
    hints:
      - "Use json.loads() to parse the string"
      - "Access dictionary keys to get values"
    solution: |
      import json

      json_str = '{"name": "Alice", "age": 30, "city": "NYC"}'

      data = json.loads(json_str)
      print(f"Name: {data['name']}")
      print(f"City: {data['city']}")

  - title: "Convert to JSON String"
    difficulty: basic
    description: "Convert a Python dictionary to a formatted JSON string."
    starter_code: |
      import json

      data = {
          'product': 'Laptop',
          'price': 999.99,
          'in_stock': True
      }

      # Convert to JSON with indentation

    expected_output: |
      {
        "product": "Laptop",
        "price": 999.99,
        "in_stock": true
      }
    hints:
      - "Use json.dumps() with indent parameter"
      - "Set indent=2 for formatting"
    solution: |
      import json

      data = {
          'product': 'Laptop',
          'price': 999.99,
          'in_stock': True
      }

      json_str = json.dumps(data, indent=2)
      print(json_str)

  - title: "Access Nested JSON"
    difficulty: intermediate
    description: "Parse nested JSON and extract values from different levels."
    starter_code: |
      import json

      json_data = '''
      {
          "user": {
              "name": "Bob",
              "contacts": {
                  "email": "bob@example.com",
                  "phone": "555-1234"
              }
          }
      }
      '''

      # Extract and print name, email, and phone

    expected_output: |
      Name: Bob
      Email: bob@example.com
      Phone: 555-1234
    hints:
      - "Parse with json.loads()"
      - "Access nested dictionaries with multiple brackets"
    solution: |
      import json

      json_data = '''
      {
          "user": {
              "name": "Bob",
              "contacts": {
                  "email": "bob@example.com",
                  "phone": "555-1234"
              }
          }
      }
      '''

      data = json.loads(json_data)
      print(f"Name: {data['user']['name']}")
      print(f"Email: {data['user']['contacts']['email']}")
      print(f"Phone: {data['user']['contacts']['phone']}")

  - title: "Filter JSON Array"
    difficulty: intermediate
    description: "Parse JSON array and filter items based on a condition."
    starter_code: |
      import json

      json_data = '''
      [
          {"name": "Alice", "score": 95},
          {"name": "Bob", "score": 87},
          {"name": "Charlie", "score": 92},
          {"name": "Diana", "score": 78}
      ]
      '''

      # Filter and print students with score >= 90

    expected_output: |
      Alice: 95
      Charlie: 92
    hints:
      - "Parse to get a list of dictionaries"
      - "Use list comprehension or for loop to filter"
      - "Check if score >= 90"
    solution: |
      import json

      json_data = '''
      [
          {"name": "Alice", "score": 95},
          {"name": "Bob", "score": 87},
          {"name": "Charlie", "score": 92},
          {"name": "Diana", "score": 78}
      ]
      '''

      students = json.loads(json_data)
      high_scorers = [s for s in students if s['score'] >= 90]

      for student in high_scorers:
          print(f"{student['name']}: {student['score']}")

  - title: "Merge JSON Objects"
    difficulty: advanced
    description: "Create a function that deep merges two JSON objects, preserving nested structures."
    starter_code: |
      import json

      def deep_merge_json(json1, json2):
          # Deep merge two JSON objects
          # json2 values override json1
          pass

      obj1 = {"a": 1, "b": {"c": 2, "d": 3}}
      obj2 = {"b": {"d": 4, "e": 5}, "f": 6}

    expected_output: |
      {
        "a": 1,
        "b": {
          "c": 2,
          "d": 4,
          "e": 5
        },
        "f": 6
      }
    hints:
      - "Recursively merge nested dictionaries"
      - "obj2 values should override obj1"
      - "Preserve keys that exist only in obj1"
    solution: |
      import json

      def deep_merge_json(json1, json2):
          result = json1.copy()
          for key, value in json2.items():
              if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                  result[key] = deep_merge_json(result[key], value)
              else:
                  result[key] = value
          return result

      obj1 = {"a": 1, "b": {"c": 2, "d": 3}}
      obj2 = {"b": {"d": 4, "e": 5}, "f": 6}

      merged = deep_merge_json(obj1, obj2)
      print(json.dumps(merged, indent=2))

  - title: "JSON Path Finder"
    difficulty: advanced
    description: "Create a function that finds all paths to a specific value in nested JSON."
    starter_code: |
      import json

      def find_paths(data, target_value, current_path=''):
          # Find all paths where value equals target_value
          # Return list of path strings
          pass

      data = {
          "a": 1,
          "b": {
              "c": 2,
              "d": {"e": 2}
          },
          "f": [1, 2, 3]
      }

      # Find all paths where value is 2

    expected_output: |
      b.c
      b.d.e
      f[1]
    hints:
      - "Recursively traverse the data structure"
      - "Track current path as you go deeper"
      - "Handle both dict and list structures"
    solution: |
      import json

      def find_paths(data, target_value, current_path=''):
          paths = []

          if isinstance(data, dict):
              for key, value in data.items():
                  new_path = f"{current_path}.{key}" if current_path else key
                  if value == target_value:
                      paths.append(new_path)
                  paths.extend(find_paths(value, target_value, new_path))
          elif isinstance(data, list):
              for i, item in enumerate(data):
                  new_path = f"{current_path}[{i}]"
                  if item == target_value:
                      paths.append(new_path)
                  paths.extend(find_paths(item, target_value, new_path))

          return paths

      data = {
          "a": 1,
          "b": {
              "c": 2,
              "d": {"e": 2}
          },
          "f": [1, 2, 3]
      }

      paths = find_paths(data, 2)
      for path in paths:
          print(path)
```
<!-- EXERCISE_END -->
