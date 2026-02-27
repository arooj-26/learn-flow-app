# Random Module

The `random` module provides functions for generating pseudo-random numbers, essential for simulations, games, statistical sampling, and cryptography. It implements various probability distributions and random selection methods, making it a versatile tool for introducing randomness and unpredictability into Python programs.

## Basic Random Number Generation

The random module offers multiple ways to generate random numbers, from simple random floats to integers within specific ranges.

```python
import random

# Set seed for reproducibility
random.seed(42)

# Random float between 0.0 and 1.0
print(random.random())  # 0.6394267984578837

# Random float in a range
print(random.uniform(1.5, 10.5))  # 7.103445867913169

# Random integer in range (inclusive)
print(random.randint(1, 10))  # 7

# Random integer from range with step
print(random.randrange(0, 100, 5))  # Random multiple of 5 between 0-95

# Random integer from range (exclusive end)
print(random.randrange(10))  # Random int from 0-9

# Multiple random numbers
random_numbers = [random.randint(1, 100) for _ in range(5)]
print(random_numbers)  # [40, 2, 80, 88, 69]

# Random bits
print(random.getrandbits(8))  # Random 8-bit integer (0-255)
```

| Function | Range | Type | Example |
|----------|-------|------|---------|
| `random()` | [0.0, 1.0) | Float | `0.6394...` |
| `uniform(a, b)` | [a, b] | Float | `uniform(1, 10)` |
| `randint(a, b)` | [a, b] | Int | `randint(1, 6)` |
| `randrange(start, stop, step)` | [start, stop) | Int | `randrange(0, 100, 5)` |
| `getrandbits(k)` | [0, 2^k) | Int | `getrandbits(8)` |

## Random Selection and Shuffling

The random module provides powerful functions for selecting items from sequences, shuffling lists, and sampling without replacement.

```python
import random

# Choose one random element
colors = ['red', 'green', 'blue', 'yellow', 'purple']
print(random.choice(colors))  # 'blue'

# Choose multiple elements with replacement
print(random.choices(colors, k=3))  # ['green', 'blue', 'green']

# Weighted random choice
weights = [10, 1, 1, 1, 1]  # 'red' is 10x more likely
print(random.choices(colors, weights=weights, k=5))
# ['red', 'red', 'yellow', 'red', 'red']

# Sample without replacement
print(random.sample(colors, k=3))  # ['yellow', 'red', 'purple']

# Shuffle list in place
deck = list(range(1, 53))  # Deck of cards
random.shuffle(deck)
print(deck[:5])  # First 5 cards: [23, 15, 41, 8, 30]

# Practical example: Random team generator
def create_teams(players, team_size):
    """Randomly divide players into teams."""
    shuffled = players.copy()
    random.shuffle(shuffled)

    teams = []
    for i in range(0, len(shuffled), team_size):
        teams.append(shuffled[i:i+team_size])

    return teams

players = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank']
teams = create_teams(players, 2)
for i, team in enumerate(teams, 1):
    print(f"Team {i}: {', '.join(team)}")

# Weighted sampling example
def weighted_lottery(participants, weights, winners=1):
    """Select lottery winners based on weights (e.g., tickets bought)."""
    return random.choices(participants, weights=weights, k=winners)

participants = ['Alice', 'Bob', 'Charlie']
tickets = [1, 5, 2]  # Bob bought 5 tickets
winners = weighted_lottery(participants, tickets, winners=3)
print(f"Winners: {winners}")
```

## Random Distributions

The random module implements various probability distributions useful for statistical simulations and modeling real-world phenomena.

