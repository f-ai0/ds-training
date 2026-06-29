# ==========================================
# Day 3 — Tuesday: NumPy Fundamentals
# ==========================================
# Task 3.1: Creating Arrays

import numpy as np

print("=== NumPy Day 3: Task 3.1 ===")

# 1. Creating arrays using different methods
a = np.array([1, 2, 3, 4, 5])                # From list
b = np.zeros((3, 4))                           # 3x4 matrix of zeros
c = np.ones((2, 3))                            # 2x3 matrix of ones
d = np.arange(0, 20, 2)                        # [0, 2, 4, ..., 18]
e = np.linspace(0, 1, 5)                       # [0, 0.25, 0.5, 0.75, 1.0]
f = np.eye(4)                                  # 4x4 identity matrix
g = np.full((3, 3), 7)                         # 3x3 filled with 7

# 2. Check and print properties of each array
print("\n--- Array Properties ---")
print(f"Array 'a' -> Shape: {a.shape}, Dims: {a.ndim}, Type: {a.dtype}, Size: {a.size}")
print(f"Array 'b' -> Shape: {b.shape}, Dims: {b.ndim}, Type: {b.dtype}, Size: {b.size}")
print(f"Array 'c' -> Shape: {c.shape}, Dims: {c.ndim}, Type: {c.dtype}, Size: {c.size}")
print(f"Array 'd' -> Shape: {d.shape}, Dims: {d.ndim}, Type: {d.dtype}, Size: {d.size}")
print(f"Array 'e' -> Shape: {e.shape}, Dims: {e.ndim}, Type: {e.dtype}, Size: {e.size}")
print(f"Array 'f' -> Shape: {f.shape}, Dims: {f.ndim}, Type: {f.dtype}, Size: {f.size}")
print(f"Array 'g' -> Shape: {g.shape}, Dims: {g.ndim}, Type: {g.dtype}, Size: {g.size}")

# 3. Create a 3D array and check its structure
array_3d = np.zeros((2, 3, 4))
print("\n--- 3D Array Visualization ---")
print(f"3D Array -> Shape: {array_3d.shape}, Dimensions: {array_3d.ndim}")

# ==========================================
# Task 3.2: Indexing & Slicing
# ==========================================

print("\n=== NumPy Day 3: Task 3.2 ===")

# 1. Create a 2D array
data = np.array([
    [10, 20, 30, 40],
    [50, 60, 70, 80],
    [90, 100, 110, 120]
])

# 2. Basic indexing
print("Top-left (0,0):", data[0, 0])
print("Bottom-right (2,3):", data[2, 3])
print("Bottom-right alternative (-1,-1):", data[-1, -1])

# 3. Slicing
print("First row:", data[0, :])
print("Second column:", data[:, 1])
print("Sub-matrix (Rows 0-1, Cols 1-2):\n", data[0:2, 1:3])

# 4. Boolean indexing (filtering)
print("Elements > 50:", data[data > 50])
print("Divisible by 20:", data[data % 20 == 0])

# 5. Fancy indexing
print("Rows 0 and 2:\n", data[[0, 2], :])

# 6. Additional exercises from lines 98-101
print("Last two rows:\n", data[-2:, :])
print("Columns 1 and 3 only:\n", data[:, [0, 2]])
print("Values between 30 and 90:", data[(data >= 30) & (data <= 90)])

# 7. Replace all values less than 50 with 0
# We take a copy first to avoid changing the original array permanently if needed later
data_modified = data.copy()
data_modified[data_modified < 50] = 0
print("Array after replacing values < 50 with 0:\n", data_modified)

# ==========================================
# Task 3.3: Math Operations
# ==========================================

print("\n=== NumPy Day 3: Task 3.3 ===")

# 1. Element-wise operations practice
arr_a = np.array([10, 20, 30, 40, 50])
arr_b = np.array([1, 2, 3, 4, 5])

print("Element-wise addition (a + b):", arr_a + arr_b)
print("Element-wise multiplication (a * 2):", arr_a * 2)
print("Element-wise power (a ** 2):", arr_a ** 2)
print("Element-wise division (a / arr_b):", arr_a / arr_b)

