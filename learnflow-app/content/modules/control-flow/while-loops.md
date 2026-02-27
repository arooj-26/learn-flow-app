# While Loops

While loops are fundamental control structures that execute a block of code repeatedly as long as a condition remains true. Unlike for loops that iterate over a sequence, while loops continue executing until their condition becomes false, making them ideal for situations where you don't know in advance how many iterations you'll need.

## Basic While Loop Syntax and Structure

A while loop consists of a condition and a code block. The condition is evaluated before each iteration, and if it's true, the code block executes. This continues until the condition becomes false.

```python
# Basic while loop structure
count = 0
while count < 5:
    print(f"Count is: {count}")
    count += 1  # Important: update the counter to avoid infinite loop

print("Loop finished")

# Countdown example
countdown = 10
while countdown > 0:
    print(f"T-minus {countdown}")
    countdown -= 1
print("Blast off!")

# User input validation loop
password = ""
while password != "secret":
    password = input("Enter password: ")
    if password != "secret":
        print("Incorrect password. Try again.")
print("Access granted!")

# Accumulator pattern with while loop
total = 0
number = 1
while number <= 10:
    total += number
    number += 1
print(f"Sum of numbers 1-10: {total}")

# Sentinel-controlled loop (stops on specific value)
def calculate_average():
    """Calculate average of numbers entered by user"""
    total = 0
    count = 0
    number = 0

    print("Enter numbers (enter -1 to stop):")
    while number != -1:
        number = float(input("Enter number: "))
        if number != -1:
            total += number
            count += 1

    if count > 0:
        average = total / count
        print(f"Average: {average:.2f}")
    else:
        print("No numbers entered")

# Note: Uncomment to test interactively
# calculate_average()
```

Key points about while loops:
- The condition is checked before each iteration
- You must update variables to eventually make the condition false
- Forgetting to update the condition can cause infinite loops
- While loops are perfect when you don't know the iteration count in advance

## Common While Loop Patterns

While loops are used in several common programming patterns. Understanding these patterns helps you recognize when to use while loops effectively.

```python
# Pattern 1: Counter-controlled loop (known number of iterations)
iteration = 1
max_iterations = 5
while iteration <= max_iterations:
    print(f"Iteration {iteration} of {max_iterations}")
    iteration += 1

# Pattern 2: Flag-controlled loop (loop until condition met)
found = False
search_list = [10, 25, 30, 45, 50]
target = 30
index = 0

while not found and index < len(search_list):
    if search_list[index] == target:
        found = True
        print(f"Found {target} at index {index}")
    else:
        index += 1

if not found:
    print(f"{target} not found in list")

# Pattern 3: Input validation loop
def get_valid_age():
    """Keep asking until valid age is entered"""
    age = -1
    while age < 0 or age > 120:
        try:
            age = int(input("Enter your age (0-120): "))
            if age < 0 or age > 120:
                print("Invalid age. Please try again.")
        except ValueError:
            print("Please enter a number.")
    return age

# Pattern 4: Menu-driven program
def display_menu():
    """Simple menu system using while loop"""
    choice = ""

    while choice != "4":
        print("\n=== Main Menu ===")
        print("1. View balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")

        choice = input("Select option (1-4): ")

        if choice == "1":
            print("Balance: $1,000")
        elif choice == "2":
            print("Deposit processed")
        elif choice == "3":
            print("Withdrawal processed")
        elif choice == "4":
            print("Thank you for banking with us!")
        else:
            print("Invalid option. Please try again.")

# Pattern 5: Processing until empty
def process_queue():
    """Process items from a queue"""
    queue = ["Task 1", "Task 2", "Task 3", "Task 4"]

    while queue:  # Continues while queue is not empty
        task = queue.pop(0)  # Remove first item
        print(f"Processing: {task}")
        print(f"Remaining tasks: {len(queue)}")

    print("All tasks completed!")

process_queue()

# Pattern 6: Retry with maximum attempts
def attempt_connection(max_retries=3):
    """Simulate connection attempts with retry limit"""
    attempts = 0
    connected = False

    while attempts < max_retries and not connected:
        attempts += 1
        print(f"Connection attempt {attempts} of {max_retries}...")

        # Simulate connection (would be actual connection logic)
        import random
        connected = random.choice([True, False])

        if connected:
            print("Connected successfully!")
        elif attempts < max_retries:
            print("Connection failed. Retrying...")
        else:
            print("Maximum retry attempts reached. Connection failed.")

    return connected

attempt_connection()
```

