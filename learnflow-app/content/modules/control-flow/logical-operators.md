# Logical Operators

Logical operators allow you to combine multiple conditions and create complex decision-making logic in your programs. The three logical operators in Python—`and`, `or`, and `not`—enable you to build sophisticated conditional expressions that reflect real-world scenarios where multiple factors influence decisions.

## The AND Operator: All Conditions Must Be True

The `and` operator returns `True` only when all conditions it connects are true. If any condition is false, the entire expression evaluates to `False`. This is perfect for scenarios where multiple requirements must be met simultaneously.

```python
# Basic AND usage
age = 25
has_license = True

if age >= 18 and has_license:
    print("You can drive a car")

# Multiple AND conditions
temperature = 72
humidity = 45
air_quality = "good"

if temperature >= 68 and temperature <= 78 and humidity < 60 and air_quality == "good":
    print("Perfect weather conditions!")

# Real-world example: Account access validation
def validate_login(username, password, account_active, email_verified):
    """
    User can login only if ALL conditions are met
    """
    if username and password and account_active and email_verified:
        print("Login successful!")
        return True
    else:
        print("Login failed - missing requirements")
        if not username or not password:
            print("  - Username or password missing")
        if not account_active:
            print("  - Account is not active")
        if not email_verified:
            print("  - Email not verified")
        return False

validate_login("john_doe", "pass123", True, True)
validate_login("jane_doe", "pass456", True, False)

# E-commerce example: Discount eligibility
def check_premium_discount(is_member, cart_total, items_count, first_purchase):
    """
    Premium discount: member AND cart > $100 AND 3+ items AND first purchase
    """
    if is_member and cart_total > 100 and items_count >= 3 and first_purchase:
        discount = 0.25  # 25% discount
        print(f"Premium discount: 25% off!")
        print(f"Cart total: ${cart_total:.2f}")
        print(f"Final price: ${cart_total * (1 - discount):.2f}")
        return True
    else:
        print("Does not qualify for premium discount")
        return False

check_premium_discount(True, 150, 4, True)

# Short-circuit evaluation
# AND stops evaluating once it finds a False condition
def expensive_check():
    print("Running expensive operation...")
    return True

x = 5
if x > 10 and expensive_check():  # expensive_check() never runs
    print("Both conditions true")
print("Expensive check was never called because first condition was False")
```

Truth table for AND operator:

| Condition A | Condition B | A and B |
|-------------|-------------|---------|
| True | True | True |
| True | False | False |
| False | True | False |
| False | False | False |

## The OR Operator: At Least One Condition Must Be True

The `or` operator returns `True` if at least one of the conditions is true. It only returns `False` when all conditions are false. This is useful for scenarios with multiple alternative paths to success.

```python
# Basic OR usage
day = "Saturday"

if day == "Saturday" or day == "Sunday":
    print("It's the weekend!")

# Access control with multiple roles
def check_access(user_role):
    """
    Grant access if user is admin OR manager OR supervisor
    """
    if user_role == "admin" or user_role == "manager" or user_role == "supervisor":
        print(f"Access granted for {user_role}")
        return True
    else:
        print(f"Access denied for {user_role}")
        return False

check_access("manager")
check_access("employee")

# Emergency alert system
def trigger_emergency_alert(temperature, smoke_detected, gas_detected, intrusion):
    """
    Trigger alert if ANY emergency condition is detected
    """
    if temperature > 150 or smoke_detected or gas_detected or intrusion:
        print("🚨 EMERGENCY ALERT TRIGGERED!")

        if temperature > 150:
            print(f"  - High temperature: {temperature}°F")
        if smoke_detected:
            print("  - Smoke detected")
        if gas_detected:
            print("  - Gas leak detected")
        if intrusion:
            print("  - Intrusion detected")

        return True
    else:
        print("All systems normal")
        return False

trigger_emergency_alert(72, False, True, False)

# Payment method validation
def process_payment(has_credit_card, has_paypal, has_apple_pay, cash_available):
    """
    Can process payment if ANY payment method is available
    """
    if has_credit_card or has_paypal or has_apple_pay or cash_available:
        print("Payment can be processed")

        # Determine which method
        if has_credit_card:
            print("Using credit card")
        elif has_paypal:
            print("Using PayPal")
        elif has_apple_pay:
            print("Using Apple Pay")
        else:
            print("Using cash")

        return True
    else:
        print("No payment method available")
        return False

process_payment(False, True, False, False)

# Short-circuit evaluation with OR
# OR stops evaluating once it finds a True condition
def quick_check():
    print("Quick check executed")
    return True

def slow_check():
    print("This won't run if quick check is True")
    return False

if quick_check() or slow_check():
    print("At least one condition was True")
```

