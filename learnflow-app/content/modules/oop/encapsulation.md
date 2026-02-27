# Encapsulation

Encapsulation is the practice of bundling data and methods that operate on that data within a single unit (class), while controlling access to that data. It's a fundamental principle of object-oriented programming that promotes data hiding, reduces complexity, and protects object integrity by preventing external code from directly accessing or modifying internal state.

## Understanding Encapsulation

Encapsulation involves restricting direct access to an object's internal state and requiring interaction through well-defined methods. This protects data from unauthorized access and modification, making code more maintainable and less prone to bugs. In Python, encapsulation is achieved through naming conventions and properties.

```python
class BankAccount:
    """Bank account demonstrating encapsulation"""

    def __init__(self, account_number, owner, initial_balance=0):
        # Public attributes (by convention)
        self.account_number = account_number
        self.owner = owner

        # Protected attributes (single underscore - internal use)
        self._balance = initial_balance
        self._transaction_history = []

        # Private attributes (double underscore - name mangling)
        self.__pin = "0000"

    def deposit(self, amount):
        """Public method to deposit money"""
        if amount > 0:
            self._balance += amount
            self._add_transaction("deposit", amount)
            return f"Deposited ${amount}. New balance: ${self._balance}"
        return "Invalid deposit amount"

    def withdraw(self, amount, pin):
        """Public method to withdraw money"""
        if not self.__verify_pin(pin):
            return "Invalid PIN"

        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            self._add_transaction("withdrawal", amount)
            return f"Withdrew ${amount}. New balance: ${self._balance}"
        return "Invalid withdrawal amount or insufficient funds"

    def get_balance(self, pin):
        """Public method to check balance"""
        if self.__verify_pin(pin):
            return f"Current balance: ${self._balance}"
        return "Invalid PIN"

    def change_pin(self, old_pin, new_pin):
        """Public method to change PIN"""
        if self.__verify_pin(old_pin):
            if len(new_pin) == 4 and new_pin.isdigit():
                self.__pin = new_pin
                return "PIN changed successfully"
            return "Invalid PIN format (must be 4 digits)"
        return "Invalid current PIN"

    def _add_transaction(self, transaction_type, amount):
        """Protected method - for internal use"""
        from datetime import datetime
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self._transaction_history.append(transaction)

    def __verify_pin(self, pin):
        """Private method - name mangling"""
        return pin == self.__pin

    def get_statement(self, pin):
        """Get account statement"""
        if not self.__verify_pin(pin):
            return "Invalid PIN"

        statement = f"Account Statement for {self.owner}\n"
        statement += f"Account Number: {self.account_number}\n"
        statement += f"Current Balance: ${self._balance}\n"
        statement += "\nRecent Transactions:\n"

        for trans in self._transaction_history[-5:]:
            statement += f"  {trans['timestamp']} - {trans['type']}: ${trans['amount']}\n"

        return statement

# Using encapsulation
account = BankAccount("ACC001", "John Doe", 1000)

# Public interface
print(account.deposit(500))
print(account.withdraw(200, "0000"))
print(account.get_balance("0000"))

# Change PIN
print(account.change_pin("0000", "1234"))
print(account.get_balance("1234"))

# Cannot access private PIN directly (but can access mangled name)
# print(account.__pin)  # AttributeError
# print(account._BankAccount__pin)  # Works but breaks encapsulation
```

## Access Modifiers in Python

Python uses naming conventions to indicate the intended access level of attributes and methods. Understanding these conventions is essential for proper encapsulation.

| Convention | Access Level | Example | Purpose |
|------------|-------------|---------|---------|
| `name` | Public | `self.balance` | Accessible from anywhere |
| `_name` | Protected | `self._internal` | Internal use, but accessible |
| `__name` | Private | `self.__secret` | Name mangled, strongly private |
| `__name__` | Special | `__init__` | Python's magic methods |

