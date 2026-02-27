# Class Variables

Class variables are attributes that are shared among all instances of a class. Unlike instance variables which are unique to each object, class variables belong to the class itself and are the same for every instance. They are useful for storing data that should be consistent across all objects, such as constants, counters, or default configurations.

## Understanding Class Variables

Class variables are defined directly in the class body, outside of any methods. They are accessed using the class name or through instances, but when modified through the class name, the change affects all instances. This makes them ideal for shared data and configurations.

```python
class Employee:
    """Demonstrates class variables vs instance variables"""

    # Class variables - shared by all instances
    company_name = "Tech Corp"
    employee_count = 0
    raise_percentage = 1.05

    def __init__(self, name, salary):
        """Initialize employee with instance variables"""
        # Instance variables - unique to each instance
        self.name = name
        self.salary = salary

        # Increment class variable when new employee is created
        Employee.employee_count += 1

    def apply_raise(self):
        """Apply raise using class variable percentage"""
        self.salary = int(self.salary * Employee.raise_percentage)
        return f"{self.name}'s new salary: ${self.salary}"

    def get_info(self):
        """Get employee information"""
        return f"{self.name} at {Employee.company_name} - ${self.salary}"

    @classmethod
    def set_raise_percentage(cls, percentage):
        """Class method to modify class variable"""
        cls.raise_percentage = percentage

    @classmethod
    def get_employee_count(cls):
        """Class method to access class variable"""
        return f"Total employees: {cls.employee_count}"

# Creating employees
emp1 = Employee("Alice", 50000)
emp2 = Employee("Bob", 60000)
emp3 = Employee("Charlie", 55000)

print(Employee.get_employee_count())  # Total employees: 3
print(f"Company: {Employee.company_name}")

# Modifying class variable affects all instances
Employee.set_raise_percentage(1.10)
print(emp1.apply_raise())
print(emp2.apply_raise())
```

## Class Variables vs Instance Variables

Understanding the difference between class and instance variables is crucial. Class variables are shared and accessed via the class, while instance variables are unique to each object. The table below summarizes the key differences:

| Feature | Class Variable | Instance Variable |
|---------|---------------|-------------------|
| Scope | Shared across all instances | Unique to each instance |
| Definition | In class body | In `__init__` with `self` |
| Access | `ClassName.variable` or `self.variable` | `self.variable` |
| Modification | Through class name | Through instance |
| Use Case | Constants, counters, defaults | Object-specific data |

```python
class BankAccount:
    """Bank account demonstrating class and instance variables"""

    # Class variables
    bank_name = "Python Bank"
    interest_rate = 0.03
    total_accounts = 0
    total_balance = 0

    def __init__(self, owner, account_number, initial_balance=0):
        """Initialize account with instance variables"""
        # Instance variables
        self.owner = owner
        self.account_number = account_number
        self.balance = initial_balance
        self.transactions = []

        # Update class variables
        BankAccount.total_accounts += 1
        BankAccount.total_balance += initial_balance

    def deposit(self, amount):
        """Deposit money"""
        if amount > 0:
            self.balance += amount
            BankAccount.total_balance += amount
            self.transactions.append(f"Deposit: +${amount}")
            return f"Deposited ${amount}. Balance: ${self.balance}"
        return "Invalid amount"

    def withdraw(self, amount):
        """Withdraw money"""
        if 0 < amount <= self.balance:
            self.balance -= amount
            BankAccount.total_balance -= amount
            self.transactions.append(f"Withdrawal: -${amount}")
            return f"Withdrew ${amount}. Balance: ${self.balance}"
        return "Insufficient funds"

    def apply_interest(self):
        """Apply interest using class variable rate"""
        interest = self.balance * BankAccount.interest_rate
        self.balance += interest
        BankAccount.total_balance += interest
        return f"Interest applied: ${interest:.2f}. New balance: ${self.balance:.2f}"

    @classmethod
    def get_bank_stats(cls):
        """Get bank-wide statistics"""
        return {
            "bank": cls.bank_name,
            "total_accounts": cls.total_accounts,
            "total_balance": f"${cls.total_balance:.2f}",
            "interest_rate": f"{cls.interest_rate * 100}%"
        }

    @classmethod
    def set_interest_rate(cls, rate):
        """Update interest rate for all accounts"""
        if 0 <= rate <= 0.20:
            cls.interest_rate = rate
            return f"Interest rate updated to {rate * 100}%"
        return "Invalid interest rate"

# Creating accounts
acc1 = BankAccount("Alice", "ACC001", 1000)
acc2 = BankAccount("Bob", "ACC002", 2000)
acc3 = BankAccount("Charlie", "ACC003", 1500)

acc1.deposit(500)
acc2.withdraw(300)

print(BankAccount.get_bank_stats())
print(acc1.apply_interest())
```

