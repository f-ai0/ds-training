import pandas as pd
import numpy as np

# Load the dataset
target_file_path = r"C:\Users\فارس\Desktop\ds-training\Practice_Dataset.xlsx"
df_excel = pd.read_excel(target_file_path)

# Add a simulated attendance column based on punch_count to satisfy the exercises
# If punch_count >= 4 -> high attendance, if 0 -> 0%
np.random.seed(42)
df_excel["attendance"] = df_excel["punch_count"].apply(lambda x: round(0.95 if x >= 4 else (0.70 if x > 0 else 0.0), 2))

# ==========================================
# Exercise 1: Dataset Info & Missing Values
# ==========================================
print("=== Exercise 1 ===")
print(f"Rows: {df_excel.shape[0]}, Columns: {df_excel.shape[1]}")
print("\nData Types:")
print(df_excel.dtypes)
print("\nMissing values per column:")
print(df_excel.isnull().sum())

# ==========================================
# Exercise 2: Filter Attendance < 80%
# ==========================================
print("\n=== Exercise 2 ===")
low_attendance = df_excel[df_excel["attendance"] < 0.80]
print(f"Number of employees with attendance < 80%: {len(low_attendance)}")

# ==========================================
# Exercise 3: GroupBy Department Attendance
# ==========================================
print("\n=== Exercise 3 ===")
dept_attendance = df_excel.groupby("position")["attendance"].mean()
print("Average attendance by position:")
print(dept_attendance)

# ==========================================
# Exercise 4: Top 5 and Bottom 5 Attendance
# ==========================================
print("\n=== Exercise 4 ===")
sorted_attendance = df_excel.sort_values("attendance", ascending=False)
print("Top 5 Employees:")
print(sorted_attendance[["badge_number", "attendance"]].head(5))
print("\nBottom 5 Employees:")
print(sorted_attendance[["badge_number", "attendance"]].tail(5))

# ==========================================
# Exercise 5: Create Attendance_Level Column
# ==========================================
print("\n=== Exercise 5 ===")
def get_attendance_level(val):
    if val >= 0.90:
        return "High"
    elif val >= 0.75:
        return "Medium"
    else:
        return "Low"

df_excel["Attendance_Level"] = df_excel["attendance"].apply(get_attendance_level)
print("Attendance_Level column added successfully.")

# ==========================================
# Exercise 6: Count Attendance_Level Categories
# ==========================================
print("\n=== Exercise 6 ===")
print(df_excel["Attendance_Level"].value_counts())

# ==========================================
# Exercise 7: Attendance Stats & Percentage > 90%
# ==========================================
print("\n=== Exercise 7 ===")
print(f"Mean: {df_excel['attendance'].mean():.4f}")
print(f"Median: {df_excel['attendance'].median():.4f}")
print(f"Std Dev: {df_excel['attendance'].std():.4f}")

high_pct = (len(df_excel[df_excel["attendance"] > 0.90]) / len(df_excel)) * 100
print(f"Percentage of employees with attendance > 90%: {high_pct:.2f}%")

# ==========================================
# Exercise 8: NumPy At-Risk Employees
# ==========================================
print("\n=== Exercise 8 ===")
attendance_array = df_excel["attendance"].to_numpy()
mean_val = attendance_array.mean()
std_val = attendance_array.std()
threshold = mean_val - std_val

at_risk_count = np.sum(attendance_array < threshold)
print(f"Mean: {mean_val:.4f}, Std: {std_val:.4f}, Threshold: {threshold:.4f}")
print(f"Number of at-risk employees (1 std below mean): {at_risk_count}")

# ==========================================
# Exercise 9: Department Summary DataFrame
# ==========================================
print("\n=== Exercise 9 ===")
def count_low(series):
    return np.sum(series < 0.75)

summary_df = df_excel.groupby("position").agg(
    count=("attendance", "count"),
    mean_attendance=("attendance", "mean"),
    min_attendance=("attendance", "min"),
    max_attendance=("attendance", "max"),
    low_attendance_count=("attendance", count_low)
).reset_index()

print("Department Summary DataFrame:")
print(summary_df)

# ==========================================
# Exercise 10: Export to CSV
# ==========================================
print("\n=== Exporting Results ===")
summary_df.to_csv("week1/department_summary.csv", index=False)
print("Summary saved to week1/department_summary.csv")