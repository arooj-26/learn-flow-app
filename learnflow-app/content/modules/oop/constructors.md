# Constructors

Constructors are special methods that initialize objects when they are created. In Python, the constructor is the `__init__` method, which is automatically called when you instantiate a class. Understanding constructors is crucial for properly setting up objects with their initial state and ensuring that all necessary attributes are defined before the object is used.

## The __init__ Method

The `__init__` method is Python's constructor. It's called automatically when you create a new instance of a class. The first parameter is always `self`, which refers to the instance being created, followed by any parameters you want to pass during initialization.

```python
class Employee:
    """Represents an employee in a company"""

    def __init__(self, name, employee_id, department, salary):
        """Constructor to initialize employee attributes"""
        self.name = name
        self.employee_id = employee_id
        self.department = department
        self.salary = salary
        self.years_of_service = 0
        self.performance_reviews = []

    def give_raise(self, amount):
        """Increase employee salary"""
        self.salary += amount
        return f"{self.name} received a ${amount} raise. New salary: ${self.salary}"

    def add_review(self, rating, comments):
        """Add a performance review"""
        review = {"rating": rating, "comments": comments}
        self.performance_reviews.append(review)
        return f"Review added for {self.name}"

# Creating employee objects
emp1 = Employee("John Doe", "E001", "Engineering", 75000)
emp2 = Employee("Jane Smith", "E002", "Marketing", 65000)

print(f"{emp1.name} works in {emp1.department}")
print(emp1.give_raise(5000))
```

## Default Parameters in Constructors

Constructors can have default parameter values, making some arguments optional when creating objects. This provides flexibility and allows for simpler object creation when not all information is available.

```python
class BlogPost:
    """Represents a blog post"""

    def __init__(self, title, author, content, published=False, tags=None):
        """
        Initialize a blog post

        Args:
            title: Post title
            author: Post author
            content: Post content
            published: Publication status (default: False)
            tags: List of tags (default: None)
        """
        self.title = title
        self.author = author
        self.content = content
        self.published = published
        self.tags = tags if tags is not None else []
        self.views = 0
        self.likes = 0
        self.comments = []

    def publish(self):
        """Publish the blog post"""
        self.published = True
        return f"'{self.title}' has been published"

    def add_tag(self, tag):
        """Add a tag to the post"""
        if tag not in self.tags:
            self.tags.append(tag)

    def increment_views(self):
        """Increment view count"""
        self.views += 1

    def get_stats(self):
        """Get post statistics"""
        return {
            "title": self.title,
            "views": self.views,
            "likes": self.likes,
            "comments": len(self.comments),
            "published": self.published
        }

# Different ways to create blog posts
post1 = BlogPost("Python Tips", "Alice", "Here are some Python tips...")
post2 = BlogPost("OOP Guide", "Bob", "Learn OOP...", published=True, tags=["python", "oop"])

post1.publish()
post1.increment_views()
post2.add_tag("tutorial")

print(post1.get_stats())
print(post2.get_stats())
```

## Constructor Validation

It's important to validate input in constructors to ensure objects are created with valid data. This prevents errors later and makes your classes more robust and reliable.

| Validation Type | Purpose | Example |
|----------------|---------|---------|
| Type checking | Ensure correct data types | `if not isinstance(age, int)` |
| Range checking | Validate numeric ranges | `if salary < 0` |
| Required fields | Ensure critical data exists | `if not email` |
| Format validation | Check string formats | `if '@' not in email` |

