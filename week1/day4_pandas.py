# ==========================================
# Day 4 — Wednesday: Pandas Fundamentals I
# ==========================================
# Task 4.1: Create Your First DataFrame

import pandas as pd

print("=== Pandas Day 4: Task 4.1 ===")

# 1. Build the DataFrame from the official dictionary
df = pd.DataFrame({
    "Name": ["Shahad", "Nora", "Reem", "Lina", "Sara", "Huda"],
    "Department": ["IT", "HR", "IT", "Finance", "IT", "HR"],
    "Salary": [8000, 7500, 9000, 8500, 7000, 7800],
    "Experience": [2, 5, 3, 7, 1, 4],
    "Rating": [4.5, 4.2, 4.8, 4.0, 3.9, 4.3],
})

# Print the full DataFrame
print("--- Full DataFrame ---")
print(df)

# 2. Inspect your DataFrame as required
print("\n--- Inspecting DataFrame ---")
print("Shape (rows, columns):", df.shape)
print("\nColumn names:", df.columns)
print("\nData types:\n", df.dtypes)

print("\n--- df.info() Full Summary ---")
df.info()

print("\n--- df.describe() Statistics ---")
print(df.describe())

print("\nFirst 3 rows:\n", df.head(3))
print("\nLast 2 rows:\n", df.tail(2))

# ==========================================
# Task 4.2: Load Data from Files
# ==========================================

print("\n=== Task 4.2: Load and Export File ===")

# Explicit path matching your actual Excel file
target_file_path = r"C:\Users\فارس\Desktop\ds-training\Practice_Dataset.xlsx"

# 1. Load the official Excel dataset using read_excel
df_excel = pd.read_excel(target_file_path)
print(f"Loaded {df_excel.shape[0]} rows and {df_excel.shape[1]} columns")

# 2. Inspect the dataset properties
print("\nFirst 5 rows:\n", df_excel.head())
print("\n--- df_excel.info() ---")
df_excel.info()
print("\n--- df_excel.describe() ---\n", df_excel.describe())

# 3. Export to a clean CSV file inside week1
import os
os.makedirs("week1", exist_ok=True)
df_excel.to_csv("week1/practice_data.csv", index=False)
print("\nSaved output to week1/practice_data.csv")

# ==========================================
# Task 4.3: Selecting Columns
# ==========================================

print("\n=== Task 4.3: Selecting Columns ===")

# 1. Select a single column using brackets (Returns a Series)
# Note: You can replace 'badge_number' with any column name from your excel, like 'name'
single_col = df_excel["badge_number"]
print("\n--- Single Column (Series) ---")
print(single_col.head(3))
print("Type of single_col:", type(single_col))

# 2. Select multiple columns using a list inside brackets (Returns a DataFrame)
multiple_cols = df_excel[["badge_number", "punch_count"]]
print("\n--- Multiple Columns (DataFrame) ---")
print(multiple_cols.head(3))
print("Type of multiple_cols:", type(multiple_cols))

# 3. Select using Dot Notation (Only works if column name has no spaces)
# df_excel.punch_count is equivalent to df_excel["punch_count"]
print("\n--- Dot Notation Selection ---")
print(df_excel.punch_count.head(2))

# ==========================================
# Task 4.4: Selecting Rows — loc & iloc
# ==========================================

print("\n=== Task 4.4: Selecting Rows — loc & iloc ===")

# 1. Using .iloc: Select by position number
print("\n--- .iloc: First Row (Index 0) ---")
print(df_excel.iloc[0])

print("\n--- .iloc: First 3 Rows ---")
print(df_excel.iloc[0:3])

print("\n--- .iloc: First 3 Rows and First 2 Columns ---")
print(df_excel.iloc[0:3, 0:2])


# 2. Using .loc: Select by label/name
print("\n--- .loc: Rows 0 to 2, Columns from badge_number to punch_count ---")
# Note: Ensure the column names exist in your Excel (e.g., 'badge_number' and 'punch_count')
print(df_excel.loc[0:2, "badge_number":"punch_count"])

print("\n--- .loc: Single Specific Value (Row 0, badge_number) ---")
print(df_excel.loc[0, "badge_number"])

# ==========================================
# Task 4.5: Filtering Rows with Conditions
# ==========================================

print("\n=== Task 4.5: Filtering Rows with Conditions ===")

# 1. Single condition: Find absent staff
absent_staff = df_excel[df_excel["status"] == "ABSENT"]
print(f"\nAbsent staff count: {len(absent_staff)}")

# 2. Multiple conditions: Use & with parentheses
# Present staff with punch count > 2
present_high = df_excel[(df_excel["status"] == "PRESENT") & (df_excel["punch_count"] > 2)]
print(f"Present staff with high punch count: {len(present_high)}")

# Challenge 1: Find rows with punch_count between 2 and 4
punch_range = df_excel[(df_excel["punch_count"] >= 2) & (df_excel["punch_count"] <= 4)]
print(f"\nPunch count between 2 and 4: {len(punch_range)}")

# Challenge 2: Technicians with punch_count >= 4
tech_high = df_excel[(df_excel["position"] == "TECHNICIAN") & (df_excel["punch_count"] >= 4)]
print(f"Technicians with high punch count: {len(tech_high)}")

# Challenge 3: Staff NOT in Administrator position
not_admin = df_excel[~(df_excel["position"] == "ADMINISTRATOR")]
print(f"Staff NOT administrator: {len(not_admin)}")


# ==========================================
# Task 4.6: Adding & Modifying Columns
# ==========================================

print("\n=== Task 4.6: Adding & Modifying Columns ===")

# 1. Add a new column by modifying an existing one (Uppercase names)
df_excel["Name_Upper"] = df_excel["position"].apply(lambda x: str(x).upper())

# 2. Add a new column based on a condition (High punch count flag)
df_excel["High_Punch"] = df_excel["punch_count"] >= 4

# Print the first 3 rows to see the new columns
print("\nDataFrame with new columns:")
print(df_excel[["badge_number", "position", "Name_Upper", "High_Punch"]].head(3))

# ==========================================
# Task 4.7: Sorting & Value Counts
# ==========================================

print("\n=== Task 4.7: Sorting & Value Counts ===")

# 1. Sort DataFrame by a column (Descending order)
sorted_df = df_excel.sort_values("punch_count", ascending=False)
print("\nTop 3 rows with highest punch count:")
print(sorted_df[["badge_number", "punch_count"]].head(3))

# 2. Count categories in a column
print("\nStatus value counts:")
print(df_excel["status"].value_counts())