# Comparison Operators

Comparison operators are fundamental tools that allow you to compare values and make decisions in your code. They form the backbone of conditional logic, returning boolean values (True or False) that determine the flow of your program. Mastering these operators is essential for writing effective conditional statements and creating dynamic, responsive applications.

## The Six Comparison Operators

Python provides six primary comparison operators, each serving a specific purpose in comparing values. Understanding the nuances of each operator helps you write precise conditional logic.

```python
# Equal to (==) - checks if two values are equal
age = 25
if age == 25:
    print("Age is exactly 25")

username = "admin"
if username == "admin":
    print("Welcome, administrator!")

# Not equal to (!=) - checks if two values are different
status = "active"
if status != "inactive":
    print("User account is active")

# Greater than (>) - checks if left value is greater than right
score = 95
if score > 90:
    print("Excellent score!")

# Less than (<) - checks if left value is less than right
temperature = 68
if temperature < 75:
    print("Room is cool")

# Greater than or equal to (>=)
inventory = 10
minimum_stock = 10
if inventory >= minimum_stock:
    print("Stock level is adequate")

# Less than or equal to (<=)
price = 49.99
budget = 50.00
if price <= budget:
    print("Item is within budget")

# Comparison operators with different data types
# Strings are compared lexicographically (alphabetically)
word1 = "apple"
word2 = "banana"
if word1 < word2:
    print(f"'{word1}' comes before '{word2}' alphabetically")

# Comparing numbers of different types (int and float)
int_value = 10
float_value = 10.0
if int_value == float_value:
    print("Integer 10 equals float 10.0")
```

Here's a reference table of all comparison operators:

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `7 > 5` | `True` |
| `<` | Less than | `3 < 5` | `True` |
| `>=` | Greater than or equal | `5 >= 5` | `True` |
| `<=` | Less than or equal | `4 <= 5` | `True` |

## Chaining Comparisons

Python allows you to chain multiple comparison operators together in a single expression, creating more readable and concise code. This is particularly useful for range checking.

```python
# Range checking with chained comparisons
age = 25
if 18 <= age <= 65:
    print("Age is within working age range")

# Temperature comfort zone
temperature = 72
if 68 <= temperature <= 78:
    print("Temperature is comfortable")

# Grade validation
score = 85
if 0 <= score <= 100:
    print(f"Valid score: {score}")
else:
    print("Invalid score - must be between 0 and 100")

# Multiple chained comparisons
x = 5
y = 10
z = 15
if x < y < z:
    print("Values are in ascending order")

# This is equivalent to:
if x < y and y < z:
    print("Values are in ascending order (using 'and')")

# Practical example: Password length validation
def validate_password_length(password):
    min_length = 8
    max_length = 128

    if min_length <= len(password) <= max_length:
        print(f"Password length {len(password)} is valid")
        return True
    else:
        print(f"Password must be between {min_length} and {max_length} characters")
        return False

validate_password_length("MySecurePass123")
validate_password_length("short")

# Business hours checker
def is_business_hours(hour):
    """Check if hour (0-23) is within business hours (9 AM - 5 PM)"""
    if 9 <= hour < 17:  # Note: < 17 means up to but not including 5 PM (17:00)
        return True
    return False

print(f"Is 14:00 business hours? {is_business_hours(14)}")
print(f"Is 18:00 business hours? {is_business_hours(18)}")
```

## Comparing Different Data Types

Understanding how Python compares different data types is crucial for avoiding bugs and writing robust code. Some comparisons work intuitively, while others require careful consideration.

