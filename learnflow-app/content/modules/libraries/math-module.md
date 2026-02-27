# Math Module

The `math` module is Python's built-in library for mathematical operations, providing access to mathematical functions defined by the C standard. It offers efficient implementations of common mathematical operations, from basic arithmetic to advanced trigonometry and logarithms, making it essential for scientific computing and numerical analysis.

## Basic Mathematical Functions

The math module provides fundamental operations that extend beyond Python's built-in arithmetic operators, including rounding functions, absolute values, and factorial calculations.

```python
import math

# Rounding and absolute values
print(math.ceil(4.3))    # 5 (round up)
print(math.floor(4.7))   # 4 (round down)
print(math.trunc(4.7))   # 4 (truncate decimal)
print(math.fabs(-5.5))   # 5.5 (absolute value as float)

# Factorial and combinations
print(math.factorial(5))  # 120 (5! = 5*4*3*2*1)
print(math.comb(5, 2))    # 10 (combinations: 5 choose 2)
print(math.perm(5, 2))    # 20 (permutations: 5P2)

# GCD and LCM
print(math.gcd(48, 18))   # 6 (greatest common divisor)
print(math.lcm(12, 18))   # 36 (least common multiple)

# Powers and roots
print(math.pow(2, 3))     # 8.0 (2^3)
print(math.sqrt(16))      # 4.0 (square root)
print(math.cbrt(27))      # 3.0 (cube root)
print(pow(8, 1/3))        # 2.0 (nth root using built-in pow)

# Exponential and logarithms
print(math.exp(2))        # 7.389... (e^2)
print(math.log(100, 10))  # 2.0 (log base 10)
print(math.log10(100))    # 2.0 (log base 10)
print(math.log2(8))       # 3.0 (log base 2)
print(math.ln(math.e))    # 1.0 (natural log)
```

| Function | Description | Example |
|----------|-------------|---------|
| `ceil(x)` | Round up to nearest integer | `ceil(4.1)` → `5` |
| `floor(x)` | Round down to nearest integer | `floor(4.9)` → `4` |
| `factorial(n)` | n! (factorial) | `factorial(5)` → `120` |
| `gcd(a, b)` | Greatest common divisor | `gcd(48, 18)` → `6` |
| `sqrt(x)` | Square root | `sqrt(16)` → `4.0` |
| `log(x, base)` | Logarithm | `log(100, 10)` → `2.0` |

## Trigonometric Functions

The math module includes comprehensive support for trigonometric operations, working with both radians and degrees, and providing inverse trigonometric functions.

```python
import math

# Constants
print(f"Pi: {math.pi}")        # 3.141592653589793
print(f"Tau: {math.tau}")      # 6.283185307179586 (2*pi)
print(f"e: {math.e}")          # 2.718281828459045

# Angle conversion
degrees = 180
radians = math.radians(degrees)
print(f"{degrees}° = {radians} radians")  # 3.141592653589793

angle_rad = math.pi / 4  # 45 degrees
angle_deg = math.degrees(angle_rad)
print(f"{angle_rad} radians = {angle_deg}°")  # 45.0

# Basic trigonometric functions (input in radians)
angle = math.pi / 6  # 30 degrees
print(f"sin(30°) = {math.sin(angle):.4f}")  # 0.5000
print(f"cos(30°) = {math.cos(angle):.4f}")  # 0.8660
print(f"tan(30°) = {math.tan(angle):.4f}")  # 0.5774

# Inverse trigonometric functions (output in radians)
print(f"arcsin(0.5) = {math.degrees(math.asin(0.5))}°")  # 30.0
print(f"arccos(0.5) = {math.degrees(math.acos(0.5))}°")  # 60.0
print(f"arctan(1) = {math.degrees(math.atan(1))}°")      # 45.0

# atan2 for better angle calculation (handles quadrants)
x, y = 1, 1
angle = math.atan2(y, x)
print(f"Angle of vector ({x}, {y}): {math.degrees(angle)}°")  # 45.0

# Hyperbolic functions
print(f"sinh(1) = {math.sinh(1):.4f}")  # 1.1752
print(f"cosh(1) = {math.cosh(1):.4f}")  # 1.5431
print(f"tanh(1) = {math.tanh(1):.4f}")  # 0.7616

# Practical example: Calculate distance using Law of Cosines
def distance_law_of_cosines(a, b, angle_degrees):
    """Calculate third side of triangle given two sides and included angle."""
    angle_rad = math.radians(angle_degrees)
    c_squared = a**2 + b**2 - 2*a*b*math.cos(angle_rad)
    return math.sqrt(c_squared)

result = distance_law_of_cosines(5, 7, 60)
print(f"Third side: {result:.2f}")  # 6.24
```

