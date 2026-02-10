"""
Custom sorting and searching algorithms for the CityBike platform.
Implementiert Merge Sort und Binary Search, sowie Benchmark-Funktionen.
"""

import time
import pandas as pd
from typing import List, Any, Tuple
import timeit


def merge_sort(arr: List[Any], key: str = None) -> List[Any]:
    """
    Implementierung des Merge-Sort-Algorithmus.
    
    Args:
        arr: Zu sortierende Liste (kann Liste von Dictionaries sein)
        key: Falls Dictionaries sortiert werden, Schlüssel zum Sortieren
        
    Returns:
        Sortierte Liste
    """
    if len(arr) <= 1:
        return arr
    
    # Teile die Liste in zwei Hälften
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    # Sortiere rekursiv beide Hälften
    left_sorted = merge_sort(left_half, key)
    right_sorted = merge_sort(right_half, key)
    
    # Füge die sortierten Hälften zusammen
    return _merge(left_sorted, right_sorted, key)


def _merge(left: List[Any], right: List[Any], key: str = None) -> List[Any]:
    """Merge two sorted lists."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        # Bestimme die zu vergleichenden Werte
        if key:
            left_val = left[i][key] if isinstance(left[i], dict) else getattr(left[i], key, None)
            right_val = right[j][key] if isinstance(right[j], dict) else getattr(right[j], key, None)
        else:
            left_val = left[i]
            right_val = right[j]
        
        # Vergleich
        if left_val <= right_val:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Füge restliche Elemente hinzu
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


def binary_search(arr: List[Any], target: Any, key: str = None) -> int:
    """
    Implementierung der binären Suche.
    
    Args:
        arr: Sortierte Liste, in der gesucht werden soll
        target: Zu suchender Wert
        key: Falls in Dictionaries gesucht wird, Schlüssel zum Vergleichen
        
    Returns:
        Index des gefundenen Elements oder -1 falls nicht gefunden
    """
    low = 0
    high = len(arr) - 1
    
    while low <= high:
        mid = (low + high) // 2
        
        # Bestimme den Vergleichswert
        if key:
            if isinstance(arr[mid], dict):
                mid_val = arr[mid][key]
            else:
                mid_val = getattr(arr[mid], key, None)
        else:
            mid_val = arr[mid]
        
        # Vergleich
        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
    
    return -1  # Nicht gefunden


def benchmark_sorting(data: List[Any], key: str = None, iterations: int = 100) -> dict:
    """
    Vergleicht die Performance von Merge Sort mit eingebauten Sortierfunktionen.
    
    Args:
        data: Zu sortierende Daten
        key: Schlüssel zum Sortieren (falls nötig)
        iterations: Anzahl der Wiederholungen für den Benchmark
        
    Returns:
        Dictionary mit Zeitmessungen
    """
    results = {}
    
    # 1. Custom Merge Sort
    print("⏱️  Benchmark: Custom Merge Sort...")
    custom_time = timeit.timeit(
        lambda: merge_sort(data.copy(), key),
        number=iterations
    ) / iterations
    results["custom_merge_sort"] = custom_time
    
    # 2. Python's built-in sorted()
    print("⏱️  Benchmark: Python sorted()...")
    if key:
        builtin_time = timeit.timeit(
            lambda: sorted(data.copy(), key=lambda x: x[key] if isinstance(x, dict) else getattr(x, key, None)),
            number=iterations
        ) / iterations
    else:
        builtin_time = timeit.timeit(
            lambda: sorted(data.copy()),
            number=iterations
        ) / iterations
    results["builtin_sorted"] = builtin_time
    
    # 3. Pandas sort_values() (falls DataFrame)
    if isinstance(data, pd.DataFrame):
        print("⏱️  Benchmark: Pandas sort_values()...")
        pandas_time = timeit.timeit(
            lambda: data.copy().sort_values(by=key if key else data.columns[0]),
            number=iterations
        ) / iterations
        results["pandas_sort_values"] = pandas_time
    elif isinstance(data[0], dict) and key:
        # Für Listen von Dictionaries simulieren wir Pandas
        print("⏱️  Benchmark: Pandas Simulation...")
        df = pd.DataFrame(data)
        pandas_time = timeit.timeit(
            lambda: df.copy().sort_values(by=key),
            number=iterations
        ) / iterations
        results["pandas_sort_values"] = pandas_time
    
    # Berechne Performance-Verhältnisse
    if "builtin_sorted" in results:
        results["custom_vs_builtin_ratio"] = custom_time / builtin_time
    
    return results


def benchmark_searching(sorted_data: List[Any], targets: List[Any], key: str = None) -> dict:
    """
    Vergleicht die Performance von Binary Search mit eingebauten Suchmethoden.
    
    Args:
        sorted_data: Sortierte Daten, in denen gesucht werden soll
        targets: Liste von zu suchenden Werten
        key: Schlüssel zum Suchen (falls nötig)
        
    Returns:
        Dictionary mit Zeitmessungen
    """
    results = {}
    
    # 1. Custom Binary Search
    print("🔍 Benchmark: Custom Binary Search...")
    start_time = time.time()
    for target in targets:
        binary_search(sorted_data, target, key)
    custom_time = (time.time() - start_time) / len(targets)
    results["custom_binary_search"] = custom_time
    
    # 2. Python's linear search (in operator)
    print("🔍 Benchmark: Python linear search (in)...")
    start_time = time.time()
    for target in targets:
        if key:
            target in [item[key] if isinstance(item, dict) else getattr(item, key, None) for item in sorted_data]
        else:
            target in sorted_data
    linear_time = (time.time() - start_time) / len(targets)
    results["linear_search_in"] = linear_time
    
    # 3. Pandas .loc[] (falls DataFrame oder Liste von Dictionaries)
    if isinstance(sorted_data, pd.DataFrame) or (sorted_data and isinstance(sorted_data[0], dict)):
        print("🔍 Benchmark: Pandas .loc[]...")
        if isinstance(sorted_data, pd.DataFrame):
            df = sorted_data
        else:
            df = pd.DataFrame(sorted_data)
        
        start_time = time.time()
        for target in targets:
            if key:
                df.loc[df[key] == target]
        pandas_time = (time.time() - start_time) / len(targets)
        results["pandas_loc"] = pandas_time
    
    return results


def print_benchmark_results(sort_results: dict, search_results: dict = None):
    """
    Gibt Benchmark-Ergebnisse formatiert aus.
    
    Args:
        sort_results: Ergebnisse der Sortier-Benchmarks
        search_results: Ergebnisse der Such-Benchmarks
    """
    print("\n" + "="*60)
    print("📊 BENCHMARK ERGEBNISSE")
    print("="*60)
    
    print("\n🔢 SORTIEREN:")
    for method, time_taken in sort_results.items():
        if "ratio" not in method:
            print(f"  {method:<25} {time_taken*1000:>8.3f} ms")
    
    if "custom_vs_builtin_ratio" in sort_results:
        ratio = sort_results["custom_vs_builtin_ratio"]
        print(f"\n  Custom vs Built-in Ratio: {ratio:.2f}x")
        if ratio > 1:
            print(f"  ⚠️  Custom ist {ratio:.1f}x langsamer als Built-in")
        else:
            print(f"  ✅ Custom ist {1/ratio:.1f}x schneller als Built-in")
    
    if search_results:
        print("\n🔍 SUCHEN:")
        for method, time_taken in search_results.items():
            print(f"  {method:<25} {time_taken*1000:>8.3f} ms")
    
    print("\n📈 KOMPLEXITÄTSANALYSE:")
    print("  Merge Sort:      O(n log n) Zeit, O(n) Speicher")
    print("  Binary Search:   O(log n) Zeit, O(1) Speicher")
    print("  Built-in sorted: O(n log n) Zeit (Timsort)")
    print("  Linear Search:   O(n) Zeit")
    
    print("\n💡 HINWEISE:")
    print("  - Built-in Funktionen sind optimiert und in C geschrieben")
    print("  - Custom Implementierungen sind didaktisch wertvoll")
    print("  - Für große Datensätze sind Built-in Funktionen meist schneller")


# Beispielverwendung
if __name__ == "__main__":
    print("🧪 Teste Algorithmen-Modul...")
    
    # Testdaten erstellen
    test_data = [
        {"id": 3, "name": "Charlie", "duration": 25},
        {"id": 1, "name": "Alice", "duration": 10},
        {"id": 2, "name": "Bob", "duration": 15},
        {"id": 4, "name": "David", "duration": 30},
    ]
    
    # Test Merge Sort
    print("\n1. Teste Merge Sort...")
    sorted_by_id = merge_sort(test_data.copy(), key="id")
    print(f"   Sortiert nach ID: {[item['id'] for item in sorted_by_id]}")
    
    sorted_by_duration = merge_sort(test_data.copy(), key="duration")
    print(f"   Sortiert nach Dauer: {[item['duration'] for item in sorted_by_duration]}")
    
    # Test Binary Search
    print("\n2. Teste Binary Search...")
    sorted_data = merge_sort(test_data.copy(), key="id")
    index = binary_search(sorted_data, target=2, key="id")
    print(f"   Suche ID=2: Index {index}, Name: {sorted_data[index]['name'] if index != -1 else 'Nicht gefunden'}")
    
    # Test Benchmarks
    print("\n3. Führe Benchmarks aus...")
    sort_results = benchmark_sorting(test_data, key="duration", iterations=1000)
    search_results = benchmark_searching(sorted_data, targets=[1, 2, 3, 4], key="id")
    
    print_benchmark_results(sort_results, search_results)