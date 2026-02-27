# Finally Block

The `finally` block is a critical component of Python's exception handling mechanism that ensures certain code executes regardless of whether an exception occurs. This is particularly important for cleanup operations like closing files, releasing network connections, or freeing system resources. Understanding when and how to use `finally` blocks is essential for writing robust, resource-safe applications.

Unlike `try` and `except` blocks that handle exceptions, the `finally` block is all about guaranteeing execution. Code in the `finally` block runs whether an exception is raised or not, whether an exception is caught or not, and even when a `return` statement is executed in the `try` or `except` blocks.

## Basic Finally Block Usage

The `finally` block always executes after the `try` and `except` blocks, making it ideal for cleanup operations:

```python
def read_file_content(filename):
    file = None
    try:
        file = open(filename, 'r')
        content = file.read()
        print(f"File read successfully: {len(content)} characters")
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None
    except PermissionError:
        print(f"Error: No permission to read '{filename}'")
        return None
    finally:
        if file:
            file.close()
            print("File closed")

# Test
content = read_file_content("example.txt")
print(f"Content: {content}")
```

The `finally` block ensures the file is closed even if an exception occurs during reading, preventing resource leaks.

## Finally with Context Managers

While `finally` is powerful, Python's context managers (using `with` statements) provide a cleaner alternative for resource management:

```python
# Using finally
def process_file_with_finally(filename):
    file = None
    try:
        file = open(filename, 'r')
        data = file.read()
        return len(data)
    except Exception as e:
        print(f"Error: {e}")
        return 0
    finally:
        if file:
            file.close()

# Using context manager (preferred)
def process_file_with_context(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
            return len(data)
    except Exception as e:
        print(f"Error: {e}")
        return 0

# Both approaches ensure file closure
result1 = process_file_with_finally("test.txt")
result2 = process_file_with_context("test.txt")
```

Comparison of cleanup approaches:

| Method | Use Case | Advantages | Disadvantages |
|--------|----------|------------|---------------|
| `finally` block | Complex cleanup logic | Explicit control, works anywhere | More verbose, manual cleanup |
| Context managers | File/connection handling | Cleaner syntax, automatic cleanup | Less flexible for complex scenarios |
| Try-except only | No cleanup needed | Simplest approach | No guaranteed cleanup |
| Destructors (`__del__`) | Object cleanup | Automatic on garbage collection | Timing unpredictable |

## Execution Flow with Finally

The `finally` block executes in all scenarios, even with return statements:

```python
def test_finally_flow(scenario):
    """Demonstrates when finally executes"""
    print(f"\n--- Scenario: {scenario} ---")

    try:
        print("1. Try block starts")

        if scenario == "success":
            print("2. No exception, completing normally")
            return "Success"

        elif scenario == "handled_exception":
            print("2. Raising ValueError")
            raise ValueError("This will be caught")

        elif scenario == "unhandled_exception":
            print("2. Raising KeyError")
            raise KeyError("This won't be caught")

    except ValueError as e:
        print(f"3. Caught ValueError: {e}")
        return "Handled"

    finally:
        print("4. Finally block executes")

# Test different scenarios
result1 = test_finally_flow("success")
print(f"Result: {result1}")

result2 = test_finally_flow("handled_exception")
print(f"Result: {result2}")

try:
    result3 = test_finally_flow("unhandled_exception")
except KeyError as e:
    print(f"Caught outside: {e}")
```

Key execution flow rules:

1. `finally` executes after `try` completes normally
2. `finally` executes after `except` handles an exception
3. `finally` executes even when `return` is in `try` or `except`
4. `finally` executes before unhandled exceptions propagate
5. `finally` executes even if the `try` block has a `break`, `continue`, or `return`

## Practical Applications

Here's a comprehensive example showing real-world usage of `finally` blocks in a database connection manager:

```python
class DatabaseConnection:
    """Simulated database connection"""

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connected = False
        self.transaction_active = False

    def connect(self):
        print(f"Connecting to {self.connection_string}...")
        if "invalid" in self.connection_string:
            raise ConnectionError("Invalid connection string")
        self.connected = True
        print("Connected successfully")

    def begin_transaction(self):
        if not self.connected:
            raise RuntimeError("Not connected to database")
        print("Transaction started")
        self.transaction_active = True

    def execute_query(self, query):
        if not self.transaction_active:
            raise RuntimeError("No active transaction")
        print(f"Executing: {query}")

        if "error" in query.lower():
            raise ValueError("Query contains errors")

        return f"Query executed: {query}"

    def commit(self):
        if self.transaction_active:
            print("Committing transaction")
            self.transaction_active = False

    def rollback(self):
        if self.transaction_active:
            print("Rolling back transaction")
            self.transaction_active = False

    def disconnect(self):
        if self.connected:
            print("Disconnecting from database")
            self.connected = False

def execute_database_operation(connection_string, queries):
    """
    Execute database operations with proper cleanup in finally block.
    """
    db = None
    results = []

    try:
        # Initialize connection
        db = DatabaseConnection(connection_string)
        db.connect()
        db.begin_transaction()

        # Execute queries
        for query in queries:
            result = db.execute_query(query)
            results.append(result)

        # Commit if all succeeded
        db.commit()
        print("All operations completed successfully")
        return True, results

    except ConnectionError as e:
        print(f"Connection error: {e}")
        return False, []

    except ValueError as e:
        print(f"Query error: {e}")
        if db:
            db.rollback()
        return False, results

    except Exception as e:
        print(f"Unexpected error: {e}")
        if db:
            db.rollback()
        return False, results

    finally:
        # Cleanup always happens
        print("\n--- Cleanup in finally block ---")
        if db:
            if db.transaction_active:
                print("Warning: Transaction still active, rolling back")
                db.rollback()
            db.disconnect()
        print("Cleanup completed\n")

# Test cases
print("=== Test 1: Successful operation ===")
success, results = execute_database_operation(
    "valid_connection",
    ["SELECT * FROM users", "UPDATE users SET active=1"]
)
print(f"Success: {success}, Results: {len(results)}")

print("\n=== Test 2: Query error ===")
success, results = execute_database_operation(
    "valid_connection",
    ["SELECT * FROM users", "ERROR query", "UPDATE users"]
)
print(f"Success: {success}, Results: {len(results)}")

print("\n=== Test 3: Connection error ===")
success, results = execute_database_operation(
    "invalid_connection",
    ["SELECT * FROM users"]
)
print(f"Success: {success}, Results: {len(results)}")
```

## Advanced Finally Patterns

Complex scenarios requiring multiple cleanup operations:

