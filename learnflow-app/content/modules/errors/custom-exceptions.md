# Custom Exceptions

Custom exceptions are user-defined exception classes that allow you to create meaningful, domain-specific error types for your applications. They make your code more expressive, improve error handling precision, and help other developers understand what went wrong and why. Creating custom exceptions is a hallmark of professional Python development.

Well-designed custom exceptions create a clear hierarchy of error conditions, making it easier to catch and handle specific problems while providing rich context about failures. They transform generic error messages into semantic information that guides proper error handling and debugging.

## Creating Basic Custom Exceptions

The simplest custom exception inherits from Python's built-in `Exception` class:

```python
class ValidationError(Exception):
    """Raised when data validation fails."""
    pass

class DatabaseError(Exception):
    """Raised when database operations fail."""
    pass

class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass

def validate_age(age):
    if not isinstance(age, int):
        raise ValidationError("Age must be an integer")
    if age < 0 or age > 150:
        raise ValidationError(f"Age {age} is out of valid range")
    return age

def login(username, password):
    if username != "admin" or password != "secret":
        raise AuthenticationError(f"Invalid credentials for user '{username}'")
    return True

# Test
try:
    validate_age(25)
    validate_age(-5)
except ValidationError as e:
    print(f"Validation failed: {e}")

try:
    login("user", "wrong")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

Benefits of custom exceptions:

| Benefit | Description | Example |
|---------|-------------|---------|
| Clarity | Semantic meaning instead of generic errors | `DatabaseConnectionError` vs `RuntimeError` |
| Specificity | Catch specific errors without false positives | Catch only auth errors, not all ValueErrors |
| Documentation | Self-documenting error conditions | Exception name explains the problem |
| Hierarchy | Group related errors under base classes | All validation errors inherit from `ValidationError` |
| Context | Add custom attributes for debugging | Include failed query in `QueryError` |

## Custom Exceptions with Attributes

Adding attributes to custom exceptions provides rich debugging context:

```python
class ConfigurationError(Exception):
    """Raised when configuration is invalid."""

    def __init__(self, message, config_key=None, config_file=None):
        super().__init__(message)
        self.config_key = config_key
        self.config_file = config_file
        self.timestamp = None

    def __str__(self):
        parts = [super().__str__()]
        if self.config_key:
            parts.append(f"Key: {self.config_key}")
        if self.config_file:
            parts.append(f"File: {self.config_file}")
        return " | ".join(parts)

class NetworkError(Exception):
    """Raised when network operations fail."""

    def __init__(self, message, host, port, retry_count=0):
        super().__init__(message)
        self.host = host
        self.port = port
        self.retry_count = retry_count

    def __repr__(self):
        return (f"{self.__class__.__name__}('{self.args[0]}', "
                f"host='{self.host}', port={self.port}, "
                f"retry_count={self.retry_count})")

# Usage
def load_config(filename, key):
    """Load configuration with detailed error reporting."""
    config = {"host": "localhost"}  # Simulated config

    if key not in config:
        raise ConfigurationError(
            f"Missing required configuration",
            config_key=key,
            config_file=filename
        )
    return config[key]

def connect_to_server(host, port, max_retries=3):
    """Connect to server with retry tracking."""
    for attempt in range(max_retries):
        # Simulate connection failure
        if "invalid" in host:
            continue
        return True

    raise NetworkError(
        "Failed to connect after multiple attempts",
        host=host,
        port=port,
        retry_count=max_retries
    )

# Test
try:
    load_config("app.conf", "missing_key")
except ConfigurationError as e:
    print(f"Config error: {e}")
    print(f"  Key: {e.config_key}")
    print(f"  File: {e.config_file}")

try:
    connect_to_server("invalid_host", 8080)
except NetworkError as e:
    print(f"\nNetwork error: {e}")
    print(f"  Details: {repr(e)}")
```

## Exception Hierarchies

Creating exception hierarchies allows granular error handling:

```python
# Base exception for the application
class AppError(Exception):
    """Base exception for all application errors."""
    pass

# Data-related exceptions
class DataError(AppError):
    """Base exception for data-related errors."""
    pass

class DataValidationError(DataError):
    """Data failed validation."""
    pass

class DataNotFoundError(DataError):
    """Requested data not found."""
    pass

class DataCorruptionError(DataError):
    """Data is corrupted or inconsistent."""
    pass