# 2. Aggregation functions with a 2D array (Scores)
scores = np.array([
    [85, 92, 78],    # Student 1: Math, Science, English
    [95, 88, 72],    # Student 2
    [90, 85, 95],    # Student 3
])

print("\n--- Scores Aggregations ---")
print("Overall mean:", np.mean(scores))
print("Mean per student (row - axis=1):", np.mean(scores, axis=1))
print("Mean per subject (col - axis=0):", np.mean(scores, axis=0))
print("Max per student (axis=1):", np.max(scores, axis=1))
print("Std per subject (axis=0):", np.std(scores, axis=0))

# ==========================================
# Task 3.4: Reshaping & Random Data
# ==========================================

print("\n=== NumPy Day 3: Task 3.4 ===")

# 1. Reshaping practice
arr_1d = np.arange(1, 13)
print("Original 1D array:", arr_1d)
print("Reshaped to 3x4:\n", arr_1d.reshape(3, 4))
print("Reshaped to 4x3:\n", arr_1d.reshape(4, 3))
print("Reshaped to 3D (2x2x3):\n", arr_1d.reshape(2, 2, 3))

# Flatten and Transpose
arr_2d = np.array([[1, 2], [3, 4], [5, 6]])
print("\nOriginal 2D array:\n", arr_2d)
print("Flattened array:", arr_2d.flatten())
print("Transposed matrix (.T):\n", arr_2d.T)

# 2. Random Data Generation and Analysis
np.random.seed(42) # Ensures same results every run

rand_uniform = np.random.rand(1000)       # 1000 values between 0-1
rand_normal = np.random.randn(1000)       # 1000 from normal distribution
rand_ints = np.random.randint(1, 100, 50) # 50 random ints from 1-99

print("\n--- Random Data Analysis ---")
print(f"Uniform: mean={rand_uniform.mean():.3f}, std={rand_uniform.std():.3f}")
print(f"Normal:  mean={rand_normal.mean():.3f}, std={rand_normal.std():.3f}")
print(f"Ints:    min={rand_ints.min()}, max={rand_ints.max()}")

# ==========================================
# Task 3.5: NumPy Mini-Challenge
# ==========================================

print("\n=== NumPy Day 3: Task 3.5 (Mini-Challenge) ===")

# Exercise 1: 5x5 Matrix and Diagonal
matrix_5x5 = np.arange(1, 26).reshape(5, 5)
diagonal_elements = np.diag(matrix_5x5)

print("--- Exercise 1 ---")
print("5x5 Matrix:\n", matrix_5x5)
print("Diagonal elements:", diagonal_elements)


# Exercise 2: Exam Scores Analysis
np.random.seed(42) # Fixed seed for consistency
scores_100 = np.random.randint(50, 101, 100)
mean_score = np.mean(scores_100)
above_80_count = np.sum(scores_100 > 80)
top_5_scores = np.sort(scores_100)[-5:][::-1] # Sort and get last 5, then reverse for descending

print("\n--- Exercise 2 ---")
print(f"Mean Score: {mean_score:.2f}")
print(f"Number of scores above 80: {above_80_count}")
print("Top 5 Scores:", top_5_scores)


# Exercise 3: Matrix Multiplication
matrix_A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
matrix_B = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
matrix_product = matrix_A @ matrix_B # or np.dot(matrix_A, matrix_B)

print("\n--- Exercise 3 ---")
print("Matrix Product (A @ B):\n", matrix_product)


# Exercise 4: Heights Standard Deviation Analysis
heights = np.random.randint(155, 196, 1000)
mean_height = np.mean(heights)
std_height = np.std(heights)

# Lower and upper bounds for 1 standard deviation
lower_bound = mean_height - std_height
upper_bound = mean_height + std_height

# Filter heights within 1 standard deviation
within_1_std = np.sum((heights >= lower_bound) & (heights <= upper_bound))

print("\n--- Exercise 4 ---")
print(f"Mean Height: {mean_height:.2f} cm, Std: {std_height:.2f} cm")
print(f"Heights within 1 Standard Deviation ({lower_bound:.2f} to {upper_bound:.2f}): {within_1_std} out of 1000")