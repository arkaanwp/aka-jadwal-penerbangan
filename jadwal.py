import csv
import time
import sys
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import os

# Increase recursion limit for recursive implementation
sys.setrecursionlimit(10000)

def load_flight_data_from_csv(filename):
    """Load flight schedule data from CSV file"""
    flights = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                flights.append(row['flight_time'])
        return flights
    except FileNotFoundError:
        print(f"Error: File {filename} tidak ditemukan!")
        print("Silakan jalankan file generator terlebih dahulu.")
        sys.exit(1)

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

# Insertion Sort - Recursive (More Naive/Inefficient Version)
def insertion_sort_recursive(arr, n=None):
    if n is None:
        # Initial call: convert to minutes
        times = [time_to_minutes(t) for t in arr]
        result = insertion_sort_recursive_helper(times[:])  # Create copy
        return [minutes_to_time(t) for t in result]

def insertion_sort_recursive_helper(arr):
    """Pure recursive helper with more overhead - creates new arrays"""
    # Base case: array with 0 or 1 element is already sorted
    if len(arr) <= 1:
        return arr
    
    # Recursively sort all elements except the last one
    # This creates a NEW array each time (more overhead)
    sorted_subarray = insertion_sort_recursive_helper(arr[:-1])
    
    # Insert the last element into the sorted subarray
    last_element = arr[-1]
    result = insert_into_sorted_recursive(sorted_subarray, last_element)
    
    return result

def insert_into_sorted_recursive(sorted_arr, element):
    """
    Recursively insert element into sorted array
    Creates new arrays at each step for maximum overhead
    """
    # Base case: empty array
    if len(sorted_arr) == 0:
        return [element]
    
    # Base case: element should be inserted at the beginning
    if element < sorted_arr[0]:
        return [element] + sorted_arr
    
    # Recursive case: insert into the rest of the array
    # This creates NEW arrays and list concatenations (inefficient)
    return [sorted_arr[0]] + insert_into_sorted_recursive(sorted_arr[1:], element)

# Main Analysis
print("=" * 60)
print("ANALISIS PERBANDINGAN INSERTION SORT")
print("Iterative vs Recursive pada Jadwal Penerbangan")
print("=" * 60)
print()

# Load datasets from CSV
data_sizes = [100, 500, 1000, 2000]
datasets = {}

print("Ambil Data dari CSV")
print()

for size in data_sizes:
    filename = f"flight_data/flight_schedule_{size}.csv"
    datasets[size] = load_flight_data_from_csv(filename)
    print(f"Mengambil {size} data dari {filename}")

print()

# Display sample data
print("Contoh Data Jadwal Penerbangan (5 data pertama):")
sample = datasets[500][:5]
print(f"Sebelum sort: {sample}")
print(f"Setelah sort:  {insertion_sort_iterative(sample.copy())}")
print()

# Benchmarking with progressive visualization
iterative_times = []
recursive_times = []

print()

# Setup figure for progressive plotting
plt.figure(figsize=(10, 6))
plt.ion()  # Turn on interactive mode

for idx, size in enumerate(data_sizes, 1):
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
    print(f"=== Hasil Benchmark {idx}/{len(data_sizes)} ===")
    print(table)
    print()
    
    # Update plot progressively
    plt.clf()  # Clear previous plot
    
    # Plot data up to current iteration
    current_sizes = data_sizes[:len(iterative_times)]
    
    plt.plot(current_sizes, iterative_times, marker='o', linewidth=2, 
             markersize=8, label='Iterative', color='#2E86AB')
    plt.plot(current_sizes, recursive_times, marker='s', linewidth=2, 
             markersize=8, label='Recursive', color='#A23B72')
    
    plt.xlabel("Jumlah Data Jadwal Penerbangan", fontsize=12, fontweight='bold')
    plt.ylabel("Waktu Eksekusi (detik)", fontsize=12, fontweight='bold')
    plt.title("Perbandingan Insertion Sort: Iterative vs Recursive\nPada Jadwal Penerbangan", 
              fontsize=14, fontweight='bold', pad=20)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.draw()
    plt.pause(1)  # Pause to show the plot
    
    time.sleep(0.5)  # Small delay for readability

plt.ioff()  # Turn off interactive mode
print("="*60)

# Analysis
print()
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
print("- Recursive versi ini juga membuat array baru setiap rekursi (overhead memori)")
print("- Untuk production: gunakan Iterative")
print("-" * 60)

# Keep the final plot displayed
plt.show()