# Service-related exceptions
class ServiceError(AppError):
    """Base exception for service-related errors."""
    pass

class ServiceUnavailableError(ServiceError):
    """Service is temporarily unavailable."""
    pass

class ServiceTimeoutError(ServiceError):
    """Service operation timed out."""
    pass

# Example usage
class UserService:
    """User service with hierarchical exceptions."""

    def __init__(self):
        self.users = {"1": {"name": "Alice", "email": "alice@example.com"}}

    def get_user(self, user_id):
        if not user_id:
            raise DataValidationError("user_id cannot be empty")

        if user_id not in self.users:
            raise DataNotFoundError(f"User {user_id} not found")

        user = self.users[user_id]
        if not user.get("email"):
            raise DataCorruptionError(f"User {user_id} has no email")

        return user

    def fetch_user_from_api(self, user_id):
        """Simulates external API call."""
        import random

        if random.random() < 0.3:
            raise ServiceTimeoutError("API request timed out")

        if random.random() < 0.3:
            raise ServiceUnavailableError("API is temporarily down")

        return self.get_user(user_id)

# Hierarchical exception handling
service = UserService()

# Catch specific error
try:
    user = service.get_user("")
except DataValidationError as e:
    print(f"Validation error: {e}")

# Catch category of errors
try:
    user = service.get_user("999")
except DataError as e:  # Catches all DataError subclasses
    print(f"Data error occurred: {type(e).__name__} - {e}")

# Catch all application errors
try:
    user = service.fetch_user_from_api("1")