```python
class Employee:
    """Employee class demonstrating access levels"""

    # Class variable - public
    company_name = "Tech Corp"

    def __init__(self, name, employee_id, salary):
        # Public attribute
        self.name = name
        self.employee_id = employee_id

        # Protected attribute (by convention)
        self._salary = salary
        self._department = None

        # Private attribute (name mangling)
        self.__social_security = "XXX-XX-XXXX"
        self.__performance_score = 0

    # Public method
    def get_info(self):
        """Get employee information"""
        return f"{self.name} ({self.employee_id})"

    # Protected method
    def _calculate_bonus(self):
        """Calculate bonus based on performance"""
        return self._salary * (self.__performance_score / 100)

    # Private method
    def __validate_salary(self, amount):
        """Validate salary amount"""
        return amount > 0 and amount < 1000000

    # Public method using private/protected methods
    def give_raise(self, amount):
        """Give raise to employee"""
        if self.__validate_salary(self._salary + amount):
            self._salary += amount
            return f"Raise approved. New salary: ${self._salary}"
        return "Invalid raise amount"

    def set_performance_score(self, score):
        """Set performance score"""
        if 0 <= score <= 100:
            self.__performance_score = score
            return f"Performance score set to {score}"
        return "Invalid score (must be 0-100)"

    def get_total_compensation(self):
        """Get total compensation including bonus"""
        bonus = self._calculate_bonus()
        return {
            "salary": self._salary,
            "bonus": bonus,
            "total": self._salary + bonus
        }

# Using the employee class
emp = Employee("Alice Johnson", "E001", 75000)

# Access public members
print(emp.name)
print(emp.get_info())

# Access protected member (possible but not recommended)
print(f"Salary (protected): ${emp._salary}")

# Cannot easily access private members
# print(emp.__social_security)  # AttributeError

# Use public interface
emp.set_performance_score(85)
print(emp.give_raise(5000))
print(f"Total compensation: {emp.get_total_compensation()}")
```

## Properties and Getters/Setters

Python's property decorator provides a Pythonic way to implement getters, setters, and deleters, allowing you to add validation and logic while maintaining a simple attribute-like interface.

```python
class Temperature:
    """Temperature class using properties"""

    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        """Get temperature in Celsius"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """Set temperature in Celsius with validation"""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):
        """Get temperature in Fahrenheit"""
        return (self._celsius * 9/5) + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        """Set temperature using Fahrenheit"""
        celsius = (value - 32) * 5/9
        self.celsius = celsius  # Uses celsius setter for validation

    @property
    def kelvin(self):
        """Get temperature in Kelvin"""
        return self._celsius + 273.15

    @kelvin.setter
    def kelvin(self, value):
        """Set temperature using Kelvin"""
        self.celsius = value - 273.15  # Uses celsius setter

class Rectangle:
    """Rectangle class with computed properties"""

    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def width(self):
        """Get width"""
        return self._width

    @width.setter
    def width(self, value):
        """Set width with validation"""
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value

    @property
    def height(self):
        """Get height"""
        return self._height

    @height.setter
    def height(self, value):
        """Set height with validation"""
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value

    @property
    def area(self):
        """Computed property - area"""
        return self._width * self._height

    @property
    def perimeter(self):
        """Computed property - perimeter"""
        return 2 * (self._width + self._height)

    @property
    def diagonal(self):
        """Computed property - diagonal"""
        return (self._width ** 2 + self._height ** 2) ** 0.5

# Using properties
temp = Temperature(25)
print(f"Celsius: {temp.celsius}")
print(f"Fahrenheit: {temp.fahrenheit}")
print(f"Kelvin: {temp.kelvin}")

# Set using different units
temp.fahrenheit = 98.6
print(f"New Celsius: {temp.celsius:.1f}")

rect = Rectangle(5, 3)
print(f"Area: {rect.area}")
print(f"Perimeter: {rect.perimeter}")

# Modify dimensions
rect.width = 10
print(f"New area: {rect.area}")
```

