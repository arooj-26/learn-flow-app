# CSV Files

CSV (Comma-Separated Values) files are one of the most common formats for storing tabular data. Python's `csv` module provides powerful tools for reading and writing CSV files, handling various dialects, and managing edge cases like quoted fields and different delimiters.

## Reading CSV Files

The `csv` module offers multiple ways to read CSV data. The `csv.reader` provides row-by-row access, while `csv.DictReader` gives you dictionary-based access with column names.

```python
import csv

# Basic CSV reading
with open('data.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)  # Each row is a list

# Reading with header
with open('employees.csv', 'r') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)  # Get first row as headers
    print(f"Headers: {headers}")

    for row in csv_reader:
        print(f"Row: {row}")

# Using DictReader for named access
with open('employees.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        print(f"Name: {row['name']}, Age: {row['age']}, Role: {row['role']}")

# Converting CSV to list of dictionaries
def csv_to_list(filename):
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(dict(row))
    return data

employees = csv_to_list('employees.csv')
print(f"Loaded {len(employees)} employees")
```

## Writing CSV Files

Writing CSV files is straightforward with `csv.writer` for list-based data and `csv.DictWriter` for dictionary-based data.

```python
import csv

# Basic CSV writing
data = [
    ['Name', 'Age', 'City'],
    ['Alice', 30, 'New York'],
    ['Bob', 25, 'Los Angeles'],
    ['Charlie', 35, 'Chicago']
]

with open('output.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)

# Writing row by row
with open('output.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Name', 'Age', 'City'])
    csv_writer.writerow(['Alice', 30, 'New York'])
    csv_writer.writerow(['Bob', 25, 'Los Angeles'])

# Using DictWriter
employees = [
    {'name': 'Alice', 'age': 30, 'role': 'Engineer'},
    {'name': 'Bob', 'age': 25, 'role': 'Designer'},
    {'name': 'Charlie', 'age': 35, 'role': 'Manager'}
]

with open('employees.csv', 'w', newline='') as file:
    fieldnames = ['name', 'age', 'role']
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

    csv_writer.writeheader()
    csv_writer.writerows(employees)

# Appending to CSV
new_employee = {'name': 'Diana', 'age': 28, 'role': 'Analyst'}

with open('employees.csv', 'a', newline='') as file:
    csv_writer = csv.DictWriter(file, fieldnames=['name', 'age', 'role'])
    csv_writer.writerow(new_employee)
```

## CSV Dialects and Formatting

CSV files can have different formats (dialects). Python's csv module handles various delimiters, quote characters, and line terminators.

| Parameter | Description | Common Values |
|-----------|-------------|---------------|
| `delimiter` | Field separator | `,`, `\t`, `;`, `|` |
| `quotechar` | Quote character | `"`, `'` |
| `quoting` | When to quote | `QUOTE_MINIMAL`, `QUOTE_ALL` |
| `lineterminator` | Line ending | `\n`, `\r\n` |
| `escapechar` | Escape character | `\` |

```python
import csv

# Reading TSV (Tab-Separated Values)
with open('data.tsv', 'r') as file:
    csv_reader = csv.reader(file, delimiter='\t')
    for row in csv_reader:
        print(row)

# Writing with semicolon delimiter
data = [['Name', 'Email'], ['Alice', 'alice@example.com']]

with open('output.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file, delimiter=';')
    csv_writer.writerows(data)

# Using different quote styles
with open('quoted.csv', 'w', newline='') as file:
    # Quote all fields
    csv_writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    csv_writer.writerow(['Alice', 30, 'New York'])

with open('minimal_quotes.csv', 'w', newline='') as file:
    # Quote only when necessary
    csv_writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['Alice', 30, 'New York, NY'])

# Custom dialect
csv.register_dialect('custom',
                     delimiter='|',
                     quotechar='"',
                     quoting=csv.QUOTE_MINIMAL,
                     lineterminator='\n')