## Advanced Mathematical Operations

The math module provides sophisticated functions for handling special cases, checking numeric properties, and performing precise calculations.

```python
import math

# Checking numeric properties
print(math.isfinite(100))      # True
print(math.isfinite(math.inf)) # False
print(math.isinf(math.inf))    # True
print(math.isnan(float('nan')))# True

# Special values
print(math.inf)     # inf (positive infinity)
print(-math.inf)    # -inf (negative infinity)
print(math.nan)     # nan (not a number)

# Precise sum (more accurate than built-in sum)
numbers = [0.1] * 10
print(sum(numbers))           # 0.9999999999999999
print(math.fsum(numbers))     # 1.0 (more precise)

# Product of all elements
from math import prod
values = [2, 3, 4, 5]
print(prod(values))  # 120

# Euclidean distance and norm
def euclidean_distance(point1, point2):
    """Calculate distance between two points."""
    differences = [(a - b) for a, b in zip(point1, point2)]
    return math.sqrt(sum(d**2 for d in differences))

p1 = (1, 2, 3)
p2 = (4, 6, 8)
print(f"Distance: {euclidean_distance(p1, p2):.2f}")  # 7.07

# Using math.hypot for distance (more efficient)
print(f"Hypot: {math.hypot(3, 4):.2f}")  # 5.00 (2D distance)
print(f"Hypot 3D: {math.hypot(3, 4, 5):.2f}")  # 7.07

# Error function (important in statistics)
print(f"erf(1) = {math.erf(1):.4f}")    # 0.8427
print(f"erfc(1) = {math.erfc(1):.4f}")  # 0.1573

# Gamma function
print(f"gamma(5) = {math.gamma(5)}")  # 24.0 (same as 4!)
print(f"lgamma(100) = {math.lgamma(100):.2f}")  # 359.13 (log of gamma)

# Copy sign
print(math.copysign(5, -1))   # -5.0
print(math.copysign(-5, 1))   # 5.0

# Remainder operations
print(math.remainder(23, 5))  # -2.0 (IEEE remainder)
print(23 % 5)                 # 3 (standard modulo)
```

| Function | Purpose | Example |
|----------|---------|---------|
| `isfinite(x)` | Check if finite | `isfinite(100)` → `True` |
| `fsum(iterable)` | Precise floating sum | `fsum([0.1]*10)` → `1.0` |
| `prod(iterable)` | Product of elements | `prod([2,3,4])` → `24` |
| `hypot(*args)` | Euclidean norm | `hypot(3,4)` → `5.0` |
| `gamma(x)` | Gamma function | `gamma(5)` → `24.0` |

## Real-World Applications

Mathematical functions are essential for solving practical problems in physics, engineering, finance, and data science.