Truth table for OR operator:

| Condition A | Condition B | A or B |
|-------------|-------------|--------|
| True | True | True |
| True | False | True |
| False | True | True |
| False | False | False |

## The NOT Operator: Inverting Boolean Values

The `not` operator inverts a boolean value: `True` becomes `False` and `False` becomes `True`. It's useful for checking negative conditions or inverting logic.

```python
# Basic NOT usage
is_raining = False

if not is_raining:
    print("You don't need an umbrella")

# Checking for empty values
username = ""
if not username:
    print("Please enter a username")

# Account status checking
account_suspended = False
account_deleted = False

if not account_suspended and not account_deleted:
    print("Account is active and accessible")

# Inverting complex conditions
def check_eligibility(age, has_criminal_record, credit_score):
    """
    Eligible if: adult AND NOT criminal record AND good credit
    """
    if age >= 18 and not has_criminal_record and credit_score >= 650:
        print("Eligible for loan")
        return True
    else:
        print("Not eligible for loan")
        if age < 18:
            print("  - Must be 18 or older")
        if has_criminal_record:
            print("  - Criminal record found")
        if credit_score < 650:
            print(f"  - Credit score {credit_score} too low (need 650+)")
        return False

check_eligibility(25, False, 700)

# Double negative (avoid in practice, but good to understand)
is_not_invalid = True
if not not is_not_invalid:  # Double negative - confusing!
    print("This is valid, but confusing to read")

# Better approach
is_valid = True
if is_valid:
    print("This is clearer")

# Using NOT with 'in' operator
allowed_users = ["admin", "moderator", "editor"]
current_user = "guest"

if current_user not in allowed_users:
    print(f"{current_user} does not have permission")

# Inverting function results
def is_weekend(day):
    return day == "Saturday" or day == "Sunday"

day = "Monday"
if not is_weekend(day):
    print("It's a weekday - time to work!")
```

## Combining Multiple Logical Operators

Real-world scenarios often require combining `and`, `or`, and `not` operators. Understanding operator precedence and using parentheses for clarity is essential.

