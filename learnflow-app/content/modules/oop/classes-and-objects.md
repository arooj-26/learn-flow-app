# Classes and Objects

Classes and objects are the fundamental building blocks of Object-Oriented Programming (OOP). A class is a blueprint or template that defines the structure and behavior of objects, while an object is a specific instance of a class. Understanding how to create and use classes effectively is essential for writing organized, reusable, and maintainable code in Python.

## Understanding Classes

A class defines a custom data type that bundles data (attributes) and functions (methods) together. Think of a class as a cookie cutter and objects as the cookies made from that cutter. Each cookie (object) has the same shape (structure) but can have different decorations (attribute values).

In Python, we define a class using the `class` keyword followed by the class name (conventionally in PascalCase):

```python
class Car:
    """A simple class representing a car"""

    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.odometer = 0

    def display_info(self):
        return f"{self.year} {self.make} {self.model}"

    def drive(self, miles):
        self.odometer += miles
        return f"Driven {miles} miles. Total: {self.odometer}"

# Creating objects (instances)
my_car = Car("Toyota", "Camry", 2022)
your_car = Car("Honda", "Civic", 2023)

print(my_car.display_info())  # 2022 Toyota Camry
print(your_car.display_info())  # 2023 Honda Civic
```

## Objects and Instances

An object is a concrete instance of a class with specific values for its attributes. When you create an object, Python allocates memory for it and initializes it using the `__init__` method (the constructor). Each object has its own namespace, so attributes of one object don't affect another.

```python
class BankAccount:
    """Represents a bank account"""

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposit: +${amount}")
            return f"Deposited ${amount}. New balance: ${self.balance}"
        return "Invalid deposit amount"

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrawal: -${amount}")
            return f"Withdrew ${amount}. New balance: ${self.balance}"
        return "Insufficient funds"

    def get_statement(self):
        statement = f"Account holder: {self.owner}\n"
        statement += f"Current balance: ${self.balance}\n"
        statement += "Recent transactions:\n"
        for transaction in self.transactions[-5:]:
            statement += f"  - {transaction}\n"
        return statement

# Each object maintains its own state
alice_account = BankAccount("Alice", 1000)
bob_account = BankAccount("Bob", 500)

alice_account.deposit(500)
bob_account.withdraw(100)

print(alice_account.get_statement())
print(bob_account.get_statement())
```

## Attributes and Methods

Attributes are variables that belong to an object and store its state, while methods are functions that belong to an object and define its behavior. Instance attributes are unique to each object, created in the `__init__` method using `self`.

| Attribute Type | Scope | Example |
|---------------|-------|---------|
| Instance Attribute | Unique to each object | `self.name = "John"` |
| Class Attribute | Shared by all objects | `Car.wheels = 4` |
| Private Attribute | Internal use only | `self._balance` |

```python
class Student:
    """Represents a student in a course management system"""

    # Class attribute - shared by all students
    school_name = "Python Academy"

    def __init__(self, name, student_id, major):
        # Instance attributes - unique to each student
        self.name = name
        self.student_id = student_id
        self.major = major
        self.courses = []
        self.gpa = 0.0

    def enroll(self, course):
        """Enroll in a course"""
        if course not in self.courses:
            self.courses.append(course)
            return f"{self.name} enrolled in {course}"
        return f"Already enrolled in {course}"

    def drop(self, course):
        """Drop a course"""
        if course in self.courses:
            self.courses.remove(course)
            return f"{self.name} dropped {course}"
        return f"Not enrolled in {course}"

    def update_gpa(self, new_gpa):
        """Update student's GPA"""
        if 0.0 <= new_gpa <= 4.0:
            self.gpa = new_gpa
            return f"GPA updated to {self.gpa}"
        return "Invalid GPA value"

    def get_info(self):
        """Get student information"""
        info = f"Name: {self.name}\n"
        info += f"ID: {self.student_id}\n"
        info += f"Major: {self.major}\n"
        info += f"GPA: {self.gpa}\n"
        info += f"Courses: {', '.join(self.courses) if self.courses else 'None'}\n"
        info += f"School: {Student.school_name}"
        return info

student1 = Student("Emma Wilson", "S12345", "Computer Science")
student1.enroll("Data Structures")
student1.enroll("Algorithms")
student1.update_gpa(3.8)

print(student1.get_info())
```

