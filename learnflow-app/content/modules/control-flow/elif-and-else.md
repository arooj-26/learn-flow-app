# Elif and Else

The `elif` (else if) and `else` statements extend the power of if statements by allowing you to handle multiple conditions and provide fallback behavior. Together with `if`, they form the complete conditional control flow toolkit in Python, enabling you to build sophisticated decision trees that handle any possible scenario.

## The Else Clause: Handling the Alternative

The `else` clause provides a default code block that executes when the if condition is false. It's the safety net that catches all cases not explicitly handled by the if statement.

```python
# Basic if-else structure
age = 16

if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")

# Practical example: User input validation
def check_username(username):
    if len(username) >= 5:
        print(f"Username '{username}' is valid.")
        return True
    else:
        print(f"Username must be at least 5 characters long.")
        return False

check_username("john")  # Too short
check_username("johndoe")  # Valid

# Example: Even or odd checker
number = 17
if number % 2 == 0:
    print(f"{number} is even")
else:
    print(f"{number} is odd")
```

The `else` clause is optional but extremely useful for:
- Providing default behavior
- Handling error cases
- Ensuring all possibilities are covered

## Elif: Checking Multiple Conditions

The `elif` statement allows you to check multiple conditions in sequence. Python evaluates each condition in order and executes the first block where the condition is true, then skips the rest.

```python
# Grade calculator with multiple conditions
def assign_letter_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

print(f"Score 85: Grade {assign_letter_grade(85)}")
print(f"Score 72: Grade {assign_letter_grade(72)}")
print(f"Score 55: Grade {assign_letter_grade(55)}")

# Traffic light control system
def traffic_light_action(color):
    if color == "red":
        print("STOP - Do not proceed")
    elif color == "yellow":
        print("CAUTION - Prepare to stop")
    elif color == "green":
        print("GO - Proceed safely")
    else:
        print("ERROR - Invalid traffic light color")

traffic_light_action("red")
traffic_light_action("green")

# Season detector based on month
def get_season(month):
    month = month.lower()
    if month in ["december", "january", "february"]:
        return "Winter"
    elif month in ["march", "april", "may"]:
        return "Spring"
    elif month in ["june", "july", "august"]:
        return "Summer"
    elif month in ["september", "october", "november"]:
        return "Fall"
    else:
        return "Invalid month"

print(get_season("july"))  # Summer
print(get_season("october"))  # Fall
```

## Building Decision Trees with If-Elif-Else

Complex decision-making often requires evaluating multiple conditions in a specific order. The if-elif-else chain creates a decision tree where conditions are checked sequentially.

```python
# Example: Shipping cost calculator
def calculate_shipping(weight, distance, is_expedited):
    """
    Calculate shipping cost based on weight, distance, and service type
    """
    base_cost = 5.00

    if is_expedited:
        if weight < 5:
            cost = base_cost + 15
        elif weight < 20:
            cost = base_cost + 25
        else:
            cost = base_cost + 40
    else:
        if weight < 5:
            cost = base_cost + 5
        elif weight < 20:
            cost = base_cost + 10
        else:
            cost = base_cost + 20

    # Add distance surcharge
    if distance > 1000:
        cost += 10
    elif distance > 500:
        cost += 5

    print(f"Weight: {weight}lbs, Distance: {distance}mi, Expedited: {is_expedited}")
    print(f"Total shipping cost: ${cost:.2f}")
    return cost

calculate_shipping(3, 600, False)
calculate_shipping(25, 1200, True)

# Example: Customer service priority system
def assign_ticket_priority(customer_type, issue_severity, response_time_hours):
    """
    Assign priority level to customer support tickets
    """
    if customer_type == "enterprise":
        if issue_severity == "critical":
            priority = "P0 - Immediate"
        elif issue_severity == "high":
            priority = "P1 - Urgent"
        else:
            priority = "P2 - High"
    elif customer_type == "premium":
        if issue_severity == "critical":
            priority = "P1 - Urgent"
        elif issue_severity == "high":
            priority = "P2 - High"
        else:
            priority = "P3 - Medium"
    else:  # standard customer
        if issue_severity == "critical":
            priority = "P2 - High"
        elif issue_severity == "high":
            priority = "P3 - Medium"
        else:
            priority = "P4 - Low"

    # Escalate if waiting too long
    if response_time_hours > 24:
        print(f"⚠ ESCALATING: Original priority {priority}")
        if "P0" in priority:
            priority = "P0 - ESCALATED"
        elif "P1" in priority:
            priority = "P0 - ESCALATED"
        else:
            priority = "P1 - ESCALATED"

    print(f"Customer: {customer_type}, Severity: {issue_severity}")
    print(f"Assigned Priority: {priority}")
    return priority

assign_ticket_priority("enterprise", "critical", 2)
assign_ticket_priority("standard", "high", 30)
```

