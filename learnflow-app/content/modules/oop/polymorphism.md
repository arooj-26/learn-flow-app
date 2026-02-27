# Polymorphism

Polymorphism is the ability of different objects to respond to the same method call in their own way. It's one of the core principles of object-oriented programming that allows you to write flexible, extensible code. In Python, polymorphism enables you to use objects of different classes interchangeably as long as they share a common interface, making your code more generic and reusable.

## Understanding Polymorphism

Polymorphism literally means "many forms." In programming, it allows objects of different types to be treated uniformly through a common interface. When you call a method on an object, the actual implementation that runs depends on the object's type, enabling different behaviors from the same method call.

```python
class Shape:
    """Base class defining the interface"""

    def __init__(self, name):
        self.name = name

    def area(self):
        """Calculate area - to be implemented by subclasses"""
        raise NotImplementedError("Subclass must implement area()")

    def perimeter(self):
        """Calculate perimeter - to be implemented by subclasses"""
        raise NotImplementedError("Subclass must implement perimeter()")

    def describe(self):
        """Common method for all shapes"""
        return f"This is a {self.name}"

class Rectangle(Shape):
    """Rectangle implementation"""

    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    """Circle implementation"""

    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius

class Triangle(Shape):
    """Triangle implementation"""

    def __init__(self, side_a, side_b, side_c):
        super().__init__("Triangle")
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    def area(self):
        # Using Heron's formula
        s = self.perimeter() / 2
        return (s * (s - self.side_a) * (s - self.side_b) * (s - self.side_c)) ** 0.5

    def perimeter(self):
        return self.side_a + self.side_b + self.side_c

# Polymorphism in action
shapes = [
    Rectangle(5, 4),
    Circle(3),
    Triangle(3, 4, 5)
]

# Same method calls, different behaviors
for shape in shapes:
    print(f"{shape.describe()}")
    print(f"  Area: {shape.area():.2f}")
    print(f"  Perimeter: {shape.perimeter():.2f}")
    print()
```

## Duck Typing

Python uses "duck typing" - if an object walks like a duck and quacks like a duck, it's treated as a duck. This means you don't need explicit inheritance to achieve polymorphism; objects just need to implement the expected methods.

| Concept | Description | Example |
|---------|-------------|---------|
| Duck Typing | Type determined by methods, not inheritance | Any object with `.read()` can be a file |
| Interface | Set of methods an object must implement | `.draw()`, `.move()` for game objects |
| Protocol | Informal interface in Python | Iterator protocol: `__iter__` and `__next__` |

```python
class FileReader:
    """Reads from actual files"""

    def __init__(self, filename):
        self.filename = filename

    def read(self):
        try:
            with open(self.filename, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return f"File {self.filename} not found"

class StringReader:
    """Reads from strings"""

    def __init__(self, content):
        self.content = content

    def read(self):
        return self.content

class URLReader:
    """Simulates reading from URLs"""

    def __init__(self, url):
        self.url = url

    def read(self):
        # Simulated response
        return f"Content from {self.url}"

class DataProcessor:
    """Processes data from any reader"""

    def __init__(self, reader):
        """Accepts any object with a read() method"""
        self.reader = reader

    def process(self):
        """Process data from reader"""
        data = self.reader.read()
        word_count = len(data.split())
        char_count = len(data)
        return {
            "word_count": word_count,
            "char_count": char_count,
            "preview": data[:50] + "..." if len(data) > 50 else data
        }

# Duck typing - different readers, same interface
readers = [
    StringReader("Hello world from a string reader"),
    URLReader("https://api.example.com/data"),
    # FileReader("data.txt")  # Would work if file exists
]

for reader in readers:
    processor = DataProcessor(reader)
    stats = processor.process()
    print(f"Processed: {stats}")
```

## Operator Overloading

Polymorphism extends to operators through special methods. By overriding methods like `__add__`, `__sub__`, etc., you can define how operators work with your objects.

