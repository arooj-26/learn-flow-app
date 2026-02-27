# If Statements

If statements are the foundation of decision-making in programming. They allow your code to execute different blocks of code based on whether a condition is true or false. Understanding if statements is crucial for creating dynamic, responsive programs that can adapt to different situations and user inputs.

## Understanding the If Statement Syntax

The basic syntax of an if statement in Python is straightforward but powerful. The condition is evaluated as a boolean expression, and if it evaluates to `True`, the indented code block beneath it executes.

```python
# Basic if statement structure
temperature = 75

if temperature > 70:
    print("It's a warm day!")
    print("Consider wearing light clothing.")

# The condition can be any expression that evaluates to True or False
user_age = 25
if user_age >= 18:
    print("You are eligible to vote.")
```

The key components are:
- The `if` keyword
- A condition that evaluates to `True` or `False`
- A colon (`:`) to end the if line
- An indented code block (typically 4 spaces) that executes when the condition is true

## Conditional Expressions and Truthy/Falsy Values

Python evaluates many types of values as either "truthy" or "falsy" in conditional contexts. Understanding this concept allows you to write more concise and Pythonic code.

```python
# Truthy and Falsy values in Python
# Falsy values: False, None, 0, 0.0, "", [], {}, ()
# Everything else is Truthy

# Using truthiness with strings
username = input("Enter your username: ")
if username:  # True if username is not empty
    print(f"Welcome, {username}!")

# Using truthiness with lists
shopping_cart = []
if shopping_cart:
    print(f"You have {len(shopping_cart)} items in your cart.")
else:
    print("Your cart is empty.")

# Using truthiness with numbers
account_balance = 0
if account_balance:
    print(f"Your balance: ${account_balance}")
else:
    print("Your account balance is zero.")
```

Here's a table of common truthy and falsy values:

| Value Type | Falsy Examples | Truthy Examples |
|------------|----------------|-----------------|
| Boolean | `False` | `True` |
| Numeric | `0`, `0.0`, `0j` | Any non-zero number |
| String | `""` (empty string) | Any non-empty string |
| List | `[]` | `[1, 2, 3]` |
| Dictionary | `{}` | `{"key": "value"}` |
| None | `None` | N/A |

## Real-World Applications of If Statements

If statements are essential for building practical applications. Let's explore some real-world scenarios where if statements solve common programming challenges.

```python
# Example 1: User authentication system
def authenticate_user(username, password):
    stored_username = "admin"
    stored_password = "secure123"

    if username == stored_username and password == stored_password:
        print("Authentication successful!")
        return True
    print("Invalid credentials.")
    return False

# Example 2: Discount calculator for e-commerce
def calculate_discount(purchase_amount, is_member):
    discount = 0

    if purchase_amount >= 100:
        discount = 0.15  # 15% discount for purchases $100+
    if is_member:
        discount += 0.05  # Additional 5% for members

    final_price = purchase_amount * (1 - discount)
    print(f"Original: ${purchase_amount:.2f}")
    print(f"Discount: {discount * 100:.0f}%")
    print(f"Final price: ${final_price:.2f}")
    return final_price

calculate_discount(150, True)  # 20% total discount

# Example 3: Input validation
def validate_email(email):
    if "@" not in email:
        print("Error: Email must contain @")
        return False
    if "." not in email:
        print("Error: Email must contain a domain extension")
        return False
    if len(email) < 5:
        print("Error: Email is too short")
        return False
    print("Email is valid!")
    return True

validate_email("user@example.com")
```

## Nested If Statements and Complex Conditions

When dealing with multiple conditions that depend on each other, nested if statements allow you to create hierarchical decision trees. This is useful for complex logic where one condition must be checked before another.

