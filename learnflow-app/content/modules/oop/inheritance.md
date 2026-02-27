# Inheritance

Inheritance is a fundamental concept in object-oriented programming that allows you to create new classes based on existing ones. The new class (child or subclass) inherits attributes and methods from the existing class (parent or superclass), promoting code reuse and establishing hierarchical relationships between classes.

## Understanding Inheritance

Inheritance enables you to create a new class that reuses, extends, or modifies the behavior of an existing class. The child class inherits all public and protected attributes and methods from the parent class, and can add new ones or override existing ones.

```python
class Animal:
    """Base class for all animals"""

    def __init__(self, name, species):
        """Initialize animal with name and species"""
        self.name = name
        self.species = species
        self.is_alive = True

    def eat(self, food):
        """Animal eating behavior"""
        return f"{self.name} is eating {food}"

    def sleep(self):
        """Animal sleeping behavior"""
        return f"{self.name} is sleeping"

    def make_sound(self):
        """Generic sound - to be overridden by subclasses"""
        return f"{self.name} makes a sound"

class Dog(Animal):
    """Dog class inheriting from Animal"""

    def __init__(self, name, breed):
        """Initialize dog with name and breed"""
        # Call parent constructor
        super().__init__(name, "Dog")
        self.breed = breed
        self.tricks = []

    def make_sound(self):
        """Override parent method"""
        return f"{self.name} barks: Woof! Woof!"

    def learn_trick(self, trick):
        """Dog-specific method"""
        self.tricks.append(trick)
        return f"{self.name} learned {trick}"

    def perform_tricks(self):
        """Perform all learned tricks"""
        if not self.tricks:
            return f"{self.name} doesn't know any tricks yet"
        return f"{self.name} performs: {', '.join(self.tricks)}"

class Cat(Animal):
    """Cat class inheriting from Animal"""

    def __init__(self, name, indoor=True):
        """Initialize cat"""
        super().__init__(name, "Cat")
        self.indoor = indoor
        self.lives = 9

    def make_sound(self):
        """Override parent method"""
        return f"{self.name} meows: Meow!"

    def climb_tree(self):
        """Cat-specific method"""
        if not self.indoor:
            return f"{self.name} climbs a tree"
        return f"{self.name} is an indoor cat and can't climb trees"

# Using inheritance
dog = Dog("Buddy", "Golden Retriever")
cat = Cat("Whiskers", indoor=True)

print(dog.make_sound())  # Overridden method
print(dog.eat("kibble"))  # Inherited method
print(dog.learn_trick("sit"))

print(cat.make_sound())  # Overridden method
print(cat.sleep())  # Inherited method
print(cat.climb_tree())
```

## The super() Function

The `super()` function is used to call methods from the parent class. It's essential for properly initializing parent class attributes and extending parent methods rather than completely replacing them.

| Use Case | Example | Purpose |
|----------|---------|---------|
| Constructor | `super().__init__()` | Initialize parent attributes |
| Method extension | `super().method()` | Call parent version then add more |
| Multiple inheritance | `super()` | Navigate inheritance chain |