```python
class Vector:
    """2D vector with operator overloading"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """String representation"""
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        """Add two vectors: v1 + v2"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        """Subtract vectors: v1 - v2"""
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, scalar):
        """Multiply vector by scalar: v * 3"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented

    def __eq__(self, other):
        """Check equality: v1 == v2"""
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False

    def __abs__(self):
        """Magnitude: abs(v)"""
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def dot(self, other):
        """Dot product"""
        return self.x * other.x + self.y * other.y

class Money:
    """Money class with operator overloading"""

    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency

    def __str__(self):
        return f"{self.currency} {self.amount:.2f}"

    def __add__(self, other):
        """Add money"""
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError("Cannot add different currencies")
            return Money(self.amount + other.amount, self.currency)
        return NotImplemented

    def __sub__(self, other):
        """Subtract money"""
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError("Cannot subtract different currencies")
            return Money(self.amount - other.amount, self.currency)
        return NotImplemented

    def __mul__(self, multiplier):
        """Multiply money by scalar"""
        if isinstance(multiplier, (int, float)):
            return Money(self.amount * multiplier, self.currency)
        return NotImplemented

    def __lt__(self, other):
        """Less than comparison"""
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError("Cannot compare different currencies")
            return self.amount < other.amount
        return NotImplemented

    def __le__(self, other):
        """Less than or equal"""
        return self < other or self == other

    def __eq__(self, other):
        """Equality"""
        if isinstance(other, Money):
            return self.amount == other.amount and self.currency == other.currency
        return False

# Using polymorphic operators
v1 = Vector(3, 4)
v2 = Vector(1, 2)
print(f"v1: {v1}")
print(f"v2: {v2}")
print(f"v1 + v2: {v1 + v2}")
print(f"v1 - v2: {v1 - v2}")
print(f"v1 * 2: {v1 * 2}")
print(f"|v1|: {abs(v1):.2f}")
print(f"v1 · v2: {v1.dot(v2)}")

print()

m1 = Money(100.50, "USD")
m2 = Money(50.25, "USD")
print(f"m1: {m1}")
print(f"m2: {m2}")
print(f"m1 + m2: {m1 + m2}")
print(f"m1 - m2: {m1 - m2}")
print(f"m1 * 2: {m1 * 2}")
print(f"m1 > m2: {m1 > m2}")
```

## Polymorphism with Abstract Base Classes

Abstract base classes (ABCs) provide a formal way to define interfaces in Python. They ensure that derived classes implement specific methods, making polymorphism more explicit and safer.

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    """Abstract base class for payment processors"""

    def __init__(self, transaction_id):
        self.transaction_id = transaction_id
        self.status = "pending"

    @abstractmethod
    def validate(self):
        """Validate payment details - must be implemented"""
        pass

    @abstractmethod
    def process_payment(self, amount):
        """Process the payment - must be implemented"""
        pass

    @abstractmethod
    def refund(self, amount):
        """Refund payment - must be implemented"""
        pass

    def get_status(self):
        """Common method for all processors"""
        return f"Transaction {self.transaction_id}: {self.status}"

class CreditCardProcessor(PaymentProcessor):
    """Credit card payment processor"""

    def __init__(self, transaction_id, card_number, cvv):
        super().__init__(transaction_id)
        self.card_number = card_number
        self.cvv = cvv

    def validate(self):
        """Validate credit card"""
        if len(self.card_number) == 16 and len(self.cvv) == 3:
            return True
        return False

    def process_payment(self, amount):
        """Process credit card payment"""
        if self.validate():
            self.status = "completed"
            return f"Processed ${amount} via credit card ending in {self.card_number[-4:]}"
        self.status = "failed"
        return "Invalid credit card details"

    def refund(self, amount):
        """Refund to credit card"""
        if self.status == "completed":
            return f"Refunded ${amount} to credit card ending in {self.card_number[-4:]}"
        return "Cannot refund: payment not completed"

class BitcoinProcessor(PaymentProcessor):
    """Bitcoin payment processor"""

    def __init__(self, transaction_id, wallet_address):
        super().__init__(transaction_id)
        self.wallet_address = wallet_address

    def validate(self):
        """Validate wallet address"""
        return len(self.wallet_address) >= 26

    def process_payment(self, amount):
        """Process bitcoin payment"""
        if self.validate():
            self.status = "completed"
            return f"Sent {amount} BTC to {self.wallet_address[:10]}..."
        self.status = "failed"
        return "Invalid wallet address"

    def refund(self, amount):
        """Refund bitcoin"""
        if self.status == "completed":
            return f"Refunded {amount} BTC to {self.wallet_address[:10]}..."
        return "Cannot refund: payment not completed"