```python
class CreditCard:
    """Represents a credit card with validation"""

    def __init__(self, card_number, holder_name, cvv, expiry_month, expiry_year, credit_limit):
        """
        Initialize credit card with validation

        Raises:
            ValueError: If any validation fails
        """
        # Validate card number
        if not isinstance(card_number, str) or len(card_number) != 16:
            raise ValueError("Card number must be 16 digits")
        if not card_number.isdigit():
            raise ValueError("Card number must contain only digits")

        # Validate holder name
        if not holder_name or len(holder_name.strip()) < 2:
            raise ValueError("Holder name is required")

        # Validate CVV
        if not isinstance(cvv, str) or len(cvv) not in [3, 4]:
            raise ValueError("CVV must be 3 or 4 digits")
        if not cvv.isdigit():
            raise ValueError("CVV must contain only digits")

        # Validate expiry
        if not (1 <= expiry_month <= 12):
            raise ValueError("Expiry month must be between 1 and 12")
        if expiry_year < 2024:
            raise ValueError("Card has expired")

        # Validate credit limit
        if credit_limit <= 0:
            raise ValueError("Credit limit must be positive")

        # Set attributes after validation
        self.card_number = card_number
        self.holder_name = holder_name.strip()
        self.cvv = cvv
        self.expiry_month = expiry_month
        self.expiry_year = expiry_year
        self.credit_limit = credit_limit
        self.current_balance = 0
        self.transactions = []

    def charge(self, amount, description):
        """Charge the card"""
        if amount <= 0:
            return "Invalid amount"

        if self.current_balance + amount > self.credit_limit:
            return "Transaction declined: Credit limit exceeded"

        self.current_balance += amount
        self.transactions.append({
            "type": "charge",
            "amount": amount,
            "description": description
        })
        return f"Charged ${amount}. Balance: ${self.current_balance}"

    def make_payment(self, amount):
        """Make a payment"""
        if amount <= 0:
            return "Invalid payment amount"

        if amount > self.current_balance:
            amount = self.current_balance

        self.current_balance -= amount
        self.transactions.append({
            "type": "payment",
            "amount": amount,
            "description": "Payment received"
        })
        return f"Payment of ${amount} received. Balance: ${self.current_balance}"

# Valid card creation
try:
    card = CreditCard("1234567890123456", "John Doe", "123", 12, 2025, 5000)
    print(card.charge(100, "Online purchase"))
    print(card.make_payment(50))
except ValueError as e:
    print(f"Error: {e}")

# Invalid card creation
try:
    invalid_card = CreditCard("123", "John", "12", 13, 2020, -100)
except ValueError as e:
    print(f"Validation error: {e}")
```

## Multiple Constructors Pattern

While Python doesn't support method overloading like some other languages, you can achieve similar functionality using class methods as alternative constructors. This pattern allows you to create objects in different ways.

