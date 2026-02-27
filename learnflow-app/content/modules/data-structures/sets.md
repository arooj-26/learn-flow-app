# Sets

Sets are unordered collections of unique elements in Python, providing powerful operations for membership testing, removing duplicates, and mathematical set operations like union, intersection, and difference. Sets are implemented as hash tables, making membership tests extremely fast (O(1) average case). Understanding sets is essential for efficient data deduplication, relationship analysis, and algorithmic problem-solving.

## Creating and Modifying Sets

Sets are created using curly braces `{}` or the `set()` constructor. Unlike dictionaries, sets contain only values, not key-value pairs.

```python
# Creating sets
fruits = {"apple", "banana", "orange"}
numbers = {1, 2, 3, 4, 5}

# Set from list (automatically removes duplicates)
duplicates = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = set(duplicates)
print(f"Original: {duplicates}")
print(f"Unique: {unique}")

# Empty set (must use set(), not {})
empty = set()  # Correct
not_empty = {}  # This is an empty dict, not set!
print(f"Type of empty: {type(empty)}")
print(f"Type of {{}}: {type(not_empty)}")

# Set from string (gets unique characters)
text = "hello world"
unique_chars = set(text)
print(f"Unique characters: {unique_chars}")

# Adding elements
tags = {"python", "programming"}
tags.add("tutorial")
tags.add("python")  # Doesn't add duplicate
print(f"Tags: {tags}")

# Adding multiple elements with update()
tags.update(["web", "api", "database"])
tags.update("ML")  # Adds 'M' and 'L' as separate elements!
print(f"Updated tags: {tags}")

# Removing elements
tags.discard("ML")  # Safe removal (no error if missing)
tags.discard("nonexistent")  # No error

try:
    tags.remove("M")  # Raises KeyError if not found
except KeyError:
    print("Key not found with remove()")

popped = tags.pop()  # Remove and return arbitrary element
print(f"Popped: {popped}")
print(f"Remaining tags: {tags}")

# Clear all elements
test_set = {1, 2, 3}
test_set.clear()
print(f"Cleared set: {test_set}")
```

## Set Operations: Union, Intersection, Difference

Sets support mathematical operations that are invaluable for data analysis and filtering.

```python
# User interest analysis
users_python = {"alice", "bob", "charlie", "diana"}
users_javascript = {"bob", "diana", "eve", "frank"}
users_sql = {"charlie", "diana", "frank", "grace"}

# Union - all users (| or union())
all_users = users_python | users_javascript | users_sql
print(f"All users: {all_users}")

# Alternative syntax
all_users_alt = users_python.union(users_javascript, users_sql)
print(f"All users (union): {all_users_alt}")

# Intersection - users interested in ALL topics (& or intersection())
polyglots = users_python & users_javascript & users_sql
print(f"Know all three: {polyglots}")

# Users interested in both Python and JavaScript
python_and_js = users_python & users_javascript
print(f"Python AND JavaScript: {python_and_js}")

# Difference - users ONLY interested in Python (- or difference())
python_only = users_python - users_javascript - users_sql
print(f"Python only: {python_only}")

# Symmetric difference - users in Python XOR JavaScript (^ or symmetric_difference())
either_not_both = users_python ^ users_javascript
print(f"Python XOR JavaScript: {either_not_both}")

# Practical example: Access control
admin_users = {"alice", "bob"}
active_users = {"bob", "charlie", "diana"}
banned_users = {"eve"}

# Users who can access admin panel
can_access_admin = admin_users & active_users
print(f"Can access admin: {can_access_admin}")

# All legitimate users
legitimate = (admin_users | active_users) - banned_users
print(f"Legitimate users: {legitimate}")

# Update operations (modify set in-place)
set1 = {1, 2, 3}
set2 = {3, 4, 5}

set1 |= set2  # Union update (same as set1.update(set2))
print(f"After |=: {set1}")

set1 = {1, 2, 3}
set1 &= set2  # Intersection update
print(f"After &=: {set1}")

set1 = {1, 2, 3}
set1 -= set2  # Difference update
print(f"After -=: {set1}")
```

Set operations table:

| Operation | Operator | Method | Description |
|-----------|----------|--------|-------------|
| Union | `\|` | `union()` | All elements from both sets |
| Intersection | `&` | `intersection()` | Elements in both sets |
| Difference | `-` | `difference()` | Elements in first but not second |
| Symmetric Diff | `^` | `symmetric_difference()` | Elements in either but not both |
| Subset | `<=` | `issubset()` | All elements in other set |
| Superset | `>=` | `issuperset()` | Contains all elements of other |
| Disjoint | - | `isdisjoint()` | No common elements |

## Set Membership and Comparisons

Sets excel at fast membership testing and relationship analysis.

```python
# Fast membership testing (O(1) average)
allowed_extensions = {".jpg", ".png", ".gif", ".webp"}
filename = "photo.jpg"
extension = filename[filename.rfind("."):]

if extension in allowed_extensions:
    print(f"{extension} is allowed")
else:
    print(f"{extension} is not allowed")

# Comparing sets
set_a = {1, 2, 3, 4}
set_b = {2, 3}
set_c = {1, 2, 3, 4}
set_d = {5, 6}

# Subset and superset
print(f"Is {set_b} subset of {set_a}? {set_b <= set_a}")
print(f"Is {set_b} proper subset? {set_b < set_a}")  # True (not equal)
print(f"Is {set_a} superset of {set_b}? {set_a >= set_b}")

# Equality
print(f"Are {set_a} and {set_c} equal? {set_a == set_c}")

# Disjoint (no common elements)
print(f"Are {set_a} and {set_d} disjoint? {set_a.isdisjoint(set_d)}")

# Practical example: Tag filtering
article_tags = {"python", "tutorial", "beginners", "programming"}
required_tags = {"python", "tutorial"}
excluded_tags = {"advanced"}

# Check if article meets criteria
has_required = required_tags <= article_tags
has_excluded = not article_tags.isdisjoint(excluded_tags)

if has_required and not has_excluded:
    print("Article matches filter criteria")
else:
    print("Article doesn't match criteria")

# Finding similar items
product_a_features = {"bluetooth", "waterproof", "rechargeable", "portable"}
product_b_features = {"wireless", "waterproof", "rechargeable", "compact"}

common_features = product_a_features & product_b_features
similarity = len(common_features) / len(product_a_features | product_b_features)
print(f"Product similarity: {similarity:.2%}")
print(f"Common features: {common_features}")
```

## Frozen Sets: Immutable Sets

Frozen sets are immutable versions of sets, allowing them to be used as dictionary keys or elements of other sets.