## Real-World Example: Library System

Let's build a more complex example that demonstrates how classes and objects work together in a library management system:

```python
class Book:
    """Represents a book in the library"""

    def __init__(self, title, author, isbn, copies=1):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = copies
        self.available_copies = copies
        self.borrowed_by = []

    def checkout(self, borrower):
        """Check out a book"""
        if self.available_copies > 0:
            self.available_copies -= 1
            self.borrowed_by.append(borrower)
            return f"'{self.title}' checked out to {borrower}"
        return f"'{self.title}' is not available"

    def return_book(self, borrower):
        """Return a book"""
        if borrower in self.borrowed_by:
            self.available_copies += 1
            self.borrowed_by.remove(borrower)
            return f"'{self.title}' returned by {borrower}"
        return f"{borrower} didn't borrow '{self.title}'"

    def get_status(self):
        """Get book availability status"""
        return f"'{self.title}' by {self.author} - {self.available_copies}/{self.total_copies} available"

class Library:
    """Represents a library with books"""

    def __init__(self, name):
        self.name = name
        self.books = {}  # ISBN -> Book object

    def add_book(self, book):
        """Add a book to the library"""
        if book.isbn in self.books:
            self.books[book.isbn].total_copies += book.total_copies
            self.books[book.isbn].available_copies += book.available_copies
            return f"Added more copies of '{book.title}'"
        else:
            self.books[book.isbn] = book
            return f"Added new book: '{book.title}'"

    def find_book(self, isbn):
        """Find a book by ISBN"""
        return self.books.get(isbn, None)

    def list_available_books(self):
        """List all available books"""
        available = [book.get_status() for book in self.books.values()
                    if book.available_copies > 0]
        return "\n".join(available) if available else "No books available"

# Create library and books
my_library = Library("City Central Library")

book1 = Book("Python Crash Course", "Eric Matthes", "978-1593279288", 3)
book2 = Book("Clean Code", "Robert Martin", "978-0132350884", 2)
book3 = Book("Design Patterns", "Gang of Four", "978-0201633610", 1)

my_library.add_book(book1)
my_library.add_book(book2)
my_library.add_book(book3)

# Simulate library operations
print(book1.checkout("Alice"))
print(book1.checkout("Bob"))
print(my_library.list_available_books())
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Create a Rectangle Class"
    difficulty: basic
    description: "Create a Rectangle class with width and height attributes, and methods to calculate area and perimeter."
    starter_code: |
      class Rectangle:
          # TODO: Add __init__ method to initialize width and height

          # TODO: Add area method

          # TODO: Add perimeter method
          pass

      # Test your class
      rect = Rectangle(5, 3)
      print(f"Area: {rect.area()}")
      print(f"Perimeter: {rect.perimeter()}")
    expected_output: |
      Area: 15
      Perimeter: 16
    hints:
      - "Area = width * height"
      - "Perimeter = 2 * (width + height)"
      - "Use self to access instance attributes"
    solution: |
      class Rectangle:
          def __init__(self, width, height):
              self.width = width
              self.height = height

          def area(self):
              return self.width * self.height

          def perimeter(self):
              return 2 * (self.width + self.height)

      # Test your class
      rect = Rectangle(5, 3)
      print(f"Area: {rect.area()}")
      print(f"Perimeter: {rect.perimeter()}")

  - title: "Product Inventory System"
    difficulty: basic
    description: "Create a Product class to manage inventory with name, price, and quantity. Include methods to add stock and sell items."
    starter_code: |
      class Product:
          # TODO: Initialize with name, price, and quantity

          # TODO: Add add_stock method

          # TODO: Add sell method (check if enough stock)

          # TODO: Add get_value method (price * quantity)
          pass

      product = Product("Laptop", 999.99, 10)
      product.add_stock(5)
      print(product.sell(3))
      print(f"Inventory value: ${product.get_value()}")
    expected_output: |
      Sold 3 units. Remaining: 12
      Inventory value: $11999.88
    hints:
      - "Check if quantity is sufficient before selling"
      - "Update quantity after adding stock or selling"
      - "Round the inventory value to 2 decimal places"
    solution: |
      class Product:
          def __init__(self, name, price, quantity):
              self.name = name
              self.price = price
              self.quantity = quantity

          def add_stock(self, amount):
              self.quantity += amount

          def sell(self, amount):
              if amount <= self.quantity:
                  self.quantity -= amount
                  return f"Sold {amount} units. Remaining: {self.quantity}"
              return "Insufficient stock"

          def get_value(self):
              return round(self.price * self.quantity, 2)

      product = Product("Laptop", 999.99, 10)
      product.add_stock(5)
      print(product.sell(3))
      print(f"Inventory value: ${product.get_value()}")

  - title: "Temperature Converter Class"
    difficulty: intermediate
    description: "Create a Temperature class that can store temperature in Celsius and convert to Fahrenheit and Kelvin. Include methods to update the temperature."
    starter_code: |
      class Temperature:
          # TODO: Initialize with celsius value

          # TODO: Add to_fahrenheit method

          # TODO: Add to_kelvin method

          # TODO: Add set_celsius method

          # TODO: Add compare method to compare with another Temperature
          pass

      temp1 = Temperature(25)
      print(f"Celsius: {temp1.celsius}")
      print(f"Fahrenheit: {temp1.to_fahrenheit()}")
      print(f"Kelvin: {temp1.to_kelvin()}")
    expected_output: |
      Celsius: 25
      Fahrenheit: 77.0
      Kelvin: 298.15
    hints:
      - "Fahrenheit = (Celsius * 9/5) + 32"
      - "Kelvin = Celsius + 273.15"
      - "Store temperature internally in Celsius"
    solution: |
      class Temperature:
          def __init__(self, celsius):
              self.celsius = celsius

          def to_fahrenheit(self):
              return (self.celsius * 9/5) + 32

          def to_kelvin(self):
              return self.celsius + 273.15

          def set_celsius(self, celsius):
              self.celsius = celsius

          def compare(self, other):
              if self.celsius > other.celsius:
                  return "warmer"
              elif self.celsius < other.celsius:
                  return "cooler"
              return "same"

      temp1 = Temperature(25)
      print(f"Celsius: {temp1.celsius}")
      print(f"Fahrenheit: {temp1.to_fahrenheit()}")
      print(f"Kelvin: {temp1.to_kelvin()}")

  - title: "Shopping Cart System"
    difficulty: intermediate
    description: "Create a ShoppingCart class that can add items, remove items, calculate total, and apply discounts. Each item should be a dictionary with name, price, and quantity."
    starter_code: |
      class ShoppingCart:
          # TODO: Initialize with empty cart

          # TODO: Add add_item method

          # TODO: Add remove_item method

          # TODO: Add calculate_total method

          # TODO: Add apply_discount method (percentage)
          pass

      cart = ShoppingCart()
      cart.add_item("Apple", 1.50, 3)
      cart.add_item("Bread", 2.50, 1)
      print(f"Total: ${cart.calculate_total()}")
      print(f"After 10% discount: ${cart.apply_discount(10)}")
    expected_output: |
      Total: $7.0
      After 10% discount: $6.3
    hints:
      - "Store items as a list of dictionaries"
      - "Discount percentage should reduce the total"
      - "Calculate total by summing price * quantity for each item"
    solution: |
      class ShoppingCart:
          def __init__(self):
              self.items = []

          def add_item(self, name, price, quantity):
              self.items.append({"name": name, "price": price, "quantity": quantity})

          def remove_item(self, name):
              self.items = [item for item in self.items if item["name"] != name]

          def calculate_total(self):
              return sum(item["price"] * item["quantity"] for item in self.items)

          def apply_discount(self, percentage):
              total = self.calculate_total()
              return round(total * (1 - percentage / 100), 2)

      cart = ShoppingCart()
      cart.add_item("Apple", 1.50, 3)
      cart.add_item("Bread", 2.50, 1)
      print(f"Total: ${cart.calculate_total()}")
      print(f"After 10% discount: ${cart.apply_discount(10)}")

  - title: "Task Management System"
    difficulty: advanced
    description: "Create a Task class and TaskManager class. Tasks should have title, description, priority (1-5), and status. TaskManager should organize and filter tasks."
    starter_code: |
      class Task:
          # TODO: Initialize task with title, description, priority, status
          pass

      class TaskManager:
          # TODO: Initialize with empty task list

          # TODO: Add create_task method

          # TODO: Add get_tasks_by_priority method

          # TODO: Add get_tasks_by_status method

          # TODO: Add complete_task method
          pass

      manager = TaskManager()
      manager.create_task("Fix bug", "Fix login issue", 5, "pending")
      manager.create_task("Write docs", "Document API", 3, "pending")
      manager.complete_task("Fix bug")
      print(f"High priority tasks: {len(manager.get_tasks_by_priority(4))}")
    expected_output: |
      High priority tasks: 1
    hints:
      - "Use a list to store all tasks"
      - "Filter tasks based on priority or status"
      - "Update task status when completing"
    solution: |
      class Task:
          def __init__(self, title, description, priority, status="pending"):
              self.title = title
              self.description = description
              self.priority = priority
              self.status = status

      class TaskManager:
          def __init__(self):
              self.tasks = []

          def create_task(self, title, description, priority, status="pending"):
              task = Task(title, description, priority, status)
              self.tasks.append(task)

          def get_tasks_by_priority(self, min_priority):
              return [task for task in self.tasks if task.priority >= min_priority]

          def get_tasks_by_status(self, status):
              return [task for task in self.tasks if task.status == status]

          def complete_task(self, title):
              for task in self.tasks:
                  if task.title == title:
                      task.status = "completed"

      manager = TaskManager()
      manager.create_task("Fix bug", "Fix login issue", 5, "pending")
      manager.create_task("Write docs", "Document API", 3, "pending")
      manager.complete_task("Fix bug")
      print(f"High priority tasks: {len(manager.get_tasks_by_priority(4))}")

  - title: "University Course System"
    difficulty: advanced
    description: "Create a Course class and University class. Courses have name, code, credits, and enrolled students (max capacity). University manages multiple courses."
    starter_code: |
      class Course:
          # TODO: Initialize with name, code, credits, capacity
          pass

      class University:
          # TODO: Initialize with name and empty course list

          # TODO: Add add_course method

          # TODO: Add enroll_student method (course_code, student_name)

          # TODO: Add get_course_info method

          # TODO: Add get_total_enrollment method
          pass

      uni = University("Tech University")
      uni.add_course("Data Structures", "CS201", 3, 30)
      uni.add_course("Algorithms", "CS301", 4, 25)
      print(uni.enroll_student("CS201", "Alice"))
      print(uni.enroll_student("CS201", "Bob"))
      print(f"Total enrollment: {uni.get_total_enrollment()}")
    expected_output: |
      Alice enrolled in Data Structures
      Bob enrolled in Data Structures
      Total enrollment: 2
    hints:
      - "Check capacity before enrolling students"
      - "Store courses in a dictionary with code as key"
      - "Track enrolled students in each course"
    solution: |
      class Course:
          def __init__(self, name, code, credits, capacity):
              self.name = name
              self.code = code
              self.credits = credits
              self.capacity = capacity
              self.enrolled = []

          def enroll(self, student_name):
              if len(self.enrolled) < self.capacity:
                  self.enrolled.append(student_name)
                  return True
              return False

      class University:
          def __init__(self, name):
              self.name = name
              self.courses = {}

          def add_course(self, name, code, credits, capacity):
              course = Course(name, code, credits, capacity)
              self.courses[code] = course

          def enroll_student(self, course_code, student_name):
              if course_code in self.courses:
                  course = self.courses[course_code]
                  if course.enroll(student_name):
                      return f"{student_name} enrolled in {course.name}"
                  return "Course is full"
              return "Course not found"

          def get_course_info(self, course_code):
              if course_code in self.courses:
                  course = self.courses[course_code]
                  return f"{course.name} ({course.code}): {len(course.enrolled)}/{course.capacity}"
              return "Course not found"

          def get_total_enrollment(self):
              return sum(len(course.enrolled) for course in self.courses.values())

      uni = University("Tech University")
      uni.add_course("Data Structures", "CS201", 3, 30)
      uni.add_course("Algorithms", "CS301", 4, 25)
      print(uni.enroll_student("CS201", "Alice"))
      print(uni.enroll_student("CS201", "Bob"))
      print(f"Total enrollment: {uni.get_total_enrollment()}")
```
<!-- EXERCISE_END -->