## Class Constants and Configuration

Class variables are perfect for storing constants and default configurations that should be consistent across all instances. Using uppercase names for constants is a Python convention.

```python
class GameCharacter:
    """Game character with class-level constants and defaults"""

    # Constants (uppercase by convention)
    MAX_LEVEL = 100
    MAX_HEALTH = 1000
    MAX_INVENTORY_SIZE = 50

    # Default configurations
    default_health = 100
    default_strength = 10
    default_defense = 5

    # Class-wide statistics
    characters_created = 0
    total_experience = 0

    def __init__(self, name, character_class):
        """Initialize character with defaults"""
        self.name = name
        self.character_class = character_class
        self.level = 1
        self.health = GameCharacter.default_health
        self.max_health = GameCharacter.default_health
        self.strength = GameCharacter.default_strength
        self.defense = GameCharacter.default_defense
        self.experience = 0
        self.inventory = []

        GameCharacter.characters_created += 1

    def gain_experience(self, amount):
        """Gain experience and level up if needed"""
        self.experience += amount
        GameCharacter.total_experience += amount

        # Check for level up
        experience_needed = self.level * 100
        if self.experience >= experience_needed and self.level < GameCharacter.MAX_LEVEL:
            self.level_up()

        return f"{self.name} gained {amount} XP"

    def level_up(self):
        """Level up character"""
        if self.level < GameCharacter.MAX_LEVEL:
            self.level += 1
            self.strength += 2
            self.defense += 1
            self.max_health += 10
            self.health = self.max_health
            return f"{self.name} leveled up to {self.level}!"
        return "Max level reached"

    def add_to_inventory(self, item):
        """Add item to inventory"""
        if len(self.inventory) < GameCharacter.MAX_INVENTORY_SIZE:
            self.inventory.append(item)
            return f"Added {item} to inventory"
        return "Inventory full"

    def take_damage(self, damage):
        """Take damage accounting for defense"""
        actual_damage = max(0, damage - self.defense)
        self.health = max(0, self.health - actual_damage)

        if self.health == 0:
            return f"{self.name} has been defeated!"
        return f"{self.name} took {actual_damage} damage. Health: {self.health}/{self.max_health}"

    @classmethod
    def get_game_stats(cls):
        """Get game-wide statistics"""
        avg_exp = cls.total_experience / cls.characters_created if cls.characters_created > 0 else 0
        return {
            "characters_created": cls.characters_created,
            "total_experience": cls.total_experience,
            "average_experience": round(avg_exp, 2),
            "max_level": cls.MAX_LEVEL
        }

    @classmethod
    def adjust_difficulty(cls, multiplier):
        """Adjust default stats based on difficulty"""
        cls.default_health = int(100 * multiplier)
        cls.default_strength = int(10 * multiplier)
        cls.default_defense = int(5 * multiplier)
        return f"Difficulty adjusted (x{multiplier})"

# Create characters
warrior = GameCharacter("Conan", "Warrior")
mage = GameCharacter("Gandalf", "Mage")

warrior.gain_experience(150)
warrior.add_to_inventory("Sword")
warrior.take_damage(25)

mage.gain_experience(200)

print(GameCharacter.get_game_stats())
```

## Tracking and Counting with Class Variables

Class variables are excellent for tracking statistics across all instances, such as counting objects created, tracking totals, or maintaining shared state.

