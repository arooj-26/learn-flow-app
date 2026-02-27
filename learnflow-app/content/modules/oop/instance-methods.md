# Instance Methods

Instance methods are functions defined inside a class that operate on instances of that class. They are the primary way objects perform actions and interact with their data. Instance methods always take `self` as their first parameter, which refers to the instance calling the method, allowing them to access and modify the object's attributes.

## Understanding Instance Methods

Instance methods define the behavior of objects. They can access and modify instance attributes using `self`, call other methods, and perform operations specific to that instance. The `self` parameter is automatically passed when you call a method on an object.

```python
class Counter:
    """A simple counter class demonstrating instance methods"""

    def __init__(self, initial_value=0):
        """Initialize counter with optional starting value"""
        self.value = initial_value
        self.history = [initial_value]

    def increment(self, amount=1):
        """Increase counter by specified amount"""
        self.value += amount
        self.history.append(self.value)
        return self.value

    def decrement(self, amount=1):
        """Decrease counter by specified amount"""
        self.value -= amount
        self.history.append(self.value)
        return self.value

    def reset(self):
        """Reset counter to zero"""
        self.value = 0
        self.history.append(self.value)
        return "Counter reset"

    def get_history(self):
        """Return the counter's history"""
        return self.history

    def get_stats(self):
        """Calculate and return counter statistics"""
        return {
            "current": self.value,
            "min": min(self.history),
            "max": max(self.history),
            "changes": len(self.history) - 1
        }

# Using instance methods
counter = Counter(10)
counter.increment(5)
counter.increment(3)
counter.decrement(2)
print(f"Current value: {counter.value}")
print(f"Statistics: {counter.get_stats()}")
print(f"History: {counter.get_history()}")
```

## Methods with Different Return Types

Instance methods can return different types of values: primitives, collections, other objects, or even `self` for method chaining. Understanding what to return and when is crucial for designing useful APIs.

| Return Type | Use Case | Example |
|------------|----------|---------|
| None | Methods that modify state | `list.append()` |
| self | Enable method chaining | `string_builder.append().append()` |
| New object | Immutable operations | `string.upper()` |
| Primitive | Calculations/queries | `list.count()` |
| Collection | Aggregated data | `dict.keys()` |

```python
class TextProcessor:
    """Process and analyze text with various return types"""

    def __init__(self, text=""):
        """Initialize with optional text"""
        self.text = text
        self.transformations = []

    def set_text(self, text):
        """Set text - returns None (modifies state)"""
        self.text = text
        self.transformations.append("set")

    def append(self, text):
        """Append text - returns self for chaining"""
        self.text += text
        self.transformations.append("append")
        return self

    def to_upper(self):
        """Convert to uppercase - returns self for chaining"""
        self.text = self.text.upper()
        self.transformations.append("upper")
        return self

    def to_lower(self):
        """Convert to lowercase - returns self for chaining"""
        self.text = self.text.lower()
        self.transformations.append("lower")
        return self

    def word_count(self):
        """Count words - returns primitive (int)"""
        return len(self.text.split())

    def get_words(self):
        """Get list of words - returns collection"""
        return self.text.split()

    def create_copy(self):
        """Create a copy - returns new object"""
        new_processor = TextProcessor(self.text)
        new_processor.transformations = self.transformations.copy()
        return new_processor

    def get_stats(self):
        """Get statistics - returns dictionary"""
        words = self.get_words()
        return {
            "characters": len(self.text),
            "words": len(words),
            "unique_words": len(set(words)),
            "transformations": len(self.transformations)
        }

# Demonstrating different return types
processor = TextProcessor("Hello")

# Method chaining (returns self)
processor.append(" World").to_upper().append("!")
print(processor.text)  # HELLO WORLD!

# Returns primitive
print(f"Word count: {processor.word_count()}")

# Returns collection
print(f"Words: {processor.get_words()}")

# Returns new object
copy = processor.create_copy()
copy.to_lower()
print(f"Original: {processor.text}")
print(f"Copy: {copy.text}")

# Returns dictionary
print(f"Stats: {processor.get_stats()}")
```

