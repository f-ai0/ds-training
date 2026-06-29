# Numbers
age = 22                  # int
gpa = 3.85                # float

# Strings
name = "Shahad"
greeting = f"Hello, {name}! GPA: {gpa}"

# Boolean
is_active = True

# Collections
scores = [85, 92, 78, 95]              # list
coords = (25.3, 45.6)                  # tuple
unique_ids = {101, 102, 103}           # set
student = {"name": "Shahad", "major": "CS", "gpa": 3.85}  # dict

# String methods practice
print("=== String Methods ===")
print(name.upper())
print(name.lower())
print(greeting.strip())
print(greeting.split())
print(greeting.replace("Shahad", "Sara"))
print(greeting.startswith("Hello"))

# Type conversion practice
print("\n=== Type Conversion ===")
print(int(gpa))
print(float(age))
print(str(is_active))
print(list(coords))

# Check types using type()
print("\n=== Type Verification ===")
print(type(age))
print(type(gpa))
print(type(name))
print(type(is_active))
print(type(scores))
print(type(coords))
print(type(unique_ids))
print(type(student))

# ==========================================
# Task 2.2: Control Flow — if/elif/else
# ==========================================

print("\n=== Control Flow Practice ===")

# Test scores from the task requirements
scores_to_test = [95, 87, 73, 61, 45, 99]

for score in scores_to_test:
    if score >= 90:
        grade = "A"
        if score > 95:
            print("Excellent!")
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    print(f"Score: {score} -> Grade: {grade}")
    
# ==========================================
# Task 2.3: Loops
# ==========================================

print("\n=== Loops Practice ===")

# 1. Enumerate departments
departments = ["IT", "HR", "Finance", "Marketing", "Operations"]
for i, dept in enumerate(departments):
    print(f"{i+1}. {dept}")

# 2. While loop countdown
print("\nCountdown:")
countdown = 10
while countdown >= 1:
    print(countdown)
    countdown -= 1
print("Launch!")

# 3. Sum of even numbers from 1 to 100
even_sum = 0
for n in range(1, 101):
    if n % 2 == 0:
        even_sum += n
print(f"\nSum of even numbers 1-100: {even_sum}")

# 4. Break and continue practice
print("\nFinding first number divisible by 7 and 3:")
for n in range(1, 100):
    if n % 7 == 0 and n % 3 == 0:
        print(f"Found: {n}")
        break
    
    
    # ==========================================
# Task 2.4: List Comprehensions
# ==========================================

print("\n=== List Comprehensions Practice ===")

numbers = list(range(1, 21))
names = ["alice", "bob", "charlie", "diana"]

# 1. Basic patterns
squares = [n**2 for n in numbers]
evens = [n for n in numbers if n % 2 == 0]
even_squares = [n**2 for n in numbers if n % 2 == 0]

print("Squares:", squares)
print("Evens:", evens)
print("Even Squares:", even_squares)

# 2. String operations
upper_names = [name.upper() for name in names]
long_names = [name for name in names if len(name) > 4]
name_lengths = {name: len(name) for name in names}

print("Upper Names:", upper_names)
print("Long Names:", long_names)
print("Name Lengths:", name_lengths)

# 3. Celsius to Fahrenheit conversion
celsius_temps = [0, 10, 20, 30, 40]
fahrenheit_temps = [(c * 9/5) + 32 for c in celsius_temps]
print("Fahrenheit Temperatures:", fahrenheit_temps)

# 4. Extract words longer than 5 characters
sentence = "Data Science and Machine Learning are amazing fields"
long_words = [word for word in sentence.split() if len(word) > 5]
print("Words longer than 5 chars:", long_words)

# ==========================================
# Task 2.5: Functions
# ==========================================

print("\n=== Functions Practice ===")

# 1. Basic statistics function
def basic_stats(numbers):
    return {
        "count": len(numbers),
        "mean": sum(numbers) / len(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "range": max(numbers) - min(numbers),
    }

scores = [85, 92, 78, 95, 88, 76, 90]
stats = basic_stats(scores)
print("Basic Statistics:")
for key, value in stats.items():
    print(f"{key}: {value}")

# 2. Function with default parameters
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

print("\nGreeting Practice:")
greet("Shahad")                  # Uses default "Hello"
greet("Sara", "Good morning")    # Overrides default

# 3. Function with *args for average
def calculate_average(*args):
    if len(args) == 0:
        return 0
    return sum(args) / len(args)

print("\n*args Average Practice:")
print("Average:", calculate_average(10, 20, 30, 40, 50))

# 4. Lambda function with map()
double = lambda x: x * 2
numbers_list = [1, 2, 3, 4, 5]
doubled_numbers = list(map(double, numbers_list))

print("\nLambda and map() Practice:")
print("Original:", numbers_list)
print("Doubled:", doubled_numbers)


# ==========================================
# Task 2.6: File I/O
# ==========================================

import csv

print("\n=== File I/O Practice ===")

# 1. Create and write to a text file (تعديل المسار هنا)
with open("training_log.txt", "w") as f:
    f.write("=== Training Log ===\n")
    f.write("Day 1: Environment setup complete\n")
    f.write("Day 2: Python review complete\n")

# 2. Read the entire file back
print("Reading full file content:")
with open("training_log.txt", "r") as f:
    content = f.read()
    print(content)

# 3. Read line by line with line numbers
print("Reading line by line:")
with open("training_log.txt", "r") as f:
    for line_num, line in enumerate(f, 1):
        print(f"Line {line_num}: {line.strip()}")

# 4. Create a CSV file manually using python's csv module (تعديل المسار هنا)
csv_data = [
    ["id", "name", "department"],
    [1, "Shahad", "CS"],
    [2, "Sara", "IT"]
]

with open("students.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)

print("\nCSV file 'students.csv' created successfully!")