with open('custom.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file, dialect='custom')
    csv_writer.writerow(['Field1', 'Field2', 'Field3'])

# Excel dialect
with open('excel_format.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file, dialect='excel')
    csv_writer.writerows(data)
```

## Handling Special Cases

CSV files often contain special cases like quoted fields, embedded commas, and empty values. Proper handling ensures data integrity.

```python
import csv

# Handling fields with commas
data = [
    ['Name', 'Address', 'Phone'],
    ['Alice', '123 Main St, Apt 4', '555-1234'],
    ['Bob', '456 Oak Ave, Suite 200', '555-5678']
]

with open('addresses.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)

# Reading handles quotes automatically
with open('addresses.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)

# Handling missing values
def read_csv_with_defaults(filename, defaults=None):
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Fill in missing values
            if defaults:
                for key, default_value in defaults.items():
                    if not row.get(key):
                        row[key] = default_value
            data.append(row)
    return data

defaults = {'age': '0', 'role': 'Unknown'}
employees = read_csv_with_defaults('employees.csv', defaults)

# Handling multiline fields
data_with_multiline = [
    ['Name', 'Description'],
    ['Product A', 'This is a long\ndescription that spans\nmultiple lines'],
    ['Product B', 'Short description']
]

with open('products.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    csv_writer.writerows(data_with_multiline)

# Reading preserves multiline
with open('products.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(f"Product: {row[0]}")
        print(f"Description: {row[1]}\n")

# Handling different encodings
with open('utf8.csv', 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Name', 'City'])
    csv_writer.writerow(['José', 'São Paulo'])
    csv_writer.writerow(['François', 'Paris'])
```

## Data Processing with CSV

CSV files are often used for data analysis and transformation. Here are common patterns for processing CSV data.

```python
import csv
from collections import defaultdict, Counter

# Filtering rows
def filter_csv(input_file, output_file, condition):
    with open(input_file, 'r') as infile, \
         open(output_file, 'w', newline='') as outfile:

        csv_reader = csv.DictReader(infile)
        csv_writer = csv.DictWriter(outfile, fieldnames=csv_reader.fieldnames)

        csv_writer.writeheader()
        for row in csv_reader:
            if condition(row):
                csv_writer.writerow(row)

# Filter employees older than 30
filter_csv('employees.csv', 'senior_employees.csv',
           lambda row: int(row['age']) > 30)

# Aggregating data
def calculate_statistics(filename, group_by, value_field):
    stats = defaultdict(list)

    with open(filename, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            key = row[group_by]
            value = float(row[value_field])
            stats[key].append(value)

    results = {}
    for key, values in stats.items():
        results[key] = {
            'count': len(values),
            'sum': sum(values),
            'average': sum(values) / len(values),
            'min': min(values),
            'max': max(values)
        }

    return results

stats = calculate_statistics('sales.csv', 'region', 'amount')
for region, data in stats.items():
    print(f"{region}: avg=${data['average']:.2f}, total=${data['sum']:.2f}")

# Transforming columns
def transform_csv(input_file, output_file, transformations):
    with open(input_file, 'r') as infile, \
         open(output_file, 'w', newline='') as outfile:

        csv_reader = csv.DictReader(infile)
        csv_writer = csv.DictWriter(outfile, fieldnames=csv_reader.fieldnames)

        csv_writer.writeheader()
        for row in csv_reader:
            for field, func in transformations.items():
                if field in row:
                    row[field] = func(row[field])
            csv_writer.writerow(row)

# Convert names to uppercase and ages to int
transformations = {
    'name': str.upper,
    'age': lambda x: str(int(x) + 1)  # Increment age
}
transform_csv('employees.csv', 'transformed.csv', transformations)

# Merging CSV files
def merge_csv_files(files, output_file):
    all_data = []
    fieldnames = None

    for filename in files:
        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)
            if fieldnames is None:
                fieldnames = csv_reader.fieldnames
            all_data.extend(list(csv_reader))

    with open(output_file, 'w', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(all_data)

merge_csv_files(['file1.csv', 'file2.csv', 'file3.csv'], 'merged.csv')
```

---

## Exercises

<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Parse CSV Data"
    difficulty: basic
    description: "Parse CSV-formatted string data and print each row."
    starter_code: |
      import csv
      from io import StringIO

      csv_data = "name,age,city\nAlice,30,NYC\nBob,25,LA\n"

      # Parse and print each row

    expected_output: |
      ['name', 'age', 'city']
      ['Alice', '30', 'NYC']
      ['Bob', '25', 'LA']
    hints:
      - "Use StringIO to create file-like object from string"
      - "Use csv.reader to parse the data"
    solution: |
      import csv
      from io import StringIO

      csv_data = "name,age,city\nAlice,30,NYC\nBob,25,LA\n"

      file = StringIO(csv_data)
      csv_reader = csv.reader(file)

      for row in csv_reader:
          print(row)

  - title: "Create CSV Output"
    difficulty: basic
    description: "Create CSV-formatted output from a list of lists."
    starter_code: |
      import csv
      from io import StringIO

      data = [
          ['Product', 'Price'],
          ['Apple', '0.50'],
          ['Banana', '0.30']
      ]

      # Convert to CSV format and print

    expected_output: |
      Product,Price
      Apple,0.50
      Banana,0.30
    hints:
      - "Use StringIO as output buffer"
      - "Use csv.writer to write rows"
      - "Print the string value"
    solution: |
      import csv
      from io import StringIO

      data = [
          ['Product', 'Price'],
          ['Apple', '0.50'],
          ['Banana', '0.30']
      ]

      output = StringIO()
      csv_writer = csv.writer(output)
      csv_writer.writerows(data)

      print(output.getvalue().strip())

  - title: "DictReader for Named Access"
    difficulty: intermediate
    description: "Use DictReader to parse CSV and access fields by name."
    starter_code: |
      import csv
      from io import StringIO

      csv_data = "name,score,grade\nAlice,95,A\nBob,87,B\nCharlie,92,A\n"

      # Use DictReader and print formatted output

    expected_output: |
      Alice scored 95 (Grade: A)
      Bob scored 87 (Grade: B)
      Charlie scored 92 (Grade: A)
    hints:
      - "Use csv.DictReader for column name access"
      - "Access fields using row['fieldname']"
    solution: |
      import csv
      from io import StringIO

      csv_data = "name,score,grade\nAlice,95,A\nBob,87,B\nCharlie,92,A\n"

      file = StringIO(csv_data)
      csv_reader = csv.DictReader(file)

      for row in csv_reader:
          print(f"{row['name']} scored {row['score']} (Grade: {row['grade']})")

  - title: "Filter CSV Rows"
    difficulty: intermediate
    description: "Filter CSV data based on a condition and output filtered rows."
    starter_code: |
      import csv
      from io import StringIO

      csv_data = "name,age,department\nAlice,30,Engineering\nBob,25,Sales\nCharlie,35,Engineering\nDiana,28,Marketing\n"

      # Filter and output only Engineering department

    expected_output: |
      name,age,department
      Alice,30,Engineering
      Charlie,35,Engineering
    hints:
      - "Use DictReader to read with field names"
      - "Check if department equals 'Engineering'"
      - "Use DictWriter to output filtered results"
    solution: |
      import csv
      from io import StringIO

      csv_data = "name,age,department\nAlice,30,Engineering\nBob,25,Sales\nCharlie,35,Engineering\nDiana,28,Marketing\n"

      input_file = StringIO(csv_data)
      output_file = StringIO()

      csv_reader = csv.DictReader(input_file)
      csv_writer = csv.DictWriter(output_file, fieldnames=['name', 'age', 'department'])

      csv_writer.writeheader()
      for row in csv_reader:
          if row['department'] == 'Engineering':
              csv_writer.writerow(row)

      print(output_file.getvalue().strip())

  - title: "Calculate CSV Statistics"
    difficulty: advanced
    description: "Read CSV data and calculate aggregate statistics grouped by a field."
    starter_code: |
      import csv
      from io import StringIO

      csv_data = "region,sales\nEast,1000\nWest,1500\nEast,2000\nWest,1200\nEast,1800\n"

      # Calculate total and average sales per region

    expected_output: |
      East: total=4800, average=1600.00
      West: total=2700, average=1350.00
    hints:
      - "Use a dictionary to group sales by region"
      - "Calculate sum and average for each region"
    solution: |
      import csv
      from io import StringIO
      from collections import defaultdict

      csv_data = "region,sales\nEast,1000\nWest,1500\nEast,2000\nWest,1200\nEast,1800\n"

      file = StringIO(csv_data)
      csv_reader = csv.DictReader(file)

      stats = defaultdict(list)
      for row in csv_reader:
          region = row['region']
          sales = int(row['sales'])
          stats[region].append(sales)

      for region, sales_list in sorted(stats.items()):
          total = sum(sales_list)
          average = total / len(sales_list)
          print(f"{region}: total={total}, average={average:.2f}")

  - title: "CSV Data Transformation Pipeline"
    difficulty: advanced
    description: "Create a pipeline that reads CSV, transforms data, and outputs modified CSV."
    starter_code: |
      import csv
      from io import StringIO

      csv_data = "name,price,quantity\napple,1.20,5\nbanana,0.50,10\ncherry,2.00,3\n"

      # Transform: uppercase names, calculate total (price * quantity)
      # Output with new 'total' column

    expected_output: |
      name,price,quantity,total
      APPLE,1.20,5,6.00
      BANANA,0.50,10,5.00
      CHERRY,2.00,3,6.00
    hints:
      - "Use DictReader to read data"
      - "Transform name to uppercase"
      - "Calculate total as price * quantity"
      - "Add 'total' to fieldnames for DictWriter"
    solution: |
      import csv
      from io import StringIO

      csv_data = "name,price,quantity\napple,1.20,5\nbanana,0.50,10\ncherry,2.00,3\n"

      input_file = StringIO(csv_data)
      output_file = StringIO()

      csv_reader = csv.DictReader(input_file)
      fieldnames = csv_reader.fieldnames + ['total']
      csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)

      csv_writer.writeheader()
      for row in csv_reader:
          row['name'] = row['name'].upper()
          price = float(row['price'])
          quantity = int(row['quantity'])
          row['total'] = f"{price * quantity:.2f}"
          csv_writer.writerow(row)

      print(output_file.getvalue().strip())
```
<!-- EXERCISE_END -->