```python
# Operator precedence: not > and > or
# Use parentheses to make intent clear

# Complex admission criteria
def check_university_admission(gpa, sat_score, extracurriculars, essay_score, athlete):
    """
    Admit if:
    - (GPA >= 3.5 AND SAT >= 1200) OR
    - (GPA >= 3.0 AND exceptional extracurriculars AND good essay) OR
    - (Recruited athlete AND GPA >= 2.5)
    """
    standard_admission = gpa >= 3.5 and sat_score >= 1200
    exceptional_admission = (gpa >= 3.0 and
                            extracurriculars >= 8 and
                            essay_score >= 85)
    athletic_admission = athlete and gpa >= 2.5

    if standard_admission or exceptional_admission or athletic_admission:
        print("🎓 ADMITTED!")

        if standard_admission:
            print("  Path: Standard admission criteria")
        elif exceptional_admission:
            print("  Path: Exceptional profile")
        elif athletic_admission:
            print("  Path: Athletic recruitment")

        return True
    else:
        print("❌ Not admitted")
        return False

check_university_admission(3.6, 1250, 5, 80, False)

# Insurance premium calculator
def calculate_insurance_premium(age, accident_history, credit_score, vehicle_age):
    """
    Determine insurance risk level using complex conditions
    """
    base_premium = 1000

    # High risk: young driver OR multiple accidents OR poor credit
    high_risk = (age < 25 or accident_history >= 2 or credit_score < 600)

    # Medium risk: middle age AND (1 accident OR fair credit OR old vehicle)
    medium_risk = (25 <= age <= 65 and
                   (accident_history == 1 or
                    (600 <= credit_score < 700) or
                    vehicle_age > 10))

    # Low risk: experienced driver AND no accidents AND good credit AND newer car
    low_risk = (age >= 25 and
                accident_history == 0 and
                credit_score >= 700 and
                vehicle_age <= 5)

    if low_risk:
        premium = base_premium * 0.8
        risk_level = "LOW"
    elif medium_risk and not high_risk:
        premium = base_premium * 1.0
        risk_level = "MEDIUM"
    else:
        premium = base_premium * 1.5
        risk_level = "HIGH"

    print(f"Risk Level: {risk_level}")
    print(f"Annual Premium: ${premium:.2f}")
    return premium

calculate_insurance_premium(30, 0, 750, 3)

# Smart home automation
def control_hvac(indoor_temp, outdoor_temp, humidity, time_hour, occupied, season):
    """
    Intelligent HVAC control with multiple factors
    """
    # Comfort range depends on season
    if season == "summer":
        target_temp = 72
    else:  # winter
        target_temp = 68

    # Determine action
    too_hot = indoor_temp > target_temp + 2
    too_cold = indoor_temp < target_temp - 2
    high_humidity = humidity > 60

    # Only run HVAC during occupied hours or extreme conditions
    should_run = occupied or too_hot or too_cold or high_humidity

    # Smart scheduling: reduce energy during unoccupied hours
    unoccupied_hours = not occupied and (time_hour < 6 or time_hour > 22)

    if should_run and not unoccupied_hours:
        if too_hot or (high_humidity and indoor_temp > 70):
            action = "COOLING"
        elif too_cold:
            action = "HEATING"
        else:
            action = "FAN ONLY"

        print(f"HVAC Status: {action}")
        print(f"Indoor: {indoor_temp}°F, Outdoor: {outdoor_temp}°F")
        print(f"Humidity: {humidity}%, Occupied: {occupied}")
    else:
        print("HVAC Status: IDLE (energy saving mode)")

control_hvac(76, 85, 65, 14, True, "summer")

# Content moderation system
def moderate_content(word_count, has_profanity, spam_score, user_reputation, flagged_count):
    """
    Determine if content should be auto-approved, flagged, or rejected
    """
    # Auto-reject: profanity OR high spam score OR multiple flags
    auto_reject = has_profanity or spam_score > 0.8 or flagged_count >= 3

    # Auto-approve: good reputation AND normal spam score AND not flagged
    auto_approve = (user_reputation >= 100 and
                   spam_score < 0.3 and
                   flagged_count == 0 and
                   not has_profanity)

    # Review needed: everything else
    needs_review = not auto_reject and not auto_approve

    if auto_reject:
        status = "REJECTED"
        print("❌ Content rejected automatically")
    elif auto_approve:
        status = "APPROVED"
        print("✅ Content approved automatically")
    else:
        status = "REVIEW"
        print("⚠️  Content flagged for manual review")

    print(f"Spam Score: {spam_score:.2f}, Reputation: {user_reputation}")
    return status

moderate_content(150, False, 0.2, 250, 0)
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Weekend Checker"
    difficulty: basic
    description: "Write a program that checks if a day is either Saturday or Sunday using the OR operator. Print 'Weekend!' if true, otherwise print 'Weekday'."
    starter_code: |
      day = "Saturday"

      # Use OR operator to check for weekend

    expected_output: |
      Weekend!
    hints:
      - "Use the or operator to check if day == 'Saturday' or day == 'Sunday'"
      - "Use an if-else statement"
    solution: |
      day = "Saturday"

      if day == "Saturday" or day == "Sunday":
          print("Weekend!")
      else:
          print("Weekday")

  - title: "Simple Access Control"
    difficulty: basic
    description: "Create a program that grants access only if BOTH username is 'admin' AND password is 'secret123'. Use the AND operator."
    starter_code: |
      username = "admin"
      password = "secret123"

      # Use AND operator to check both conditions

    expected_output: |
      Access granted
    hints:
      - "Use the and operator to combine both conditions"
      - "Check username == 'admin' and password == 'secret123'"
    solution: |
      username = "admin"
      password = "secret123"

      if username == "admin" and password == "secret123":
          print("Access granted")
      else:
          print("Access denied")

  - title: "Voting Eligibility Checker"
    difficulty: intermediate
    description: "Write a function that determines voting eligibility. A person can vote if they are 18 or older AND are a citizen AND are NOT currently imprisoned. Print detailed eligibility status."
    starter_code: |
      def check_voting_eligibility(age, is_citizen, is_imprisoned):
          # Use AND and NOT operators
          pass

      # Test: 25 years old, citizen, not imprisoned
      check_voting_eligibility(25, True, False)

    expected_output: |
      Eligible to vote
    hints:
      - "Use: age >= 18 and is_citizen and not is_imprisoned"
      - "Remember to use 'not' before is_imprisoned"
    solution: |
      def check_voting_eligibility(age, is_citizen, is_imprisoned):
          if age >= 18 and is_citizen and not is_imprisoned:
              print("Eligible to vote")
          else:
              print("Not eligible to vote")

      check_voting_eligibility(25, True, False)

  - title: "Free Shipping Calculator"
    difficulty: intermediate
    description: "Create a function that determines if an order qualifies for free shipping. Free shipping if: (order total >= $50) OR (customer is premium member) OR (order has 10+ items AND total >= $30). Print qualification status."
    starter_code: |
      def check_free_shipping(order_total, is_premium, item_count):
          # Combine multiple conditions with OR and AND
          pass

      # Test: $40 order, not premium, 12 items
      check_free_shipping(40, False, 12)

    expected_output: |
      Qualifies for free shipping
    hints:
      - "Use OR to combine three conditions"
      - "Third condition needs AND: item_count >= 10 and order_total >= 30"
      - "Use parentheses for clarity: (condition1) or (condition2) or (condition3)"
    solution: |
      def check_free_shipping(order_total, is_premium, item_count):
          if order_total >= 50 or is_premium or (item_count >= 10 and order_total >= 30):
              print("Qualifies for free shipping")
          else:
              print("Does not qualify for free shipping")

      check_free_shipping(40, False, 12)

  - title: "Security System Controller"
    difficulty: advanced
    description: "Build a security system that determines alarm status. Trigger alarm if: (motion detected AND NOT armed away mode) OR (door open AND after hours) OR (glass broken). After hours is 10 PM to 6 AM (22-6). Print alarm status and reason."
    starter_code: |
      def check_alarm(motion_detected, armed_away, door_open, hour, glass_broken):
          # Complex logical conditions
          pass

      # Test: motion detected, not armed away, door closed, 2 AM, no glass broken
      check_alarm(True, False, False, 2, False)

    expected_output: |
      🚨 ALARM TRIGGERED
      Reason: Motion detected while not in away mode
    hints:
      - "After hours: hour >= 22 or hour < 6"
      - "First condition: motion_detected and not armed_away"
      - "Second condition: door_open and (hour >= 22 or hour < 6)"
      - "Third condition: glass_broken (always triggers)"
      - "Combine all three with OR"
    solution: |
      def check_alarm(motion_detected, armed_away, door_open, hour, glass_broken):
          after_hours = hour >= 22 or hour < 6

          trigger1 = motion_detected and not armed_away
          trigger2 = door_open and after_hours
          trigger3 = glass_broken

          if trigger1 or trigger2 or trigger3:
              print("🚨 ALARM TRIGGERED")
              if trigger1:
                  print("Reason: Motion detected while not in away mode")
              if trigger2:
                  print("Reason: Door opened during after hours")
              if trigger3:
                  print("Reason: Glass breakage detected")
          else:
              print("System armed - All clear")

      check_alarm(True, False, False, 2, False)

  - title: "Loan Approval System"
    difficulty: advanced
    description: "Create a comprehensive loan approval function. Approve if: (credit_score >= 700 AND income >= 50000 AND debt_ratio < 0.4) OR (credit_score >= 650 AND income >= 75000 AND debt_ratio < 0.3 AND has_cosigner). Print detailed decision with reasons."
    starter_code: |
      def evaluate_loan_application(credit_score, annual_income, debt_ratio, has_cosigner):
          # Complex approval logic with multiple paths
          pass

      # Test: 680 score, $80000 income, 0.25 debt ratio, has cosigner
      evaluate_loan_application(680, 80000, 0.25, True)

    expected_output: |
      ✅ LOAN APPROVED
      Approval path: Alternative criteria with cosigner
      Credit Score: 680
      Annual Income: $80,000
      Debt-to-Income Ratio: 25.0%
    hints:
      - "Create two approval paths: standard and alternative"
      - "Standard: credit_score >= 700 and annual_income >= 50000 and debt_ratio < 0.4"
      - "Alternative: credit_score >= 650 and annual_income >= 75000 and debt_ratio < 0.3 and has_cosigner"
      - "Use OR to combine both paths"
      - "Format debt_ratio as percentage: debt_ratio * 100"
    solution: |
      def evaluate_loan_application(credit_score, annual_income, debt_ratio, has_cosigner):
          standard_approval = (credit_score >= 700 and
                              annual_income >= 50000 and
                              debt_ratio < 0.4)

          alternative_approval = (credit_score >= 650 and
                                 annual_income >= 75000 and
                                 debt_ratio < 0.3 and
                                 has_cosigner)

          if standard_approval or alternative_approval:
              print("✅ LOAN APPROVED")
              if standard_approval:
                  print("Approval path: Standard criteria met")
              else:
                  print("Approval path: Alternative criteria with cosigner")
              print(f"Credit Score: {credit_score}")
              print(f"Annual Income: ${annual_income:,}")
              print(f"Debt-to-Income Ratio: {debt_ratio * 100:.1f}%")
          else:
              print("❌ LOAN DENIED")
              print("Does not meet approval criteria")

      evaluate_loan_application(680, 80000, 0.25, True)
```
<!-- EXERCISE_END -->