```python
# Creating frozen sets
frozen = frozenset([1, 2, 3, 4])
print(f"Frozen set: {frozen}")

# Frozen sets can't be modified
try:
    frozen.add(5)
except AttributeError as e:
    print(f"Error: {e}")

# Frozen sets as dictionary keys
city_coords = {
    frozenset(["New York", "NYC"]): (40.7128, -74.0060),
    frozenset(["Los Angeles", "LA"]): (34.0522, -118.2437),
    frozenset(["Chicago"]): (41.8781, -87.6298)
}

# Look up by any alias
ny_coords = city_coords[frozenset(["NYC", "New York"])]
print(f"NYC coordinates: {ny_coords}")

# Sets of sets (must use frozenset)
groups = {
    frozenset(["alice", "bob"]),
    frozenset(["charlie", "diana"]),
    frozenset(["eve", "frank"])
}
print(f"Groups: {groups}")

# Practical example: Caching unique combinations
from functools import lru_cache

@lru_cache(maxsize=128)
def analyze_combination(items):
    """Analyze a combination of items (must be hashable)"""
    # Expensive computation here
    return f"Analysis of {items}"

# Must use frozenset for caching
result1 = analyze_combination(frozenset(["a", "b", "c"]))
result2 = analyze_combination(frozenset(["c", "b", "a"]))  # Same as above!
print(f"Results equal: {result1 == result2}")

# Permission system example
class User:
    def __init__(self, username, permissions):
        self.username = username
        self.permissions = frozenset(permissions)  # Immutable

    def has_permission(self, perm):
        return perm in self.permissions

    def has_all_permissions(self, perms):
        return set(perms) <= self.permissions

admin = User("alice", ["read", "write", "delete", "admin"])
user = User("bob", ["read", "write"])

print(f"Bob can write: {user.has_permission('write')}")
print(f"Bob can delete: {user.has_permission('delete')}")
print(f"Alice has all perms: {admin.has_all_permissions(['read', 'write', 'admin'])}")
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Remove Duplicates"
    difficulty: basic
    description: "Given a list with duplicate values, create a set to get unique values and convert back to a sorted list."
    starter_code: |
      numbers = [5, 2, 8, 2, 9, 5, 3, 8, 1, 2]

      # Convert to set to remove duplicates
      # Convert back to sorted list
      # Print the result

    expected_output: |
      [1, 2, 3, 5, 8, 9]
    hints:
      - "Use set() to remove duplicates"
      - "Use sorted() to get a sorted list"
    solution: |
      numbers = [5, 2, 8, 2, 9, 5, 3, 8, 1, 2]

      # Convert to set to remove duplicates
      unique = set(numbers)

      # Convert back to sorted list
      result = sorted(unique)

      # Print the result
      print(result)

  - title: "Common Friends Finder"
    difficulty: basic
    description: "Find mutual friends between two users using set intersection."
    starter_code: |
      alice_friends = {"bob", "charlie", "diana", "eve"}
      bob_friends = {"alice", "charlie", "frank", "grace"}

      # Find common friends (excluding alice and bob themselves)
      # Print the result

    expected_output: |
      {'charlie'}
    hints:
      - "Use & or intersection() to find common elements"
      - "Remove alice and bob from the result"
    solution: |
      alice_friends = {"bob", "charlie", "diana", "eve"}
      bob_friends = {"alice", "charlie", "frank", "grace"}

      # Find common friends (excluding alice and bob themselves)
      mutual = alice_friends & bob_friends

      # Print the result
      print(mutual)

  - title: "Email Domain Extractor"
    difficulty: intermediate
    description: "Extract unique email domains from a list of email addresses."
    starter_code: |
      emails = [
          "alice@gmail.com",
          "bob@yahoo.com",
          "charlie@gmail.com",
          "diana@outlook.com",
          "eve@gmail.com",
          "frank@yahoo.com"
      ]

      # Extract unique domains
      # Print sorted domains

    expected_output: |
      ['gmail.com', 'outlook.com', 'yahoo.com']
    hints:
      - "Split each email by '@' to get the domain"
      - "Use a set to collect unique domains"
      - "Convert to sorted list for output"
    solution: |
      emails = [
          "alice@gmail.com",
          "bob@yahoo.com",
          "charlie@gmail.com",
          "diana@outlook.com",
          "eve@gmail.com",
          "frank@yahoo.com"
      ]

      # Extract unique domains
      domains = {email.split("@")[1] for email in emails}

      # Print sorted domains
      print(sorted(domains))

  - title: "Skills Gap Analysis"
    difficulty: intermediate
    description: "Given required skills for a job and a candidate's skills, identify missing skills and extra skills."
    starter_code: |
      required_skills = {"python", "sql", "git", "docker", "aws"}
      candidate_skills = {"python", "sql", "javascript", "react", "git"}

      # Find missing skills (required but not in candidate)
      # Find extra skills (candidate has but not required)
      # Print both

    expected_output: |
      Missing skills: {'aws', 'docker'}
      Extra skills: {'javascript', 'react'}
    hints:
      - "Use difference (-) to find missing skills"
      - "Use reverse difference for extra skills"
    solution: |
      required_skills = {"python", "sql", "git", "docker", "aws"}
      candidate_skills = {"python", "sql", "javascript", "react", "git"}

      # Find missing skills (required but not in candidate)
      missing = required_skills - candidate_skills

      # Find extra skills (candidate has but not required)
      extra = candidate_skills - required_skills

      # Print both
      print(f"Missing skills: {missing}")
      print(f"Extra skills: {extra}")

  - title: "Tag Recommendation System"
    difficulty: advanced
    description: "Build a tag recommendation system that suggests tags based on similar articles."
    starter_code: |
      articles = {
          "article1": {"python", "tutorial", "beginners", "programming"},
          "article2": {"python", "advanced", "decorators", "programming"},
          "article3": {"javascript", "tutorial", "beginners", "web"},
          "article4": {"python", "tutorial", "functions", "programming"}
      }

      def recommend_tags(current_tags, articles, max_recommendations=3):
          # Find articles with overlapping tags
          # Collect tags from similar articles
          # Return top N recommended tags not in current_tags
          pass

      current = {"python", "tutorial"}
      recommended = recommend_tags(current, articles, max_recommendations=3)
      print(f"Recommended tags: {recommended}")

    expected_output: |
      Recommended tags: ['beginners', 'programming', 'functions']
    hints:
      - "Calculate overlap between current tags and each article"
      - "Collect all tags from articles with overlap"
      - "Exclude tags already in current_tags"
      - "Count frequency and return most common"
    solution: |
      articles = {
          "article1": {"python", "tutorial", "beginners", "programming"},
          "article2": {"python", "advanced", "decorators", "programming"},
          "article3": {"javascript", "tutorial", "beginners", "web"},
          "article4": {"python", "tutorial", "functions", "programming"}
      }

      def recommend_tags(current_tags, articles, max_recommendations=3):
          # Find articles with overlapping tags
          candidate_tags = {}
          for article_tags in articles.values():
              overlap = current_tags & article_tags
              if overlap:  # Has some overlap
                  # Collect tags from similar articles
                  for tag in article_tags - current_tags:
                      candidate_tags[tag] = candidate_tags.get(tag, 0) + 1

          # Return top N recommended tags not in current_tags
          sorted_tags = sorted(candidate_tags.items(), key=lambda x: x[1], reverse=True)
          return [tag for tag, count in sorted_tags[:max_recommendations]]

      current = {"python", "tutorial"}
      recommended = recommend_tags(current, articles, max_recommendations=3)
      print(f"Recommended tags: {recommended}")

  - title: "Access Control System"
    difficulty: advanced
    description: "Implement an access control system using frozen sets to determine if users have required permissions."
    starter_code: |
      from functools import lru_cache

      # Define role permissions using frozen sets
      ROLES = {
          "admin": frozenset(["read", "write", "delete", "manage_users"]),
          "editor": frozenset(["read", "write"]),
          "viewer": frozenset(["read"])
      }

      @lru_cache(maxsize=128)
      def check_access(user_roles, required_permissions):
          # user_roles and required_permissions are frozensets
          # Return True if user has all required permissions
          pass

      def has_access(user_roles_list, required_perms_list):
          # Convert to frozensets and check access
          user_roles = frozenset(user_roles_list)
          required = frozenset(required_perms_list)
          return check_access(user_roles, required)

      # Test cases
      print(has_access(["admin"], ["read", "write"]))
      print(has_access(["editor"], ["delete"]))
      print(has_access(["admin", "editor"], ["read", "write"]))

    expected_output: |
      True
      False
      True
    hints:
      - "Combine all permissions from user roles"
      - "Check if required permissions is a subset of user permissions"
      - "Use frozenset for caching with lru_cache"
    solution: |
      from functools import lru_cache

      # Define role permissions using frozen sets
      ROLES = {
          "admin": frozenset(["read", "write", "delete", "manage_users"]),
          "editor": frozenset(["read", "write"]),
          "viewer": frozenset(["read"])
      }

      @lru_cache(maxsize=128)
      def check_access(user_roles, required_permissions):
          # user_roles and required_permissions are frozensets
          # Combine all permissions from user roles
          all_permissions = set()
          for role in user_roles:
              if role in ROLES:
                  all_permissions |= ROLES[role]

          # Return True if user has all required permissions
          return required_permissions <= all_permissions

      def has_access(user_roles_list, required_perms_list):
          # Convert to frozensets and check access
          user_roles = frozenset(user_roles_list)
          required = frozenset(required_perms_list)
          return check_access(user_roles, required)

      # Test cases
      print(has_access(["admin"], ["read", "write"]))
      print(has_access(["editor"], ["delete"]))
      print(has_access(["admin", "editor"], ["read", "write"]))
```
<!-- EXERCISE_END -->
