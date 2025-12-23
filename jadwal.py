import random
import time
import sys
import matplotlib.pyplot as plt
from prettytable import PrettyTable

# Increase recursion limit for recursive implementation
# Default is ~1000, we need more for large datasets
sys.setrecursionlimit(10000)

def generate_flight_schedule(n):
    """Generate random flight times in HH:MM format"""
    flights = []
    for _ in range(n):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        flights.append(f"{hour:02d}:{minute:02d}")
    return flights

def time_to_minutes(time_str):
    """Convert HH:MM to minutes for comparison"""
    hour, minute = map(int, time_str.split(':'))
    return hour * 60 + minute

def minutes_to_time(minutes):
    """Convert minutes back to HH:MM format"""
    hour = minutes // 60
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"

# Insertion Sort - Iterative
def insertion_sort_iterative(arr):
    # Convert to minutes for sorting
    times = [time_to_minutes(t) for t in arr]
    
    for i in range(1, len(times)):
        key = times[i]
        j = i - 1
        while j >= 0 and times[j] > key:
            times[j + 1] = times[j]
            j -= 1
        times[j + 1] = key
    
    # Convert back to HH:MM format
    return [minutes_to_time(t) for t in times]

# Insertion Sort - Recursive (Pure Recursive)
def insertion_sort_recursive(arr, n=None):
    if n is None:
        # Initial call: convert to minutes
        times = [time_to_minutes(t) for t in arr]
        result = insertion_sort_recursive_helper(times, len(times))
        return [minutes_to_time(t) for t in result]

def insertion_sort_recursive_helper(arr, n):
    # Base case: array with 0 or 1 element is already sorted
    if n <= 1:
        return arr
    
    # Recursively sort first n-1 elements
    insertion_sort_recursive_helper(arr, n - 1)
    
    # Insert nth element using recursive insertion
    last = arr[n - 1]
    insert_recursive(arr, n - 2, last, n - 1)
    
    return arr

def insert_recursive(arr, j, key, pos):
    """Recursive function to insert key at correct position"""
    # Base case: reached beginning
    if j < 0:
        arr[0] = key
        return
    
    # Base case: found correct position
    if arr[j] <= key:
        arr[j + 1] = key
        return
    
    # Shift element and recursively insert
    arr[j + 1] = arr[j]
    insert_recursive(arr, j - 1, key, j)

# Generate datasets
data_sizes = [100, 500, 1000, 2000]
datasets = {size: generate_flight_schedule(size) for size in data_sizes}

print("=" * 60)
print("ANALISIS PERBANDINGAN INSERTION SORT")
print("Iterative vs Recursive pada Jadwal Penerbangan")
print("=" * 60)
print()

# Display sample data
print("Contoh Data Jadwal Penerbangan (5 data pertama):")
sample = datasets[100][:5]
print(f"Sebelum sort: {sample}")
print(f"Setelah sort:  {insertion_sort_iterative(sample.copy())}")
print()

# Benchmarking
iterative_times = []
recursive_times = []

print("Mengukur waktu eksekusi...")
print()

for size in data_sizes:
    data = datasets[size]
    
    # Iterative
    start = time.time()
    insertion_sort_iterative(data.copy())
    iter_time = time.time() - start
    iterative_times.append(iter_time)
    
    # Recursive
    start = time.time()
    insertion_sort_recursive(data.copy())
    rec_time = time.time() - start
    recursive_times.append(rec_time)
    
    diff = abs(rec_time - iter_time)
    
    # Create new table for each iteration
    table = PrettyTable()
    table.field_names = ["Jumlah Data", "Iterative (s)", "Recursive (s)", "Selisih (s)"]
    
    # Add all results up to current iteration
    for i in range(len(iterative_times)):
        table.add_row([
            data_sizes[i],
            f"{iterative_times[i]:.6f}",
            f"{recursive_times[i]:.6f}",
            f"{abs(recursive_times[i] - iterative_times[i]):.6f}"
        ])
    
    # Print table after each benchmark
    print(table)
    print()
    time.sleep(0.5)  # Small delay for readability

# Analysis
print("ANALISIS:")
print("-" * 60)
avg_iter = sum(iterative_times) / len(iterative_times)
avg_rec = sum(recursive_times) / len(recursive_times)

if avg_iter < avg_rec:
    faster = "Iterative"
    percentage = ((avg_rec - avg_iter) / avg_rec) * 100
else:
    faster = "Recursive"
    percentage = ((avg_iter - avg_rec) / avg_iter) * 100

print(f"Rata-rata waktu Iterative: {avg_iter:.6f} detik")
print(f"Rata-rata waktu Recursive: {avg_rec:.6f} detik")
print(f"\n{faster} lebih cepat rata-rata {percentage:.2f}%")
print()
print("KESIMPULAN:")
print("- Iterative umumnya lebih efisien (overhead function call lebih kecil)")
print("- Recursive menggunakan call stack, risiko stack overflow pada data besar")
print("- Untuk production: gunakan Iterative")
print("-" * 60)

# Visualization
plt.figure(figsize=(10, 6))

plt.plot(data_sizes, iterative_times, marker='o', linewidth=2, 
         markersize=8, label='Iterative', color='#2E86AB')
plt.plot(data_sizes, recursive_times, marker='s', linewidth=2, 
         markersize=8, label='Recursive', color='#A23B72')

plt.xlabel("Jumlah Data Jadwal Penerbangan", fontsize=12, fontweight='bold')
plt.ylabel("Waktu Eksekusi (detik)", fontsize=12, fontweight='bold')
plt.title("Perbandingan Insertion Sort: Iterative vs Recursive\nPada Jadwal Penerbangan", 
          fontsize=14, fontweight='bold', pad=20)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.show()