```python
from datetime import datetime

class Event:
    """Represents an event with multiple creation methods"""

    def __init__(self, name, date, location, capacity):
        """Standard constructor"""
        self.name = name
        self.date = date
        self.location = location
        self.capacity = capacity
        self.attendees = []
        self.waitlist = []

    @classmethod
    def from_string(cls, event_string):
        """
        Alternative constructor: Create event from formatted string
        Format: "Name|YYYY-MM-DD|Location|Capacity"
        """
        parts = event_string.split('|')
        if len(parts) != 4:
            raise ValueError("Invalid event string format")

        name = parts[0].strip()
        date = datetime.strptime(parts[1].strip(), "%Y-%m-%d")
        location = parts[2].strip()
        capacity = int(parts[3].strip())

        return cls(name, date, location, capacity)

    @classmethod
    def from_dict(cls, event_dict):
        """Alternative constructor: Create event from dictionary"""
        return cls(
            event_dict['name'],
            datetime.strptime(event_dict['date'], "%Y-%m-%d"),
            event_dict['location'],
            event_dict['capacity']
        )

    @classmethod
    def create_webinar(cls, name, date, max_participants=100):
        """Alternative constructor: Create online webinar"""
        return cls(name, date, "Online", max_participants)

    def register_attendee(self, attendee_name):
        """Register an attendee"""
        if len(self.attendees) < self.capacity:
            self.attendees.append(attendee_name)
            return f"{attendee_name} registered for {self.name}"
        else:
            self.waitlist.append(attendee_name)
            return f"{attendee_name} added to waitlist"

    def get_info(self):
        """Get event information"""
        return {
            "name": self.name,
            "date": self.date.strftime("%Y-%m-%d"),
            "location": self.location,
            "capacity": self.capacity,
            "registered": len(self.attendees),
            "waitlist": len(self.waitlist)
        }

# Different ways to create events
event1 = Event("Tech Conference", datetime(2024, 6, 15), "New York", 500)
event2 = Event.from_string("Python Workshop|2024-07-20|San Francisco|50")
event3 = Event.from_dict({
    'name': 'AI Summit',
    'date': '2024-08-10',
    'location': 'Boston',
    'capacity': 200
})
event4 = Event.create_webinar("Cloud Computing 101", datetime(2024, 9, 5))

event1.register_attendee("Alice")
event4.register_attendee("Bob")

print(event1.get_info())
print(event4.get_info())
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Basic Constructor with Validation"
    difficulty: basic
    description: "Create a Person class with name and age. Validate that age is between 0 and 120 in the constructor."
    starter_code: |
      class Person:
          def __init__(self, name, age):
              # TODO: Validate name is not empty
              # TODO: Validate age is between 0 and 120
              # TODO: Set attributes
              pass

      # Test
      try:
          person1 = Person("Alice", 30)
          print(f"{person1.name} is {person1.age} years old")
          person2 = Person("", 150)
      except ValueError as e:
          print(f"Error: {e}")
    expected_output: |
      Alice is 30 years old
      Error: Age must be between 0 and 120
    hints:
      - "Check if name is empty using if not name.strip()"
      - "Use if not (0 <= age <= 120) to validate age"
      - "Raise ValueError with descriptive messages"
    solution: |
      class Person:
          def __init__(self, name, age):
              if not name or not name.strip():
                  raise ValueError("Name cannot be empty")
              if not (0 <= age <= 120):
                  raise ValueError("Age must be between 0 and 120")
              self.name = name.strip()
              self.age = age

      # Test
      try:
          person1 = Person("Alice", 30)
          print(f"{person1.name} is {person1.age} years old")
          person2 = Person("", 150)
      except ValueError as e:
          print(f"Error: {e}")

  - title: "Constructor with Default Values"
    difficulty: basic
    description: "Create a Book class with title, author, pages, and optional price (default 0). Add a method to get book info."
    starter_code: |
      class Book:
          def __init__(self, title, author, pages, price=0):
              # TODO: Initialize attributes
              pass

          def get_info(self):
              # TODO: Return formatted book information
              pass

      book1 = Book("1984", "George Orwell", 328, 15.99)
      book2 = Book("Free Book", "Unknown", 100)
      print(book1.get_info())
      print(book2.get_info())
    expected_output: |
      1984 by George Orwell - 328 pages - $15.99
      Free Book by Unknown - 100 pages - $0
    hints:
      - "Use default parameter syntax: parameter=default_value"
      - "Format the output string with all attributes"
      - "Use f-string for clean formatting"
    solution: |
      class Book:
          def __init__(self, title, author, pages, price=0):
              self.title = title
              self.author = author
              self.pages = pages
              self.price = price

          def get_info(self):
              return f"{self.title} by {self.author} - {self.pages} pages - ${self.price}"

      book1 = Book("1984", "George Orwell", 328, 15.99)
      book2 = Book("Free Book", "Unknown", 100)
      print(book1.get_info())
      print(book2.get_info())

  - title: "Email Validation in Constructor"
    difficulty: intermediate
    description: "Create an EmailAccount class that validates email format in constructor and provides methods to send and receive emails."
    starter_code: |
      class EmailAccount:
          def __init__(self, email, password):
              # TODO: Validate email contains @ and .
              # TODO: Validate password is at least 8 characters
              # TODO: Initialize inbox as empty list
              pass

          def send_email(self, to, subject, body):
              # TODO: Return confirmation message
              pass

          def receive_email(self, from_addr, subject):
              # TODO: Add to inbox
              pass

      try:
          account = EmailAccount("user@example.com", "password123")
          account.send_email("friend@test.com", "Hello", "How are you?")
          print(f"Inbox: {len(account.inbox)} messages")
      except ValueError as e:
          print(f"Error: {e}")
    expected_output: |
      Inbox: 0 messages
    hints:
      - "Check '@' in email and '.' in email"
      - "Use len(password) >= 8 for validation"
      - "Store received emails as dictionaries in inbox list"
    solution: |
      class EmailAccount:
          def __init__(self, email, password):
              if '@' not in email or '.' not in email:
                  raise ValueError("Invalid email format")
              if len(password) < 8:
                  raise ValueError("Password must be at least 8 characters")
              self.email = email
              self.password = password
              self.inbox = []

          def send_email(self, to, subject, body):
              return f"Email sent to {to}"

          def receive_email(self, from_addr, subject):
              self.inbox.append({"from": from_addr, "subject": subject})

      try:
          account = EmailAccount("user@example.com", "password123")
          account.send_email("friend@test.com", "Hello", "How are you?")
          print(f"Inbox: {len(account.inbox)} messages")
      except ValueError as e:
          print(f"Error: {e}")

  - title: "Alternative Constructor Pattern"
    difficulty: intermediate
    description: "Create a Date class with standard constructor and an alternative from_string classmethod that parses 'YYYY-MM-DD' format."
    starter_code: |
      class Date:
          def __init__(self, year, month, day):
              # TODO: Validate month (1-12) and day (1-31)
              # TODO: Set attributes
              pass

          @classmethod
          def from_string(cls, date_string):
              # TODO: Parse YYYY-MM-DD format
              # TODO: Return new Date instance
              pass

          def __str__(self):
              return f"{self.year}-{self.month:02d}-{self.day:02d}"

      date1 = Date(2024, 3, 15)
      date2 = Date.from_string("2024-12-25")
      print(date1)
      print(date2)
    expected_output: |
      2024-03-15
      2024-12-25
    hints:
      - "Use date_string.split('-') to parse the string"
      - "Convert string parts to integers"
      - "Validate ranges: 1 <= month <= 12, 1 <= day <= 31"
    solution: |
      class Date:
          def __init__(self, year, month, day):
              if not (1 <= month <= 12):
                  raise ValueError("Month must be between 1 and 12")
              if not (1 <= day <= 31):
                  raise ValueError("Day must be between 1 and 31")
              self.year = year
              self.month = month
              self.day = day

          @classmethod
          def from_string(cls, date_string):
              parts = date_string.split('-')
              year = int(parts[0])
              month = int(parts[1])
              day = int(parts[2])
              return cls(year, month, day)

          def __str__(self):
              return f"{self.year}-{self.month:02d}-{self.day:02d}"

      date1 = Date(2024, 3, 15)
      date2 = Date.from_string("2024-12-25")
      print(date1)
      print(date2)

  - title: "Complex Validation Constructor"
    difficulty: advanced
    description: "Create a BankAccount class with account number validation (must be 10 digits), initial deposit minimum ($100), and transaction tracking."
    starter_code: |
      class BankAccount:
          def __init__(self, account_number, holder_name, initial_deposit):
              # TODO: Validate account_number is 10 digits
              # TODO: Validate holder_name is not empty
              # TODO: Validate initial_deposit >= 100
              # TODO: Initialize balance and transaction list
              pass

          def deposit(self, amount):
              # TODO: Add to balance and track transaction
              pass

          def get_statement(self):
              # TODO: Return formatted statement
              pass

      try:
          account = BankAccount("1234567890", "Alice Smith", 500)
          account.deposit(100)
          print(account.get_statement())
      except ValueError as e:
          print(f"Error: {e}")
    expected_output: |
      Account: 1234567890
      Holder: Alice Smith
      Balance: $600
      Transactions: 2
    hints:
      - "Use len(account_number) == 10 and account_number.isdigit()"
      - "Track each transaction with type and amount"
      - "Include initial deposit as first transaction"
    solution: |
      class BankAccount:
          def __init__(self, account_number, holder_name, initial_deposit):
              if len(account_number) != 10 or not account_number.isdigit():
                  raise ValueError("Account number must be 10 digits")
              if not holder_name or not holder_name.strip():
                  raise ValueError("Holder name is required")
              if initial_deposit < 100:
                  raise ValueError("Initial deposit must be at least $100")

              self.account_number = account_number
              self.holder_name = holder_name.strip()
              self.balance = initial_deposit
              self.transactions = [{"type": "initial", "amount": initial_deposit}]

          def deposit(self, amount):
              if amount > 0:
                  self.balance += amount
                  self.transactions.append({"type": "deposit", "amount": amount})

          def get_statement(self):
              return f"Account: {self.account_number}\nHolder: {self.holder_name}\nBalance: ${self.balance}\nTransactions: {len(self.transactions)}"

      try:
          account = BankAccount("1234567890", "Alice Smith", 500)
          account.deposit(100)
          print(account.get_statement())
      except ValueError as e:
          print(f"Error: {e}")

  - title: "Multiple Constructor Methods"
    difficulty: advanced
    description: "Create a Product class with standard constructor, from_dict, and from_csv alternative constructors. Include inventory tracking."
    starter_code: |
      class Product:
          def __init__(self, name, sku, price, quantity):
              # TODO: Initialize attributes
              # TODO: Initialize sales_history list
              pass

          @classmethod
          def from_dict(cls, data):
              # TODO: Create from dictionary
              pass

          @classmethod
          def from_csv(cls, csv_line):
              # TODO: Parse CSV line (name,sku,price,quantity)
              pass

          def sell(self, quantity):
              # TODO: Update quantity and track sale
              pass

          def get_value(self):
              return self.price * self.quantity

      p1 = Product("Laptop", "SKU001", 999.99, 10)
      p2 = Product.from_dict({"name": "Mouse", "sku": "SKU002", "price": 29.99, "quantity": 50})
      p3 = Product.from_csv("Keyboard,SKU003,79.99,20")
      print(f"Total inventory value: ${p1.get_value() + p2.get_value() + p3.get_value()}")
    expected_output: |
      Total inventory value: $13098.9
    hints:
      - "For CSV, use csv_line.split(',')"
      - "Convert price to float and quantity to int"
      - "from_dict and from_csv should return cls(...)"
    solution: |
      class Product:
          def __init__(self, name, sku, price, quantity):
              self.name = name
              self.sku = sku
              self.price = float(price)
              self.quantity = int(quantity)
              self.sales_history = []

          @classmethod
          def from_dict(cls, data):
              return cls(data["name"], data["sku"], data["price"], data["quantity"])

          @classmethod
          def from_csv(cls, csv_line):
              parts = csv_line.split(',')
              return cls(parts[0], parts[1], float(parts[2]), int(parts[3]))

          def sell(self, quantity):
              if quantity <= self.quantity:
                  self.quantity -= quantity
                  self.sales_history.append(quantity)
                  return f"Sold {quantity} units"
              return "Insufficient stock"

          def get_value(self):
              return self.price * self.quantity

      p1 = Product("Laptop", "SKU001", 999.99, 10)
      p2 = Product.from_dict({"name": "Mouse", "sku": "SKU002", "price": 29.99, "quantity": 50})
      p3 = Product.from_csv("Keyboard,SKU003,79.99,20")
      print(f"Total inventory value: ${p1.get_value() + p2.get_value() + p3.get_value()}")
```
<!-- EXERCISE_END -->