## While Loops with Complex Conditions

While loops can have complex conditions combining multiple boolean expressions. This allows for sophisticated control flow based on multiple factors.

```python
# Example 1: Game loop with multiple exit conditions
def simple_game():
    """Simple game that runs until player wins or runs out of lives"""
    lives = 3
    score = 0
    won = False

    print("=== Number Guessing Game ===")
    secret_number = 7

    while lives > 0 and not won:
        print(f"\nLives: {lives} | Score: {score}")

        try:
            guess = int(input("Guess a number (1-10): "))

            if guess == secret_number:
                won = True
                score += 100
                print(f"Correct! You won! Final score: {score}")
            elif guess < secret_number:
                print("Too low!")
                lives -= 1
                score -= 10
            else:
                print("Too high!")
                lives -= 1
                score -= 10
        except ValueError:
            print("Please enter a valid number")

    if lives == 0:
        print(f"Game Over! The number was {secret_number}")

# Example 2: Data validation with multiple criteria
def validate_username(username):
    """Validate username meets all criteria"""
    valid = False
    checks_passed = 0
    total_checks = 4

    while checks_passed < total_checks:
        if checks_passed == 0:
            if len(username) >= 5:
                checks_passed += 1
            else:
                print("❌ Username must be at least 5 characters")
                break

        elif checks_passed == 1:
            if username.isalnum():
                checks_passed += 1
            else:
                print("❌ Username must be alphanumeric")
                break

        elif checks_passed == 2:
            if not username[0].isdigit():
                checks_passed += 1
            else:
                print("❌ Username cannot start with a number")
                break

        elif checks_passed == 3:
            if username.lower() not in ['admin', 'root', 'system']:
                checks_passed += 1
            else:
                print("❌ Username is reserved")
                break

    if checks_passed == total_checks:
        print("✅ Username is valid!")
        valid = True

    return valid

validate_username("john123")

# Example 3: Resource monitoring loop
def monitor_resources(cpu_threshold=80, memory_threshold=75, duration=10):
    """Monitor system resources until threshold exceeded or duration met"""
    import random

    seconds_elapsed = 0
    alert_triggered = False

    print("Starting resource monitoring...")

    while seconds_elapsed < duration and not alert_triggered:
        # Simulate resource readings
        cpu_usage = random.randint(50, 95)
        memory_usage = random.randint(40, 90)

        print(f"\n[{seconds_elapsed}s] CPU: {cpu_usage}% | Memory: {memory_usage}%")

        if cpu_usage > cpu_threshold or memory_usage > memory_threshold:
            alert_triggered = True
            print("⚠️  ALERT: Resource threshold exceeded!")

            if cpu_usage > cpu_threshold:
                print(f"   CPU usage {cpu_usage}% exceeds {cpu_threshold}%")
            if memory_usage > memory_threshold:
                print(f"   Memory usage {memory_usage}% exceeds {memory_threshold}%")

        seconds_elapsed += 1

    if not alert_triggered:
        print(f"\nMonitoring complete. No alerts in {duration} seconds.")

monitor_resources(duration=5)

# Example 4: Simulated ATM withdrawal
def atm_withdrawal(account_balance=1000):
    """Process withdrawals with balance and limit checking"""
    daily_limit = 500
    withdrawn_today = 0
    session_active = True

    print(f"Account Balance: ${account_balance}")
    print(f"Daily Withdrawal Limit: ${daily_limit}")

    while session_active and account_balance > 0 and withdrawn_today < daily_limit:
        print(f"\nAvailable: ${account_balance}")
        print(f"Remaining daily limit: ${daily_limit - withdrawn_today}")

        try:
            amount = float(input("Enter amount to withdraw (0 to exit): "))

            if amount == 0:
                session_active = False
                print("Thank you for using our ATM")
            elif amount < 0:
                print("Invalid amount")
            elif amount > account_balance:
                print("Insufficient funds")
            elif withdrawn_today + amount > daily_limit:
                print(f"Would exceed daily limit by ${(withdrawn_today + amount) - daily_limit:.2f}")
            else:
                account_balance -= amount
                withdrawn_today += amount
                print(f"Dispensing ${amount:.2f}")
                print(f"New balance: ${account_balance:.2f}")

        except ValueError:
            print("Please enter a valid amount")

    if withdrawn_today >= daily_limit:
        print("\nDaily withdrawal limit reached")

    print(f"\nFinal balance: ${account_balance:.2f}")
    print(f"Total withdrawn today: ${withdrawn_today:.2f}")

# Note: Uncomment to test interactively
# atm_withdrawal()
```