```python
# Example: Loan approval system
def check_loan_approval(credit_score, annual_income, employment_years):
    if credit_score >= 700:
        print("Excellent credit score!")
        if annual_income >= 50000:
            print("Income requirement met.")
            if employment_years >= 2:
                print("✓ Loan APPROVED")
                return True
            else:
                print("✗ Insufficient employment history")
        else:
            print("✗ Income too low")
    else:
        print("✗ Credit score too low")
    return False

# Test cases
check_loan_approval(750, 60000, 3)  # Approved
print()
check_loan_approval(680, 70000, 5)  # Denied - low credit score

# Example: Grading system with nested conditions
def assign_grade(score, attendance_rate):
    if score >= 90:
        if attendance_rate >= 0.9:
            print("Grade: A+ (Excellent performance and attendance)")
        else:
            print("Grade: A (Excellent score, but attendance could improve)")
    if score >= 80:
        if attendance_rate >= 0.85:
            print("Grade: B+ (Good work!)")
    if score < 60:
        print("Grade: F (Please see instructor)")

# Example: Multi-level access control
def check_access(user_role, resource_type, is_business_hours):
    if user_role == "admin":
        if resource_type in ["database", "config", "logs"]:
            print(f"Admin access granted to {resource_type}")
            return True

    if user_role == "developer":
        if is_business_hours:
            if resource_type in ["database", "logs"]:
                print(f"Developer access granted to {resource_type}")
                return True
        else:
            print("Developers can only access resources during business hours")

    print("Access denied")
    return False

check_access("developer", "database", True)
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Temperature Advisory"
    difficulty: basic
    description: "Write a program that takes a temperature value and prints 'It is freezing!' if the temperature is below 32 degrees Fahrenheit."
    starter_code: |
      temperature = 28

      # Write your if statement here

    expected_output: |
      It is freezing!
    hints:
      - "Use the less than operator (<) to compare the temperature with 32"
      - "Remember to indent the print statement under the if statement"
    solution: |
      temperature = 28

      if temperature < 32:
          print("It is freezing!")

  - title: "Age Verification"
    difficulty: basic
    description: "Create a program that checks if a person's age is 21 or older. If so, print 'You can enter the venue.' Store the age in a variable and use an if statement."
    starter_code: |
      age = 25

      # Write your if statement here

    expected_output: |
      You can enter the venue.
    hints:
      - "Use the >= operator to check if age is greater than or equal to 21"
      - "Make sure your indentation is correct"
    solution: |
      age = 25

      if age >= 21:
          print("You can enter the venue.")

  - title: "Password Strength Checker"
    difficulty: intermediate
    description: "Write a function that checks if a password is strong. A strong password must be at least 8 characters long AND contain the '@' symbol. Use nested if statements."
    starter_code: |
      def check_password_strength(password):
          # Write your nested if statements here
          pass

      # Test your function
      check_password_strength("secure@123")

    expected_output: |
      Password is strong!
    hints:
      - "First check if the password length is >= 8"
      - "Inside that if block, check if '@' is in the password"
      - "Use the len() function to get the password length"
    solution: |
      def check_password_strength(password):
          if len(password) >= 8:
              if "@" in password:
                  print("Password is strong!")
              else:
                  print("Password needs an @ symbol")
          else:
              print("Password is too short")

      check_password_strength("secure@123")

  - title: "Shopping Cart Discount"
    difficulty: intermediate
    description: "Create a function that calculates if a customer gets free shipping. Free shipping applies if the cart total is $50 or more OR if the customer is a premium member. Print appropriate messages."
    starter_code: |
      def check_free_shipping(cart_total, is_premium_member):
          # Write your code here
          pass

      # Test cases
      check_free_shipping(60, False)
      check_free_shipping(30, True)

    expected_output: |
      You qualify for free shipping!
      You qualify for free shipping!
    hints:
      - "You need two separate if statements, not nested"
      - "Check cart_total >= 50 in the first if"
      - "Check is_premium_member in the second if"
    solution: |
      def check_free_shipping(cart_total, is_premium_member):
          if cart_total >= 50:
              print("You qualify for free shipping!")
              return
          if is_premium_member:
              print("You qualify for free shipping!")
              return
          print("Add more items for free shipping")

      check_free_shipping(60, False)
      check_free_shipping(30, True)

  - title: "Investment Risk Analyzer"
    difficulty: advanced
    description: "Create a function that analyzes investment risk. It should check: if investment amount >= $10,000 AND risk tolerance is 'high' AND investor age is between 25-45, recommend 'Aggressive Growth Portfolio'. Use nested conditions."
    starter_code: |
      def analyze_investment(amount, risk_tolerance, age):
          # Write your nested if statements here
          pass

      # Test your function
      analyze_investment(15000, "high", 35)

    expected_output: |
      Recommended: Aggressive Growth Portfolio
    hints:
      - "Start with checking if amount >= 10000"
      - "Then check if risk_tolerance == 'high'"
      - "Finally check if age >= 25 and age <= 45"
      - "Nest each condition inside the previous one"
    solution: |
      def analyze_investment(amount, risk_tolerance, age):
          if amount >= 10000:
              if risk_tolerance == "high":
                  if age >= 25 and age <= 45:
                      print("Recommended: Aggressive Growth Portfolio")
                  else:
                      print("Age range not optimal for aggressive portfolio")
              else:
                  print("Risk tolerance too low for this portfolio")
          else:
              print("Minimum investment amount not met")

      analyze_investment(15000, "high", 35)

  - title: "Smart Home Security System"
    difficulty: advanced
    description: "Build a security system that grants access based on multiple factors. Access is granted if: (time is between 6-22 hours) AND (correct PIN is entered OR biometric matches) AND (not in lockdown mode). Create a function with nested if statements."
    starter_code: |
      def check_access(hour, pin_entered, correct_pin, biometric_match, lockdown_mode):
          # Write your complex nested if logic here
          pass

      # Test case: 14 (2 PM), PIN 1234, correct PIN 1234, no biometric, not in lockdown
      check_access(14, 1234, 1234, False, False)

    expected_output: |
      Access Granted
    hints:
      - "First check if NOT lockdown_mode (use 'not' keyword)"
      - "Then check if hour >= 6 and hour <= 22"
      - "Then check if pin_entered == correct_pin OR biometric_match"
      - "Each condition should be nested inside the previous one"
    solution: |
      def check_access(hour, pin_entered, correct_pin, biometric_match, lockdown_mode):
          if not lockdown_mode:
              if hour >= 6 and hour <= 22:
                  if pin_entered == correct_pin or biometric_match:
                      print("Access Granted")
                  else:
                      print("Access Denied: Invalid credentials")
              else:
                  print("Access Denied: Outside allowed hours")
          else:
              print("Access Denied: System in lockdown mode")

      check_access(14, 1234, 1234, False, False)
```
<!-- EXERCISE_END -->
