# Method Overriding

Method overriding is a feature of inheritance that allows a subclass to provide a specific implementation of a method that is already defined in its parent class. When a method in a child class has the same name and signature as a method in the parent class, the child class method overrides the parent method, enabling polymorphic behavior and specialization.

## Understanding Method Overriding

Method overriding enables subclasses to modify or completely replace the behavior inherited from a parent class. When you call an overridden method on a child class instance, Python executes the child's version, not the parent's version. This is fundamental to polymorphism and allows objects of different types to respond differently to the same method call.

```python
class Payment:
    """Base payment class"""

    def __init__(self, amount, description):
        """Initialize payment"""
        self.amount = amount
        self.description = description
        self.status = "pending"

    def process(self):
        """Process payment - to be overridden"""
        return f"Processing ${self.amount} payment"

    def get_receipt(self):
        """Generate receipt"""
        return f"Receipt: {self.description} - ${self.amount}"

class CreditCardPayment(Payment):
    """Credit card payment"""

    def __init__(self, amount, description, card_number, cvv):
        """Initialize credit card payment"""
        super().__init__(amount, description)
        self.card_number = card_number[-4:]  # Store only last 4 digits
        self.cvv = cvv

    def process(self):
        """Override: Process credit card payment"""
        # Simulate card validation
        if len(self.cvv) == 3:
            self.status = "completed"
            return f"Credit card payment of ${self.amount} processed successfully (Card ending in {self.card_number})"
        self.status = "failed"
        return "Credit card payment failed: Invalid CVV"

class PayPalPayment(Payment):
    """PayPal payment"""

    def __init__(self, amount, description, email):
        """Initialize PayPal payment"""
        super().__init__(amount, description)
        self.email = email

    def process(self):
        """Override: Process PayPal payment"""
        # Simulate PayPal processing
        if "@" in self.email:
            self.status = "completed"
            return f"PayPal payment of ${self.amount} sent to {self.email}"
        self.status = "failed"
        return "PayPal payment failed: Invalid email"

class CryptoPayment(Payment):
    """Cryptocurrency payment"""

    def __init__(self, amount, description, wallet_address, crypto_type):
        """Initialize crypto payment"""
        super().__init__(amount, description)
        self.wallet_address = wallet_address
        self.crypto_type = crypto_type

    def process(self):
        """Override: Process crypto payment"""
        # Simulate blockchain transaction
        if len(self.wallet_address) >= 26:
            self.status = "completed"
            return f"{self.crypto_type} payment of ${self.amount} sent to wallet {self.wallet_address[:10]}..."
        self.status = "failed"
        return "Crypto payment failed: Invalid wallet address"

# Using polymorphism with overridden methods
payments = [
    CreditCardPayment(100.00, "Monthly subscription", "1234567890123456", "123"),
    PayPalPayment(50.00, "Online purchase", "user@example.com"),
    CryptoPayment(200.00, "Investment", "1A2B3C4D5E6F7G8H9I0J1K2L3M", "Bitcoin")
]

for payment in payments:
    print(payment.process())  # Each calls its own version
    print(payment.get_receipt())  # All use inherited version
    print()
```

## Overriding vs Extending Methods

Sometimes you want to completely replace a parent method (override), and other times you want to add to it (extend). Using `super()` allows you to extend parent functionality while adding new behavior.

| Approach | When to Use | Example |
|----------|-------------|---------|
| Complete Override | Replace parent behavior entirely | Different validation logic |
| Extend with super() | Add to parent behavior | Log before calling parent |
| Call super() first | Execute parent then add more | Initialize parent, add child attributes |
| Call super() last | Add behavior before parent | Validate before parent processes |