## Best Practices and Common Patterns

Understanding when and how to use if-elif-else chains effectively is crucial for writing clean, maintainable code. Here are key patterns and best practices.

```python
# Pattern 1: Order matters - check most specific conditions first
def categorize_temperature(temp_f):
    if temp_f < -20:
        return "Dangerously cold"
    elif temp_f < 32:
        return "Freezing"
    elif temp_f < 50:
        return "Cold"
    elif temp_f < 70:
        return "Cool"
    elif temp_f < 85:
        return "Warm"
    elif temp_f < 100:
        return "Hot"
    else:
        return "Extremely hot"

# Pattern 2: Using elif vs multiple ifs
# INEFFICIENT - checks all conditions even after finding a match
def process_inefficient(value):
    result = None
    if value < 10:
        result = "Small"
    if value >= 10 and value < 100:  # Still checked even if first was true
        result = "Medium"
    if value >= 100:  # Still checked
        result = "Large"
    return result

# EFFICIENT - stops after first match
def process_efficient(value):
    if value < 10:
        return "Small"
    elif value < 100:
        return "Medium"
    else:
        return "Large"

# Pattern 3: Complex condition checking with clear logic
def validate_password(password, username):
    """
    Validate password with multiple requirements
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    elif password.isalpha():
        return False, "Password must contain numbers or special characters"
    elif password.isdigit():
        return False, "Password must contain letters"
    elif username.lower() in password.lower():
        return False, "Password cannot contain username"
    elif password.isupper() or password.islower():
        return False, "Password must contain both uppercase and lowercase"
    else:
        return True, "Password is strong"

is_valid, message = validate_password("Pass123", "john")
print(f"Valid: {is_valid}, Message: {message}")

# Pattern 4: Handling ranges with lookup tables (alternative to long elif chains)
def get_tax_bracket_traditional(income):
    """Traditional elif approach"""
    if income <= 10275:
        return 0.10
    elif income <= 41775:
        return 0.12
    elif income <= 89075:
        return 0.22
    elif income <= 170050:
        return 0.24
    elif income <= 215950:
        return 0.32
    elif income <= 539900:
        return 0.35
    else:
        return 0.37

# Comparison table for tax brackets
print("\nTax Bracket Reference:")
print("| Income Range | Tax Rate |")
print("|--------------|----------|")
print("| $0 - $10,275 | 10% |")
print("| $10,276 - $41,775 | 12% |")
print("| $41,776 - $89,075 | 22% |")
print("| $89,076 - $170,050 | 24% |")
print("| $170,051 - $215,950 | 32% |")
print("| $215,951 - $539,900 | 35% |")
print("| $539,901+ | 37% |")

income = 75000
tax_rate = get_tax_bracket_traditional(income)
print(f"\nIncome: ${income:,} → Tax Rate: {tax_rate * 100}%")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Number Sign Checker"
    difficulty: basic
    description: "Write a program that checks if a number is positive, negative, or zero. Use if-elif-else to print the appropriate message."
    starter_code: |
      number = -5

      # Write your if-elif-else statements here

    expected_output: |
      The number is negative
    hints:
      - "Check if number > 0 for positive"
      - "Use elif to check if number < 0 for negative"
      - "Use else for when number equals zero"
    solution: |
      number = -5

      if number > 0:
          print("The number is positive")
      elif number < 0:
          print("The number is negative")
      else:
          print("The number is zero")

  - title: "Day Type Classifier"
    difficulty: basic
    description: "Create a program that takes a day number (1-7) and prints whether it's a weekday or weekend. Use if-elif-else. Days 1-5 are weekdays, 6-7 are weekends."
    starter_code: |
      day = 6

      # Write your if-elif-else statements here

    expected_output: |
      Weekend
    hints:
      - "Check if day >= 1 and day <= 5 for weekdays"
      - "Use elif to check if day == 6 or day == 7 for weekends"
      - "Use else for invalid day numbers"
    solution: |
      day = 6

      if day >= 1 and day <= 5:
          print("Weekday")
      elif day == 6 or day == 7:
          print("Weekend")
      else:
          print("Invalid day")

  - title: "Movie Ticket Pricing"
    difficulty: intermediate
    description: "Create a function that calculates movie ticket prices based on age. Children (under 12): $8, Teens (12-17): $10, Adults (18-64): $15, Seniors (65+): $10. Return the price."
    starter_code: |
      def calculate_ticket_price(age):
          # Write your if-elif-else chain here
          pass

      # Test your function
      price = calculate_ticket_price(25)
      print(f"Ticket price: ${price}")

    expected_output: |
      Ticket price: $15
    hints:
      - "Check conditions in order: age < 12, age < 18, age < 65, else"
      - "Return the appropriate price for each condition"
      - "Make sure to use elif, not multiple ifs"
    solution: |
      def calculate_ticket_price(age):
          if age < 12:
              return 8
          elif age < 18:
              return 10
          elif age < 65:
              return 15
          else:
              return 10

      price = calculate_ticket_price(25)
      print(f"Ticket price: ${price}")

  - title: "BMI Category Calculator"
    difficulty: intermediate
    description: "Write a function that calculates BMI category. Underweight: BMI < 18.5, Normal: 18.5-24.9, Overweight: 25-29.9, Obese: 30+. Print the category and BMI value formatted to 1 decimal."
    starter_code: |
      def calculate_bmi_category(weight_kg, height_m):
          # Calculate BMI and determine category
          pass

      # Test: 70kg, 1.75m should be Normal
      calculate_bmi_category(70, 1.75)

    expected_output: |
      BMI: 22.9 - Category: Normal weight
    hints:
      - "BMI formula: weight_kg / (height_m ** 2)"
      - "Use if-elif-else to check BMI ranges"
      - "Format BMI with {bmi:.1f} in the print statement"
    solution: |
      def calculate_bmi_category(weight_kg, height_m):
          bmi = weight_kg / (height_m ** 2)

          if bmi < 18.5:
              category = "Underweight"
          elif bmi < 25:
              category = "Normal weight"
          elif bmi < 30:
              category = "Overweight"
          else:
              category = "Obese"

          print(f"BMI: {bmi:.1f} - Category: {category}")

      calculate_bmi_category(70, 1.75)

  - title: "Water State Determiner"
    difficulty: advanced
    description: "Create a function that determines the state of water (ice, liquid, or steam) based on temperature in Celsius and pressure in atmospheres. At 1 atm: ice if temp <= 0, steam if temp >= 100, else liquid. At high pressure (>10 atm): ice if temp <= -5, steam if temp >= 150, else liquid."
    starter_code: |
      def water_state(temperature_c, pressure_atm):
          # Write your nested if-elif-else logic here
          pass

      # Test at normal pressure, 25°C
      water_state(25, 1)

    expected_output: |
      At 25°C and 1 atm: Water is liquid
    hints:
      - "First check if pressure > 10 for high pressure conditions"
      - "Use else for normal pressure (around 1 atm)"
      - "Within each pressure condition, use if-elif-else for temperature ranges"
      - "Include the temperature and pressure in your output"
    solution: |
      def water_state(temperature_c, pressure_atm):
          if pressure_atm > 10:
              if temperature_c <= -5:
                  state = "ice"
              elif temperature_c >= 150:
                  state = "steam"
              else:
                  state = "liquid"
          else:
              if temperature_c <= 0:
                  state = "ice"
              elif temperature_c >= 100:
                  state = "steam"
              else:
                  state = "liquid"

          print(f"At {temperature_c}°C and {pressure_atm} atm: Water is {state}")

      water_state(25, 1)

  - title: "Smart Thermostat Controller"
    difficulty: advanced
    description: "Build a thermostat function that decides actions based on current temp, target temp, time of day (0-23), and occupancy. If occupied: maintain target ±2°. If unoccupied and daytime (6-18): target -5°. If unoccupied and night: target -8°. Return heating/cooling/idle status."
    starter_code: |
      def thermostat_control(current_temp, target_temp, hour, occupied):
          # Write your complex if-elif-else logic here
          pass

      # Test: 65°F current, 72°F target, 10 AM, occupied
      thermostat_control(65, 72, 10, True)

    expected_output: |
      Status: Heating - Current: 65°F, Target: 72°F
    hints:
      - "First determine the effective target based on occupancy and time"
      - "If occupied, use target_temp directly"
      - "If unoccupied, check if hour is between 6-18 for daytime"
      - "Then compare current_temp with effective target (±2 degree tolerance)"
      - "Print heating if too cold, cooling if too hot, idle if within range"
    solution: |
      def thermostat_control(current_temp, target_temp, hour, occupied):
          # Determine effective target temperature
          if occupied:
              effective_target = target_temp
          else:
              if hour >= 6 and hour <= 18:
                  effective_target = target_temp - 5
              else:
                  effective_target = target_temp - 8

          # Determine action based on current temperature
          if current_temp < effective_target - 2:
              status = "Heating"
          elif current_temp > effective_target + 2:
              status = "Cooling"
          else:
              status = "Idle"

          print(f"Status: {status} - Current: {current_temp}°F, Target: {effective_target}°F")

      thermostat_control(65, 72, 10, True)
```
<!-- EXERCISE_END -->