except AppError as e:  # Catches all AppError subclasses
    print(f"Application error: {type(e).__name__} - {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

Exception hierarchy benefits:

```
AppError (catch all app errors)
├── DataError (catch all data errors)
│   ├── DataValidationError (catch validation only)
│   ├── DataNotFoundError (catch not found only)
│   └── DataCorruptionError (catch corruption only)
└── ServiceError (catch all service errors)
    ├── ServiceUnavailableError (catch unavailable only)
    └── ServiceTimeoutError (catch timeout only)
```

## Advanced Custom Exception Patterns

Here's a comprehensive example showing professional-grade custom exceptions:

```python
from datetime import datetime
from typing import Optional, Dict, Any

class PaymentError(Exception):
    """Base exception for payment processing errors."""

    def __init__(
        self,
        message: str,
        transaction_id: Optional[str] = None,
        amount: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.transaction_id = transaction_id
        self.amount = amount
        self.metadata = metadata or {}
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for logging/API responses."""
        return {
            "error_type": self.__class__.__name__,
            "message": str(self),
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }

    def __str__(self):
        parts = [super().__str__()]
        if self.transaction_id:
            parts.append(f"Transaction: {self.transaction_id}")
        if self.amount is not None:
            parts.append(f"Amount: ${self.amount:.2f}")
        return " | ".join(parts)

class InsufficientFundsError(PaymentError):
    """Raised when account has insufficient funds."""

    def __init__(self, message, balance, required, **kwargs):
        super().__init__(message, **kwargs)
        self.balance = balance
        self.required = required
        self.shortfall = required - balance

    def __str__(self):
        base = super().__str__()
        return f"{base} | Balance: ${self.balance:.2f} | Required: ${self.required:.2f}"

class PaymentDeclinedError(PaymentError):
    """Raised when payment is declined by processor."""

    def __init__(self, message, decline_code, **kwargs):
        super().__init__(message, **kwargs)
        self.decline_code = decline_code

class PaymentTimeoutError(PaymentError):
    """Raised when payment processing times out."""

    def __init__(self, message, timeout_seconds, **kwargs):
        super().__init__(message, **kwargs)
        self.timeout_seconds = timeout_seconds

class PaymentProcessor:
    """Payment processor with custom exceptions."""

    def __init__(self):
        self.accounts = {
            "ACC001": {"balance": 1000.0, "status": "active"},
            "ACC002": {"balance": 50.0, "status": "active"},
            "ACC003": {"balance": 500.0, "status": "frozen"}
        }

    def process_payment(self, account_id, amount, description=""):
        """Process payment with detailed error handling."""
        transaction_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Validate account exists
        if account_id not in self.accounts:
            raise PaymentError(
                f"Account not found",
                transaction_id=transaction_id,
                amount=amount,
                metadata={"account_id": account_id}
            )

        account = self.accounts[account_id]

        # Check account status
        if account["status"] == "frozen":
            raise PaymentDeclinedError(
                "Account is frozen",
                decline_code="ACCOUNT_FROZEN",
                transaction_id=transaction_id,
                amount=amount,
                metadata={"account_id": account_id, "status": account["status"]}
            )

        # Check sufficient funds
        if account["balance"] < amount:
            raise InsufficientFundsError(
                "Insufficient funds for transaction",
                balance=account["balance"],
                required=amount,
                transaction_id=transaction_id,
                amount=amount,
                metadata={"account_id": account_id, "description": description}
            )

        # Simulate timeout
        if amount > 5000:
            raise PaymentTimeoutError(
                "Payment processing timed out",
                timeout_seconds=30,
                transaction_id=transaction_id,
                amount=amount
            )

        # Process payment
        account["balance"] -= amount
        return {
            "success": True,
            "transaction_id": transaction_id,
            "new_balance": account["balance"]
        }

# Comprehensive error handling
processor = PaymentProcessor()

def make_payment(account_id, amount):
    """Make payment with comprehensive error handling."""
    try:
        result = processor.process_payment(account_id, amount)
        print(f"Payment successful: {result}")
        return True

    except InsufficientFundsError as e:
        print(f"\nInsufficient funds:")
        print(f"  {e}")
        print(f"  Shortfall: ${e.shortfall:.2f}")
        print(f"  Error details: {e.to_dict()}")
        return False

    except PaymentDeclinedError as e:
        print(f"\nPayment declined:")
        print(f"  {e}")
        print(f"  Decline code: {e.decline_code}")
        return False

    except PaymentTimeoutError as e:
        print(f"\nPayment timeout:")
        print(f"  {e}")
        print(f"  Timeout: {e.timeout_seconds}s")
        return False

    except PaymentError as e:
        print(f"\nPayment error:")
        print(f"  {e}")
        print(f"  Error details: {e.to_dict()}")
        return False

# Test different scenarios
print("=== Test 1: Successful payment ===")
make_payment("ACC001", 100)

print("\n=== Test 2: Insufficient funds ===")
make_payment("ACC002", 100)

print("\n=== Test 3: Account frozen ===")
make_payment("ACC003", 100)

print("\n=== Test 4: Account not found ===")
make_payment("ACC999", 100)
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Create Basic Custom Exception"
    difficulty: basic
    description: "Define a custom InvalidEmailError exception and use it to validate email addresses."
    starter_code: |
      # Your code here
      class InvalidEmailError(Exception):
          pass

      def validate_email(email):
          # Your code here
          pass

      # Test
      print(validate_email("user@example.com"))
      print(validate_email("invalid-email"))

    expected_output: |
      user@example.com
      Error: Email must contain @ symbol

    hints:
      - "Create InvalidEmailError inheriting from Exception"
      - "Check if email contains '@' and '.'"
      - "Raise InvalidEmailError with descriptive message"
    solution: |
      class InvalidEmailError(Exception):
          pass

      def validate_email(email):
          if "@" not in email:
              raise InvalidEmailError("Email must contain @ symbol")
          if "." not in email:
              raise InvalidEmailError("Email must contain a domain")
          return email

      # Test
      print(validate_email("user@example.com"))
      try:
          print(validate_email("invalid-email"))
      except InvalidEmailError as e:
          print(f"Error: {e}")

  - title: "Exception with Attributes"
    difficulty: basic
    description: "Create a custom exception that stores the invalid value and the valid range."
    starter_code: |
      class RangeError(Exception):
          # Your code here
          pass

      def check_range(value, min_val, max_val):
          # Your code here
          pass

      # Test
      try:
          check_range(15, 0, 100)
          check_range(150, 0, 100)
      except RangeError as e:
          print(f"Error: {e}")
          print(f"Value: {e.value}, Range: {e.min_val}-{e.max_val}")

    expected_output: |
      Error: Value 150 is out of range [0, 100]
      Value: 150, Range: 0-100

    hints:
      - "Add __init__ method to store value, min_val, max_val"
      - "Override __str__ to create custom message"
      - "Raise exception when value is out of range"
    solution: |
      class RangeError(Exception):
          def __init__(self, value, min_val, max_val):
              self.value = value
              self.min_val = min_val
              self.max_val = max_val
              super().__init__(f"Value {value} is out of range [{min_val}, {max_val}]")

      def check_range(value, min_val, max_val):
          if value < min_val or value > max_val:
              raise RangeError(value, min_val, max_val)
          return value

      # Test
      try:
          check_range(15, 0, 100)
          check_range(150, 0, 100)
      except RangeError as e:
          print(f"Error: {e}")
          print(f"Value: {e.value}, Range: {e.min_val}-{e.max_val}")

  - title: "Exception Hierarchy"
    difficulty: intermediate
    description: "Create an exception hierarchy for a file processing system with base and specific exceptions."
    starter_code: |
      # Your code here
      class FileProcessingError(Exception):
          pass

      class FileReadError(FileProcessingError):
          pass

      class FileParseError(FileProcessingError):
          pass

      def process_file(filename, content):
          # Your code here
          pass

      # Test
      try:
          process_file("test.txt", "valid content")
      except FileProcessingError as e:
          print(f"Caught: {type(e).__name__} - {e}")

      try:
          process_file("", "content")
      except FileProcessingError as e:
          print(f"Caught: {type(e).__name__} - {e}")

    expected_output: |
      Caught: FileParseError - Content is too short
      Caught: FileReadError - Filename cannot be empty

    hints:
      - "Create base FileProcessingError class"
      - "Create FileReadError and FileParseError subclasses"
      - "Raise specific exception based on error type"
      - "Catch using base class to handle all file errors"
    solution: |
      class FileProcessingError(Exception):
          pass

      class FileReadError(FileProcessingError):
          pass

      class FileParseError(FileProcessingError):
          pass

      def process_file(filename, content):
          if not filename:
              raise FileReadError("Filename cannot be empty")

          if len(content) < 10:
              raise FileParseError("Content is too short")

          return f"Processed {filename}"

      # Test
      try:
          process_file("test.txt", "valid content")
      except FileProcessingError as e:
          print(f"Caught: {type(e).__name__} - {e}")

      try:
          process_file("", "content")
      except FileProcessingError as e:
          print(f"Caught: {type(e).__name__} - {e}")

  - title: "Exception with Metadata"
    difficulty: intermediate
    description: "Create a custom exception that includes metadata dictionary and a method to convert to JSON-like dict."
    starter_code: |
      class APIError(Exception):
          def __init__(self, message, status_code, endpoint):
              # Your code here
              pass

          def to_dict(self):
              # Your code here
              pass

      def call_api(endpoint, data):
          # Your code here
          pass

      # Test
      try:
          call_api("/users", {"name": ""})
      except APIError as e:
          print(e.to_dict())

    expected_output: |
      {'message': 'Invalid request data', 'status_code': 400, 'endpoint': '/users'}

    hints:
      - "Store message, status_code, and endpoint in __init__"
      - "Create to_dict method returning dictionary"
      - "Raise APIError with appropriate status code"
    solution: |
      class APIError(Exception):
          def __init__(self, message, status_code, endpoint):
              super().__init__(message)
              self.status_code = status_code
              self.endpoint = endpoint

          def to_dict(self):
              return {
                  "message": str(self),
                  "status_code": self.status_code,
                  "endpoint": self.endpoint
              }

      def call_api(endpoint, data):
          if not data.get("name"):
              raise APIError("Invalid request data", 400, endpoint)
          return {"success": True}

      # Test
      try:
          call_api("/users", {"name": ""})
      except APIError as e:
          print(e.to_dict())

  - title: "Shopping Cart Exception System"
    difficulty: advanced
    description: "Build a comprehensive exception system for a shopping cart with multiple specific error types."
    starter_code: |
      class CartError(Exception):
          pass

      class ItemNotFoundError(CartError):
          pass

      class InsufficientStockError(CartError):
          pass

      class InvalidQuantityError(CartError):
          pass

      class ShoppingCart:
          def __init__(self):
              self.items = {}
              self.inventory = {
                  "apple": {"price": 1.0, "stock": 10},
                  "banana": {"price": 0.5, "stock": 5}
              }

          def add_item(self, item_name, quantity):
              # Your code here
              pass

          def get_total(self):
              # Your code here
              pass

      # Test
      cart = ShoppingCart()
      try:
          cart.add_item("apple", 3)
          cart.add_item("orange", 2)
      except CartError as e:
          print(f"{type(e).__name__}: {e}")

    expected_output: |
      ItemNotFoundError: Item 'orange' not found in inventory

    hints:
      - "Check if item exists in inventory"
      - "Check if quantity is valid (> 0)"
      - "Check if sufficient stock available"
      - "Raise appropriate exception for each case"
    solution: |
      class CartError(Exception):
          pass

      class ItemNotFoundError(CartError):
          pass

      class InsufficientStockError(CartError):
          pass

      class InvalidQuantityError(CartError):
          pass

      class ShoppingCart:
          def __init__(self):
              self.items = {}
              self.inventory = {
                  "apple": {"price": 1.0, "stock": 10},
                  "banana": {"price": 0.5, "stock": 5}
              }

          def add_item(self, item_name, quantity):
              if quantity <= 0:
                  raise InvalidQuantityError(f"Quantity must be positive, got {quantity}")

              if item_name not in self.inventory:
                  raise ItemNotFoundError(f"Item '{item_name}' not found in inventory")

              if self.inventory[item_name]["stock"] < quantity:
                  raise InsufficientStockError(
                      f"Insufficient stock for '{item_name}'. "
                      f"Available: {self.inventory[item_name]['stock']}, Requested: {quantity}"
                  )

              self.items[item_name] = self.items.get(item_name, 0) + quantity
              self.inventory[item_name]["stock"] -= quantity

          def get_total(self):
              total = 0
              for item, quantity in self.items.items():
                  total += self.inventory[item]["price"] * quantity
              return total

      # Test
      cart = ShoppingCart()
      try:
          cart.add_item("apple", 3)
          cart.add_item("orange", 2)
      except CartError as e:
          print(f"{type(e).__name__}: {e}")

  - title: "Database Exception System"
    difficulty: advanced
    description: "Create a complete database exception hierarchy with connection, query, and transaction errors."
    starter_code: |
      from datetime import datetime

      class DatabaseError(Exception):
          def __init__(self, message, query=None, timestamp=None):
              # Your code here
              pass

      class ConnectionError(DatabaseError):
          pass

      class QueryError(DatabaseError):
          pass

      class TransactionError(DatabaseError):
          pass

      class Database:
          def __init__(self):
              self.connected = False
              self.in_transaction = False

          def connect(self, connection_string):
              # Your code here
              pass

          def execute(self, query):
              # Your code here
              pass

          def begin_transaction(self):
              # Your code here
              pass

          def commit(self):
              # Your code here
              pass

      # Test
      db = Database()
      try:
          db.execute("SELECT * FROM users")
      except DatabaseError as e:
          print(f"{type(e).__name__}: {e}")

    expected_output: |
      ConnectionError: Not connected to database

    hints:
      - "Create base DatabaseError with query and timestamp attributes"
      - "Create specific error classes for different database operations"
      - "Check connection state before executing queries"
      - "Track transaction state"
    solution: |
      from datetime import datetime

      class DatabaseError(Exception):
          def __init__(self, message, query=None, timestamp=None):
              super().__init__(message)
              self.query = query
              self.timestamp = timestamp or datetime.now()

      class ConnectionError(DatabaseError):
          pass

      class QueryError(DatabaseError):
          pass

      class TransactionError(DatabaseError):
          pass

      class Database:
          def __init__(self):
              self.connected = False
              self.in_transaction = False

          def connect(self, connection_string):
              if not connection_string:
                  raise ConnectionError("Connection string cannot be empty")
              self.connected = True

          def execute(self, query):
              if not self.connected:
                  raise ConnectionError("Not connected to database", query=query)

              if "ERROR" in query:
                  raise QueryError("Syntax error in query", query=query)

              return f"Executed: {query}"

          def begin_transaction(self):
              if not self.connected:
                  raise ConnectionError("Not connected to database")
              if self.in_transaction:
                  raise TransactionError("Transaction already in progress")
              self.in_transaction = True

          def commit(self):
              if not self.in_transaction:
                  raise TransactionError("No active transaction to commit")
              self.in_transaction = False

      # Test
      db = Database()
      try:
          db.execute("SELECT * FROM users")
      except DatabaseError as e:
          print(f"{type(e).__name__}: {e}")
```
<!-- EXERCISE_END -->
