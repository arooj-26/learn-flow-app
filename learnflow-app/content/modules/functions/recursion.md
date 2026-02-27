# Recursion in Python

Recursion is a programming technique where a function calls itself to solve a problem by breaking it down into smaller, similar sub-problems. Understanding recursion is essential for solving certain types of problems elegantly, particularly those involving tree structures, mathematical sequences, and divide-and-conquer algorithms.

## Basic Recursion Concepts

A recursive function must have two essential components:

```python
def countdown(n):
    """Simple recursive countdown."""
    # Base case - stops recursion
    if n <= 0:
        print("Blast off!")
        return

    # Recursive case
    print(n)
    countdown(n - 1)  # Function calls itself

countdown(5)
# Output:
# 5
# 4
# 3
# 2
# 1
# Blast off!

# Factorial: Classic recursion example
def factorial(n):
    """Calculate n! recursively."""
    # Base case
    if n == 0 or n == 1:
        return 1

    # Recursive case: n! = n * (n-1)!
    return n * factorial(n - 1)

print(factorial(5))  # 120 (5 * 4 * 3 * 2 * 1)
print(factorial(0))  # 1
```

## Recursion Components Table

| Component | Description | Example | Required |
|-----------|-------------|---------|----------|
| Base Case | Condition to stop recursion | `if n == 0: return 1` | Yes |
| Recursive Case | Function calling itself | `return n * factorial(n-1)` | Yes |
| Progress Toward Base | Each call gets closer to base case | `n - 1` decreases | Yes |
| Return Value | What function returns | Result of computation | Usually |

## Recursion vs Iteration

Compare recursive and iterative solutions:

```python
# Recursive sum
def recursive_sum(numbers):
    """Sum list recursively."""
    # Base case: empty list
    if not numbers:
        return 0

    # Recursive case: first element + sum of rest
    return numbers[0] + recursive_sum(numbers[1:])

# Iterative sum
def iterative_sum(numbers):
    """Sum list iteratively."""
    total = 0
    for num in numbers:
        total += num
    return total

nums = [1, 2, 3, 4, 5]
print(recursive_sum(nums))  # 15
print(iterative_sum(nums))  # 15

# Recursive vs Iterative Fibonacci
def fibonacci_recursive(n):
    """Fibonacci using recursion (inefficient)."""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def fibonacci_iterative(n):
    """Fibonacci using iteration (efficient)."""
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

print(fibonacci_recursive(7))  # 13
print(fibonacci_iterative(7))  # 13
```

## Tree Recursion

Recursion excels with tree-like structures:

```python
# Binary search (divide and conquer)
def binary_search(arr, target, left=0, right=None):
    """Search for target in sorted array recursively."""
    if right is None:
        right = len(arr) - 1

    # Base case: element not found
    if left > right:
        return -1

    # Find middle
    mid = (left + right) // 2

    # Base case: found target
    if arr[mid] == target:
        return mid

    # Recursive cases: search left or right half
    if arr[mid] > target:
        return binary_search(arr, target, left, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, right)

sorted_list = [1, 3, 5, 7, 9, 11, 13, 15]
print(binary_search(sorted_list, 7))   # 3
print(binary_search(sorted_list, 15))  # 7
print(binary_search(sorted_list, 4))   # -1

# Directory tree traversal (recursive)
def print_directory_tree(path, prefix=""):
    """Print directory structure recursively."""
    import os

    # Base case is handled by for loop ending
    if os.path.isfile(path):
        print(f"{prefix}{os.path.basename(path)}")
        return

    print(f"{prefix}{os.path.basename(path)}/")

    # Recursive case: process subdirectories
    try:
        items = os.listdir(path)
        for item in items:
            item_path = os.path.join(path, item)
            print_directory_tree(item_path, prefix + "  ")
    except PermissionError:
        print(f"{prefix}  [Permission Denied]")

# Usage: print_directory_tree("/path/to/directory")
```

## Recursion with Lists and Strings

Recursion naturally handles sequence processing:

```python
# Reverse a string recursively
def reverse_string(s):
    """Reverse string using recursion."""
    # Base case: empty or single character
    if len(s) <= 1:
        return s

    # Recursive case: last char + reverse of rest
    return s[-1] + reverse_string(s[:-1])

print(reverse_string("hello"))  # olleh
print(reverse_string("Python"))  # nohtyP

# Flatten nested list
def flatten(nested_list):
    """Flatten a nested list recursively."""
    result = []

    for item in nested_list:
        if isinstance(item, list):
            # Recursive case: flatten sub-list
            result.extend(flatten(item))
        else:
            # Base case: add non-list item
            result.append(item)

    return result

nested = [1, [2, 3], [4, [5, 6]], 7]
print(flatten(nested))  # [1, 2, 3, 4, 5, 6, 7]

# Count occurrences in nested structure
def count_item(nested, target):
    """Count occurrences of target in nested list."""
    count = 0

    for item in nested:
        if isinstance(item, list):
            # Recursive case
            count += count_item(item, target)
        elif item == target:
            # Base case: found target
            count += 1

    return count

nested = [1, 2, [3, 1, [1, 4]], 1, 5]
print(count_item(nested, 1))  # 4
```

## Advanced Recursion Patterns

More sophisticated recursive techniques:

```python
# Memoization to optimize recursion
def fibonacci_memo(n, memo={}):
    """Fibonacci with memoization."""
    if n in memo:
        return memo[n]

    if n <= 1:
        return n

    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]

print(fibonacci_memo(50))  # Fast! 12586269025

# Tower of Hanoi
def hanoi(n, source, target, auxiliary):
    """Solve Tower of Hanoi puzzle."""
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return

    # Move n-1 disks from source to auxiliary
    hanoi(n - 1, source, auxiliary, target)

    # Move largest disk from source to target
    print(f"Move disk {n} from {source} to {target}")

    # Move n-1 disks from auxiliary to target
    hanoi(n - 1, auxiliary, target, source)

print("Tower of Hanoi solution for 3 disks:")
hanoi(3, 'A', 'C', 'B')

# Permutations of a list
def permutations(items):
    """Generate all permutations of items."""
    # Base case: single item
    if len(items) <= 1:
        return [items]

    result = []
    for i in range(len(items)):
        # Fix one item
        current = items[i]
        # Get permutations of remaining items
        remaining = items[:i] + items[i+1:]

        for perm in permutations(remaining):
            result.append([current] + perm)

    return result

perms = permutations([1, 2, 3])
for p in perms:
    print(p)
# Output: All 6 permutations of [1, 2, 3]
```

## Recursion Depth and Tail Recursion

Understanding limitations and optimization:

```python
import sys

# Check recursion limit
print(f"Recursion limit: {sys.getrecursionlimit()}")  # Usually 1000

# This will cause RecursionError
def infinite_recursion(n):
    """Don't do this!"""
    return infinite_recursion(n + 1)

# Uncomment to see error:
# infinite_recursion(0)

# Tail recursion (not optimized in Python, but good pattern)
def factorial_tail(n, accumulator=1):
    """Tail recursive factorial."""
    if n == 0:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)

print(factorial_tail(5))  # 120

# Convert tail recursion to iteration
def factorial_iterative(n):
    """Iterative version of tail recursive factorial."""
    accumulator = 1
    while n > 0:
        accumulator *= n
        n -= 1
    return accumulator

print(factorial_iterative(5))  # 120

# Deep recursion with iteration (when recursion would overflow)
def sum_range_recursive(start, end):
    """Sum range - can overflow with large ranges."""
    if start > end:
        return 0
    return start + sum_range_recursive(start + 1, end)

def sum_range_iterative(start, end):
    """Sum range - handles large ranges."""
    return sum(range(start, end + 1))

print(sum_range_recursive(1, 10))    # 55
print(sum_range_iterative(1, 1000))  # 500500 (recursion would be slow)
```

## When to Use Recursion

Best use cases and alternatives:

```python
# GOOD: Tree/graph traversal
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def tree_sum(node):
    """Sum all values in binary tree - recursion is natural."""
    if node is None:
        return 0
    return node.value + tree_sum(node.left) + tree_sum(node.right)

# GOOD: Divide and conquer algorithms
def merge_sort(arr):
    """Sort array using merge sort - recursive by nature."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    # Merge sorted halves
    return merge(left, right)

def merge(left, right):
    """Merge two sorted arrays."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

print(merge_sort([64, 34, 25, 12, 22, 11, 90]))
# [11, 12, 22, 25, 34, 64, 90]

# BAD: Simple iteration tasks
# Don't use recursion for simple loops
def print_numbers_recursive(n):
    """Unnecessary recursion."""
    if n > 0:
        print_numbers_recursive(n - 1)
        print(n)

# Use iteration instead:
def print_numbers_iterative(n):
    """Better approach."""
    for i in range(1, n + 1):
        print(i)
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Simple Countdown"
    difficulty: basic
    description: "Create a recursive function `countdown(n)` that prints numbers from n down to 1, then prints 'Done!'. Test with countdown(3)."
    starter_code: |
      # Create recursive countdown

    expected_output: |
      3
      2
      1
      Done!
    hints:
      - "Base case: if n <= 0"
      - "Print n, then call countdown(n - 1)"
    solution: |
      def countdown(n):
          if n <= 0:
              print("Done!")
              return
          print(n)
          countdown(n - 1)

      countdown(3)

  - title: "Recursive Sum"
    difficulty: basic
    description: "Create a recursive function `sum_to_n(n)` that returns sum of numbers from 1 to n. Test with sum_to_n(5)."
    starter_code: |
      # Create recursive sum

    expected_output: "15"
    hints:
      - "Base case: if n == 1, return 1"
      - "Recursive: return n + sum_to_n(n - 1)"
    solution: |
      def sum_to_n(n):
          if n == 1:
              return 1
          return n + sum_to_n(n - 1)

      print(sum_to_n(5))

  - title: "Power Function"
    difficulty: intermediate
    description: "Create a recursive function `power(base, exp)` that calculates base^exp. Test with power(2, 5)."
    starter_code: |
      # Create recursive power function

    expected_output: "32"
    hints:
      - "Base case: if exp == 0, return 1"
      - "Recursive: base * power(base, exp - 1)"
    solution: |
      def power(base, exp):
          if exp == 0:
              return 1
          return base * power(base, exp - 1)

      print(power(2, 5))

  - title: "List Sum Recursive"
    difficulty: intermediate
    description: "Create a recursive function `list_sum(numbers)` that sums a list. Test with list_sum([1, 2, 3, 4, 5])."
    starter_code: |
      # Create recursive list sum

    expected_output: "15"
    hints:
      - "Base case: empty list returns 0"
      - "Recursive: first element + list_sum(rest)"
      - "Use numbers[0] and numbers[1:]"
    solution: |
      def list_sum(numbers):
          if not numbers:
              return 0
          return numbers[0] + list_sum(numbers[1:])

      print(list_sum([1, 2, 3, 4, 5]))

  - title: "Fibonacci with Memoization"
    difficulty: advanced
    description: "Create `fibonacci(n, memo={})` that calculates nth Fibonacci number with memoization. Test with fibonacci(10)."
    starter_code: |
      # Create memoized Fibonacci

    expected_output: "55"
    hints:
      - "Check if n in memo first"
      - "Base case: n <= 1 returns n"
      - "Store result in memo before returning"
    solution: |
      def fibonacci(n, memo={}):
          if n in memo:
              return memo[n]
          if n <= 1:
              return n
          memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
          return memo[n]

      print(fibonacci(10))

  - title: "Flatten Nested List"
    difficulty: advanced
    description: "Create a recursive function `flatten(nested)` that flattens a nested list. Test with flatten([1, [2, 3], [4, [5, 6]]])."
    starter_code: |
      # Create recursive flatten function

    expected_output: "[1, 2, 3, 4, 5, 6]"
    hints:
      - "Loop through items in nested list"
      - "Check if item is a list with isinstance(item, list)"
      - "If list, recursively flatten and extend result"
      - "If not list, append to result"
    solution: |
      def flatten(nested):
          result = []
          for item in nested:
              if isinstance(item, list):
                  result.extend(flatten(item))
              else:
                  result.append(item)
          return result

      print(flatten([1, [2, 3], [4, [5, 6]]]))
```
<!-- EXERCISE_END -->