```python
# String comparisons (case-sensitive, lexicographical order)
print("A" < "B")  # True - alphabetical order
print("apple" < "banana")  # True
print("Apple" < "apple")  # True - uppercase comes before lowercase in ASCII

# Case-insensitive string comparison
name1 = "Alice"
name2 = "alice"
if name1.lower() == name2.lower():
    print("Names are the same (case-insensitive)")

# String length vs content
if len("apple") == len("berry"):
    print("Words have same length")

# Numeric string vs number (be careful!)
string_number = "10"
actual_number = 10
# This would cause TypeError: if string_number > actual_number

# Correct way: convert string to int
if int(string_number) == actual_number:
    print("String '10' equals number 10 when converted")

# List comparisons (element by element)
list1 = [1, 2, 3]
list2 = [1, 2, 3]
list3 = [1, 2, 4]

if list1 == list2:
    print("Lists are identical")

if list1 < list3:
    print("list1 is 'less than' list3 (compared element by element)")

# None comparisons - use 'is' instead of '=='
value = None
if value is None:  # Correct way
    print("Value is None")

# Comparing floats (be careful with precision)
a = 0.1 + 0.2
b = 0.3
print(f"0.1 + 0.2 = {a}")
print(f"0.3 = {b}")
print(f"Are they equal? {a == b}")  # False due to floating-point precision!

# Correct way to compare floats
tolerance = 0.0001
if abs(a - b) < tolerance:
    print("Values are approximately equal")

# Boolean comparisons
is_active = True
if is_active == True:  # Works but not Pythonic
    print("Active")

if is_active:  # Preferred Pythonic way
    print("Active (Pythonic)")

# Comparing with type conversion
def safe_compare(val1, val2):
    """Safely compare values that might be different types"""
    try:
        # Attempt numeric comparison
        return float(val1) == float(val2)
    except (ValueError, TypeError):
        # Fall back to string comparison
        return str(val1) == str(val2)

print(safe_compare(10, "10"))  # True
print(safe_compare("apple", "apple"))  # True
```

## Practical Applications and Real-World Examples

Comparison operators are used extensively in real-world applications. Here are practical examples demonstrating their use in common programming scenarios.