## Methods Calling Other Methods

Instance methods can call other methods of the same class using `self`. This promotes code reuse, improves organization, and allows you to build complex operations from simpler ones.

```python
class ShoppingCart:
    """Shopping cart with methods that call other methods"""

    def __init__(self):
        """Initialize empty cart"""
        self.items = []
        self.discount_rate = 0
        self.tax_rate = 0.08

    def add_item(self, name, price, quantity=1):
        """Add item to cart"""
        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })
        return f"Added {quantity}x {name}"

    def remove_item(self, name):
        """Remove item from cart"""
        self.items = [item for item in self.items if item["name"] != name]
        return f"Removed {name}"

    def calculate_subtotal(self):
        """Calculate subtotal before discount and tax"""
        return sum(item["price"] * item["quantity"] for item in self.items)

    def calculate_discount(self):
        """Calculate discount amount"""
        subtotal = self.calculate_subtotal()
        return subtotal * self.discount_rate

    def calculate_tax(self):
        """Calculate tax on discounted amount"""
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        taxable_amount = subtotal - discount
        return taxable_amount * self.tax_rate

    def calculate_total(self):
        """Calculate final total (calls other calculation methods)"""
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        tax = self.calculate_tax()
        return subtotal - discount + tax

    def apply_discount(self, rate):
        """Apply discount percentage"""
        if 0 <= rate <= 1:
            self.discount_rate = rate
            return f"Discount of {rate*100}% applied"
        return "Invalid discount rate"

    def get_receipt(self):
        """Generate receipt (calls multiple methods)"""
        receipt = "=" * 40 + "\n"
        receipt += "RECEIPT\n"
        receipt += "=" * 40 + "\n"

        for item in self.items:
            line_total = item["price"] * item["quantity"]
            receipt += f"{item['name']} x{item['quantity']} @ ${item['price']:.2f} = ${line_total:.2f}\n"

        receipt += "-" * 40 + "\n"
        receipt += f"Subtotal:     ${self.calculate_subtotal():.2f}\n"

        if self.discount_rate > 0:
            receipt += f"Discount:    -${self.calculate_discount():.2f}\n"

        receipt += f"Tax (8%):     ${self.calculate_tax():.2f}\n"
        receipt += "=" * 40 + "\n"
        receipt += f"TOTAL:        ${self.calculate_total():.2f}\n"
        receipt += "=" * 40

        return receipt

# Using the shopping cart
cart = ShoppingCart()
cart.add_item("Laptop", 999.99, 1)
cart.add_item("Mouse", 29.99, 2)
cart.add_item("Keyboard", 79.99, 1)
cart.apply_discount(0.10)  # 10% discount

print(cart.get_receipt())
```

## Getter and Setter Methods

Getter and setter methods (also called accessor and mutator methods) provide controlled access to an object's attributes. They allow you to add validation, logging, or transformations when getting or setting values.