```python
class Employee:
    """Base employee class"""

    company_name = "Tech Corp"

    def __init__(self, name, employee_id, salary):
        """Initialize employee"""
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
        self.years_of_service = 0

    def give_raise(self, amount):
        """Give raise to employee"""
        self.salary += amount
        return f"{self.name} received ${amount} raise"

    def get_info(self):
        """Get employee information"""
        return f"{self.name} ({self.employee_id}) - ${self.salary}"

class Manager(Employee):
    """Manager class extending Employee"""

    def __init__(self, name, employee_id, salary, department):
        """Initialize manager"""
        # Call parent constructor
        super().__init__(name, employee_id, salary)
        self.department = department
        self.team_members = []

    def add_team_member(self, employee):
        """Add team member"""
        self.team_members.append(employee)
        return f"{employee.name} added to {self.name}'s team"

    def get_team_size(self):
        """Get number of team members"""
        return len(self.team_members)

    def get_info(self):
        """Override and extend parent method"""
        # Call parent method first
        base_info = super().get_info()
        # Add manager-specific information
        return f"{base_info} | Manager of {self.department} ({self.get_team_size()} team members)"

class Developer(Employee):
    """Developer class extending Employee"""

    def __init__(self, name, employee_id, salary, programming_languages):
        """Initialize developer"""
        super().__init__(name, employee_id, salary)
        self.programming_languages = programming_languages
        self.projects = []

    def add_project(self, project_name):
        """Add project to developer"""
        self.projects.append(project_name)
        return f"{self.name} assigned to {project_name}"

    def give_raise(self, amount):
        """Override raise method with performance bonus"""
        # Call parent raise method
        result = super().give_raise(amount)
        # Add performance bonus
        bonus = amount * 0.1
        self.salary += bonus
        return f"{result} + ${bonus:.2f} performance bonus"

    def get_info(self):
        """Override parent method"""
        base_info = super().get_info()
        languages = ", ".join(self.programming_languages)
        return f"{base_info} | Languages: {languages} | Projects: {len(self.projects)}"

# Using the hierarchy
manager = Manager("Sarah Johnson", "M001", 90000, "Engineering")
dev1 = Developer("John Doe", "D001", 75000, ["Python", "JavaScript", "Go"])
dev2 = Developer("Jane Smith", "D002", 80000, ["Java", "C++"])

manager.add_team_member(dev1)
manager.add_team_member(dev2)

dev1.add_project("Project Alpha")
dev1.give_raise(5000)

print(manager.get_info())
print(dev1.get_info())
```

## Multi-Level Inheritance

Multi-level inheritance occurs when a class inherits from a child class, creating a chain of inheritance. This creates a hierarchy where each level adds or refines functionality.

```python
class Vehicle:
    """Base vehicle class"""

    def __init__(self, make, model, year):
        """Initialize vehicle"""
        self.make = make
        self.model = model
        self.year = year
        self.odometer = 0

    def drive(self, miles):
        """Drive the vehicle"""
        self.odometer += miles
        return f"Driven {miles} miles. Total: {self.odometer}"

    def get_description(self):
        """Get vehicle description"""
        return f"{self.year} {self.make} {self.model}"

class Car(Vehicle):
    """Car class extending Vehicle"""

    def __init__(self, make, model, year, num_doors):
        """Initialize car"""
        super().__init__(make, model, year)
        self.num_doors = num_doors
        self.fuel_level = 100

    def refuel(self, amount):
        """Refuel the car"""
        self.fuel_level = min(100, self.fuel_level + amount)
        return f"Fuel level: {self.fuel_level}%"

    def drive(self, miles):
        """Override drive to consume fuel"""
        fuel_needed = miles * 0.5
        if self.fuel_level >= fuel_needed:
            self.fuel_level -= fuel_needed
            result = super().drive(miles)
            return f"{result} | Fuel: {self.fuel_level:.1f}%"
        return "Not enough fuel"

    def get_description(self):
        """Extend parent description"""
        base = super().get_description()
        return f"{base} ({self.num_doors} doors)"

class ElectricCar(Car):
    """Electric car extending Car"""

    def __init__(self, make, model, year, num_doors, battery_capacity):
        """Initialize electric car"""
        super().__init__(make, model, year, num_doors)
        self.battery_capacity = battery_capacity
        self.charge_level = 100

    def refuel(self, amount):
        """Override refuel - electric cars don't use fuel"""
        return "Electric cars don't use fuel. Use charge() instead."

    def charge(self, amount):
        """Charge the battery"""
        self.charge_level = min(100, self.charge_level + amount)
        return f"Battery charged to {self.charge_level}%"

    def drive(self, miles):
        """Override drive to use battery"""
        charge_needed = miles * 0.3
        if self.charge_level >= charge_needed:
            self.charge_level -= charge_needed
            self.odometer += miles
            return f"Driven {miles} miles. Battery: {self.charge_level:.1f}% | Odometer: {self.odometer}"
        return "Not enough battery charge"

    def get_description(self):
        """Extend parent description"""
        base = super().get_description()
        return f"{base} | Electric ({self.battery_capacity}kWh battery)"

# Multi-level inheritance in action
tesla = ElectricCar("Tesla", "Model 3", 2024, 4, 75)
print(tesla.get_description())
print(tesla.drive(50))
print(tesla.charge(20))
print(tesla.drive(100))
```