```python
import random

# Gaussian (Normal) Distribution
# Parameters: mean (mu), standard deviation (sigma)
mean = 100
std_dev = 15

# Generate normally distributed random numbers
iq_scores = [random.gauss(mean, std_dev) for _ in range(10)]
print(f"IQ Scores: {[round(s) for s in iq_scores]}")

# Alternative: normalvariate (slightly slower but thread-safe)
height = random.normalvariate(170, 10)  # Mean 170cm, std 10cm
print(f"Height: {height:.1f}cm")

# Triangular Distribution
# Parameters: low, high, mode (peak)
# Useful when you know min, max, and most likely value
response_time = random.triangular(1, 10, 3)  # Mode at 3
print(f"Response time: {response_time:.2f}s")

# Beta Distribution
# Parameters: alpha, beta
# Values between 0 and 1, shape controlled by parameters
probability = random.betavariate(5, 2)
print(f"Probability: {probability:.3f}")

# Exponential Distribution
# Parameter: lambda (1/mean)
# Useful for modeling time between events
time_between_calls = random.expovariate(1/5)  # Mean of 5 minutes
print(f"Time to next call: {time_between_calls:.2f} minutes")

# Gamma Distribution
# Parameters: alpha, beta
value = random.gammavariate(2, 3)
print(f"Gamma value: {value:.2f}")

# Lognormal Distribution
# Parameters: mean, sigma of underlying normal distribution
income = random.lognormvariate(10, 1)
print(f"Income: ${income:.2f}")

# Pareto Distribution
# Parameter: alpha (shape)
wealth = random.paretovariate(3)
print(f"Wealth distribution: {wealth:.2f}")

# Von Mises Distribution (circular data)
# Parameters: mean, concentration
angle = random.vonmisesvariate(0, 1)
print(f"Angle: {angle:.2f} radians")

# Weibull Distribution
# Parameters: alpha, beta
lifetime = random.weibullvariate(2, 5)
print(f"Component lifetime: {lifetime:.2f} years")
```

| Distribution | Use Case | Example |
|--------------|----------|---------|
| `gauss(mu, sigma)` | Normal distribution | Heights, IQ scores |
| `triangular(low, high, mode)` | Known min/max/mode | Estimation |
| `expovariate(lambd)` | Time between events | Queue arrivals |
| `lognormvariate(mu, sigma)` | Positive skewed data | Incomes, file sizes |
| `betavariate(alpha, beta)` | Probabilities | Success rates |

## Random Simulation and Applications

Random numbers are fundamental to many real-world applications, from game development to Monte Carlo simulations.