```python
# Example 1: E-commerce discount eligibility
def check_discount_eligibility(cart_total, items_count, is_member, account_age_days):
    """
    Determine if customer qualifies for discount
    Rules: Cart > $50 OR (Member AND 5+ items) OR (Account > 30 days AND cart > $30)
    """
    qualifies = False
    reason = ""

    if cart_total > 50:
        qualifies = True
        reason = "Cart total exceeds $50"
    elif is_member and items_count >= 5:
        qualifies = True
        reason = "Member with 5+ items"
    elif account_age_days > 30 and cart_total > 30:
        qualifies = True
        reason = "Loyal customer threshold met"
    else:
        reason = "Does not meet discount criteria"

    print(f"Discount eligible: {qualifies}")
    print(f"Reason: {reason}")
    return qualifies

check_discount_eligibility(45, 6, True, 15)

# Example 2: User authentication and authorization
def check_user_access(user_role, resource_sensitivity, user_clearance_level):
    """
    Determine if user can access a resource
    Clearance levels: 1 (lowest) to 5 (highest)
    """
    access_granted = False

    if user_role == "admin":
        access_granted = True
        print("Admin access: GRANTED")
    elif resource_sensitivity == "public":
        access_granted = True
        print("Public resource: GRANTED")
    elif user_clearance_level >= resource_sensitivity:
        access_granted = True
        print(f"Clearance level {user_clearance_level} sufficient: GRANTED")
    else:
        print(f"Clearance level {user_clearance_level} insufficient: DENIED")

    return access_granted

check_user_access("user", 3, 4)

# Example 3: Inventory management system
def check_inventory_status(current_stock, reorder_point, max_capacity):
    """
    Determine inventory status and recommended actions
    """
    print(f"\nInventory Analysis:")
    print(f"Current Stock: {current_stock}")
    print(f"Reorder Point: {reorder_point}")
    print(f"Max Capacity: {max_capacity}")
    print("-" * 40)

    if current_stock <= 0:
        status = "OUT OF STOCK"
        action = "URGENT: Order immediately"
    elif current_stock < reorder_point:
        status = "LOW STOCK"
        action = "Reorder recommended"
    elif current_stock > max_capacity:
        status = "OVERSTOCK"
        action = "Consider clearance sale"
    elif current_stock == max_capacity:
        status = "AT CAPACITY"
        action = "Stop ordering until stock decreases"
    else:
        status = "NORMAL"
        action = "No action needed"

    print(f"Status: {status}")
    print(f"Action: {action}")

    # Calculate stock percentage
    if max_capacity > 0:
        percentage = (current_stock / max_capacity) * 100
        print(f"Capacity: {percentage:.1f}%")

check_inventory_status(15, 20, 100)

# Example 4: Grade boundary calculator
def calculate_final_grade(assignments_avg, midterm, final_exam, participation):
    """
    Calculate final grade with weighted components
    Assignments: 30%, Midterm: 25%, Final: 35%, Participation: 10%
    """
    final_score = (assignments_avg * 0.30 +
                   midterm * 0.25 +
                   final_exam * 0.35 +
                   participation * 0.10)

    print(f"\nGrade Calculation:")
    print(f"Assignments: {assignments_avg:.1f} (30%)")
    print(f"Midterm: {midterm:.1f} (25%)")
    print(f"Final Exam: {final_exam:.1f} (35%)")
    print(f"Participation: {participation:.1f} (10%)")
    print(f"Final Score: {final_score:.2f}")

    # Determine letter grade
    if final_score >= 93:
        grade = "A"
    elif final_score >= 90:
        grade = "A-"
    elif final_score >= 87:
        grade = "B+"
    elif final_score >= 83:
        grade = "B"
    elif final_score >= 80:
        grade = "B-"
    elif final_score >= 77:
        grade = "C+"
    elif final_score >= 73:
        grade = "C"
    elif final_score >= 70:
        grade = "C-"
    elif final_score >= 60:
        grade = "D"
    else:
        grade = "F"

    print(f"Letter Grade: {grade}")
    return grade

calculate_final_grade(88, 85, 92, 95)
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Simple Price Comparison"
    difficulty: basic
    description: "Write a program that compares two product prices and prints which one is cheaper. If prices are equal, print that they are the same."
    starter_code: |
      price_a = 29.99
      price_b = 34.99

      # Write your comparison code here

    expected_output: |
      Product A is cheaper
    hints:
      - "Use if-elif-else structure"
      - "First check if price_a < price_b"
      - "Then check if price_a > price_b"
      - "Use else for when they are equal"
    solution: |
      price_a = 29.99
      price_b = 34.99

      if price_a < price_b:
          print("Product A is cheaper")
      elif price_a > price_b:
          print("Product B is cheaper")
      else:
          print("Prices are the same")

  - title: "Age Category Checker"
    difficulty: basic
    description: "Create a program that checks if a person's age falls into categories: child (under 13), teen (13-19), adult (20-64), or senior (65+). Use comparison operators."
    starter_code: |
      age = 16

      # Write your code here using comparison operators

    expected_output: |
      Teen
    hints:
      - "Use if-elif-else chain"
      - "Check age < 13 for child"
      - "Check age <= 19 for teen (since we already ruled out < 13)"
      - "Check age <= 64 for adult"
      - "Use else for senior"
    solution: |
      age = 16

      if age < 13:
          print("Child")
      elif age <= 19:
          print("Teen")
      elif age <= 64:
          print("Adult")
      else:
          print("Senior")

  - title: "Temperature Range Validator"
    difficulty: intermediate
    description: "Write a function that checks if a temperature is within a safe range (36.5°C to 37.5°C). Use chained comparisons. Print 'Normal', 'Low', or 'High' accordingly."
    starter_code: |
      def check_temperature(temp):
          # Use chained comparison operators
          pass

      # Test with normal temperature
      check_temperature(37.0)

    expected_output: |
      Temperature: 37.0°C - Status: Normal
    hints:
      - "Use chained comparison: 36.5 <= temp <= 37.5 for normal"
      - "Check if temp < 36.5 for low"
      - "Otherwise it's high"
      - "Include the temperature value in your output"
    solution: |
      def check_temperature(temp):
          if 36.5 <= temp <= 37.5:
              print(f"Temperature: {temp}°C - Status: Normal")
          elif temp < 36.5:
              print(f"Temperature: {temp}°C - Status: Low")
          else:
              print(f"Temperature: {temp}°C - Status: High")

      check_temperature(37.0)

  - title: "Test Score Analyzer"
    difficulty: intermediate
    description: "Create a function that analyzes if a student passed (score >= 60) and determines honor status: regular pass (60-79), honor (80-89), high honor (90-100). Handle invalid scores (< 0 or > 100)."
    starter_code: |
      def analyze_score(score):
          # Write your comparison logic here
          pass

      # Test with an honor score
      analyze_score(85)

    expected_output: |
      Score: 85 - Status: Passed with Honor
    hints:
      - "First check if score < 0 or score > 100 for invalid"
      - "Then check if score < 60 for failed"
      - "Use chained comparisons for ranges: 60 <= score < 80, etc."
      - "Check conditions from highest to lowest"
    solution: |
      def analyze_score(score):
          if score < 0 or score > 100:
              print(f"Score: {score} - Status: Invalid score")
          elif score < 60:
              print(f"Score: {score} - Status: Failed")
          elif 60 <= score < 80:
              print(f"Score: {score} - Status: Passed")
          elif 80 <= score < 90:
              print(f"Score: {score} - Status: Passed with Honor")
          else:
              print(f"Score: {score} - Status: Passed with High Honor")

      analyze_score(85)

  - title: "Product Pricing Comparator"
    difficulty: advanced
    description: "Create a function that compares two products considering price, rating (1-5), and shipping cost. Product A wins if: (lower total cost) OR (same total cost AND higher rating). Print detailed comparison."
    starter_code: |
      def compare_products(price_a, rating_a, shipping_a, price_b, rating_b, shipping_b):
          # Calculate totals and compare
          pass

      # Test: Product A $50, 4.5 rating, $5 shipping vs Product B $52, 4.8 rating, $3 shipping
      compare_products(50, 4.5, 5, 52, 4.8, 3)

    expected_output: |
      Product A Total: $55.00 (Rating: 4.5)
      Product B Total: $55.00 (Rating: 4.8)
      Winner: Product B (same price, higher rating)
    hints:
      - "Calculate total_a = price_a + shipping_a"
      - "Calculate total_b = price_b + shipping_b"
      - "First compare totals with <"
      - "Use elif to check if totals are equal AND compare ratings"
      - "Use elif to check if total_b < total_a"
      - "Include calculations and reasoning in output"
    solution: |
      def compare_products(price_a, rating_a, shipping_a, price_b, rating_b, shipping_b):
          total_a = price_a + shipping_a
          total_b = price_b + shipping_b

          print(f"Product A Total: ${total_a:.2f} (Rating: {rating_a})")
          print(f"Product B Total: ${total_b:.2f} (Rating: {rating_b})")

          if total_a < total_b:
              print("Winner: Product A (lower total cost)")
          elif total_a == total_b and rating_a > rating_b:
              print("Winner: Product A (same price, higher rating)")
          elif total_a == total_b and rating_b > rating_a:
              print("Winner: Product B (same price, higher rating)")
          elif total_a == total_b:
              print("Tie: Same total cost and rating")
          else:
              print("Winner: Product B (lower total cost)")

      compare_products(50, 4.5, 5, 52, 4.8, 3)

  - title: "Financial Credit Score Evaluator"
    difficulty: advanced
    description: "Build a function that evaluates loan approval based on: credit score (300-850), debt-to-income ratio (DTI, 0-1), and years of credit history. Approve if: (score >= 700 AND DTI <= 0.36) OR (score >= 650 AND DTI <= 0.28 AND history >= 5). Print detailed evaluation."
    starter_code: |
      def evaluate_loan(credit_score, dti_ratio, credit_history_years):
          # Write complex comparison logic
          pass

      # Test: 680 score, 0.25 DTI, 6 years history
      evaluate_loan(680, 0.25, 6)

    expected_output: |
      Credit Score: 680 (Fair)
      Debt-to-Income: 25.0%
      Credit History: 6 years
      Decision: APPROVED (Alternative criteria met)
    hints:
      - "Determine score category: Excellent (750+), Good (700-749), Fair (650-699), Poor (<650)"
      - "Check primary approval: credit_score >= 700 and dti_ratio <= 0.36"
      - "Check alternative approval: credit_score >= 650 and dti_ratio <= 0.28 and credit_history_years >= 5"
      - "Use elif for different approval paths"
      - "Convert DTI to percentage in output: dti_ratio * 100"
    solution: |
      def evaluate_loan(credit_score, dti_ratio, credit_history_years):
          # Determine credit score category
          if credit_score >= 750:
              score_category = "Excellent"
          elif credit_score >= 700:
              score_category = "Good"
          elif credit_score >= 650:
              score_category = "Fair"
          else:
              score_category = "Poor"

          print(f"Credit Score: {credit_score} ({score_category})")
          print(f"Debt-to-Income: {dti_ratio * 100:.1f}%")
          print(f"Credit History: {credit_history_years} years")

          # Evaluate approval
          if credit_score >= 700 and dti_ratio <= 0.36:
              print("Decision: APPROVED (Primary criteria met)")
          elif credit_score >= 650 and dti_ratio <= 0.28 and credit_history_years >= 5:
              print("Decision: APPROVED (Alternative criteria met)")
          else:
              print("Decision: DENIED (Criteria not met)")

      evaluate_loan(680, 0.25, 6)
```
<!-- EXERCISE_END -->