```python
class Order:
    """Order system using class variables for tracking"""

    # Order tracking
    order_count = 0
    total_revenue = 0
    order_history = []

    # Status constants
    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_SHIPPED = "shipped"
    STATUS_DELIVERED = "delivered"

    # Configuration
    tax_rate = 0.08
    shipping_cost = 10.00

    def __init__(self, customer_name, items):
        """Initialize order"""
        Order.order_count += 1
        self.order_id = f"ORD{Order.order_count:05d}"
        self.customer_name = customer_name
        self.items = items  # List of {"name": str, "price": float, "quantity": int}
        self.status = Order.STATUS_PENDING
        self.subtotal = self._calculate_subtotal()
        self.tax = self.subtotal * Order.tax_rate
        self.total = self.subtotal + self.tax + Order.shipping_cost

        # Update class variables
        Order.total_revenue += self.total
        Order.order_history.append(self.order_id)

    def _calculate_subtotal(self):
        """Calculate subtotal (private helper method)"""
        return sum(item["price"] * item["quantity"] for item in self.items)

    def update_status(self, new_status):
        """Update order status"""
        valid_statuses = [
            Order.STATUS_PENDING,
            Order.STATUS_PROCESSING,
            Order.STATUS_SHIPPED,
            Order.STATUS_DELIVERED
        ]

        if new_status in valid_statuses:
            self.status = new_status
            return f"Order {self.order_id} status updated to {new_status}"
        return "Invalid status"

    def get_summary(self):
        """Get order summary"""
        summary = f"Order ID: {self.order_id}\n"
        summary += f"Customer: {self.customer_name}\n"
        summary += f"Status: {self.status}\n"
        summary += f"Subtotal: ${self.subtotal:.2f}\n"
        summary += f"Tax: ${self.tax:.2f}\n"
        summary += f"Shipping: ${Order.shipping_cost:.2f}\n"
        summary += f"Total: ${self.total:.2f}"
        return summary

    @classmethod
    def get_statistics(cls):
        """Get order statistics"""
        avg_order = cls.total_revenue / cls.order_count if cls.order_count > 0 else 0
        return {
            "total_orders": cls.order_count,
            "total_revenue": f"${cls.total_revenue:.2f}",
            "average_order_value": f"${avg_order:.2f}",
            "recent_orders": cls.order_history[-5:]
        }

    @classmethod
    def set_tax_rate(cls, rate):
        """Update tax rate"""
        if 0 <= rate <= 0.20:
            cls.tax_rate = rate
            return f"Tax rate updated to {rate * 100}%"
        return "Invalid tax rate"

    @classmethod
    def set_shipping_cost(cls, cost):
        """Update shipping cost"""
        if cost >= 0:
            cls.shipping_cost = cost
            return f"Shipping cost updated to ${cost}"
        return "Invalid shipping cost"

# Create orders
items1 = [
    {"name": "Laptop", "price": 999.99, "quantity": 1},
    {"name": "Mouse", "price": 29.99, "quantity": 2}
]
items2 = [
    {"name": "Keyboard", "price": 79.99, "quantity": 1},
    {"name": "Monitor", "price": 299.99, "quantity": 1}
]

order1 = Order("Alice Johnson", items1)
order2 = Order("Bob Smith", items2)

order1.update_status(Order.STATUS_SHIPPED)
order2.update_status(Order.STATUS_PROCESSING)

print(order1.get_summary())
print("\n" + "="*40 + "\n")
print(Order.get_statistics())
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Student ID Counter"
    difficulty: basic
    description: "Create a Student class that automatically assigns unique student IDs using a class variable counter."
    starter_code: |
      class Student:
          # TODO: Add class variable for student count

          def __init__(self, name):
              # TODO: Increment counter and assign unique ID
              # TODO: Set name
              pass

          @classmethod
          def get_total_students(cls):
              # TODO: Return total number of students
              pass

      s1 = Student("Alice")
      s2 = Student("Bob")
      s3 = Student("Charlie")
      print(f"Student {s1.name} has ID: {s1.student_id}")
      print(f"Total students: {Student.get_total_students()}")
    expected_output: |
      Student Alice has ID: 1
      Total students: 3
    hints:
      - "Create a class variable student_count = 0"
      - "Increment the counter in __init__"
      - "Assign the current counter value to self.student_id"
    solution: |
      class Student:
          student_count = 0

          def __init__(self, name):
              Student.student_count += 1
              self.student_id = Student.student_count
              self.name = name

          @classmethod
          def get_total_students(cls):
              return cls.student_count

      s1 = Student("Alice")
      s2 = Student("Bob")
      s3 = Student("Charlie")
      print(f"Student {s1.name} has ID: {s1.student_id}")
      print(f"Total students: {Student.get_total_students()}")

  - title: "Pizza Shop with Class Constants"
    difficulty: basic
    description: "Create a Pizza class with class constants for sizes and a base price. Calculate total price based on size multiplier."
    starter_code: |
      class Pizza:
          # TODO: Add class constants for sizes and prices
          BASE_PRICE = 10.00
          SIZE_SMALL = 1.0
          SIZE_MEDIUM = 1.5
          SIZE_LARGE = 2.0

          def __init__(self, size_multiplier, toppings):
              # TODO: Initialize size and toppings
              # TODO: Calculate price
              pass

          def get_price(self):
              # TODO: Return total price
              pass

      pizza1 = Pizza(Pizza.SIZE_MEDIUM, ["pepperoni", "mushrooms"])
      pizza2 = Pizza(Pizza.SIZE_LARGE, ["extra cheese"])
      print(f"Medium pizza: ${pizza1.get_price()}")
      print(f"Large pizza: ${pizza2.get_price()}")
    expected_output: |
      Medium pizza: $15.0
      Large pizza: $20.0
    hints:
      - "Price = BASE_PRICE * size_multiplier"
      - "Store size_multiplier and toppings as instance variables"
      - "Calculate price in __init__"
    solution: |
      class Pizza:
          BASE_PRICE = 10.00
          SIZE_SMALL = 1.0
          SIZE_MEDIUM = 1.5
          SIZE_LARGE = 2.0

          def __init__(self, size_multiplier, toppings):
              self.size_multiplier = size_multiplier
              self.toppings = toppings
              self.price = Pizza.BASE_PRICE * size_multiplier

          def get_price(self):
              return self.price

      pizza1 = Pizza(Pizza.SIZE_MEDIUM, ["pepperoni", "mushrooms"])
      pizza2 = Pizza(Pizza.SIZE_LARGE, ["extra cheese"])
      print(f"Medium pizza: ${pizza1.get_price()}")
      print(f"Large pizza: ${pizza2.get_price()}")

  - title: "Library Book Tracking"
    difficulty: intermediate
    description: "Create a Book class that tracks total books, total pages, and provides class methods to get statistics."
    starter_code: |
      class Book:
          # TODO: Add class variables for tracking

          def __init__(self, title, author, pages):
              # TODO: Initialize instance variables
              # TODO: Update class variables
              pass

          @classmethod
          def get_total_books(cls):
              # TODO: Return total books
              pass

          @classmethod
          def get_average_pages(cls):
              # TODO: Calculate and return average pages
              pass

      b1 = Book("1984", "Orwell", 328)
      b2 = Book("Brave New World", "Huxley", 288)
      b3 = Book("Fahrenheit 451", "Bradbury", 158)
      print(f"Total books: {Book.get_total_books()}")
      print(f"Average pages: {Book.get_average_pages()}")
    expected_output: |
      Total books: 3
      Average pages: 258.0
    hints:
      - "Create class variables: total_books and total_pages"
      - "Increment both in __init__"
      - "Average = total_pages / total_books"
    solution: |
      class Book:
          total_books = 0
          total_pages = 0

          def __init__(self, title, author, pages):
              self.title = title
              self.author = author
              self.pages = pages
              Book.total_books += 1
              Book.total_pages += pages

          @classmethod
          def get_total_books(cls):
              return cls.total_books

          @classmethod
          def get_average_pages(cls):
              if cls.total_books == 0:
                  return 0
              return cls.total_pages / cls.total_books

      b1 = Book("1984", "Orwell", 328)
      b2 = Book("Brave New World", "Huxley", 288)
      b3 = Book("Fahrenheit 451", "Bradbury", 158)
      print(f"Total books: {Book.get_total_books()}")
      print(f"Average pages: {Book.get_average_pages()}")

  - title: "Product with Dynamic Tax Rate"
    difficulty: intermediate
    description: "Create a Product class with a class variable tax_rate that can be updated. Calculate prices including tax."
    starter_code: |
      class Product:
          tax_rate = 0.10  # Default 10% tax

          def __init__(self, name, base_price):
              # TODO: Initialize name and base_price
              pass

          def get_price_with_tax(self):
              # TODO: Calculate price including tax
              pass

          @classmethod
          def set_tax_rate(cls, rate):
              # TODO: Update tax rate
              pass

      p1 = Product("Laptop", 1000)
      p2 = Product("Mouse", 50)
      print(f"Laptop with tax: ${p1.get_price_with_tax()}")
      Product.set_tax_rate(0.08)
      print(f"Laptop with new tax: ${p1.get_price_with_tax()}")
    expected_output: |
      Laptop with tax: $1100.0
      Laptop with new tax: $1080.0
    hints:
      - "Price with tax = base_price * (1 + tax_rate)"
      - "Use Product.tax_rate in calculation"
      - "When tax_rate changes, all products are affected"
    solution: |
      class Product:
          tax_rate = 0.10

          def __init__(self, name, base_price):
              self.name = name
              self.base_price = base_price

          def get_price_with_tax(self):
              return self.base_price * (1 + Product.tax_rate)

          @classmethod
          def set_tax_rate(cls, rate):
              cls.tax_rate = rate

      p1 = Product("Laptop", 1000)
      p2 = Product("Mouse", 50)
      print(f"Laptop with tax: ${p1.get_price_with_tax()}")
      Product.set_tax_rate(0.08)
      print(f"Laptop with new tax: ${p1.get_price_with_tax()}")

  - title: "Game Character Class System"
    difficulty: advanced
    description: "Create a Character class with class variables for different character classes (Warrior, Mage, Rogue) with different stat multipliers."
    starter_code: |
      class Character:
          # TODO: Add class constants for character classes
          # TODO: Add stat multipliers dictionary
          total_characters = 0

          CLASS_WARRIOR = "warrior"
          CLASS_MAGE = "mage"
          CLASS_ROGUE = "rogue"

          stat_multipliers = {
              CLASS_WARRIOR: {"strength": 1.5, "intelligence": 0.8, "agility": 1.0},
              CLASS_MAGE: {"strength": 0.7, "intelligence": 1.8, "agility": 0.9},
              CLASS_ROGUE: {"strength": 1.0, "intelligence": 1.0, "agility": 1.6}
          }

          def __init__(self, name, char_class, base_stats=None):
              # TODO: Initialize with base stats and apply multipliers
              pass

          def get_total_power(self):
              # TODO: Calculate total power (sum of all stats)
              pass

          @classmethod
          def get_class_info(cls, char_class):
              # TODO: Return multipliers for a class
              pass

      warrior = Character("Conan", Character.CLASS_WARRIOR, {"strength": 10, "intelligence": 10, "agility": 10})
      mage = Character("Gandalf", Character.CLASS_MAGE, {"strength": 10, "intelligence": 10, "agility": 10})
      print(f"Warrior power: {warrior.get_total_power()}")
      print(f"Mage power: {mage.get_total_power()}")
    expected_output: |
      Warrior power: 33.0
      Mage power: 34.0
    hints:
      - "Apply multipliers to base stats in __init__"
      - "Store calculated stats as instance variables"
      - "Total power = sum of all stat values"
    solution: |
      class Character:
          total_characters = 0

          CLASS_WARRIOR = "warrior"
          CLASS_MAGE = "mage"
          CLASS_ROGUE = "rogue"

          stat_multipliers = {
              CLASS_WARRIOR: {"strength": 1.5, "intelligence": 0.8, "agility": 1.0},
              CLASS_MAGE: {"strength": 0.7, "intelligence": 1.8, "agility": 0.9},
              CLASS_ROGUE: {"strength": 1.0, "intelligence": 1.0, "agility": 1.6}
          }

          def __init__(self, name, char_class, base_stats=None):
              self.name = name
              self.char_class = char_class

              if base_stats is None:
                  base_stats = {"strength": 10, "intelligence": 10, "agility": 10}

              multipliers = Character.stat_multipliers[char_class]
              self.strength = base_stats["strength"] * multipliers["strength"]
              self.intelligence = base_stats["intelligence"] * multipliers["intelligence"]
              self.agility = base_stats["agility"] * multipliers["agility"]

              Character.total_characters += 1

          def get_total_power(self):
              return self.strength + self.intelligence + self.agility

          @classmethod
          def get_class_info(cls, char_class):
              return cls.stat_multipliers.get(char_class, {})

      warrior = Character("Conan", Character.CLASS_WARRIOR, {"strength": 10, "intelligence": 10, "agility": 10})
      mage = Character("Gandalf", Character.CLASS_MAGE, {"strength": 10, "intelligence": 10, "agility": 10})
      print(f"Warrior power: {warrior.get_total_power()}")
      print(f"Mage power: {mage.get_total_power()}")

  - title: "Flight Booking System"
    difficulty: advanced
    description: "Create a Flight class that tracks total bookings, revenue, and available seats across all flights. Include class methods for statistics."
    starter_code: |
      class Flight:
          # TODO: Add class variables for tracking
          total_bookings = 0
          total_revenue = 0
          all_flights = []

          def __init__(self, flight_number, destination, total_seats, price_per_seat):
              # TODO: Initialize flight details
              # TODO: Add to all_flights list
              pass

          def book_seats(self, num_seats):
              # TODO: Book seats if available
              # TODO: Update class variables
              pass

          @classmethod
          def get_statistics(cls):
              # TODO: Return booking statistics
              pass

          @classmethod
          def get_available_flights(cls):
              # TODO: Return flights with available seats
              pass

      f1 = Flight("AA101", "New York", 100, 250)
      f2 = Flight("AA102", "London", 150, 500)
      f1.book_seats(30)
      f2.book_seats(50)
      print(f"Total revenue: ${Flight.total_revenue}")
      print(f"Total bookings: {Flight.total_bookings}")
    expected_output: |
      Total revenue: $32500
      Total bookings: 80
    hints:
      - "Track booked_seats as instance variable"
      - "Update total_bookings and total_revenue when booking"
      - "Calculate revenue as num_seats * price_per_seat"
    solution: |
      class Flight:
          total_bookings = 0
          total_revenue = 0
          all_flights = []

          def __init__(self, flight_number, destination, total_seats, price_per_seat):
              self.flight_number = flight_number
              self.destination = destination
              self.total_seats = total_seats
              self.price_per_seat = price_per_seat
              self.booked_seats = 0
              Flight.all_flights.append(self)

          def book_seats(self, num_seats):
              available = self.total_seats - self.booked_seats
              if num_seats <= available:
                  self.booked_seats += num_seats
                  Flight.total_bookings += num_seats
                  revenue = num_seats * self.price_per_seat
                  Flight.total_revenue += revenue
                  return f"Booked {num_seats} seats"
              return "Not enough seats available"

          @classmethod
          def get_statistics(cls):
              return {
                  "total_bookings": cls.total_bookings,
                  "total_revenue": cls.total_revenue,
                  "total_flights": len(cls.all_flights)
              }

          @classmethod
          def get_available_flights(cls):
              return [f for f in cls.all_flights if f.booked_seats < f.total_seats]

      f1 = Flight("AA101", "New York", 100, 250)
      f2 = Flight("AA102", "London", 150, 500)
      f1.book_seats(30)
      f2.book_seats(50)
      print(f"Total revenue: ${Flight.total_revenue}")
      print(f"Total bookings: {Flight.total_bookings}")
```
<!-- EXERCISE_END -->
