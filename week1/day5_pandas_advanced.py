import pandas as pd
import numpy as np

# Load the official dataset
target_file_path = r"C:\Users\فارس\Desktop\ds-training\Practice_Dataset.xlsx"
df_excel = pd.read_excel(target_file_path)

print("=== Task 5.1: GroupBy & Aggregation ===")

# 1. Simple GroupBy: Average punch count per position
dept_avg = df_excel.groupby("position")["punch_count"].mean()
print("\nAverage punch count by position:")
print(dept_avg)

# 2. Named Aggregations: Clean summary with custom column names
summary = df_excel.groupby("position").agg(
    avg_punch=("punch_count", "mean"),
    max_punch=("punch_count", "max"),
    min_punch=("punch_count", "min"),
    total_staff=("position", "count")
).reset_index()

print("\nDetailed Position Summary:")
print(summary)

# ==========================================
# Task 5.2: Merge & Join
# ==========================================

print("\n=== Task 5.2: Merge & Join ===")

# --- 1. Exact Code From The Document ---

# Table 1: Employees
employees = pd.DataFrame({
    "emp_id": [1, 2, 3, 4, 5],
    "name": ["Shahad", "Nora", "Reem", "Lina", "Sara"],
    "dept_id": [10, 20, 10, 30, 40],  # Note: 40 has no match
})

# Table 2: Departments
departments = pd.DataFrame({
    "dept_id": [10, 20, 30],           # Note: no dept 40
    "dept_name": ["IT", "HR", "Finance"],
})

# Inner join (only matching rows)
inner = pd.merge(employees, departments, on="dept_id", how="inner")
print("INNER JOIN:\n", inner)   # Sara (dept 40) is dropped

# Left join (keep all employees)
left = pd.merge(employees, departments, on="dept_id", how="left")
print("LEFT JOIN:\n", left)     # Sara shows NaN for dept_name


# --- 2. Additional Required Joins & Functions ---

# Right join (keep all departments)
right = pd.merge(employees, departments, on="dept_id", how="right")
print("RIGHT JOIN:\n", right)

# Outer join (keep everything)
outer = pd.merge(employees, departments, on="dept_id", how="outer")
print("OUTER JOIN:\n", outer)

# Practice merging on different column names using left_on= and right_on=
departments_diff_col = pd.DataFrame({
    "id_of_dept": [10, 20, 30],
    "dept_name": ["IT", "HR", "Finance"],
})
diff_names_merge = pd.merge(employees, departments_diff_col, left_on="dept_id", right_on="id_of_dept", how="inner")
print("MERGE WITH DIFFERENT COLUMN NAMES:\n", diff_names_merge.head(2))

# Concatenate (stack rows)
jan = pd.DataFrame({"month": ["Jan"]*3, "sales": [100, 200, 150]})
feb = pd.DataFrame({"month": ["Feb"]*3, "sales": [120, 180, 160]})
combined = pd.concat([jan, feb], ignore_index=True)
print("COMBINED (CONCAT):\n", combined)

# ==========================================
# Task 5.3: Descriptive Statistics & Missing Data
# ==========================================

print("\n=== Task 5.3: Descriptive Statistics & Missing Data ===")

# Quick overview
print("=== Shape ===")
print(df_excel.shape)

print("\n=== Numeric Summary ===")
print(df_excel.describe())

print("\n=== Category Counts ===")
for col in df_excel.select_dtypes(include='object').columns:
    print(f"\n{col}:")
    print(df_excel[col].value_counts())

print("\n=== Missing Values ===")
print(df_excel.isnull().sum())
print(f"Total missing: {df_excel.isnull().sum().sum()}")

print("\n=== Duplicates ===")
print(f"Duplicate rows: {df_excel.duplicated().sum()}")

print("\n=== Correlation ===")
print(df_excel.corr(numeric_only=True).round(2))