## Infinite Loops and Loop Control

Understanding infinite loops and how to control loop execution with `break` and `continue` is crucial for effective while loop usage.

```python
# Infinite loop (intentional, controlled with break)
def server_simulation():
    """Simulate a server that runs until shutdown command"""
    print("Server starting...")

    request_count = 0

    while True:  # Infinite loop
        command = input("Enter command (status/shutdown): ")

        if command == "shutdown":
            print(f"Shutting down server. Processed {request_count} requests.")
            break  # Exit the infinite loop
        elif command == "status":
            print(f"Server running. Requests processed: {request_count}")
            request_count += 1
        else:
            print("Unknown command")

# Note: Uncomment to test interactively
# server_simulation()

# Using continue to skip iterations
def process_numbers():
    """Process only even numbers from user input"""
    numbers_processed = 0
    target_count = 5

    print(f"Enter {target_count} even numbers:")

    while numbers_processed < target_count:
        try:
            num = int(input(f"Enter even number ({numbers_processed + 1}/{target_count}): "))

            if num % 2 != 0:
                print("That's odd! Please enter an even number.")
                continue  # Skip rest of loop, go to next iteration

            print(f"✓ Accepted: {num}")
            numbers_processed += 1

        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

    print("All numbers collected!")

# Example: Password attempts with lockout
def login_system():
    """Login system with maximum attempts"""
    correct_password = "secure123"
    max_attempts = 3
    attempts = 0
    locked_out = False

    while attempts < max_attempts:
        password = input(f"Enter password (Attempt {attempts + 1}/{max_attempts}): ")

        if password == correct_password:
            print("Login successful!")
            break
        else:
            attempts += 1
            remaining = max_attempts - attempts

            if remaining > 0:
                print(f"Incorrect password. {remaining} attempts remaining.")
            else:
                locked_out = True
                print("Account locked due to too many failed attempts.")

    return not locked_out

# Example: Search with early termination
def search_database(query, max_results=100):
    """Simulate database search that stops when enough results found"""
    import random

    results = []
    records_scanned = 0
    max_scan = 1000

    print(f"Searching for '{query}'...")

    while len(results) < max_results and records_scanned < max_scan:
        records_scanned += 1

        # Simulate finding a match (20% chance)
        if random.random() < 0.2:
            results.append(f"Result {len(results) + 1}")

        # Progress update every 100 records
        if records_scanned % 100 == 0:
            print(f"Scanned {records_scanned} records, found {len(results)} matches")

    print(f"\nSearch complete!")
    print(f"Found {len(results)} results after scanning {records_scanned} records")

    return results

search_database("python", max_results=10)
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Count to Ten"
    difficulty: basic
    description: "Write a while loop that counts from 1 to 10 and prints each number on a separate line."
    starter_code: |
      counter = 1

      # Write your while loop here

    expected_output: |
      1
      2
      3
      4
      5
      6
      7
      8
      9
      10
    hints:
      - "Use while counter <= 10"
      - "Print the counter inside the loop"
      - "Don't forget to increment counter with counter += 1"
    solution: |
      counter = 1

      while counter <= 10:
          print(counter)
          counter += 1

  - title: "Sum Calculator"
    difficulty: basic
    description: "Create a program that calculates the sum of numbers from 1 to 5 using a while loop. Print the final sum."
    starter_code: |
      total = 0
      number = 1

      # Write your while loop to add numbers 1 through 5

    expected_output: |
      Total sum: 15
    hints:
      - "Use while number <= 5"
      - "Add number to total: total += number"
      - "Increment number: number += 1"
      - "Print total after the loop ends"
    solution: |
      total = 0
      number = 1

      while number <= 5:
          total += number
          number += 1

      print(f"Total sum: {total}")

  - title: "Password Validator"
    difficulty: intermediate
    description: "Write a function that keeps asking for a password until the user enters one that is at least 8 characters long. Print 'Valid password!' when accepted."
    starter_code: |
      def validate_password():
          password = ""
          # Write your while loop here
          pass

      # Simulate with a test
      def test_validate():
          # Simulated inputs: "abc", "hello", "password123"
          test_inputs = ["abc", "hello", "password123"]
          for i, pwd in enumerate(test_inputs):
              if len(pwd) >= 8:
                  print(f"Valid password!")
                  break
              else:
                  print(f"Password too short. Try again.")

      test_validate()

    expected_output: |
      Password too short. Try again.
      Password too short. Try again.
      Valid password!
    hints:
      - "Use while len(password) < 8"
      - "In real scenario: password = input('Enter password: ')"
      - "For this exercise, the test function simulates the behavior"
    solution: |
      def validate_password():
          password = ""
          while len(password) < 8:
              password = input("Enter password (min 8 characters): ")
              if len(password) < 8:
                  print("Password too short. Try again.")
          print("Valid password!")

      def test_validate():
          test_inputs = ["abc", "hello", "password123"]
          for i, pwd in enumerate(test_inputs):
              if len(pwd) >= 8:
                  print(f"Valid password!")
                  break
              else:
                  print(f"Password too short. Try again.")

      test_validate()

  - title: "Countdown Timer"
    difficulty: intermediate
    description: "Create a function that counts down from a given number to 1, printing each number, then prints 'Done!'. Use a while loop."
    starter_code: |
      def countdown(start):
          # Write your while loop here
          pass

      # Test with countdown from 5
      countdown(5)

    expected_output: |
      5
      4
      3
      2
      1
      Done!
    hints:
      - "Use while start > 0"
      - "Print start, then decrement: start -= 1"
      - "Print 'Done!' after the loop"
    solution: |
      def countdown(start):
          while start > 0:
              print(start)
              start -= 1
          print("Done!")

      countdown(5)

  - title: "Number Guessing Game"
    difficulty: advanced
    description: "Build a number guessing game where the secret number is 42. Keep looping until user guesses correctly. Give 'Too high' or 'Too low' hints. Track attempts and print total attempts when correct."
    starter_code: |
      def guessing_game():
          secret_number = 42
          attempts = 0
          # Simulate guesses: [50, 30, 45, 42]
          guesses = [50, 30, 45, 42]

          # Write your game logic here
          pass

      guessing_game()

    expected_output: |
      Too high!
      Too low!
      Too high!
      Correct! You guessed it in 4 attempts.
    hints:
      - "Use a while loop with a found flag or check if guess != secret_number"
      - "Increment attempts each iteration"
      - "Compare guess with secret_number for hints"
      - "For this exercise, iterate through the guesses list"
    solution: |
      def guessing_game():
          secret_number = 42
          attempts = 0
          guesses = [50, 30, 45, 42]

          for guess in guesses:
              attempts += 1

              if guess > secret_number:
                  print("Too high!")
              elif guess < secret_number:
                  print("Too low!")
              else:
                  print(f"Correct! You guessed it in {attempts} attempts.")
                  break

      guessing_game()

  - title: "Account Balance Tracker"
    difficulty: advanced
    description: "Create a function that processes transactions. Start with $100. Process transactions until balance reaches $0 or below, or all transactions are processed. Print running balance. Transactions: [-20, -30, -15, -40, -10]"
    starter_code: |
      def process_transactions():
          balance = 100
          transactions = [-20, -30, -15, -40, -10]
          index = 0

          # Write your while loop here
          pass

      process_transactions()

    expected_output: |
      Transaction: -$20, New balance: $80
      Transaction: -$30, New balance: $50
      Transaction: -$15, New balance: $35
      Transaction: -$40, New balance: -$5
      Account depleted. Final balance: -$5
    hints:
      - "Use while balance > 0 and index < len(transactions)"
      - "Process transaction: balance += transactions[index]"
      - "Print transaction and new balance"
      - "Increment index"
      - "Check if balance <= 0 after the loop to print depletion message"
    solution: |
      def process_transactions():
          balance = 100
          transactions = [-20, -30, -15, -40, -10]
          index = 0

          while index < len(transactions):
              transaction = transactions[index]
              balance += transaction
              print(f"Transaction: -${abs(transaction)}, New balance: ${balance}")
              index += 1

              if balance <= 0:
                  print(f"Account depleted. Final balance: ${balance}")
                  break

          if balance > 0:
              print(f"All transactions processed. Final balance: ${balance}")

      process_transactions()
```
<!-- EXERCISE_END -->
