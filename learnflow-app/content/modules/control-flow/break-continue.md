# Break and Continue

The `break` and `continue` statements provide fine-grained control over loop execution in Python. While loops naturally iterate through all elements or until a condition is met, these control statements allow you to exit loops early (`break`) or skip specific iterations (`continue`), enabling more sophisticated and efficient loop behavior.

## The Break Statement: Early Loop Termination

The `break` statement immediately exits the innermost loop it's in, regardless of the loop's condition. This is useful when you've found what you're looking for or encountered a condition that makes further iteration unnecessary.

```python
# Basic break usage in for loop
numbers = [1, 5, 8, 12, 15, 20, 25]
target = 12

for num in numbers:
    if num == target:
        print(f"Found {target}!")
        break
    print(f"Checking {num}...")

print("Search complete")

# Break in while loop - search until found
def find_divisor(number):
    """Find the first divisor of a number (other than 1)"""
    divisor = 2

    while divisor < number:
        if number % divisor == 0:
            print(f"Found divisor: {divisor}")
            break
        divisor += 1
    else:
        # This else executes only if loop completes without break
        print(f"{number} is prime")

find_divisor(15)  # Composite number
find_divisor(17)  # Prime number

# Real-world example: Login system with max attempts
def authenticate_user(correct_password="secure123", max_attempts=3):
    """Allow user to login with limited attempts"""

    # Simulated password attempts
    attempts_list = ["wrong1", "wrong2", "secure123"]

    for attempt_num in range(1, max_attempts + 1):
        if attempt_num - 1 < len(attempts_list):
            password = attempts_list[attempt_num - 1]
        else:
            password = ""

        print(f"Attempt {attempt_num}/{max_attempts}")

        if password == correct_password:
            print("✅ Login successful!")
            return True
            # break would work here too, but return exits the function
        else:
            print("❌ Incorrect password")

    print("🔒 Account locked - too many failed attempts")
    return False

authenticate_user()

# Example: Processing data until error encountered
def process_data_batch(data):
    """Process data items until an error is encountered"""
    processed_count = 0

    for item in data:
        # Simulate processing
        if item < 0:  # Negative numbers are errors
            print(f"❌ Error encountered at item {item}")
            print(f"Processed {processed_count} items before error")
            break

        print(f"✓ Processed: {item}")
        processed_count += 1
    else:
        # Executes only if loop completed without break
        print(f"✅ All {processed_count} items processed successfully")

process_data_batch([10, 20, 30, -5, 40, 50])
print()
process_data_batch([10, 20, 30, 40, 50])

# Example: File search in directory structure
def search_file(filename, directories):
    """Search for a file in multiple directories"""

    for directory in directories:
        print(f"Searching in {directory}...")

        # Simulate file check
        if filename in directory:
            print(f"📁 Found '{filename}' in {directory}")
            return directory
            # Could use break if not returning

    print(f"❌ '{filename}' not found in any directory")
    return None

dirs = ["/home/user/documents", "/home/user/downloads", "/home/user/pictures/vacation"]
search_file("vacation", dirs)
```

## The Continue Statement: Skipping Iterations

The `continue` statement skips the rest of the current iteration and moves to the next iteration of the loop. This is useful for filtering out unwanted values or skipping processing based on conditions.

```python
# Basic continue usage - skip even numbers
for num in range(1, 11):
    if num % 2 == 0:
        continue  # Skip even numbers
    print(f"{num} is odd")

# Process only valid data
def process_scores(scores):
    """Calculate average of valid scores (0-100)"""
    total = 0
    valid_count = 0

    for score in scores:
        if score < 0 or score > 100:
            print(f"⚠️  Skipping invalid score: {score}")
            continue  # Skip invalid scores

        total += score
        valid_count += 1
        print(f"✓ Valid score: {score}")

    if valid_count > 0:
        average = total / valid_count
        print(f"\nAverage of {valid_count} valid scores: {average:.2f}")
    else:
        print("\nNo valid scores to process")

process_scores([85, 92, -5, 78, 105, 88, 95])

# Example: Skip weekends in date processing
def count_business_days(days):
    """Count only weekdays (skip Saturday and Sunday)"""
    business_day_count = 0

    for day in days:
        if day in ["Saturday", "Sunday"]:
            print(f"Skipping {day} (weekend)")
            continue

        business_day_count += 1
        print(f"✓ {day} is a business day")

    print(f"\nTotal business days: {business_day_count}")

days_of_week = ["Monday", "Tuesday", "Wednesday", "Saturday", "Sunday", "Monday"]
count_business_days(days_of_week)

# Example: Filter and process user input
def process_user_comments(comments):
    """Process comments, skipping empty or spam comments"""
    processed = 0

    for i, comment in enumerate(comments, 1):
        # Skip empty comments
        if not comment.strip():
            print(f"Comment {i}: [Empty - skipped]")
            continue

        # Skip spam (comments with excessive punctuation)
        if comment.count('!') > 3:
            print(f"Comment {i}: [Spam detected - skipped]")
            continue

        # Process valid comment
        print(f"Comment {i}: {comment}")
        processed += 1

    print(f"\nProcessed {processed} valid comments")

comments = [
    "Great article!",
    "",
    "Thanks for sharing",
    "BUY NOW!!!!!",
    "Very helpful"
]
process_user_comments(comments)

# Continue in while loop
def clean_data_stream():
    """Process data stream, skipping corrupted entries"""
    data_stream = [100, None, 200, None, 300, 400, None, 500]
    index = 0
    processed = []

    while index < len(data_stream):
        value = data_stream[index]

        if value is None:
            print(f"Position {index}: Corrupted data - skipping")
            index += 1
            continue  # Skip to next iteration

        processed.append(value)
        print(f"Position {index}: Processed {value}")
        index += 1

    print(f"\nProcessed values: {processed}")
    return processed

clean_data_stream()
```