class PayPalProcessor(PaymentProcessor):
    """PayPal payment processor"""

    def __init__(self, transaction_id, email):
        super().__init__(transaction_id)
        self.email = email

    def validate(self):
        """Validate PayPal email"""
        return "@" in self.email and "." in self.email

    def process_payment(self, amount):
        """Process PayPal payment"""
        if self.validate():
            self.status = "completed"
            return f"Sent ${amount} to PayPal account {self.email}"
        self.status = "failed"
        return "Invalid PayPal email"

    def refund(self, amount):
        """Refund via PayPal"""
        if self.status == "completed":
            return f"Refunded ${amount} to {self.email}"
        return "Cannot refund: payment not completed"

# Polymorphic payment processing
def process_transaction(processor, amount):
    """Process any payment type polymorphically"""
    print(f"Processing transaction...")
    print(processor.process_payment(amount))
    print(processor.get_status())
    print()

processors = [
    CreditCardProcessor("TXN001", "1234567890123456", "123"),
    BitcoinProcessor("TXN002", "1A2B3C4D5E6F7G8H9I0J1K2L3M"),
    PayPalProcessor("TXN003", "user@example.com")
]

for processor in processors:
    process_transaction(processor, 100)
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Basic Polymorphic Animals"
    difficulty: basic
    description: "Create an Animal base class and Dog/Cat subclasses. Each should implement make_sound() differently."
    starter_code: |
      class Animal:
          def __init__(self, name):
              self.name = name

          def make_sound(self):
              pass

      class Dog(Animal):
          # TODO: Implement make_sound to return bark
          pass

      class Cat(Animal):
          # TODO: Implement make_sound to return meow
          pass

      animals = [Dog("Buddy"), Cat("Whiskers")]
      for animal in animals:
          print(f"{animal.name}: {animal.make_sound()}")
    expected_output: |
      Buddy: Woof!
      Whiskers: Meow!
    hints:
      - "Override make_sound() in each subclass"
      - "Return the appropriate sound as a string"
      - "Use self.name to include the animal's name"
    solution: |
      class Animal:
          def __init__(self, name):
              self.name = name

          def make_sound(self):
              pass

      class Dog(Animal):
          def make_sound(self):
              return "Woof!"

      class Cat(Animal):
          def make_sound(self):
              return "Meow!"

      animals = [Dog("Buddy"), Cat("Whiskers")]
      for animal in animals:
          print(f"{animal.name}: {animal.make_sound()}")

  - title: "Duck Typing with Readers"
    difficulty: basic
    description: "Create different reader classes that all implement a read() method, demonstrating duck typing."
    starter_code: |
      class TextReader:
          def __init__(self, text):
              self.text = text

          def read(self):
              return self.text

      class NumberReader:
          # TODO: Implement read() to return numbers as string
          def __init__(self, numbers):
              self.numbers = numbers
          pass

      def process_data(reader):
          # TODO: Call read() and return length
          pass

      t = TextReader("Hello World")
      n = NumberReader([1, 2, 3, 4, 5])
      print(f"Text length: {process_data(t)}")
      print(f"Number length: {process_data(n)}")
    expected_output: |
      Text length: 11
      Number length: 9
    hints:
      - "NumberReader.read() should convert numbers to string"
      - "Use str(self.numbers) for conversion"
      - "process_data should work with any object that has read()"
    solution: |
      class TextReader:
          def __init__(self, text):
              self.text = text

          def read(self):
              return self.text

      class NumberReader:
          def __init__(self, numbers):
              self.numbers = numbers

          def read(self):
              return str(self.numbers)

      def process_data(reader):
          return len(reader.read())

      t = TextReader("Hello World")
      n = NumberReader([1, 2, 3, 4, 5])
      print(f"Text length: {process_data(t)}")
      print(f"Number length: {process_data(n)}")

  - title: "Operator Overloading for Point"
    difficulty: intermediate
    description: "Create a Point class that overloads +, -, and == operators for 2D points."
    starter_code: |
      class Point:
          def __init__(self, x, y):
              self.x = x
              self.y = y

          # TODO: Override __add__ for point addition
          # TODO: Override __sub__ for point subtraction
          # TODO: Override __eq__ for equality
          # TODO: Override __str__ for printing
          pass

      p1 = Point(3, 4)
      p2 = Point(1, 2)
      p3 = p1 + p2
      p4 = p1 - p2
      print(f"p1 + p2 = {p3}")
      print(f"p1 - p2 = {p4}")
      print(f"p1 == p2: {p1 == p2}")
    expected_output: |
      p1 + p2 = Point(4, 6)
      p1 - p2 = Point(2, 2)
      p1 == p2: False
    hints:
      - "__add__ returns new Point with added coordinates"
      - "__sub__ returns new Point with subtracted coordinates"
      - "__eq__ compares both x and y"
      - "__str__ returns formatted string"
    solution: |
      class Point:
          def __init__(self, x, y):
              self.x = x
              self.y = y

          def __add__(self, other):
              return Point(self.x + other.x, self.y + other.y)

          def __sub__(self, other):
              return Point(self.x - other.x, self.y - other.y)

          def __eq__(self, other):
              return self.x == other.x and self.y == other.y

          def __str__(self):
              return f"Point({self.x}, {self.y})"

      p1 = Point(3, 4)
      p2 = Point(1, 2)
      p3 = p1 + p2
      p4 = p1 - p2
      print(f"p1 + p2 = {p3}")
      print(f"p1 - p2 = {p4}")
      print(f"p1 == p2: {p1 == p2}")

  - title: "Polymorphic File Processors"
    difficulty: intermediate
    description: "Create different file processor classes (CSV, JSON, XML) that all implement a process() method."
    starter_code: |
      class CSVProcessor:
          def __init__(self, data):
              self.data = data

          def process(self):
              # Return number of lines
              return len(self.data.split('\n'))

      class JSONProcessor:
          # TODO: Implement process() to count keys
          def __init__(self, data):
              self.data = data  # Dictionary
          pass

      class XMLProcessor:
          # TODO: Implement process() to count tags
          def __init__(self, data):
              self.data = data  # String with tags
          pass

      def analyze_file(processor):
          return f"Processed: {processor.process()} items"

      csv = CSVProcessor("a,b,c\n1,2,3\n4,5,6")
      json = JSONProcessor({"name": "Alice", "age": 30, "city": "NYC"})
      xml = XMLProcessor("<root><item/><item/></root>")
      print(analyze_file(csv))
      print(analyze_file(json))
      print(analyze_file(xml))
    expected_output: |
      Processed: 3 items
      Processed: 3 items
      Processed: 2 items
    hints:
      - "CSVProcessor counts lines using split"
      - "JSONProcessor counts dictionary keys"
      - "XMLProcessor counts '<item/>' occurrences"
    solution: |
      class CSVProcessor:
          def __init__(self, data):
              self.data = data

          def process(self):
              return len(self.data.split('\n'))

      class JSONProcessor:
          def __init__(self, data):
              self.data = data

          def process(self):
              return len(self.data.keys())

      class XMLProcessor:
          def __init__(self, data):
              self.data = data

          def process(self):
              return self.data.count('<item/>')

      def analyze_file(processor):
          return f"Processed: {processor.process()} items"

      csv = CSVProcessor("a,b,c\n1,2,3\n4,5,6")
      json = JSONProcessor({"name": "Alice", "age": 30, "city": "NYC"})
      xml = XMLProcessor("<root><item/><item/></root>")
      print(analyze_file(csv))
      print(analyze_file(json))
      print(analyze_file(xml))

  - title: "Advanced Operator Overloading"
    difficulty: advanced
    description: "Create a Fraction class with full operator overloading (+, -, *, /, ==, <, str)."
    starter_code: |
      class Fraction:
          def __init__(self, numerator, denominator):
              if denominator == 0:
                  raise ValueError("Denominator cannot be zero")
              self.numerator = numerator
              self.denominator = denominator
              self._simplify()

          def _gcd(self, a, b):
              # Greatest common divisor
              while b:
                  a, b = b, a % b
              return a

          def _simplify(self):
              # TODO: Simplify fraction using GCD
              pass

          # TODO: Implement __add__, __sub__, __mul__, __truediv__
          # TODO: Implement __eq__, __lt__, __str__
          pass

      f1 = Fraction(1, 2)
      f2 = Fraction(1, 3)
      print(f"{f1} + {f2} = {f1 + f2}")
      print(f"{f1} * {f2} = {f1 * f2}")
      print(f"{f1} < {f2}: {f1 < f2}")
    expected_output: |
      1/2 + 1/3 = 5/6
      1/2 * 1/3 = 1/6
      1/2 < 1/3: False
    hints:
      - "Addition: (a/b) + (c/d) = (ad + bc) / (bd)"
      - "Multiplication: (a/b) * (c/d) = (ac) / (bd)"
      - "Comparison: convert to decimal or cross multiply"
      - "Simplify by dividing by GCD"
    solution: |
      class Fraction:
          def __init__(self, numerator, denominator):
              if denominator == 0:
                  raise ValueError("Denominator cannot be zero")
              self.numerator = numerator
              self.denominator = denominator
              self._simplify()

          def _gcd(self, a, b):
              while b:
                  a, b = b, a % b
              return a

          def _simplify(self):
              gcd = self._gcd(abs(self.numerator), abs(self.denominator))
              self.numerator //= gcd
              self.denominator //= gcd

          def __add__(self, other):
              num = self.numerator * other.denominator + other.numerator * self.denominator
              den = self.denominator * other.denominator
              return Fraction(num, den)

          def __sub__(self, other):
              num = self.numerator * other.denominator - other.numerator * self.denominator
              den = self.denominator * other.denominator
              return Fraction(num, den)

          def __mul__(self, other):
              return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

          def __truediv__(self, other):
              return Fraction(self.numerator * other.denominator, self.denominator * other.numerator)

          def __eq__(self, other):
              return self.numerator == other.numerator and self.denominator == other.denominator

          def __lt__(self, other):
              return self.numerator * other.denominator < other.numerator * self.denominator

          def __str__(self):
              return f"{self.numerator}/{self.denominator}"

      f1 = Fraction(1, 2)
      f2 = Fraction(1, 3)
      print(f"{f1} + {f2} = {f1 + f2}")
      print(f"{f1} * {f2} = {f1 * f2}")
      print(f"{f1} < {f2}: {f1 < f2}")

  - title: "Polymorphic Storage System"
    difficulty: advanced
    description: "Create a storage interface with different implementations (Memory, File, Database) that can be used interchangeably."
    starter_code: |
      class Storage:
          def save(self, key, value):
              raise NotImplementedError

          def load(self, key):
              raise NotImplementedError

          def delete(self, key):
              raise NotImplementedError

      class MemoryStorage(Storage):
          # TODO: Implement using a dictionary
          pass

      class FileStorage(Storage):
          # TODO: Implement using a dictionary (simulate file)
          pass

      def test_storage(storage, name):
          storage.save("user1", "Alice")
          storage.save("user2", "Bob")
          print(f"{name}: {storage.load('user1')}")
          storage.delete("user1")
          print(f"{name} after delete: {storage.load('user1')}")

      memory = MemoryStorage()
      file_storage = FileStorage()
      test_storage(memory, "Memory")
      test_storage(file_storage, "File")
    expected_output: |
      Memory: Alice
      Memory after delete: None
      File: Alice
      File after delete: None
    hints:
      - "Use a dictionary to store key-value pairs"
      - "save() adds to dictionary"
      - "load() returns value or None if not found"
      - "delete() removes key from dictionary"
    solution: |
      class Storage:
          def save(self, key, value):
              raise NotImplementedError

          def load(self, key):
              raise NotImplementedError

          def delete(self, key):
              raise NotImplementedError

      class MemoryStorage(Storage):
          def __init__(self):
              self.data = {}

          def save(self, key, value):
              self.data[key] = value

          def load(self, key):
              return self.data.get(key)

          def delete(self, key):
              if key in self.data:
                  del self.data[key]

      class FileStorage(Storage):
          def __init__(self):
              self.data = {}

          def save(self, key, value):
              self.data[key] = value

          def load(self, key):
              return self.data.get(key)

          def delete(self, key):
              if key in self.data:
                  del self.data[key]

      def test_storage(storage, name):
          storage.save("user1", "Alice")
          storage.save("user2", "Bob")
          print(f"{name}: {storage.load('user1')}")
          storage.delete("user1")
          print(f"{name} after delete: {storage.load('user1')}")

      memory = MemoryStorage()
      file_storage = FileStorage()
      test_storage(memory, "Memory")
      test_storage(file_storage, "File")
```
<!-- EXERCISE_END -->