```python
class Logger:
    """Base logger class"""

    def __init__(self, name):
        """Initialize logger"""
        self.name = name
        self.logs = []

    def log(self, message):
        """Log a message"""
        entry = f"[{self.name}] {message}"
        self.logs.append(entry)
        return entry

    def get_logs(self):
        """Get all logs"""
        return self.logs

class TimestampLogger(Logger):
    """Logger with timestamps - extends parent"""

    def __init__(self, name):
        """Initialize with timestamp support"""
        super().__init__(name)
        from datetime import datetime
        self.created_at = datetime.now()

    def log(self, message):
        """Override: Add timestamp before calling parent"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamped_message = f"[{timestamp}] {message}"
        # Call parent with modified message
        return super().log(timestamped_message)

class FilteredLogger(Logger):
    """Logger with filtering - extends parent"""

    def __init__(self, name, min_level="INFO"):
        """Initialize with filtering"""
        super().__init__(name)
        self.min_level = min_level
        self.levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}

    def log(self, message, level="INFO"):
        """Override: Filter messages by level"""
        if self.levels.get(level, 0) >= self.levels.get(self.min_level, 0):
            # Call parent only if level is sufficient
            formatted = f"[{level}] {message}"
            return super().log(formatted)
        return f"Message filtered (level too low): {message}"

class FileLogger(Logger):
    """Logger that writes to file - extends parent"""

    def __init__(self, name, filename):
        """Initialize file logger"""
        super().__init__(name)
        self.filename = filename

    def log(self, message):
        """Override: Log to memory AND file"""
        # Call parent first to log to memory
        entry = super().log(message)
        # Then add file writing behavior
        try:
            with open(self.filename, 'a') as f:
                f.write(entry + '\n')
            return f"{entry} (saved to {self.filename})"
        except Exception as e:
            return f"{entry} (file save failed: {e})"

# Using different override strategies
basic_logger = Logger("Basic")
ts_logger = TimestampLogger("Timestamp")
filtered_logger = FilteredLogger("Filtered", "WARNING")
file_logger = FileLogger("File", "app.log")

print(basic_logger.log("Simple message"))
print(ts_logger.log("Message with timestamp"))
print(filtered_logger.log("This is info", "INFO"))
print(filtered_logger.log("This is a warning", "WARNING"))
# print(file_logger.log("Saved to file"))
```

## Overriding Special Methods

Python's special methods (also called magic methods or dunder methods) can be overridden to customize object behavior. These methods control how objects are represented, compared, and used in operations.

```python
class Product:
    """Product class with overridden special methods"""

    def __init__(self, name, price, quantity):
        """Initialize product"""
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        """Override: String representation for users"""
        return f"{self.name} - ${self.price} ({self.quantity} in stock)"

    def __repr__(self):
        """Override: String representation for developers"""
        return f"Product('{self.name}', {self.price}, {self.quantity})"

    def __eq__(self, other):
        """Override: Equality comparison"""
        if not isinstance(other, Product):
            return False
        return self.name == other.name and self.price == other.price

    def __lt__(self, other):
        """Override: Less than comparison (for sorting)"""
        return self.price < other.price

    def __add__(self, other):
        """Override: Addition operator"""
        if isinstance(other, Product) and self.name == other.name:
            # Combine quantities
            return Product(self.name, self.price, self.quantity + other.quantity)
        return NotImplemented

    def __len__(self):
        """Override: Length returns quantity"""
        return self.quantity

    def __bool__(self):
        """Override: Boolean is True if in stock"""
        return self.quantity > 0

class DiscountProduct(Product):
    """Product with discount, overriding more methods"""

    def __init__(self, name, price, quantity, discount_percent):
        """Initialize discounted product"""
        super().__init__(name, price, quantity)
        self.discount_percent = discount_percent
        self.final_price = price * (1 - discount_percent / 100)

    def __str__(self):
        """Override: Include discount in string"""
        original = super().__str__()
        return f"{original} | {self.discount_percent}% OFF - Final: ${self.final_price:.2f}"

    def __lt__(self, other):
        """Override: Compare by final price instead of base price"""
        if isinstance(other, DiscountProduct):
            return self.final_price < other.final_price
        return self.final_price < other.price

    def get_savings(self):
        """Calculate savings"""
        return self.price - self.final_price

# Using overridden special methods
p1 = Product("Laptop", 1000, 5)
p2 = Product("Mouse", 25, 100)
p3 = DiscountProduct("Keyboard", 80, 50, 20)

print(p1)  # Uses __str__
print(repr(p1))  # Uses __repr__
print(f"In stock: {bool(p1)}")  # Uses __bool__
print(f"Quantity: {len(p1)}")  # Uses __len__

# Comparison
print(f"p1 < p2: {p1 < p2}")  # Uses __lt__
print(f"p2 < p3: {p2 < p3}")  # Uses overridden __lt__

# Sorting
products = [p1, p2, p3]
products.sort()
print("Sorted by price:", [p.name for p in products])
```