```python
import random

# 1. Dice Rolling Simulator
def roll_dice(num_dice=2, num_sides=6):
    """Roll multiple dice and return results."""
    return [random.randint(1, num_sides) for _ in range(num_dice)]

def dice_statistics(rolls=10000):
    """Analyze dice roll statistics."""
    results = {i: 0 for i in range(2, 13)}

    for _ in range(rolls):
        total = sum(roll_dice())
        results[total] += 1

    print("Dice Roll Statistics (10000 rolls):")
    for value, count in sorted(results.items()):
        percentage = (count / rolls) * 100
        bar = '█' * int(percentage * 2)
        print(f"{value:2d}: {bar} {percentage:.1f}%")

dice_statistics()

# 2. Monte Carlo Pi Estimation
def estimate_pi(num_samples=100000):
    """Estimate pi using Monte Carlo method."""
    inside_circle = 0

    for _ in range(num_samples):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        if x*x + y*y <= 1:
            inside_circle += 1

    pi_estimate = 4 * inside_circle / num_samples
    return pi_estimate

pi_value = estimate_pi()
print(f"\nEstimated Pi: {pi_value:.5f}")
print(f"Actual Pi: 3.14159")
print(f"Error: {abs(pi_value - 3.14159):.5f}")

# 3. Password Generator
def generate_password(length=12, include_special=True):
    """Generate a secure random password."""
    import string

    chars = string.ascii_letters + string.digits
    if include_special:
        chars += string.punctuation

    # Ensure at least one of each type
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
    ]

    if include_special:
        password.append(random.choice(string.punctuation))

    # Fill remaining length
    while len(password) < length:
        password.append(random.choice(chars))

    # Shuffle to randomize positions
    random.shuffle(password)
    return ''.join(password)

print(f"\nGenerated password: {generate_password()}")

# 4. Random Walk Simulation
def random_walk_1d(steps=100):
    """Simulate 1D random walk."""
    position = 0
    positions = [position]

    for _ in range(steps):
        step = random.choice([-1, 1])
        position += step
        positions.append(position)

    return positions

walk = random_walk_1d(50)
print(f"\nRandom walk final position: {walk[-1]}")
print(f"Max distance: {max(abs(p) for p in walk)}")

# 5. Inventory System with Random Events
class LootBox:
    """Simulate a loot box system with rarity."""

    def __init__(self):
        self.items = {
            'Common': ['Potion', 'Wood', 'Stone'],
            'Rare': ['Steel Sword', 'Magic Ring'],
            'Epic': ['Dragon Scale', 'Legendary Gem'],
            'Legendary': ['Excalibur']
        }

        self.rarity_weights = {
            'Common': 60,
            'Rare': 25,
            'Epic': 12,
            'Legendary': 3
        }

    def open_box(self):
        """Open a loot box and get a random item."""
        rarities = list(self.rarity_weights.keys())
        weights = list(self.rarity_weights.values())

        rarity = random.choices(rarities, weights=weights)[0]
        item = random.choice(self.items[rarity])

        return rarity, item

loot = LootBox()
print("\nOpening 10 loot boxes:")
for i in range(10):
    rarity, item = loot.open_box()
    print(f"  Box {i+1}: [{rarity}] {item}")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Random Number Generation"
    difficulty: basic
    description: "Generate 5 random integers between 1 and 100, then calculate their sum and average."
    starter_code: |
      import random

      # Set seed for reproducibility
      random.seed(42)

      # Generate 5 random integers between 1 and 100
      numbers =

      # Calculate sum and average
      total =
      average =

      print(f"Numbers: {numbers}")
      print(f"Sum: {total}")
      print(f"Average: {average:.2f}")
    expected_output: |
      Numbers: [82, 15, 87, 89, 74]
      Sum: 347
      Average: 69.40
    hints:
      - "Use list comprehension with random.randint(1, 100)"
      - "Sum with sum() function"
      - "Average = sum / length"
    solution: |
      import random

      # Set seed for reproducibility
      random.seed(42)

      # Generate 5 random integers between 1 and 100
      numbers = [random.randint(1, 100) for _ in range(5)]

      # Calculate sum and average
      total = sum(numbers)
      average = total / len(numbers)

      print(f"Numbers: {numbers}")
      print(f"Sum: {total}")
      print(f"Average: {average:.2f}")

  - title: "Random Selection"
    difficulty: basic
    description: "Create a function that randomly selects a specified number of winners from a list of participants without replacement."
    starter_code: |
      import random

      def select_winners(participants, num_winners):
          # Use random.sample to select winners without replacement


      # Set seed
      random.seed(10)

      contestants = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank']
      winners = select_winners(contestants, 3)

      print(f"Contestants: {', '.join(contestants)}")
      print(f"Winners: {', '.join(winners)}")
    expected_output: |
      Contestants: Alice, Bob, Charlie, Diana, Eve, Frank
      Winners: Frank, Diana, Alice
    hints:
      - "Use random.sample(list, k) for sampling without replacement"
      - "Returns a list of k unique elements"
    solution: |
      import random

      def select_winners(participants, num_winners):
          # Use random.sample to select winners without replacement
          return random.sample(participants, num_winners)

      # Set seed
      random.seed(10)

      contestants = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank']
      winners = select_winners(contestants, 3)

      print(f"Contestants: {', '.join(contestants)}")
      print(f"Winners: {', '.join(winners)}")

  - title: "Card Deck Simulator"
    difficulty: intermediate
    description: "Create a deck of cards, shuffle it, and deal hands to multiple players."
    starter_code: |
      import random

      def create_deck():
          """Create a standard 52-card deck."""
          suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
          ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
          # Create deck as list of tuples


      def deal_hands(num_players, cards_per_player):
          """Deal cards to players."""
          deck = create_deck()
          # Shuffle deck

          hands = []
          # Deal cards to each player


          return hands

      random.seed(5)
      hands = deal_hands(4, 5)

      for i, hand in enumerate(hands, 1):
          cards = [f"{rank} of {suit}" for rank, suit in hand]
          print(f"Player {i}: {', '.join(cards)}")
    expected_output: |
      Player 1: 10 of Hearts, 7 of Clubs, 9 of Clubs, Q of Hearts, 5 of Spades
      Player 2: 8 of Spades, 4 of Clubs, 5 of Hearts, 10 of Spades, 8 of Diamonds
      Player 3: 6 of Clubs, 7 of Diamonds, J of Spades, 3 of Diamonds, K of Clubs
      Player 4: 5 of Clubs, 6 of Spades, 2 of Hearts, 3 of Hearts, Q of Diamonds
    hints:
      - "Create deck with nested loops or list comprehension"
      - "Use random.shuffle() to shuffle in place"
      - "Deal by slicing: deck[i*cards_per_player:(i+1)*cards_per_player]"
    solution: |
      import random

      def create_deck():
          """Create a standard 52-card deck."""
          suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
          ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
          # Create deck as list of tuples
          return [(rank, suit) for suit in suits for rank in ranks]

      def deal_hands(num_players, cards_per_player):
          """Deal cards to players."""
          deck = create_deck()
          # Shuffle deck
          random.shuffle(deck)

          hands = []
          # Deal cards to each player
          for i in range(num_players):
              hand = deck[i*cards_per_player:(i+1)*cards_per_player]
              hands.append(hand)

          return hands

      random.seed(5)
      hands = deal_hands(4, 5)

      for i, hand in enumerate(hands, 1):
          cards = [f"{rank} of {suit}" for rank, suit in hand]
          print(f"Player {i}: {', '.join(cards)}")

  - title: "Weighted Random Events"
    difficulty: intermediate
    description: "Simulate a game where different outcomes have different probabilities. Track how many times each outcome occurs over 1000 trials."
    starter_code: |
      import random

      def simulate_game(trials=1000):
          """Simulate game with weighted outcomes."""
          outcomes = ['Win', 'Lose', 'Draw']
          weights = [20, 70, 10]  # 20% win, 70% lose, 10% draw

          results = {'Win': 0, 'Lose': 0, 'Draw': 0}

          for _ in range(trials):
              # Choose outcome with weights
              outcome =
              results[outcome] += 1

          return results

      random.seed(100)
      results = simulate_game(1000)

      print("Game Results (1000 trials):")
      for outcome, count in results.items():
          percentage = (count / 1000) * 100
          print(f"{outcome}: {count} ({percentage:.1f}%)")
    expected_output: |
      Game Results (1000 trials):
      Win: 207 (20.7%)
      Lose: 692 (69.2%)
      Draw: 101 (10.1%)
    hints:
      - "Use random.choices() with weights parameter"
      - "random.choices(outcomes, weights=weights, k=1)[0]"
      - "Increment the count in results dictionary"
    solution: |
      import random

      def simulate_game(trials=1000):
          """Simulate game with weighted outcomes."""
          outcomes = ['Win', 'Lose', 'Draw']
          weights = [20, 70, 10]  # 20% win, 70% lose, 10% draw

          results = {'Win': 0, 'Lose': 0, 'Draw': 0}

          for _ in range(trials):
              # Choose outcome with weights
              outcome = random.choices(outcomes, weights=weights, k=1)[0]
              results[outcome] += 1

          return results

      random.seed(100)
      results = simulate_game(1000)

      print("Game Results (1000 trials):")
      for outcome, count in results.items():
          percentage = (count / 1000) * 100
          print(f"{outcome}: {count} ({percentage:.1f}%)")

  - title: "Monte Carlo Integration"
    difficulty: advanced
    description: "Use Monte Carlo method to estimate the area under the curve y = x² from 0 to 1."
    starter_code: |
      import random

      def monte_carlo_integrate(func, x_min, x_max, y_min, y_max, samples=10000):
          """Estimate integral using Monte Carlo method."""
          inside = 0

          for _ in range(samples):
              # Generate random point
              x =
              y =

              # Check if point is under the curve
              if y <= func(x):
                  inside += 1

          # Calculate area
          rectangle_area =
          estimated_area =

          return estimated_area

      # Function to integrate: f(x) = x^2
      def f(x):
          return x ** 2

      random.seed(42)
      estimated = monte_carlo_integrate(f, 0, 1, 0, 1, samples=100000)
      actual = 1/3  # Integral of x^2 from 0 to 1 is 1/3

      print(f"Estimated area: {estimated:.5f}")
      print(f"Actual area: {actual:.5f}")
      print(f"Error: {abs(estimated - actual):.5f}")
    expected_output: |
      Estimated area: 0.33279
      Actual area: 0.33333
      Error: 0.00054
    hints:
      - "Generate random x in [x_min, x_max] with uniform()"
      - "Generate random y in [y_min, y_max]"
      - "Rectangle area = (x_max - x_min) * (y_max - y_min)"
      - "Estimated area = rectangle_area * (inside / samples)"
    solution: |
      import random

      def monte_carlo_integrate(func, x_min, x_max, y_min, y_max, samples=10000):
          """Estimate integral using Monte Carlo method."""
          inside = 0

          for _ in range(samples):
              # Generate random point
              x = random.uniform(x_min, x_max)
              y = random.uniform(y_min, y_max)

              # Check if point is under the curve
              if y <= func(x):
                  inside += 1

          # Calculate area
          rectangle_area = (x_max - x_min) * (y_max - y_min)
          estimated_area = rectangle_area * (inside / samples)

          return estimated_area

      # Function to integrate: f(x) = x^2
      def f(x):
          return x ** 2

      random.seed(42)
      estimated = monte_carlo_integrate(f, 0, 1, 0, 1, samples=100000)
      actual = 1/3  # Integral of x^2 from 0 to 1 is 1/3

      print(f"Estimated area: {estimated:.5f}")
      print(f"Actual area: {actual:.55f}")
      print(f"Error: {abs(estimated - actual):.5f}")

  - title: "Random Walk 2D Visualization"
    difficulty: advanced
    description: "Simulate a 2D random walk and calculate statistics including final distance from origin and maximum distance reached."
    starter_code: |
      import random
      import math

      def random_walk_2d(steps=1000):
          """Simulate 2D random walk and return statistics."""
          x, y = 0, 0
          positions = [(x, y)]
          max_distance = 0

          for _ in range(steps):
              # Choose random direction (up, down, left, right)
              direction =

              # Update position
              if direction == 'up':
                  y += 1
              elif direction == 'down':
                  y -= 1
              elif direction == 'left':
                  x -= 1
              else:  # right
                  x += 1

              positions.append((x, y))

              # Calculate distance from origin
              distance =

              # Update max distance
              max_distance = max(max_distance, distance)

          final_distance =

          return {
              'final_position': (x, y),
              'final_distance': final_distance,
              'max_distance': max_distance,
              'positions': positions
          }

      random.seed(777)
      result = random_walk_2d(1000)

      print(f"Final position: {result['final_position']}")
      print(f"Final distance from origin: {result['final_distance']:.2f}")
      print(f"Maximum distance reached: {result['max_distance']:.2f}")
    expected_output: |
      Final position: (-18, 6)
      Final distance from origin: 18.97
      Maximum distance reached: 34.48
    hints:
      - "Use random.choice(['up', 'down', 'left', 'right'])"
      - "Distance = sqrt(x² + y²)"
      - "Use math.sqrt() and math.hypot()"
    solution: |
      import random
      import math

      def random_walk_2d(steps=1000):
          """Simulate 2D random walk and return statistics."""
          x, y = 0, 0
          positions = [(x, y)]
          max_distance = 0

          for _ in range(steps):
              # Choose random direction (up, down, left, right)
              direction = random.choice(['up', 'down', 'left', 'right'])

              # Update position
              if direction == 'up':
                  y += 1
              elif direction == 'down':
                  y -= 1
              elif direction == 'left':
                  x -= 1
              else:  # right
                  x += 1

              positions.append((x, y))

              # Calculate distance from origin
              distance = math.hypot(x, y)

              # Update max distance
              max_distance = max(max_distance, distance)

          final_distance = math.hypot(x, y)

          return {
              'final_position': (x, y),
              'final_distance': final_distance,
              'max_distance': max_distance,
              'positions': positions
          }

      random.seed(777)
      result = random_walk_2d(1000)

      print(f"Final position: {result['final_position']}")
      print(f"Final distance from origin: {result['final_distance']:.2f}")
      print(f"Maximum distance reached: {result['max_distance']:.2f}")
```
<!-- EXERCISE_END -->