```python
import math

# 1. Compound Interest Calculator
def compound_interest(principal, rate, time, compounds_per_year):
    """Calculate compound interest."""
    amount = principal * math.pow(1 + rate/compounds_per_year, compounds_per_year * time)
    interest = amount - principal
    return amount, interest

investment = 10000
annual_rate = 0.05  # 5%
years = 10
compounds = 12  # monthly

final_amount, earned = compound_interest(investment, annual_rate, years, compounds)
print(f"Initial: ${investment:,.2f}")
print(f"Final: ${final_amount:,.2f}")
print(f"Interest earned: ${earned:,.2f}")

# 2. Projectile Motion Calculator
def projectile_range(velocity, angle_degrees, height=0):
    """Calculate range of projectile."""
    g = 9.81  # gravity
    angle_rad = math.radians(angle_degrees)

    # Range formula
    range_flat = (velocity**2 * math.sin(2 * angle_rad)) / g

    # Adjust for initial height
    time_to_ground = (velocity * math.sin(angle_rad) +
                      math.sqrt((velocity * math.sin(angle_rad))**2 + 2*g*height)) / g
    range_total = velocity * math.cos(angle_rad) * time_to_ground

    return range_total

v = 20  # m/s
angle = 45  # degrees
h = 0   # meters
distance = projectile_range(v, angle, h)
print(f"\nProjectile range: {distance:.2f} meters")

# 3. Signal Processing - Decibel Conversion
def power_to_db(power, reference=1.0):
    """Convert power to decibels."""
    return 10 * math.log10(power / reference)

def db_to_power(db, reference=1.0):
    """Convert decibels to power."""
    return reference * math.pow(10, db / 10)

signal_power = 100
db = power_to_db(signal_power)
print(f"\nPower {signal_power}W = {db:.2f} dB")

# 4. Haversine Distance (Great Circle Distance)
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points on Earth (in km)."""
    R = 6371  # Earth's radius in km

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (math.sin(delta_lat/2)**2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

# Distance from New York to London
ny_lat, ny_lon = 40.7128, -74.0060
london_lat, london_lon = 51.5074, -0.1278
distance_km = haversine_distance(ny_lat, ny_lon, london_lat, london_lon)
print(f"\nNY to London: {distance_km:.2f} km")

# 5. Standard Deviation and Normal Distribution
def standard_deviation(data):
    """Calculate standard deviation."""
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean)**2 for x in data) / n
    return math.sqrt(variance)

def normal_distribution(x, mean, std_dev):
    """Calculate probability density for normal distribution."""
    coefficient = 1 / (std_dev * math.sqrt(2 * math.pi))
    exponent = -0.5 * ((x - mean) / std_dev)**2
    return coefficient * math.exp(exponent)

data = [2, 4, 4, 4, 5, 5, 7, 9]
std = standard_deviation(data)
mean = sum(data) / len(data)
print(f"\nMean: {mean}, Std Dev: {std:.2f}")
print(f"P(x=5): {normal_distribution(5, mean, std):.4f}")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Circle Calculations"
    difficulty: basic
    description: "Create functions to calculate the area and circumference of a circle given its radius using math.pi."
    starter_code: |
      import math

      def circle_area(radius):
          # Calculate area: pi * r^2


      def circle_circumference(radius):
          # Calculate circumference: 2 * pi * r


      r = 5
      print(f"Radius: {r}")
      print(f"Area: {circle_area(r):.2f}")
      print(f"Circumference: {circle_circumference(r):.2f}")
    expected_output: |
      Radius: 5
      Area: 78.54
      Circumference: 31.42
    hints:
      - "Use math.pi for π"
      - "Area = π × r²"
      - "Circumference = 2 × π × r"
    solution: |
      import math

      def circle_area(radius):
          # Calculate area: pi * r^2
          return math.pi * radius ** 2

      def circle_circumference(radius):
          # Calculate circumference: 2 * pi * r
          return 2 * math.pi * radius

      r = 5
      print(f"Radius: {r}")
      print(f"Area: {circle_area(r):.2f}")
      print(f"Circumference: {circle_circumference(r):.2f}")

  - title: "Angle Conversions"
    difficulty: basic
    description: "Convert angles between degrees and radians, and calculate sine and cosine values."
    starter_code: |
      import math

      angle_degrees = 60

      # Convert to radians
      angle_radians =

      # Calculate sin and cos
      sin_value =
      cos_value =

      print(f"{angle_degrees}° = {angle_radians:.4f} radians")
      print(f"sin({angle_degrees}°) = {sin_value:.4f}")
      print(f"cos({angle_degrees}°) = {cos_value:.4f}")
    expected_output: |
      60° = 1.0472 radians
      sin(60°) = 0.8660
      cos(60°) = 0.5000
    hints:
      - "Use math.radians() to convert degrees to radians"
      - "Use math.sin() and math.cos() with radian values"
    solution: |
      import math

      angle_degrees = 60

      # Convert to radians
      angle_radians = math.radians(angle_degrees)

      # Calculate sin and cos
      sin_value = math.sin(angle_radians)
      cos_value = math.cos(angle_radians)

      print(f"{angle_degrees}° = {angle_radians:.4f} radians")
      print(f"sin({angle_degrees}°) = {sin_value:.4f}")
      print(f"cos({angle_degrees}°) = {cos_value:.4f}")

  - title: "Quadratic Formula Solver"
    difficulty: intermediate
    description: "Implement a quadratic equation solver that handles real and complex roots using the discriminant."
    starter_code: |
      import math

      def solve_quadratic(a, b, c):
          """Solve ax^2 + bx + c = 0"""
          # Calculate discriminant
          discriminant =

          if discriminant > 0:
              # Two real roots
              root1 =
              root2 =
              return (root1, root2)
          elif discriminant == 0:
              # One real root
              root =
              return (root,)
          else:
              # Complex roots
              real_part =
              imag_part =
              return (f"{real_part}+{imag_part}i", f"{real_part}-{imag_part}i")

      # Test: x^2 - 5x + 6 = 0 (roots: 2 and 3)
      roots = solve_quadratic(1, -5, 6)
      print(f"Roots: {roots}")
    expected_output: |
      Roots: (3.0, 2.0)
    hints:
      - "Discriminant = b² - 4ac"
      - "Roots = (-b ± √discriminant) / (2a)"
      - "For complex: real = -b/(2a), imag = √|discriminant|/(2a)"
    solution: |
      import math

      def solve_quadratic(a, b, c):
          """Solve ax^2 + bx + c = 0"""
          # Calculate discriminant
          discriminant = b**2 - 4*a*c

          if discriminant > 0:
              # Two real roots
              root1 = (-b + math.sqrt(discriminant)) / (2*a)
              root2 = (-b - math.sqrt(discriminant)) / (2*a)
              return (root1, root2)
          elif discriminant == 0:
              # One real root
              root = -b / (2*a)
              return (root,)
          else:
              # Complex roots
              real_part = -b / (2*a)
              imag_part = math.sqrt(abs(discriminant)) / (2*a)
              return (f"{real_part}+{imag_part}i", f"{real_part}-{imag_part}i")

      # Test: x^2 - 5x + 6 = 0 (roots: 2 and 3)
      roots = solve_quadratic(1, -5, 6)
      print(f"Roots: {roots}")

  - title: "Distance Between Points"
    difficulty: intermediate
    description: "Calculate the Euclidean distance between two 3D points using math.sqrt and math.hypot, comparing both methods."
    starter_code: |
      import math

      def distance_manual(p1, p2):
          """Calculate distance using sqrt."""
          # Calculate sum of squared differences


      def distance_hypot(p1, p2):
          """Calculate distance using hypot."""
          # Use math.hypot with the differences


      point1 = (1, 2, 3)
      point2 = (4, 6, 8)

      dist1 = distance_manual(point1, point2)
      dist2 = distance_hypot(point1, point2)

      print(f"Manual method: {dist1:.2f}")
      print(f"Hypot method: {dist2:.2f}")
    expected_output: |
      Manual method: 7.07
      Hypot method: 7.07
    hints:
      - "Manual: sqrt((x2-x1)² + (y2-y1)² + (z2-z1)²)"
      - "Hypot: math.hypot(x2-x1, y2-y1, z2-z1)"
    solution: |
      import math

      def distance_manual(p1, p2):
          """Calculate distance using sqrt."""
          # Calculate sum of squared differences
          sum_squares = sum((a - b)**2 for a, b in zip(p1, p2))
          return math.sqrt(sum_squares)

      def distance_hypot(p1, p2):
          """Calculate distance using hypot."""
          # Use math.hypot with the differences
          differences = [a - b for a, b in zip(p1, p2)]
          return math.hypot(*differences)

      point1 = (1, 2, 3)
      point2 = (4, 6, 8)

      dist1 = distance_manual(point1, point2)
      dist2 = distance_hypot(point1, point2)

      print(f"Manual method: {dist1:.2f}")
      print(f"Hypot method: {dist2:.2f}")

  - title: "Logarithmic Growth Model"
    difficulty: advanced
    description: "Model population growth using logarithms. Given initial population, growth rate, and time, calculate final population and time to double."
    starter_code: |
      import math

      def population_growth(initial, rate, time):
          """Calculate population using exponential growth: P = P0 * e^(rt)"""


      def doubling_time(rate):
          """Calculate time for population to double: t = ln(2) / r"""


      def time_to_reach(initial, target, rate):
          """Calculate time to reach target population: t = ln(target/initial) / r"""


      P0 = 1000
      r = 0.05  # 5% growth rate
      t = 10    # years

      final_pop = population_growth(P0, r, t)
      double_time = doubling_time(r)
      time_to_5000 = time_to_reach(P0, 5000, r)

      print(f"Initial population: {P0}")
      print(f"After {t} years: {final_pop:.0f}")
      print(f"Doubling time: {double_time:.2f} years")
      print(f"Time to reach 5000: {time_to_5000:.2f} years")
    expected_output: |
      Initial population: 1000
      After 10 years: 1649
      Doubling time: 13.86 years
      Time to reach 5000: 32.19 years
    hints:
      - "Use math.exp() for e^x"
      - "Use math.log() for natural logarithm"
      - "Doubling: ln(2) / rate"
      - "Time to target: ln(target/initial) / rate"
    solution: |
      import math

      def population_growth(initial, rate, time):
          """Calculate population using exponential growth: P = P0 * e^(rt)"""
          return initial * math.exp(rate * time)

      def doubling_time(rate):
          """Calculate time for population to double: t = ln(2) / r"""
          return math.log(2) / rate

      def time_to_reach(initial, target, rate):
          """Calculate time to reach target population: t = ln(target/initial) / r"""
          return math.log(target / initial) / rate

      P0 = 1000
      r = 0.05  # 5% growth rate
      t = 10    # years

      final_pop = population_growth(P0, r, t)
      double_time = doubling_time(r)
      time_to_5000 = time_to_reach(P0, 5000, r)

      print(f"Initial population: {P0}")
      print(f"After {t} years: {final_pop:.0f}")
      print(f"Doubling time: {double_time:.2f} years")
      print(f"Time to reach 5000: {time_to_5000:.2f} years")

  - title: "Trigonometric Triangle Solver"
    difficulty: advanced
    description: "Implement a triangle solver using the Law of Cosines and Law of Sines to find all sides and angles given partial information."
    starter_code: |
      import math

      def solve_triangle_sss(a, b, c):
          """Given three sides, find all angles using Law of Cosines."""
          # Angle A opposite to side a
          cos_A =
          angle_A =

          # Angle B opposite to side b
          cos_B =
          angle_B =

          # Angle C
          angle_C =

          return {
              'A': math.degrees(angle_A),
              'B': math.degrees(angle_B),
              'C': math.degrees(angle_C)
          }

      def solve_triangle_sas(a, b, angle_C_deg):
          """Given two sides and included angle, find third side and other angles."""
          angle_C = math.radians(angle_C_deg)

          # Find side c using Law of Cosines
          c =

          # Find other angles
          angles = solve_triangle_sss(a, b, c)

          return {
              'c': c,
              'angles': angles
          }

      # Test with sides 3, 4, 5 (right triangle)
      result = solve_triangle_sss(3, 4, 5)
      print(f"Angles: A={result['A']:.1f}°, B={result['B']:.1f}°, C={result['C']:.1f}°")

      # Test SAS
      result2 = solve_triangle_sas(5, 7, 60)
      print(f"Third side: {result2['c']:.2f}")
      print(f"Angles: A={result2['angles']['A']:.1f}°, B={result2['angles']['B']:.1f}°")
    expected_output: |
      Angles: A=36.9°, B=53.1°, C=90.0°
      Third side: 6.24
      Angles: A=46.6°, B=73.4°
    hints:
      - "Law of Cosines: c² = a² + b² - 2ab·cos(C)"
      - "To find angle: cos(A) = (b² + c² - a²) / (2bc)"
      - "Use math.acos() to get angle from cosine"
      - "Sum of angles in triangle = 180°"
    solution: |
      import math

      def solve_triangle_sss(a, b, c):
          """Given three sides, find all angles using Law of Cosines."""
          # Angle A opposite to side a
          cos_A = (b**2 + c**2 - a**2) / (2*b*c)
          angle_A = math.acos(cos_A)

          # Angle B opposite to side b
          cos_B = (a**2 + c**2 - b**2) / (2*a*c)
          angle_B = math.acos(cos_B)

          # Angle C
          angle_C = math.pi - angle_A - angle_B

          return {
              'A': math.degrees(angle_A),
              'B': math.degrees(angle_B),
              'C': math.degrees(angle_C)
          }

      def solve_triangle_sas(a, b, angle_C_deg):
          """Given two sides and included angle, find third side and other angles."""
          angle_C = math.radians(angle_C_deg)

          # Find side c using Law of Cosines
          c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(angle_C))

          # Find other angles
          angles = solve_triangle_sss(a, b, c)

          return {
              'c': c,
              'angles': angles
          }

      # Test with sides 3, 4, 5 (right triangle)
      result = solve_triangle_sss(3, 4, 5)
      print(f"Angles: A={result['A']:.1f}°, B={result['B']:.1f}°, C={result['C']:.1f}°")

      # Test SAS
      result2 = solve_triangle_sas(5, 7, 60)
      print(f"Third side: {result2['c']:.2f}")
      print(f"Angles: A={result2['angles']['A']:.1f}°, B={result2['angles']['B']:.1f}°")
```
<!-- EXERCISE_END -->