## Combining Break and Continue

Using break and continue together allows for complex loop control logic, handling multiple conditions and flow paths within a single loop.

```python
# Example 1: Data validation with multiple exit conditions
def validate_and_process_data(data, max_errors=3):
    """
    Process data with error tolerance
    - Skip invalid entries (continue)
    - Stop if too many errors (break)
    """
    error_count = 0
    processed_items = []

    for item in data:
        # Check for null/None values
        if item is None:
            print(f"⚠️  Null value - skipping")
            error_count += 1

            if error_count >= max_errors:
                print(f"❌ Too many errors ({error_count}) - stopping")
                break
            continue

        # Check for negative values
        if item < 0:
            print(f"⚠️  Negative value {item} - skipping")
            error_count += 1

            if error_count >= max_errors:
                print(f"❌ Too many errors ({error_count}) - stopping")
                break
            continue

        # Process valid item
        processed_items.append(item * 2)
        print(f"✓ Processed {item} → {item * 2}")

    print(f"\nResults: {len(processed_items)} items processed, {error_count} errors")
    return processed_items

data = [10, None, 20, -5, 30, None, -10, 40]
validate_and_process_data(data, max_errors=2)

# Example 2: Advanced search with filtering
def advanced_search(items, search_term, min_score=50, max_results=3):
    """
    Search items with score threshold and result limit
    - Continue: skip items below score threshold
    - Break: stop after finding max_results
    """
    results = []

    for item in items:
        name, score = item

        # Skip items below minimum score
        if score < min_score:
            print(f"⊘ {name} (score: {score}) - below threshold")
            continue

        # Check if item matches search term
        if search_term.lower() not in name.lower():
            print(f"⊘ {name} - doesn't match search")
            continue

        # Found a valid result
        results.append(item)
        print(f"✓ Found: {name} (score: {score})")

        # Stop if we have enough results
        if len(results) >= max_results:
            print(f"✓ Reached maximum results ({max_results})")
            break

    print(f"\nFound {len(results)} results")
    return results

products = [
    ("Python Programming Book", 85),
    ("Java Guide", 45),
    ("Python Course", 92),
    ("Python Basics", 60),
    ("JavaScript Tutorial", 70),
    ("Python Advanced", 88),
]

advanced_search(products, "Python", min_score=50, max_results=3)

# Example 3: Network packet processor
def process_network_packets(packets, max_malformed=5):
    """
    Process network packets with error handling
    """
    total_bytes = 0
    packet_count = 0
    malformed_count = 0

    for packet_num, packet in enumerate(packets, 1):
        packet_type, size, is_valid = packet

        print(f"\nPacket {packet_num}: {packet_type}")

        # Skip malformed packets
        if not is_valid:
            print(f"  ⚠️  Malformed packet - skipping")
            malformed_count += 1

            if malformed_count >= max_malformed:
                print(f"  ❌ Too many malformed packets - stopping")
                break
            continue

        # Skip zero-size packets
        if size == 0:
            print(f"  ⊘ Zero-size packet - skipping")
            continue

        # Process valid packet
        total_bytes += size
        packet_count += 1
        print(f"  ✓ Processed {size} bytes")

    print(f"\n=== Summary ===")
    print(f"Packets processed: {packet_count}")
    print(f"Total bytes: {total_bytes}")
    print(f"Malformed packets: {malformed_count}")

packets = [
    ("DATA", 1024, True),
    ("ACK", 64, True),
    ("DATA", 0, True),
    ("SYN", 128, False),
    ("DATA", 2048, True),
    ("FIN", 64, False),
    ("DATA", 512, False),
]

process_network_packets(packets, max_malformed=2)
```