## Multiple Inheritance

Python supports multiple inheritance, where a class can inherit from multiple parent classes. This powerful feature requires careful design to avoid complexity and conflicts.

```python
class Flyer:
    """Mixin for flying ability"""

    def __init__(self):
        """Initialize flying attributes"""
        self.altitude = 0
        self.max_altitude = 10000

    def take_off(self):
        """Take off"""
        self.altitude = 100
        return f"Taking off. Altitude: {self.altitude} feet"

    def fly(self, height):
        """Fly to specific height"""
        if height <= self.max_altitude:
            self.altitude = height
            return f"Flying at {self.altitude} feet"
        return f"Cannot fly above {self.max_altitude} feet"

    def land(self):
        """Land"""
        self.altitude = 0
        return "Landed safely"

class Swimmer:
    """Mixin for swimming ability"""

    def __init__(self):
        """Initialize swimming attributes"""
        self.depth = 0
        self.max_depth = 100

    def dive(self, depth):
        """Dive to specific depth"""
        if depth <= self.max_depth:
            self.depth = depth
            return f"Diving to {self.depth} feet"
        return f"Cannot dive below {self.max_depth} feet"

    def swim(self, distance):
        """Swim distance"""
        return f"Swimming {distance} feet"

    def surface(self):
        """Return to surface"""
        self.depth = 0
        return "Surfaced"

class Bird(Animal, Flyer):
    """Bird class with multiple inheritance"""

    def __init__(self, name, species, wingspan):
        """Initialize bird"""
        Animal.__init__(self, name, species)
        Flyer.__init__(self)
        self.wingspan = wingspan

    def make_sound(self):
        """Override make_sound"""
        return f"{self.name} chirps"

class Duck(Animal, Flyer, Swimmer):
    """Duck class inheriting from multiple classes"""

    def __init__(self, name):
        """Initialize duck"""
        Animal.__init__(self, name, "Duck")
        Flyer.__init__(self)
        Swimmer.__init__(self)
        self.max_altitude = 5000
        self.max_depth = 20

    def make_sound(self):
        """Override make_sound"""
        return f"{self.name} quacks"

    def get_abilities(self):
        """List all abilities"""
        return f"{self.name} can fly and swim"

# Multiple inheritance in action
eagle = Bird("Eddie", "Eagle", 7.5)
print(eagle.make_sound())
print(eagle.take_off())
print(eagle.fly(1000))

duck = Duck("Donald")
print(duck.make_sound())
print(duck.take_off())
print(duck.fly(500))
print(duck.land())
print(duck.dive(10))
print(duck.swim(100))
print(duck.get_abilities())
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Basic Shape Inheritance"
    difficulty: basic
    description: "Create a Shape base class and Circle/Rectangle subclasses that inherit from it. Each shape should calculate its area."
    starter_code: |
      class Shape:
          def __init__(self, name):
              self.name = name

          def describe(self):
              return f"This is a {self.name}"

      class Circle(Shape):
          # TODO: Initialize with name and radius
          # TODO: Add area method (π * r²)
          pass

      class Rectangle(Shape):
          # TODO: Initialize with name, width, and height
          # TODO: Add area method (width * height)
          pass

      circle = Circle("Circle", 5)
      rectangle = Rectangle("Rectangle", 4, 6)
      print(f"{circle.describe()} with area: {circle.area():.2f}")
      print(f"{rectangle.describe()} with area: {rectangle.area()}")
    expected_output: |
      This is a Circle with area: 78.54
      This is a Rectangle with area: 24
    hints:
      - "Use super().__init__(name) to call parent constructor"
      - "For circle area, use 3.14159 * radius * radius"
      - "Store dimensions as instance variables"
    solution: |
      class Shape:
          def __init__(self, name):
              self.name = name

          def describe(self):
              return f"This is a {self.name}"

      class Circle(Shape):
          def __init__(self, name, radius):
              super().__init__(name)
              self.radius = radius

          def area(self):
              return 3.14159 * self.radius * self.radius

      class Rectangle(Shape):
          def __init__(self, name, width, height):
              super().__init__(name)
              self.width = width
              self.height = height

          def area(self):
              return self.width * self.height

      circle = Circle("Circle", 5)
      rectangle = Rectangle("Rectangle", 4, 6)
      print(f"{circle.describe()} with area: {circle.area():.2f}")
      print(f"{rectangle.describe()} with area: {rectangle.area()}")

  - title: "Vehicle Hierarchy"
    difficulty: basic
    description: "Create a Vehicle base class and Motorcycle subclass. Motorcycle should extend Vehicle with additional features."
    starter_code: |
      class Vehicle:
          def __init__(self, brand, model):
              self.brand = brand
              self.model = model
              self.speed = 0

          def accelerate(self, amount):
              self.speed += amount
              return f"Speed: {self.speed} mph"

      class Motorcycle(Vehicle):
          # TODO: Add has_sidecar parameter
          # TODO: Call parent constructor
          # TODO: Add wheelie method
          pass

      bike = Motorcycle("Harley", "Sportster", False)
      print(bike.accelerate(30))
      print(bike.wheelie())
    expected_output: |
      Speed: 30 mph
      Harley Sportster is doing a wheelie!
    hints:
      - "Use super().__init__(brand, model) in child constructor"
      - "Add has_sidecar as an instance variable"
      - "Use self.brand and self.model in wheelie method"
    solution: |
      class Vehicle:
          def __init__(self, brand, model):
              self.brand = brand
              self.model = model
              self.speed = 0

          def accelerate(self, amount):
              self.speed += amount
              return f"Speed: {self.speed} mph"

      class Motorcycle(Vehicle):
          def __init__(self, brand, model, has_sidecar):
              super().__init__(brand, model)
              self.has_sidecar = has_sidecar

          def wheelie(self):
              return f"{self.brand} {self.model} is doing a wheelie!"

      bike = Motorcycle("Harley", "Sportster", False)
      print(bike.accelerate(30))
      print(bike.wheelie())

  - title: "Account Inheritance with Override"
    difficulty: intermediate
    description: "Create a BankAccount base class and SavingsAccount subclass. SavingsAccount should override withdraw to enforce minimum balance."
    starter_code: |
      class BankAccount:
          def __init__(self, owner, balance):
              self.owner = owner
              self.balance = balance

          def deposit(self, amount):
              self.balance += amount
              return f"Deposited ${amount}. Balance: ${self.balance}"

          def withdraw(self, amount):
              if amount <= self.balance:
                  self.balance -= amount
                  return f"Withdrew ${amount}. Balance: ${self.balance}"
              return "Insufficient funds"

      class SavingsAccount(BankAccount):
          # TODO: Add minimum_balance parameter
          # TODO: Override withdraw to check minimum balance
          pass

      savings = SavingsAccount("Alice", 1000, 100)
      print(savings.deposit(500))
      print(savings.withdraw(1300))
      print(savings.withdraw(100))
    expected_output: |
      Deposited $500. Balance: $1500
      Withdrew $1300. Balance: $200
      Cannot withdraw: minimum balance is $100
    hints:
      - "Call super().__init__() for parent initialization"
      - "Check if balance - amount >= minimum_balance"
      - "Only call parent withdraw if check passes"
    solution: |
      class BankAccount:
          def __init__(self, owner, balance):
              self.owner = owner
              self.balance = balance

          def deposit(self, amount):
              self.balance += amount
              return f"Deposited ${amount}. Balance: ${self.balance}"

          def withdraw(self, amount):
              if amount <= self.balance:
                  self.balance -= amount
                  return f"Withdrew ${amount}. Balance: ${self.balance}"
              return "Insufficient funds"

      class SavingsAccount(BankAccount):
          def __init__(self, owner, balance, minimum_balance):
              super().__init__(owner, balance)
              self.minimum_balance = minimum_balance

          def withdraw(self, amount):
              if self.balance - amount >= self.minimum_balance:
                  return super().withdraw(amount)
              return f"Cannot withdraw: minimum balance is ${self.minimum_balance}"

      savings = SavingsAccount("Alice", 1000, 100)
      print(savings.deposit(500))
      print(savings.withdraw(1300))
      print(savings.withdraw(100))

  - title: "Multi-Level Student Hierarchy"
    difficulty: intermediate
    description: "Create Person -> Student -> GraduateStudent hierarchy. Each level should add attributes and extend get_info method."
    starter_code: |
      class Person:
          def __init__(self, name, age):
              self.name = name
              self.age = age

          def get_info(self):
              return f"{self.name}, {self.age} years old"

      class Student(Person):
          # TODO: Add student_id and major
          # TODO: Extend get_info
          pass

      class GraduateStudent(Student):
          # TODO: Add thesis_topic
          # TODO: Extend get_info
          pass

      grad = GraduateStudent("Alice", 25, "S001", "Computer Science", "Machine Learning")
      print(grad.get_info())
    expected_output: |
      Alice, 25 years old | Student ID: S001 | Major: Computer Science | Thesis: Machine Learning
    hints:
      - "Each level should call super().__init__() and super().get_info()"
      - "Add to the parent's info string using +"
      - "Pass all necessary parameters up the chain"
    solution: |
      class Person:
          def __init__(self, name, age):
              self.name = name
              self.age = age

          def get_info(self):
              return f"{self.name}, {self.age} years old"

      class Student(Person):
          def __init__(self, name, age, student_id, major):
              super().__init__(name, age)
              self.student_id = student_id
              self.major = major

          def get_info(self):
              return f"{super().get_info()} | Student ID: {self.student_id} | Major: {self.major}"

      class GraduateStudent(Student):
          def __init__(self, name, age, student_id, major, thesis_topic):
              super().__init__(name, age, student_id, major)
              self.thesis_topic = thesis_topic

          def get_info(self):
              return f"{super().get_info()} | Thesis: {self.thesis_topic}"

      grad = GraduateStudent("Alice", 25, "S001", "Computer Science", "Machine Learning")
      print(grad.get_info())

  - title: "Product Hierarchy with Discounts"
    difficulty: advanced
    description: "Create Product base class with DiscountedProduct and BulkProduct subclasses. Each should calculate price differently."
    starter_code: |
      class Product:
          def __init__(self, name, base_price, quantity):
              self.name = name
              self.base_price = base_price
              self.quantity = quantity

          def get_total_price(self):
              return self.base_price * self.quantity

      class DiscountedProduct(Product):
          # TODO: Add discount_percent
          # TODO: Override get_total_price to apply discount
          pass

      class BulkProduct(Product):
          # TODO: Add bulk_threshold and bulk_discount
          # TODO: Override get_total_price for bulk pricing
          pass

      p1 = DiscountedProduct("Laptop", 1000, 2, 10)
      p2 = BulkProduct("Mouse", 25, 15, 10, 20)
      print(f"{p1.name}: ${p1.get_total_price()}")
      print(f"{p2.name}: ${p2.get_total_price()}")
    expected_output: |
      Laptop: $1800.0
      Mouse: $300.0
    hints:
      - "DiscountedProduct: price * (1 - discount/100)"
      - "BulkProduct: if quantity >= threshold, apply discount"
      - "Call super().__init__() in both subclasses"
    solution: |
      class Product:
          def __init__(self, name, base_price, quantity):
              self.name = name
              self.base_price = base_price
              self.quantity = quantity

          def get_total_price(self):
              return self.base_price * self.quantity

      class DiscountedProduct(Product):
          def __init__(self, name, base_price, quantity, discount_percent):
              super().__init__(name, base_price, quantity)
              self.discount_percent = discount_percent

          def get_total_price(self):
              total = super().get_total_price()
              return total * (1 - self.discount_percent / 100)

      class BulkProduct(Product):
          def __init__(self, name, base_price, quantity, bulk_threshold, bulk_discount):
              super().__init__(name, base_price, quantity)
              self.bulk_threshold = bulk_threshold
              self.bulk_discount = bulk_discount

          def get_total_price(self):
              total = super().get_total_price()
              if self.quantity >= self.bulk_threshold:
                  return total * (1 - self.bulk_discount / 100)
              return total

      p1 = DiscountedProduct("Laptop", 1000, 2, 10)
      p2 = BulkProduct("Mouse", 25, 15, 10, 20)
      print(f"{p1.name}: ${p1.get_total_price()}")
      print(f"{p2.name}: ${p2.get_total_price()}")

  - title: "Game Character Inheritance System"
    difficulty: advanced
    description: "Create Character base class with Warrior and Mage subclasses. Each has unique abilities and should override attack method."
    starter_code: |
      class Character:
          def __init__(self, name, health, base_damage):
              self.name = name
              self.health = health
              self.max_health = health
              self.base_damage = base_damage

          def take_damage(self, amount):
              self.health = max(0, self.health - amount)
              return f"{self.name} took {amount} damage. Health: {self.health}/{self.max_health}"

          def attack(self):
              return f"{self.name} attacks for {self.base_damage} damage"

      class Warrior(Character):
          # TODO: Add armor attribute
          # TODO: Override take_damage to reduce damage by armor
          # TODO: Add special_attack method (2x damage)
          pass

      class Mage(Character):
          # TODO: Add mana attribute
          # TODO: Add cast_spell method (costs mana, does 3x damage)
          pass

      warrior = Warrior("Conan", 150, 20, 5)
      mage = Mage("Gandalf", 100, 15, 50)
      print(warrior.take_damage(30))
      print(mage.cast_spell())
      print(warrior.special_attack())
    expected_output: |
      Conan took 25 damage. Health: 125/150
      Gandalf casts a spell for 45 damage! Mana: 30/50
      Conan performs a special attack for 40 damage!
    hints:
      - "Warrior reduces damage: actual_damage = amount - armor"
      - "Mage spell costs 20 mana and does base_damage * 3"
      - "Use super().take_damage() in Warrior"
    solution: |
      class Character:
          def __init__(self, name, health, base_damage):
              self.name = name
              self.health = health
              self.max_health = health
              self.base_damage = base_damage

          def take_damage(self, amount):
              self.health = max(0, self.health - amount)
              return f"{self.name} took {amount} damage. Health: {self.health}/{self.max_health}"

          def attack(self):
              return f"{self.name} attacks for {self.base_damage} damage"

      class Warrior(Character):
          def __init__(self, name, health, base_damage, armor):
              super().__init__(name, health, base_damage)
              self.armor = armor

          def take_damage(self, amount):
              reduced_damage = max(0, amount - self.armor)
              return super().take_damage(reduced_damage)

          def special_attack(self):
              damage = self.base_damage * 2
              return f"{self.name} performs a special attack for {damage} damage!"

      class Mage(Character):
          def __init__(self, name, health, base_damage, mana):
              super().__init__(name, health, base_damage)
              self.mana = mana
              self.max_mana = mana

          def cast_spell(self):
              if self.mana >= 20:
                  self.mana -= 20
                  damage = self.base_damage * 3
                  return f"{self.name} casts a spell for {damage} damage! Mana: {self.mana}/{self.max_mana}"
              return "Not enough mana!"

      warrior = Warrior("Conan", 150, 20, 5)
      mage = Mage("Gandalf", 100, 15, 50)
      print(warrior.take_damage(30))
      print(mage.cast_spell())
      print(warrior.special_attack())
```
<!-- EXERCISE_END -->