```python
import time

class ResourceManager:
    """Manages multiple resources with guaranteed cleanup"""

    def __init__(self):
        self.resources = []
        self.locks = []
        self.temp_files = []

    def acquire_resource(self, resource_id):
        print(f"Acquiring resource: {resource_id}")
        self.resources.append(resource_id)

    def acquire_lock(self, lock_id):
        print(f"Acquiring lock: {lock_id}")
        self.locks.append(lock_id)

    def create_temp_file(self, filename):
        print(f"Creating temp file: {filename}")
        self.temp_files.append(filename)

    def release_all(self):
        """Release all resources in reverse order"""
        print("\n--- Releasing resources ---")

        # Release in reverse order of acquisition
        for temp_file in reversed(self.temp_files):
            print(f"Deleting temp file: {temp_file}")

        for lock in reversed(self.locks):
            print(f"Releasing lock: {lock}")

        for resource in reversed(self.resources):
            print(f"Releasing resource: {resource}")

        # Clear all lists
        self.resources.clear()
        self.locks.clear()
        self.temp_files.clear()

def complex_operation(should_fail=False):
    """
    Demonstrates proper cleanup with multiple resources.
    """
    manager = ResourceManager()

    try:
        print("Starting complex operation...")

        # Acquire resources
        manager.acquire_resource("database_connection")
        manager.acquire_lock("table_lock_1")
        manager.create_temp_file("temp_data.tmp")

        # Simulate work
        print("Performing operations...")
        time.sleep(0.1)

        if should_fail:
            raise RuntimeError("Operation failed during processing")

        manager.acquire_lock("table_lock_2")
        manager.create_temp_file("temp_results.tmp")

        print("Operations completed successfully")
        return True

    except RuntimeError as e:
        print(f"Error during operation: {e}")
        return False

    finally:
        # Guaranteed cleanup regardless of success or failure
        manager.release_all()
        print("Cleanup completed")

# Test
print("=== Test 1: Successful operation ===")
result = complex_operation(should_fail=False)
print(f"Result: {result}\n")

print("=== Test 2: Failed operation ===")
result = complex_operation(should_fail=True)
print(f"Result: {result}")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "File Writer with Cleanup"
    difficulty: basic
    description: "Create a function that writes to a file and ensures the file is closed using a finally block."
    starter_code: |
      def write_to_file(filename, content):
          # Your code here
          pass

      # Test
      write_to_file("test.txt", "Hello, World!")

    expected_output: |
      Writing to file: test.txt
      Write successful
      File closed in finally block

    hints:
      - "Open the file in the try block"
      - "Write content and print success message"
      - "Close the file in the finally block"
    solution: |
      def write_to_file(filename, content):
          file = None
          try:
              print(f"Writing to file: {filename}")
              file = open(filename, 'w')
              file.write(content)
              print("Write successful")
          except Exception as e:
              print(f"Error: {e}")
          finally:
              if file:
                  file.close()
                  print("File closed in finally block")

      # Test
      write_to_file("test.txt", "Hello, World!")

  - title: "Counter with Finally"
    difficulty: basic
    description: "Create a function that increments a counter in a finally block to track how many times it's called."
    starter_code: |
      call_count = 0

      def process_with_counter(value):
          # Your code here
          pass

      # Test
      process_with_counter(10)
      process_with_counter(0)
      process_with_counter("invalid")
      print(f"Total calls: {call_count}")

    expected_output: |
      Processing: 10
      Result: 100
      Processing: 0
      Error: Cannot divide by zero
      Processing: invalid
      Error: Invalid type
      Total calls: 3

    hints:
      - "Use global keyword to modify call_count"
      - "Increment counter in finally block"
      - "Handle different exceptions in except blocks"
    solution: |
      call_count = 0

      def process_with_counter(value):
          global call_count
          try:
              print(f"Processing: {value}")
              result = 100 / value
              print(f"Result: {result}")
          except ZeroDivisionError:
              print("Error: Cannot divide by zero")
          except TypeError:
              print("Error: Invalid type")
          finally:
              call_count += 1

      # Test
      process_with_counter(10)
      process_with_counter(0)
      process_with_counter("invalid")
      print(f"Total calls: {call_count}")

  - title: "Connection Manager"
    difficulty: intermediate
    description: "Build a connection manager that ensures disconnection in the finally block."
    starter_code: |
      class Connection:
          def __init__(self, host):
              self.host = host
              self.connected = False

          def connect(self):
              print(f"Connecting to {self.host}")
              if "invalid" in self.host:
                  raise ValueError("Invalid host")
              self.connected = True
              print("Connected")

          def send_data(self, data):
              if not self.connected:
                  raise RuntimeError("Not connected")
              print(f"Sending: {data}")

          def disconnect(self):
              if self.connected:
                  print("Disconnecting")
                  self.connected = False

      def send_message(host, message):
          # Your code here
          pass

      # Test
      send_message("valid_host", "Hello")
      send_message("invalid_host", "Hello")

    expected_output: |
      Connecting to valid_host
      Connected
      Sending: Hello
      Disconnecting
      Connecting to invalid_host
      Error: Invalid host
      Cleanup complete

    hints:
      - "Create Connection instance in try block"
      - "Call connect() and send_data() in try"
      - "Always call disconnect() in finally"
      - "Handle exceptions appropriately"
    solution: |
      class Connection:
          def __init__(self, host):
              self.host = host
              self.connected = False

          def connect(self):
              print(f"Connecting to {self.host}")
              if "invalid" in self.host:
                  raise ValueError("Invalid host")
              self.connected = True
              print("Connected")

          def send_data(self, data):
              if not self.connected:
                  raise RuntimeError("Not connected")
              print(f"Sending: {data}")

          def disconnect(self):
              if self.connected:
                  print("Disconnecting")
                  self.connected = False

      def send_message(host, message):
          conn = None
          try:
              conn = Connection(host)
              conn.connect()
              conn.send_data(message)
          except ValueError as e:
              print(f"Error: {e}")
          except RuntimeError as e:
              print(f"Error: {e}")
          finally:
              if conn:
                  conn.disconnect()
              print("Cleanup complete")

      # Test
      send_message("valid_host", "Hello")
      send_message("invalid_host", "Hello")

  - title: "Transaction Manager"
    difficulty: intermediate
    description: "Create a transaction manager that commits on success and rolls back on failure, with cleanup in finally."
    starter_code: |
      class Transaction:
          def __init__(self):
              self.active = False
              self.operations = []

          def begin(self):
              print("Transaction started")
              self.active = True

          def add_operation(self, op):
              if not self.active:
                  raise RuntimeError("No active transaction")
              print(f"Adding operation: {op}")
              if "error" in op:
                  raise ValueError("Invalid operation")
              self.operations.append(op)

          def commit(self):
              if self.active:
                  print(f"Committing {len(self.operations)} operations")
                  self.active = False

          def rollback(self):
              if self.active:
                  print(f"Rolling back {len(self.operations)} operations")
                  self.operations.clear()
                  self.active = False

      def execute_transaction(operations):
          # Your code here
          pass

      # Test
      execute_transaction(["op1", "op2", "op3"])
      execute_transaction(["op1", "error_op", "op3"])

    expected_output: |
      Transaction started
      Adding operation: op1
      Adding operation: op2
      Adding operation: op3
      Committing 3 operations
      Transaction closed
      Transaction started
      Adding operation: op1
      Adding operation: error_op
      Error occurred: Invalid operation
      Rolling back 1 operations
      Transaction closed

    hints:
      - "Begin transaction in try block"
      - "Add operations in a loop"
      - "Commit if no exceptions occur"
      - "Rollback in except block"
      - "Ensure transaction is closed in finally"
    solution: |
      class Transaction:
          def __init__(self):
              self.active = False
              self.operations = []

          def begin(self):
              print("Transaction started")
              self.active = True

          def add_operation(self, op):
              if not self.active:
                  raise RuntimeError("No active transaction")
              print(f"Adding operation: {op}")
              if "error" in op:
                  raise ValueError("Invalid operation")
              self.operations.append(op)

          def commit(self):
              if self.active:
                  print(f"Committing {len(self.operations)} operations")
                  self.active = False

          def rollback(self):
              if self.active:
                  print(f"Rolling back {len(self.operations)} operations")
                  self.operations.clear()
                  self.active = False

      def execute_transaction(operations):
          trans = Transaction()
          try:
              trans.begin()
              for op in operations:
                  trans.add_operation(op)
              trans.commit()
          except ValueError as e:
              print(f"Error occurred: {e}")
              trans.rollback()
          finally:
              print("Transaction closed")

      # Test
      execute_transaction(["op1", "op2", "op3"])
      execute_transaction(["op1", "error_op", "op3"])

  - title: "Resource Pool Manager"
    difficulty: advanced
    description: "Build a resource pool that tracks acquired resources and ensures all are released in finally, even if some releases fail."
    starter_code: |
      class ResourcePool:
          def __init__(self):
              self.acquired = []

          def acquire(self, resource_id):
              print(f"Acquiring: {resource_id}")
              self.acquired.append(resource_id)
              if "fail" in resource_id:
                  raise RuntimeError(f"Failed to acquire {resource_id}")

          def release(self, resource_id):
              print(f"Releasing: {resource_id}")
              if "error" in resource_id:
                  raise RuntimeError(f"Failed to release {resource_id}")

          def release_all(self):
              # Your code here to release all resources
              pass

      def use_resources(resource_ids):
          # Your code here
          pass

      # Test
      use_resources(["res1", "res2", "res3"])
      use_resources(["res1", "res_fail", "res3"])
      use_resources(["res1", "res_error", "res3"])

    expected_output: |
      Acquiring: res1
      Acquiring: res2
      Acquiring: res3
      Using resources...
      Releasing: res3
      Releasing: res2
      Releasing: res1
      All resources released
      Acquiring: res1
      Acquire failed: Failed to acquire res_fail
      Releasing: res1
      All resources released
      Acquiring: res1
      Acquiring: res_error
      Acquiring: res3
      Using resources...
      Releasing: res3
      Releasing: res_error
      Failed to release: res_error
      Releasing: res1
      All resources released

    hints:
      - "Acquire resources in try block"
      - "Release in reverse order in finally"
      - "Handle release failures gracefully"
      - "Continue releasing even if one fails"
    solution: |
      class ResourcePool:
          def __init__(self):
              self.acquired = []

          def acquire(self, resource_id):
              print(f"Acquiring: {resource_id}")
              self.acquired.append(resource_id)
              if "fail" in resource_id:
                  raise RuntimeError(f"Failed to acquire {resource_id}")

          def release(self, resource_id):
              print(f"Releasing: {resource_id}")
              if "error" in resource_id:
                  raise RuntimeError(f"Failed to release {resource_id}")

          def release_all(self):
              for resource in reversed(self.acquired):
                  try:
                      self.release(resource)
                  except RuntimeError as e:
                      print(f"Failed to release: {resource}")
              self.acquired.clear()

      def use_resources(resource_ids):
          pool = ResourcePool()
          try:
              for res_id in resource_ids:
                  pool.acquire(res_id)
              print("Using resources...")
          except RuntimeError as e:
              print(f"Acquire failed: {e}")
          finally:
              pool.release_all()
              print("All resources released")

      # Test
      use_resources(["res1", "res2", "res3"])
      use_resources(["res1", "res_fail", "res3"])
      use_resources(["res1", "res_error", "res3"])

  - title: "Logging Context Manager"
    difficulty: advanced
    description: "Create a logging context that tracks execution time and logs entry/exit, even when exceptions occur."
    starter_code: |
      import time

      class ExecutionLogger:
          def __init__(self, operation_name):
              self.operation_name = operation_name
              self.start_time = None
              self.success = False

          def __enter__(self):
              # Your code here
              pass

          def __exit__(self, exc_type, exc_val, exc_tb):
              # Your code here
              pass

      def perform_operation(name, should_fail=False):
          # Your code here using ExecutionLogger
          pass

      # Test
      perform_operation("task1", False)
      perform_operation("task2", True)

    expected_output: |
      [START] task1
      Executing task1
      [END] task1 - Status: SUCCESS - Duration: 0.10s
      [START] task2
      Executing task2
      Operation failed!
      [END] task2 - Status: FAILED - Duration: 0.10s

    hints:
      - "Record start time in __enter__"
      - "Calculate duration in __exit__"
      - "Check exc_type to determine if exception occurred"
      - "Use with statement to use the context manager"
      - "Return False from __exit__ to propagate exceptions"
    solution: |
      import time

      class ExecutionLogger:
          def __init__(self, operation_name):
              self.operation_name = operation_name
              self.start_time = None
              self.success = False

          def __enter__(self):
              print(f"[START] {self.operation_name}")
              self.start_time = time.time()
              return self

          def __exit__(self, exc_type, exc_val, exc_tb):
              duration = time.time() - self.start_time
              status = "SUCCESS" if exc_type is None else "FAILED"
              print(f"[END] {self.operation_name} - Status: {status} - Duration: {duration:.2f}s")
              return False

      def perform_operation(name, should_fail=False):
          with ExecutionLogger(name):
              print(f"Executing {name}")
              time.sleep(0.1)
              if should_fail:
                  print("Operation failed!")
                  raise RuntimeError("Operation failed")

      # Test
      perform_operation("task1", False)
      try:
          perform_operation("task2", True)
      except RuntimeError:
          pass
```
<!-- EXERCISE_END -->