## Nested Loops with Break and Continue

When working with nested loops, break and continue only affect the innermost loop they're in. Understanding this behavior is crucial for complex loop structures.

```python
# Break in nested loops - affects only inner loop
def find_in_matrix(matrix, target):
    """Search for value in 2D matrix"""
    found = False
    found_position = None

    for row_idx, row in enumerate(matrix):
        for col_idx, value in enumerate(row):
            if value == target:
                found_position = (row_idx, col_idx)
                found = True
                print(f"Found {target} at position {found_position}")
                break  # Only exits inner loop

        if found:
            break  # Need another break to exit outer loop

    if not found:
        print(f"{target} not found in matrix")

    return found_position

matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]

find_in_matrix(matrix, 7)

# Continue in nested loops
def print_multiplication_table(size=10, skip_number=5):
    """Print multiplication table, skipping rows with skip_number"""

    for i in range(1, size + 1):
        if i == skip_number:
            print(f"[Skipping row {skip_number}]")
            continue  # Skip entire row

        row = []
        for j in range(1, size + 1):
            if j == skip_number:
                continue  # Skip column in this row

            row.append(f"{i*j:3d}")

        print(f"{i}: {' '.join(row)}")

print_multiplication_table(5, skip_number=3)

# Complex example: Student grade processor
def process_student_grades(students):
    """
    Process student grades with various conditions
    - Skip students with incomplete data (continue)
    - Stop class if average is too low (break)
    """
    class_total = 0
    student_count = 0

    for student_name, grades in students.items():
        print(f"\nProcessing {student_name}:")

        # Skip students with no grades
        if not grades:
            print(f"  ⊘ No grades - skipping student")
            continue

        # Calculate student average
        valid_grades = []
        for grade in grades:
            # Skip invalid grades
            if grade < 0 or grade > 100:
                print(f"  ⊘ Invalid grade {grade} - skipping")
                continue

            valid_grades.append(grade)

        # Skip student if no valid grades
        if not valid_grades:
            print(f"  ⊘ No valid grades - skipping student")
            continue

        student_avg = sum(valid_grades) / len(valid_grades)
        print(f"  ✓ Average: {student_avg:.2f}")

        class_total += student_avg
        student_count += 1

    if student_count > 0:
        class_avg = class_total / student_count
        print(f"\n=== Class Average: {class_avg:.2f} ===")
    else:
        print("\n=== No students to process ===")

students = {
    "Alice": [85, 90, 92],
    "Bob": [],
    "Charlie": [78, 105, 82, -5, 88],
    "Diana": [95, 98, 96],
    "Eve": [150, -10, 200]
}

process_student_grades(students)
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Find First Negative"
    difficulty: basic
    description: "Write a program that loops through a list of numbers and stops when it finds the first negative number. Print that number."
    starter_code: |
      numbers = [5, 12, 8, -3, 15, 20]

      # Use a for loop with break

    expected_output: |
      Found first negative: -3
    hints:
      - "Loop through numbers with: for num in numbers:"
      - "Check if num < 0"
      - "Print the number and use break to exit"
    solution: |
      numbers = [5, 12, 8, -3, 15, 20]

      for num in numbers:
          if num < 0:
              print(f"Found first negative: {num}")
              break

  - title: "Skip Even Numbers"
    difficulty: basic
    description: "Create a program that prints only odd numbers from 1 to 10. Use continue to skip even numbers."
    starter_code: |
      # Loop from 1 to 10 and print only odd numbers

    expected_output: |
      1
      3
      5
      7
      9
    hints:
      - "Use for i in range(1, 11):"
      - "Check if i % 2 == 0 (even number)"
      - "Use continue to skip even numbers"
      - "Print i for odd numbers"
    solution: |
      for i in range(1, 11):
          if i % 2 == 0:
              continue
          print(i)

  - title: "Word Finder with Limit"
    difficulty: intermediate
    description: "Write a function that searches for a target word in a list of words. Stop after finding 2 occurrences. Count and print how many times it was found."
    starter_code: |
      def find_word(words, target, max_finds=2):
          # Write your code here
          pass

      # Test
      word_list = ["apple", "banana", "apple", "cherry", "apple", "date"]
      find_word(word_list, "apple", 2)

    expected_output: |
      Found 'apple' at position 0
      Found 'apple' at position 2
      Search stopped after finding 2 occurrences
    hints:
      - "Use a counter variable to track finds"
      - "Loop through words with enumerate to get position"
      - "When word matches target, print and increment counter"
      - "Use break when counter reaches max_finds"
    solution: |
      def find_word(words, target, max_finds=2):
          found_count = 0

          for i, word in enumerate(words):
              if word == target:
                  print(f"Found '{target}' at position {i}")
                  found_count += 1

                  if found_count >= max_finds:
                      print(f"Search stopped after finding {max_finds} occurrences")
                      break

      word_list = ["apple", "banana", "apple", "cherry", "apple", "date"]
      find_word(word_list, "apple", 2)

  - title: "Valid Email Counter"
    difficulty: intermediate
    description: "Create a function that counts valid emails (must contain '@' and '.'). Skip invalid emails with continue. Print each email's status and final count."
    starter_code: |
      def count_valid_emails(emails):
          # Write your code here
          pass

      # Test
      email_list = ["user@example.com", "invalid.email", "admin@site.org", "noatsign.com"]
      count_valid_emails(email_list)

    expected_output: |
      ✓ Valid: user@example.com
      ✗ Invalid: invalid.email
      ✓ Valid: admin@site.org
      ✗ Invalid: noatsign.com
      Total valid emails: 2
    hints:
      - "Check if '@' in email and '.' in email"
      - "If invalid, print invalid message and use continue"
      - "If valid, print valid message and increment counter"
      - "Print total count after loop"
    solution: |
      def count_valid_emails(emails):
          valid_count = 0

          for email in emails:
              if '@' not in email or '.' not in email:
                  print(f"✗ Invalid: {email}")
                  continue

              print(f"✓ Valid: {email}")
              valid_count += 1

          print(f"Total valid emails: {valid_count}")

      email_list = ["user@example.com", "invalid.email", "admin@site.org", "noatsign.com"]
      count_valid_emails(email_list)

  - title: "Grade Processor with Error Limit"
    difficulty: advanced
    description: "Build a function that processes student grades (0-100). Skip invalid grades (outside range) but stop if more than 2 invalid grades are found. Calculate average of valid grades."
    starter_code: |
      def process_grades(grades):
          # Write your code here
          pass

      # Test
      student_grades = [85, 92, -5, 78, 105, 88, 150]
      process_grades(student_grades)

    expected_output: |
      ✓ Valid grade: 85
      ✓ Valid grade: 92
      ✗ Invalid grade: -5 (skipped)
      ✓ Valid grade: 78
      ✗ Invalid grade: 105 (skipped)
      ✗ Invalid grade: 88 (skipped)
      Too many invalid grades. Stopping.
      Processed 3 valid grades, Average: 85.00
    hints:
      - "Track valid_grades list and invalid_count"
      - "Check if grade < 0 or grade > 100 for invalid"
      - "Use continue to skip invalid, but increment invalid_count first"
      - "Use break if invalid_count > 2"
      - "Calculate average from valid_grades list"
    solution: |
      def process_grades(grades):
          valid_grades = []
          invalid_count = 0

          for grade in grades:
              if grade < 0 or grade > 100:
                  print(f"✗ Invalid grade: {grade} (skipped)")
                  invalid_count += 1

                  if invalid_count > 2:
                      print("Too many invalid grades. Stopping.")
                      break
                  continue

              print(f"✓ Valid grade: {grade}")
              valid_grades.append(grade)

          if valid_grades:
              average = sum(valid_grades) / len(valid_grades)
              print(f"Processed {len(valid_grades)} valid grades, Average: {average:.2f}")
          else:
              print("No valid grades to process")

      student_grades = [85, 92, -5, 78, 105, 88, 150]
      process_grades(student_grades)

  - title: "Matrix Target Finder"
    difficulty: advanced
    description: "Create a function that searches a 2D matrix for a target value. When found, print the position (row, col) and stop searching completely (exit both loops). If not found, print not found message."
    starter_code: |
      def find_in_matrix(matrix, target):
          # Write your nested loop code here
          pass

      # Test
      grid = [
          [1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]
      ]
      find_in_matrix(grid, 5)
      print()
      find_in_matrix(grid, 10)

    expected_output: |
      Found 5 at position (1, 1)

      10 not found in matrix
    hints:
      - "Use nested loops: for row_idx, row in enumerate(matrix):"
      - "Inner loop: for col_idx, value in enumerate(row):"
      - "When value == target, print position and set found flag"
      - "Break inner loop, then check found flag and break outer loop"
      - "Use else clause on outer loop for not found message"
    solution: |
      def find_in_matrix(matrix, target):
          found = False

          for row_idx, row in enumerate(matrix):
              for col_idx, value in enumerate(row):
                  if value == target:
                      print(f"Found {target} at position ({row_idx}, {col_idx})")
                      found = True
                      break

              if found:
                  break
          else:
              if not found:
                  print(f"{target} not found in matrix")

      grid = [
          [1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]
      ]
      find_in_matrix(grid, 5)
      print()
      find_in_matrix(grid, 10)
```
<!-- EXERCISE_END -->