```python
class Temperature:
    """Temperature class with getter/setter methods"""

    def __init__(self, celsius=0):
        """Initialize temperature in Celsius"""
        self._celsius = celsius  # Protected attribute
        self._history = [celsius]

    def get_celsius(self):
        """Get temperature in Celsius"""
        return self._celsius

    def set_celsius(self, value):
        """Set temperature in Celsius with validation"""
        if value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero")
        self._celsius = value
        self._history.append(value)

    def get_fahrenheit(self):
        """Get temperature in Fahrenheit"""
        return (self._celsius * 9/5) + 32

    def set_fahrenheit(self, value):
        """Set temperature using Fahrenheit"""
        celsius = (value - 32) * 5/9
        self.set_celsius(celsius)

    def get_kelvin(self):
        """Get temperature in Kelvin"""
        return self._celsius + 273.15

    def set_kelvin(self, value):
        """Set temperature using Kelvin"""
        celsius = value - 273.15
        self.set_celsius(celsius)

    def get_min_max(self):
        """Get minimum and maximum recorded temperatures"""
        return {
            "min": min(self._history),
            "max": max(self._history),
            "current": self._celsius
        }

    def reset_history(self):
        """Reset temperature history"""
        self._history = [self._celsius]

# Using getter and setter methods
temp = Temperature(25)
print(f"Celsius: {temp.get_celsius()}")
print(f"Fahrenheit: {temp.get_fahrenheit()}")
print(f"Kelvin: {temp.get_kelvin()}")

temp.set_fahrenheit(98.6)
print(f"After setting to 98.6°F: {temp.get_celsius()}°C")

temp.set_celsius(30)
temp.set_celsius(20)
print(f"Temperature range: {temp.get_min_max()}")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Basic Calculator Methods"
    difficulty: basic
    description: "Create a Calculator class with instance methods for basic arithmetic operations (add, subtract, multiply, divide)."
    starter_code: |
      class Calculator:
          def __init__(self):
              self.result = 0

          def add(self, value):
              # TODO: Add value to result
              pass

          def subtract(self, value):
              # TODO: Subtract value from result
              pass

          def multiply(self, value):
              # TODO: Multiply result by value
              pass

          def get_result(self):
              # TODO: Return current result
              pass

      calc = Calculator()
      calc.add(10)
      calc.multiply(5)
      calc.subtract(8)
      print(f"Result: {calc.get_result()}")
    expected_output: |
      Result: 42
    hints:
      - "Use self.result to store the current value"
      - "Each method should modify self.result"
      - "Return the updated result from each operation"
    solution: |
      class Calculator:
          def __init__(self):
              self.result = 0

          def add(self, value):
              self.result += value
              return self.result

          def subtract(self, value):
              self.result -= value
              return self.result

          def multiply(self, value):
              self.result *= value
              return self.result

          def get_result(self):
              return self.result

      calc = Calculator()
      calc.add(10)
      calc.multiply(5)
      calc.subtract(8)
      print(f"Result: {calc.get_result()}")

  - title: "String Builder with Method Chaining"
    difficulty: basic
    description: "Create a StringBuilder class with methods that return self to enable method chaining."
    starter_code: |
      class StringBuilder:
          def __init__(self):
              self.text = ""

          def append(self, text):
              # TODO: Append text and return self
              pass

          def prepend(self, text):
              # TODO: Prepend text and return self
              pass

          def build(self):
              # TODO: Return final string
              pass

      builder = StringBuilder()
      result = builder.append("World").prepend("Hello ").append("!").build()
      print(result)
    expected_output: |
      Hello World!
    hints:
      - "Return self from append and prepend to enable chaining"
      - "Prepend means adding to the beginning"
      - "build() should return self.text"
    solution: |
      class StringBuilder:
          def __init__(self):
              self.text = ""

          def append(self, text):
              self.text += text
              return self

          def prepend(self, text):
              self.text = text + self.text
              return self

          def build(self):
              return self.text

      builder = StringBuilder()
      result = builder.append("World").prepend("Hello ").append("!").build()
      print(result)

  - title: "Player Stats Tracker"
    difficulty: intermediate
    description: "Create a Player class with methods to update stats, calculate averages, and check achievements. Methods should call other methods."
    starter_code: |
      class Player:
          def __init__(self, name):
              self.name = name
              self.scores = []
              self.games_played = 0

          def add_score(self, score):
              # TODO: Add score and increment games_played
              pass

          def get_average(self):
              # TODO: Calculate average score
              pass

          def get_high_score(self):
              # TODO: Return highest score or 0 if no scores
              pass

          def has_achievement(self, threshold):
              # TODO: Check if average is above threshold
              pass

      player = Player("Alice")
      player.add_score(85)
      player.add_score(92)
      player.add_score(88)
      print(f"Average: {player.get_average()}")
      print(f"Achievement unlocked: {player.has_achievement(90)}")
    expected_output: |
      Average: 88.33
      Achievement unlocked: False
    hints:
      - "Use sum(self.scores) / len(self.scores) for average"
      - "has_achievement should call get_average()"
      - "Round average to 2 decimal places"
    solution: |
      class Player:
          def __init__(self, name):
              self.name = name
              self.scores = []
              self.games_played = 0

          def add_score(self, score):
              self.scores.append(score)
              self.games_played += 1

          def get_average(self):
              if not self.scores:
                  return 0
              return round(sum(self.scores) / len(self.scores), 2)

          def get_high_score(self):
              return max(self.scores) if self.scores else 0

          def has_achievement(self, threshold):
              return self.get_average() >= threshold

      player = Player("Alice")
      player.add_score(85)
      player.add_score(92)
      player.add_score(88)
      print(f"Average: {player.get_average()}")
      print(f"Achievement unlocked: {player.has_achievement(90)}")

  - title: "Bank Account with Validation"
    difficulty: intermediate
    description: "Create a BankAccount class with deposit, withdraw, and transfer methods. Include validation and transaction history."
    starter_code: |
      class BankAccount:
          def __init__(self, owner, initial_balance=0):
              self.owner = owner
              self.balance = initial_balance
              self.transactions = []

          def deposit(self, amount):
              # TODO: Validate amount > 0, update balance, record transaction
              pass

          def withdraw(self, amount):
              # TODO: Validate amount and balance, update, record transaction
              pass

          def get_transaction_count(self):
              # TODO: Return number of transactions
              pass

      account = BankAccount("John", 1000)
      account.deposit(500)
      account.withdraw(200)
      print(f"Balance: ${account.balance}")
      print(f"Transactions: {account.get_transaction_count()}")
    expected_output: |
      Balance: $1300
      Transactions: 2
    hints:
      - "Check if amount > 0 before processing"
      - "For withdraw, check if amount <= balance"
      - "Store transactions as dictionaries with type and amount"
    solution: |
      class BankAccount:
          def __init__(self, owner, initial_balance=0):
              self.owner = owner
              self.balance = initial_balance
              self.transactions = []

          def deposit(self, amount):
              if amount > 0:
                  self.balance += amount
                  self.transactions.append({"type": "deposit", "amount": amount})
                  return True
              return False

          def withdraw(self, amount):
              if amount > 0 and amount <= self.balance:
                  self.balance -= amount
                  self.transactions.append({"type": "withdraw", "amount": amount})
                  return True
              return False

          def get_transaction_count(self):
              return len(self.transactions)

      account = BankAccount("John", 1000)
      account.deposit(500)
      account.withdraw(200)
      print(f"Balance: ${account.balance}")
      print(f"Transactions: {account.get_transaction_count()}")

  - title: "Playlist Manager"
    difficulty: advanced
    description: "Create a Playlist class that manages songs with methods for adding, removing, shuffling, and getting song statistics. Methods should call each other."
    starter_code: |
      import random

      class Playlist:
          def __init__(self, name):
              self.name = name
              self.songs = []
              self.current_index = 0

          def add_song(self, title, artist, duration):
              # TODO: Add song as dictionary
              pass

          def remove_song(self, title):
              # TODO: Remove song by title
              pass

          def get_total_duration(self):
              # TODO: Calculate total duration in seconds
              pass

          def shuffle(self):
              # TODO: Shuffle songs and reset index
              pass

          def get_next_song(self):
              # TODO: Get next song and increment index (wrap around)
              pass

      playlist = Playlist("My Favorites")
      playlist.add_song("Song A", "Artist 1", 180)
      playlist.add_song("Song B", "Artist 2", 200)
      playlist.add_song("Song C", "Artist 1", 190)
      print(f"Total duration: {playlist.get_total_duration()} seconds")
      print(f"Songs: {len(playlist.songs)}")
    expected_output: |
      Total duration: 570 seconds
      Songs: 3
    hints:
      - "Store songs as list of dictionaries with title, artist, duration"
      - "Use random.shuffle() for shuffling"
      - "Use modulo for wrapping index: (index + 1) % len(songs)"
    solution: |
      import random

      class Playlist:
          def __init__(self, name):
              self.name = name
              self.songs = []
              self.current_index = 0

          def add_song(self, title, artist, duration):
              self.songs.append({"title": title, "artist": artist, "duration": duration})

          def remove_song(self, title):
              self.songs = [song for song in self.songs if song["title"] != title]

          def get_total_duration(self):
              return sum(song["duration"] for song in self.songs)

          def shuffle(self):
              random.shuffle(self.songs)
              self.current_index = 0

          def get_next_song(self):
              if not self.songs:
                  return None
              song = self.songs[self.current_index]
              self.current_index = (self.current_index + 1) % len(self.songs)
              return song

      playlist = Playlist("My Favorites")
      playlist.add_song("Song A", "Artist 1", 180)
      playlist.add_song("Song B", "Artist 2", 200)
      playlist.add_song("Song C", "Artist 1", 190)
      print(f"Total duration: {playlist.get_total_duration()} seconds")
      print(f"Songs: {len(playlist.songs)}")

  - title: "Inventory Management System"
    difficulty: advanced
    description: "Create an Inventory class with methods for stock management, low stock alerts, restocking, and generating reports. Use getter/setter patterns and method composition."
    starter_code: |
      class Inventory:
          def __init__(self):
              self.products = {}
              self.low_stock_threshold = 10

          def add_product(self, product_id, name, quantity, price):
              # TODO: Add product to inventory
              pass

          def update_quantity(self, product_id, quantity):
              # TODO: Update product quantity
              pass

          def get_low_stock_items(self):
              # TODO: Return list of products below threshold
              pass

          def get_inventory_value(self):
              # TODO: Calculate total inventory value
              pass

          def restock(self, product_id, quantity):
              # TODO: Add to existing quantity
              pass

          def generate_report(self):
              # TODO: Return formatted inventory report
              pass

      inv = Inventory()
      inv.add_product("P001", "Laptop", 5, 999.99)
      inv.add_product("P002", "Mouse", 25, 29.99)
      inv.restock("P001", 10)
      print(f"Low stock items: {len(inv.get_low_stock_items())}")
      print(f"Total value: ${inv.get_inventory_value()}")
    expected_output: |
      Low stock items: 0
      Total value: $15749.6
    hints:
      - "Store products as dictionary: {product_id: {name, quantity, price}}"
      - "get_low_stock_items filters products where quantity < threshold"
      - "Calculate value as sum of (quantity * price) for all products"
    solution: |
      class Inventory:
          def __init__(self):
              self.products = {}
              self.low_stock_threshold = 10

          def add_product(self, product_id, name, quantity, price):
              self.products[product_id] = {
                  "name": name,
                  "quantity": quantity,
                  "price": price
              }

          def update_quantity(self, product_id, quantity):
              if product_id in self.products:
                  self.products[product_id]["quantity"] = quantity

          def get_low_stock_items(self):
              return [
                  pid for pid, product in self.products.items()
                  if product["quantity"] < self.low_stock_threshold
              ]

          def get_inventory_value(self):
              return sum(
                  product["quantity"] * product["price"]
                  for product in self.products.values()
              )

          def restock(self, product_id, quantity):
              if product_id in self.products:
                  self.products[product_id]["quantity"] += quantity

          def generate_report(self):
              report = "Inventory Report\n"
              for pid, product in self.products.items():
                  report += f"{pid}: {product['name']} - Qty: {product['quantity']} @ ${product['price']}\n"
              return report

      inv = Inventory()
      inv.add_product("P001", "Laptop", 5, 999.99)
      inv.add_product("P002", "Mouse", 25, 29.99)
      inv.restock("P001", 10)
      print(f"Low stock items: {len(inv.get_low_stock_items())}")
      print(f"Total value: ${inv.get_inventory_value()}")
```
<!-- EXERCISE_END -->