## Method Resolution Order (MRO)

When using inheritance, especially multiple inheritance, Python follows a specific order to resolve which method to call. Understanding MRO is crucial for correctly overriding methods in complex hierarchies.

```python
class A:
    """Base class A"""
    def process(self):
        return "A.process()"

    def display(self):
        return "A.display()"

class B(A):
    """B inherits from A"""
    def process(self):
        return "B.process()"

class C(A):
    """C inherits from A"""
    def process(self):
        return "C.process()"

    def display(self):
        return "C.display()"

class D(B, C):
    """D inherits from both B and C"""
    def show(self):
        """D's own method"""
        return "D.show()"

# Method Resolution Order
print("MRO for D:", [cls.__name__ for cls in D.__mro__])
# Output: ['D', 'B', 'C', 'A', 'object']

d = D()
print(d.process())  # Calls B.process() (B comes before C in MRO)
print(d.display())  # Calls C.display() (B doesn't have it, C does)
print(d.show())     # Calls D.show() (D's own method)

class E(B, C):
    """E overrides process and calls super()"""
    def process(self):
        # super() follows MRO
        parent_result = super().process()
        return f"E.process() -> {parent_result}"

e = E()
print(e.process())  # E calls B.process() via super()

class SmartDevice:
    """Base smart device"""
    def __init__(self, name):
        self.name = name
        self.is_on = False

    def turn_on(self):
        self.is_on = True
        return f"{self.name} is ON"

    def status(self):
        return f"{self.name}: {'ON' if self.is_on else 'OFF'}"

class NetworkEnabled:
    """Mixin for network functionality"""
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.connected = False

    def connect(self):
        self.connected = True
        return f"Connected to {self.ip_address}"

    def status(self):
        return f"Network: {'Connected' if self.connected else 'Disconnected'}"

class SmartLight(SmartDevice, NetworkEnabled):
    """Smart light with device and network features"""

    def __init__(self, name, ip_address, brightness=100):
        SmartDevice.__init__(self, name)
        NetworkEnabled.__init__(self, ip_address)
        self.brightness = brightness

    def status(self):
        """Override to combine both status methods"""
        device_status = SmartDevice.status(self)
        network_status = NetworkEnabled.status(self)
        return f"{device_status} | {network_status} | Brightness: {self.brightness}%"

    def dim(self, level):
        """Smart light specific method"""
        if 0 <= level <= 100:
            self.brightness = level
            return f"Brightness set to {level}%"
        return "Invalid brightness level"

# Using smart light
light = SmartLight("Living Room Light", "192.168.1.100")
print(light.turn_on())
print(light.connect())
print(light.dim(50))
print(light.status())  # Uses overridden method that combines both parents
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Override String Representation"
    difficulty: basic
    description: "Create a Book class that overrides __str__ to return a formatted string with title and author."
    starter_code: |
      class Book:
          def __init__(self, title, author, pages):
              self.title = title
              self.author = author
              self.pages = pages

          # TODO: Override __str__ method
          pass

      book = Book("1984", "George Orwell", 328)
      print(book)
    expected_output: |
      1984 by George Orwell (328 pages)
    hints:
      - "Define __str__(self) method"
      - "Return a formatted string using f-string"
      - "Include title, author, and pages"
    solution: |
      class Book:
          def __init__(self, title, author, pages):
              self.title = title
              self.author = author
              self.pages = pages

          def __str__(self):
              return f"{self.title} by {self.author} ({self.pages} pages)"

      book = Book("1984", "George Orwell", 328)
      print(book)

  - title: "Override Comparison Method"
    difficulty: basic
    description: "Create a Student class that overrides __eq__ to compare students by student_id."
    starter_code: |
      class Student:
          def __init__(self, name, student_id):
              self.name = name
              self.student_id = student_id

          # TODO: Override __eq__ method
          pass

      s1 = Student("Alice", "S001")
      s2 = Student("Alice", "S001")
      s3 = Student("Bob", "S002")
      print(f"s1 == s2: {s1 == s2}")
      print(f"s1 == s3: {s1 == s3}")
    expected_output: |
      s1 == s2: True
      s1 == s3: False
    hints:
      - "Define __eq__(self, other) method"
      - "Check if other is a Student instance first"
      - "Compare student_id attributes"
    solution: |
      class Student:
          def __init__(self, name, student_id):
              self.name = name
              self.student_id = student_id

          def __eq__(self, other):
              if not isinstance(other, Student):
                  return False
              return self.student_id == other.student_id

      s1 = Student("Alice", "S001")
      s2 = Student("Alice", "S001")
      s3 = Student("Bob", "S002")
      print(f"s1 == s2: {s1 == s2}")
      print(f"s1 == s3: {s1 == s3}")

  - title: "Override with Super Extension"
    difficulty: intermediate
    description: "Create a BankAccount and SavingsAccount where SavingsAccount overrides deposit to add interest after calling parent method."
    starter_code: |
      class BankAccount:
          def __init__(self, owner, balance):
              self.owner = owner
              self.balance = balance

          def deposit(self, amount):
              self.balance += amount
              return f"Deposited ${amount}"

      class SavingsAccount(BankAccount):
          def __init__(self, owner, balance, interest_rate):
              super().__init__(owner, balance)
              self.interest_rate = interest_rate

          # TODO: Override deposit to add interest after parent deposit
          # Interest = deposited amount * interest_rate
          pass

      savings = SavingsAccount("Alice", 1000, 0.05)
      print(savings.deposit(100))
      print(f"Balance: ${savings.balance}")
    expected_output: |
      Deposited $100
      Balance: $1105.0
    hints:
      - "Call super().deposit(amount) first"
      - "Calculate interest = amount * interest_rate"
      - "Add interest to balance"
    solution: |
      class BankAccount:
          def __init__(self, owner, balance):
              self.owner = owner
              self.balance = balance

          def deposit(self, amount):
              self.balance += amount
              return f"Deposited ${amount}"

      class SavingsAccount(BankAccount):
          def __init__(self, owner, balance, interest_rate):
              super().__init__(owner, balance)
              self.interest_rate = interest_rate

          def deposit(self, amount):
              result = super().deposit(amount)
              interest = amount * self.interest_rate
              self.balance += interest
              return result

      savings = SavingsAccount("Alice", 1000, 0.05)
      print(savings.deposit(100))
      print(f"Balance: ${savings.balance}")

  - title: "Override Multiple Special Methods"
    difficulty: intermediate
    description: "Create a Rectangle class that overrides __str__, __eq__, and __lt__ for complete comparison support."
    starter_code: |
      class Rectangle:
          def __init__(self, width, height):
              self.width = width
              self.height = height

          def area(self):
              return self.width * self.height

          # TODO: Override __str__ to show dimensions
          # TODO: Override __eq__ to compare areas
          # TODO: Override __lt__ to compare areas (for sorting)
          pass

      r1 = Rectangle(5, 4)
      r2 = Rectangle(10, 2)
      r3 = Rectangle(3, 6)
      print(r1)
      print(f"r1 == r2: {r1 == r2}")
      print(f"r1 < r3: {r1 < r3}")
    expected_output: |
      Rectangle(5x4)
      r1 == r2: True
      r1 < r3: False
    hints:
      - "__str__ returns string like 'Rectangle(5x4)'"
      - "__eq__ compares self.area() == other.area()"
      - "__lt__ compares self.area() < other.area()"
    solution: |
      class Rectangle:
          def __init__(self, width, height):
              self.width = width
              self.height = height

          def area(self):
              return self.width * self.height

          def __str__(self):
              return f"Rectangle({self.width}x{self.height})"

          def __eq__(self, other):
              if not isinstance(other, Rectangle):
                  return False
              return self.area() == other.area()

          def __lt__(self, other):
              return self.area() < other.area()

      r1 = Rectangle(5, 4)
      r2 = Rectangle(10, 2)
      r3 = Rectangle(3, 6)
      print(r1)
      print(f"r1 == r2: {r1 == r2}")
      print(f"r1 < r3: {r1 < r3}")

  - title: "Complete vs Partial Override"
    difficulty: advanced
    description: "Create a Notification system where EmailNotification completely overrides send, and SMSNotification extends it using super()."
    starter_code: |
      class Notification:
          def __init__(self, message):
              self.message = message
              self.sent = False

          def send(self):
              self.sent = True
              return f"Notification sent: {self.message}"

      class EmailNotification(Notification):
          def __init__(self, message, email):
              super().__init__(message)
              self.email = email

          # TODO: Completely override send (don't call super)
          # Include email validation
          pass

      class SMSNotification(Notification):
          def __init__(self, message, phone):
              super().__init__(message)
              self.phone = phone

          # TODO: Override send but call super() first
          # Add phone number to output
          pass

      email = EmailNotification("Meeting at 3pm", "user@example.com")
      sms = SMSNotification("Meeting at 3pm", "555-1234")
      print(email.send())
      print(sms.send())
    expected_output: |
      Email sent to user@example.com: Meeting at 3pm
      Notification sent: Meeting at 3pm | SMS to 555-1234
    hints:
      - "EmailNotification: don't use super(), create custom message"
      - "SMSNotification: call super().send() then add SMS info"
      - "Both should set self.sent = True"
    solution: |
      class Notification:
          def __init__(self, message):
              self.message = message
              self.sent = False

          def send(self):
              self.sent = True
              return f"Notification sent: {self.message}"

      class EmailNotification(Notification):
          def __init__(self, message, email):
              super().__init__(message)
              self.email = email

          def send(self):
              self.sent = True
              return f"Email sent to {self.email}: {self.message}"

      class SMSNotification(Notification):
          def __init__(self, message, phone):
              super().__init__(message)
              self.phone = phone

          def send(self):
              result = super().send()
              return f"{result} | SMS to {self.phone}"

      email = EmailNotification("Meeting at 3pm", "user@example.com")
      sms = SMSNotification("Meeting at 3pm", "555-1234")
      print(email.send())
      print(sms.send())

  - title: "Complex Method Override Chain"
    difficulty: advanced
    description: "Create a Vehicle -> Car -> ElectricCar hierarchy where each level overrides get_info to add more details using super()."
    starter_code: |
      class Vehicle:
          def __init__(self, make, model):
              self.make = make
              self.model = model

          def get_info(self):
              return f"{self.make} {self.model}"

      class Car(Vehicle):
          def __init__(self, make, model, doors):
              super().__init__(make, model)
              self.doors = doors

          # TODO: Override get_info, call super() and add doors
          pass

      class ElectricCar(Car):
          def __init__(self, make, model, doors, battery_size):
              super().__init__(make, model, doors)
              self.battery_size = battery_size

          # TODO: Override get_info, call super() and add battery
          pass

      tesla = ElectricCar("Tesla", "Model 3", 4, 75)
      print(tesla.get_info())
    expected_output: |
      Tesla Model 3 | 4 doors | 75kWh battery
    hints:
      - "Each level calls super().get_info() first"
      - "Then add their own information with |"
      - "Build the string progressively through the chain"
    solution: |
      class Vehicle:
          def __init__(self, make, model):
              self.make = make
              self.model = model

          def get_info(self):
              return f"{self.make} {self.model}"

      class Car(Vehicle):
          def __init__(self, make, model, doors):
              super().__init__(make, model)
              self.doors = doors

          def get_info(self):
              return f"{super().get_info()} | {self.doors} doors"

      class ElectricCar(Car):
          def __init__(self, make, model, doors, battery_size):
              super().__init__(make, model, doors)
              self.battery_size = battery_size

          def get_info(self):
              return f"{super().get_info()} | {self.battery_size}kWh battery"

      tesla = ElectricCar("Tesla", "Model 3", 4, 75)
      print(tesla.get_info())
```
<!-- EXERCISE_END -->