## Data Validation and Integrity

Encapsulation allows you to enforce business rules and maintain data integrity by validating inputs and ensuring objects remain in valid states.

```python
class CreditCard:
    """Credit card with strong encapsulation and validation"""

    def __init__(self, card_number, holder_name, cvv, expiry_month, expiry_year):
        # Use setters for validation
        self.card_number = card_number
        self.holder_name = holder_name
        self.cvv = cvv
        self.expiry_month = expiry_month
        self.expiry_year = expiry_year

        # Private attributes
        self.__balance = 0
        self.__credit_limit = 5000
        self.__is_active = True

    @property
    def card_number(self):
        """Get masked card number"""
        return f"****-****-****-{self._card_number[-4:]}"

    @card_number.setter
    def card_number(self, value):
        """Set card number with validation"""
        # Remove spaces and dashes
        cleaned = value.replace(" ", "").replace("-", "")

        if not cleaned.isdigit():
            raise ValueError("Card number must contain only digits")
        if len(cleaned) != 16:
            raise ValueError("Card number must be 16 digits")

        self._card_number = cleaned

    @property
    def holder_name(self):
        """Get holder name"""
        return self._holder_name

    @holder_name.setter
    def holder_name(self, value):
        """Set holder name with validation"""
        if not value or len(value.strip()) < 2:
            raise ValueError("Holder name must be at least 2 characters")
        self._holder_name = value.strip().upper()

    @property
    def cvv(self):
        """CVV is write-only for security"""
        raise AttributeError("CVV cannot be read")

    @cvv.setter
    def cvv(self, value):
        """Set CVV with validation"""
        if not isinstance(value, str) or len(value) not in [3, 4]:
            raise ValueError("CVV must be 3 or 4 digits")
        if not value.isdigit():
            raise ValueError("CVV must contain only digits")
        self.__cvv = value

    @property
    def expiry_month(self):
        """Get expiry month"""
        return self._expiry_month

    @expiry_month.setter
    def expiry_month(self, value):
        """Set expiry month with validation"""
        if not 1 <= value <= 12:
            raise ValueError("Expiry month must be between 1 and 12")
        self._expiry_month = value

    @property
    def expiry_year(self):
        """Get expiry year"""
        return self._expiry_year

    @expiry_year.setter
    def expiry_year(self, value):
        """Set expiry year with validation"""
        if value < 2024:
            raise ValueError("Card has expired")
        self._expiry_year = value

    def charge(self, amount):
        """Charge amount to card"""
        if not self.__is_active:
            return "Card is not active"

        if amount <= 0:
            return "Invalid charge amount"

        if self.__balance + amount > self.__credit_limit:
            return "Transaction declined: Credit limit exceeded"

        self.__balance += amount
        return f"Charged ${amount}. Balance: ${self.__balance}"

    def make_payment(self, amount):
        """Make payment on card"""
        if amount <= 0:
            return "Invalid payment amount"

        if amount > self.__balance:
            amount = self.__balance

        self.__balance -= amount
        return f"Payment of ${amount} received. Balance: ${self.__balance}"

    def get_balance(self):
        """Get current balance"""
        return self.__balance

    def get_available_credit(self):
        """Get available credit"""
        return self.__credit_limit - self.__balance

    def set_credit_limit(self, new_limit):
        """Set new credit limit"""
        if new_limit < self.__balance:
            return "Cannot set limit below current balance"

        if new_limit < 0:
            return "Credit limit must be positive"

        self.__credit_limit = new_limit
        return f"Credit limit updated to ${new_limit}"

# Using the credit card
try:
    card = CreditCard("1234567890123456", "John Doe", "123", 12, 2025)
    print(f"Card: {card.card_number}")
    print(f"Holder: {card.holder_name}")
    print(card.charge(100))
    print(card.charge(200))
    print(f"Balance: ${card.get_balance()}")
    print(f"Available credit: ${card.get_available_credit()}")
    print(card.make_payment(150))
    print(f"New balance: ${card.get_balance()}")

    # Try to read CVV (will fail)
    # print(card.cvv)

except ValueError as e:
    print(f"Validation error: {e}")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Basic Encapsulation with Private Attribute"
    difficulty: basic
    description: "Create a Person class with a private age attribute accessible only through getter and setter methods."
    starter_code: |
      class Person:
          def __init__(self, name, age):
              self.name = name
              # TODO: Make age private (use __)
              self.__age = age

          # TODO: Add get_age method
          # TODO: Add set_age method with validation (0-120)
          pass

      person = Person("Alice", 30)
      print(f"{person.name} is {person.get_age()} years old")
      person.set_age(31)
      print(f"{person.name} is now {person.get_age()} years old")
    expected_output: |
      Alice is 30 years old
      Alice is now 31 years old
    hints:
      - "Use double underscore for private: self.__age"
      - "get_age() returns self.__age"
      - "set_age() validates age is between 0 and 120"
    solution: |
      class Person:
          def __init__(self, name, age):
              self.name = name
              self.__age = age

          def get_age(self):
              return self.__age

          def set_age(self, age):
              if 0 <= age <= 120:
                  self.__age = age
                  return True
              return False

      person = Person("Alice", 30)
      print(f"{person.name} is {person.get_age()} years old")
      person.set_age(31)
      print(f"{person.name} is now {person.get_age()} years old")

  - title: "Property Decorator for Validation"
    difficulty: basic
    description: "Create a Product class using @property decorator for price with validation."
    starter_code: |
      class Product:
          def __init__(self, name, price):
              self.name = name
              self._price = price

          # TODO: Add price property getter
          # TODO: Add price property setter with validation (price > 0)
          pass

      product = Product("Laptop", 999.99)
      print(f"{product.name}: ${product.price}")
      product.price = 1099.99
      print(f"{product.name}: ${product.price}")
    expected_output: |
      Laptop: $999.99
      Laptop: $1099.99
    hints:
      - "Use @property decorator for getter"
      - "Use @price.setter decorator for setter"
      - "Validate price > 0 in setter"
    solution: |
      class Product:
          def __init__(self, name, price):
              self.name = name
              self._price = price

          @property
          def price(self):
              return self._price

          @price.setter
          def price(self, value):
              if value > 0:
                  self._price = value
              else:
                  raise ValueError("Price must be positive")

      product = Product("Laptop", 999.99)
      print(f"{product.name}: ${product.price}")
      product.price = 1099.99
      print(f"{product.name}: ${product.price}")

  - title: "Protected Methods Pattern"
    difficulty: intermediate
    description: "Create a BankAccount class with protected methods for internal operations and public methods for user interface."
    starter_code: |
      class BankAccount:
          def __init__(self, owner, balance):
              self.owner = owner
              self._balance = balance
              self._transactions = []

          def _record_transaction(self, trans_type, amount):
              # TODO: Add transaction to list
              pass

          def deposit(self, amount):
              # TODO: Validate, update balance, record transaction
              pass

          def withdraw(self, amount):
              # TODO: Validate, check balance, update, record
              pass

          def get_balance(self):
              return self._balance

      account = BankAccount("Alice", 1000)
      account.deposit(500)
      account.withdraw(200)
      print(f"Balance: ${account.get_balance()}")
    expected_output: |
      Balance: $1300
    hints:
      - "_record_transaction is protected (single underscore)"
      - "Store transactions as dictionaries with type and amount"
      - "Call _record_transaction from deposit and withdraw"
    solution: |
      class BankAccount:
          def __init__(self, owner, balance):
              self.owner = owner
              self._balance = balance
              self._transactions = []

          def _record_transaction(self, trans_type, amount):
              self._transactions.append({"type": trans_type, "amount": amount})

          def deposit(self, amount):
              if amount > 0:
                  self._balance += amount
                  self._record_transaction("deposit", amount)
                  return True
              return False

          def withdraw(self, amount):
              if 0 < amount <= self._balance:
                  self._balance -= amount
                  self._record_transaction("withdrawal", amount)
                  return True
              return False

          def get_balance(self):
              return self._balance

      account = BankAccount("Alice", 1000)
      account.deposit(500)
      account.withdraw(200)
      print(f"Balance: ${account.get_balance()}")

  - title: "Computed Properties"
    difficulty: intermediate
    description: "Create a Circle class with radius as a property and area/circumference as computed properties."
    starter_code: |
      class Circle:
          def __init__(self, radius):
              self._radius = radius

          @property
          def radius(self):
              return self._radius

          @radius.setter
          def radius(self, value):
              # TODO: Validate radius > 0
              pass

          # TODO: Add area property (computed, no setter)
          # TODO: Add circumference property (computed, no setter)
          pass

      circle = Circle(5)
      print(f"Radius: {circle.radius}")
      print(f"Area: {circle.area:.2f}")
      print(f"Circumference: {circle.circumference:.2f}")
      circle.radius = 10
      print(f"New area: {circle.area:.2f}")
    expected_output: |
      Radius: 5
      Area: 78.54
      Circumference: 31.42
      New area: 314.16
    hints:
      - "Area = π * r²"
      - "Circumference = 2 * π * r"
      - "Use 3.14159 for π"
      - "Computed properties only have @property, no setter"
    solution: |
      class Circle:
          def __init__(self, radius):
              self._radius = radius

          @property
          def radius(self):
              return self._radius

          @radius.setter
          def radius(self, value):
              if value > 0:
                  self._radius = value
              else:
                  raise ValueError("Radius must be positive")

          @property
          def area(self):
              return 3.14159 * self._radius ** 2

          @property
          def circumference(self):
              return 2 * 3.14159 * self._radius

      circle = Circle(5)
      print(f"Radius: {circle.radius}")
      print(f"Area: {circle.area:.2f}")
      print(f"Circumference: {circle.circumference:.2f}")
      circle.radius = 10
      print(f"New area: {circle.area:.2f}")

  - title: "Data Validation with Properties"
    difficulty: advanced
    description: "Create a User class with username, email, and password properties, each with comprehensive validation."
    starter_code: |
      class User:
          def __init__(self, username, email, password):
              self.username = username
              self.email = email
              self.password = password

          @property
          def username(self):
              return self._username

          @username.setter
          def username(self, value):
              # TODO: Validate: 3-20 chars, alphanumeric only
              pass

          @property
          def email(self):
              return self._email

          @email.setter
          def email(self, value):
              # TODO: Validate: contains @ and .
              pass

          @property
          def password(self):
              # TODO: Make write-only (raise error on read)
              pass

          @password.setter
          def password(self, value):
              # TODO: Validate: at least 8 characters
              # TODO: Store hashed (use simple hash for exercise)
              pass

          def verify_password(self, password):
              # TODO: Compare hashed passwords
              pass

      user = User("alice123", "alice@example.com", "password123")
      print(f"Username: {user.username}")
      print(f"Email: {user.email}")
      print(f"Password verified: {user.verify_password('password123')}")
    expected_output: |
      Username: alice123
      Email: alice@example.com
      Password verified: True
    hints:
      - "Use str.isalnum() for alphanumeric check"
      - "Check '@' in email and '.' in email"
      - "Store hash(password) instead of plain password"
      - "Password getter should raise AttributeError"
    solution: |
      class User:
          def __init__(self, username, email, password):
              self.username = username
              self.email = email
              self.password = password

          @property
          def username(self):
              return self._username

          @username.setter
          def username(self, value):
              if not (3 <= len(value) <= 20):
                  raise ValueError("Username must be 3-20 characters")
              if not value.isalnum():
                  raise ValueError("Username must be alphanumeric")
              self._username = value

          @property
          def email(self):
              return self._email

          @email.setter
          def email(self, value):
              if '@' not in value or '.' not in value:
                  raise ValueError("Invalid email format")
              self._email = value

          @property
          def password(self):
              raise AttributeError("Password cannot be read")

          @password.setter
          def password(self, value):
              if len(value) < 8:
                  raise ValueError("Password must be at least 8 characters")
              self._password_hash = hash(value)

          def verify_password(self, password):
              return hash(password) == self._password_hash

      user = User("alice123", "alice@example.com", "password123")
      print(f"Username: {user.username}")
      print(f"Email: {user.email}")
      print(f"Password verified: {user.verify_password('password123')}")

  - title: "Complete Encapsulation System"
    difficulty: advanced
    description: "Create a Wallet class with private balance, transaction history, and PIN protection for all operations."
    starter_code: |
      class Wallet:
          def __init__(self, owner, initial_balance, pin):
              self.owner = owner
              self.__balance = initial_balance
              self.__pin = pin
              self.__transactions = []

          def __verify_pin(self, pin):
              # TODO: Verify PIN
              pass

          def __add_transaction(self, trans_type, amount):
              # TODO: Add transaction to history
              pass

          def deposit(self, amount, pin):
              # TODO: Verify PIN, validate amount, update balance
              pass

          def withdraw(self, amount, pin):
              # TODO: Verify PIN, check balance, update
              pass

          def get_balance(self, pin):
              # TODO: Verify PIN and return balance
              pass

          def change_pin(self, old_pin, new_pin):
              # TODO: Verify old PIN and change to new PIN
              pass

      wallet = Wallet("Alice", 1000, "1234")
      print(wallet.deposit(500, "1234"))
      print(wallet.withdraw(200, "1234"))
      print(f"Balance: ${wallet.get_balance('1234')}")
      wallet.change_pin("1234", "5678")
      print(f"New balance: ${wallet.get_balance('5678')}")
    expected_output: |
      Deposited $500
      Withdrew $200
      Balance: $1300
      New balance: $1300
    hints:
      - "Use double underscore for private: __balance, __pin"
      - "All operations should verify PIN first"
      - "__add_transaction is private helper method"
      - "Return descriptive messages from each operation"
    solution: |
      class Wallet:
          def __init__(self, owner, initial_balance, pin):
              self.owner = owner
              self.__balance = initial_balance
              self.__pin = pin
              self.__transactions = []

          def __verify_pin(self, pin):
              return pin == self.__pin

          def __add_transaction(self, trans_type, amount):
              self.__transactions.append({"type": trans_type, "amount": amount})

          def deposit(self, amount, pin):
              if not self.__verify_pin(pin):
                  return "Invalid PIN"
              if amount > 0:
                  self.__balance += amount
                  self.__add_transaction("deposit", amount)
                  return f"Deposited ${amount}"
              return "Invalid amount"

          def withdraw(self, amount, pin):
              if not self.__verify_pin(pin):
                  return "Invalid PIN"
              if 0 < amount <= self.__balance:
                  self.__balance -= amount
                  self.__add_transaction("withdrawal", amount)
                  return f"Withdrew ${amount}"
              return "Invalid amount or insufficient funds"

          def get_balance(self, pin):
              if not self.__verify_pin(pin):
                  return "Invalid PIN"
              return self.__balance

          def change_pin(self, old_pin, new_pin):
              if not self.__verify_pin(old_pin):
                  return "Invalid PIN"
              self.__pin = new_pin
              return "PIN changed"

      wallet = Wallet("Alice", 1000, "1234")
      print(wallet.deposit(500, "1234"))
      print(wallet.withdraw(200, "1234"))
      print(f"Balance: ${wallet.get_balance('1234')}")
      wallet.change_pin("1234", "5678")
      print(f"New balance: ${wallet.get_balance('5678')}")
```
<!-- EXERCISE_END -->
