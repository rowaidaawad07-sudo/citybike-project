"""
Custom sorting and searching algorithms.

Provided:
    - merge_sort
    - benchmark_sort

Students must implement:
    - insertion_sort   — second sorting algorithm
    - binary_search    — search on sorted data
    - linear_search    — brute-force search for comparison
    - benchmark_search — timing comparison for search algorithms

Use timeit to measure execution times.
Document the Big-O complexity of each algorithm.
"""

import timeit
from collections.abc import Callable
from typing import Any


# ---------------------------------------------------------------------------
# Sorting — Merge Sort
# ---------------------------------------------------------------------------

def merge_sort(data: list[Any], key: Callable = lambda x: x) -> list[Any]:
    """Sort *data* using the merge-sort algorithm.

    Args:
        data: List of items to sort.
        key: Function that extracts a comparison key from each item.

    Returns:
        A new sorted list.

    Complexity:
        Time  — O(n log n)
        Space — O(n)
    """
    if len(data) <= 1:
        return list(data)

    mid = len(data) // 2
    left = merge_sort(data[:mid], key=key)
    right = merge_sort(data[mid:], key=key)

    return _merge(left, right, key=key)


def _merge(
    left: list[Any], right: list[Any], key: Callable
) -> list[Any]:
    """Merge two sorted lists into one sorted list."""
    result: list[Any] = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------------------------
# Sorting — Insertion Sort
# ---------------------------------------------------------------------------

def insertion_sort(data: list[Any], key: Callable = lambda x: x) -> list[Any]:
    """Sort *data* using the insertion-sort algorithm.

    Args:
        data: List of items to sort.
        key: Function that extracts a comparison key from each item.

    Returns:
        A new sorted list (the original is not modified).

    Complexity:
        Time  — O(n²) worst / average, O(n) best (already sorted)
        Space — O(n) for the copy
    """
    arr = list(data)  # copy input

    for i in range(1, len(arr)):
        current = arr[i]
        current_key = key(current)
        j = i - 1

        # shift larger elements to the right
        while j >= 0 and key(arr[j]) > current_key:
            arr[j + 1] = arr[j]
            j -= 1

        # insert current element
        arr[j + 1] = current

    return arr


# ---------------------------------------------------------------------------
# Searching — Binary Search
# ---------------------------------------------------------------------------

def binary_search(
    sorted_data: list[Any],
    target: Any,
    key: Callable = lambda x: x,
) -> int | None:
    """Search for *target* in a sorted list using binary search.

    Args:
        sorted_data: A list sorted in ascending order by *key*.
        target: The value to search for.
        key: Function that extracts the comparison value from each item.

    Returns:
        The index of the found item, or None if not found.

    Complexity:
        Time  — O(log n)
        Space — O(1)
    """
    low, high = 0, len(sorted_data) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = key(sorted_data[mid])

        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return None


# ---------------------------------------------------------------------------
# Searching — Linear Search
# ---------------------------------------------------------------------------

def linear_search(
    data: list[Any],
    target: Any,
    key: Callable = lambda x: x,
) -> int | None:
    """Search for *target* by scanning every element in *data*.

    Args:
        data: List of items (does not need to be sorted).
        target: The value to search for.
        key: Function that extracts the comparison value from each item.

    Returns:
        The index of the first matching item, or None if not found.

    Complexity:
        Time  — O(n)
        Space — O(1)
    """
    for i, item in enumerate(data):
        if key(item) == target:
            return i
    return None


# ---------------------------------------------------------------------------
# Benchmarking helper
# ---------------------------------------------------------------------------

def benchmark_sort(data: list, key: Callable = lambda x: x, repeats: int = 5) -> dict:
    """Compare custom merge_sort vs. built-in sorted().

    Returns:
        A dict with 'merge_sort_ms' and 'builtin_sorted_ms' timings.
    """
    custom_time = timeit.timeit(
        lambda: merge_sort(data, key=key), number=repeats
    )
    builtin_time = timeit.timeit(
        lambda: sorted(data, key=key), number=repeats
    )

    return {
        "merge_sort_ms": round(custom_time / repeats * 1000, 2),
        "builtin_sorted_ms": round(builtin_time / repeats * 1000, 2),
    }


def benchmark_search(
    data: list,
    target: Any,
    key: Callable = lambda x: x,
    repeats: int = 5,
) -> dict:
    """Compare custom binary_search vs. built-in methods.

    *data* must already be sorted by *key* for binary_search.

    Returns:
        A dict with 'binary_search_ms', 'linear_search_ms',
        and 'builtin_in_ms' timings.
    """
    # --- Binary Search ---
    binary_time = timeit.timeit(
        lambda: binary_search(data, target, key=key),
        number=repeats
    )

    # --- Linear Search ---
    linear_time = timeit.timeit(
        lambda: linear_search(data, target, key=key),
        number=repeats
    )

    # --- Built-in search (in operator) ---
    builtin_time = timeit.timeit(
        lambda: target in [key(item) for item in data],
        number=repeats
    )

    return {
        "binary_search_ms": round(binary_time / repeats * 1000, 2),
        "linear_search_ms": round(linear_time / repeats * 1000, 2),
        "builtin_in_ms": round(builtin_time / repeats * 1000, 2),
    }
"""
Custom sorting and searching algorithms for the CityBike platform.
This module implements Merge Sort, Insertion Sort, Binary Search, and Linear Search.
"""

import timeit
from collections.abc import Callable
from typing import Any, List, Optional

# ---------------------------------------------------------------------------
# Sorting — Merge Sort
# ---------------------------------------------------------------------------

def merge_sort(data: list[Any], key: Callable = lambda x: x) -> list[Any]:
    """
    Sorts *data* using the merge-sort algorithm.
    
    Complexity:
        Time  — O(n log n) [cite: 72]
        Space — O(n) [cite: 72]
    """
    if len(data) <= 1:
        return list(data)

    mid = len(data) // 2
    left = merge_sort(data[:mid], key=key)
    right = merge_sort(data[mid:], key=key)

    return _merge(left, right, key=key)


def _merge(left: list[Any], right: list[Any], key: Callable) -> list[Any]:
    """Merge two sorted lists into one sorted list."""
    result: list[Any] = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------------------------
# Sorting — Insertion Sort
# ---------------------------------------------------------------------------

def insertion_sort(data: list[Any], key: Callable = lambda x: x) -> list[Any]:
    """
    Sorts *data* using the insertion-sort algorithm.
    
    Complexity:
        Time  — O(n²) worst/average, O(n) best [cite: 81]
        Space — O(n) for the copy
    """
    # Create a copy to avoid modifying the original list [cite: 128, 177]
    arr = list(data)
    for i in range(1, len(arr)):
        current_item = arr[i]
        current_key = key(current_item)
        j = i - 1
        
        # Shift elements of arr[0..i-1] that are greater than current_key
        while j >= 0 and key(arr[j]) > current_key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current_item
        
    return arr


# ---------------------------------------------------------------------------
# Searching — Binary Search
# ---------------------------------------------------------------------------

def binary_search(
    sorted_data: list[Any],
    target: Any,
    key: Callable = lambda x: x,
) -> Optional[int]:
    """
    Search for *target* in a sorted list using binary search[cite: 78].
    
    Complexity:
        Time  — O(log n) [cite: 81]
        Space — O(1)
    """
    low, high = 0, len(sorted_data) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = key(sorted_data[mid])

        if mid_val == target:
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return None


# ---------------------------------------------------------------------------
# Searching — Linear Search
# ---------------------------------------------------------------------------

def linear_search(
    data: list[Any],
    target: Any,
    key: Callable = lambda x: x,
) -> Optional[int]:
    """
    Search for *target* by scanning every element in *data*[cite: 78].
    
    Complexity:
        Time  — O(n) [cite: 81]
        Space — O(1)
    """
    for index, item in enumerate(data):
        if key(item) == target:
            return index
    return None


# ---------------------------------------------------------------------------
# Benchmarking helpers
# ---------------------------------------------------------------------------

def benchmark_sort(data: list, key: Callable = lambda x: x, repeats: int = 5) -> dict:
    """
    Compare custom merge_sort vs. built-in sorted().
    """
    custom_time = timeit.timeit(
        lambda: merge_sort(data, key=key), number=repeats
    )
    builtin_time = timeit.timeit(
        lambda: sorted(data, key=key), number=repeats
    )

    return {
        "merge_sort_ms": round(custom_time / repeats * 1000, 3),
        "builtin_sorted_ms": round(builtin_time / repeats * 1000, 3),
        "ratio": round(custom_time / builtin_time, 2)
    }


def benchmark_search(
    data: list,
    target: Any,
    key: Callable = lambda x: x,
    repeats: int = 100,
) -> dict:
    """
    Compare custom binary_search vs. linear search and built-in methods[cite: 79, 251].
    *data* must already be sorted by *key* for binary_search.
    """
    bin_time = timeit.timeit(
        lambda: binary_search(data, target, key=key), number=repeats
    )
    lin_time = timeit.timeit(
        lambda: linear_search(data, target, key=key), number=repeats
    )
    
    # Built-in check (using 'in' operator on a list of keys)
    keys_list = [key(item) for item in data]
    builtin_time = timeit.timeit(
        lambda: target in keys_list, number=repeats
    )

    return {
        "binary_search_ms": round(bin_time / repeats * 1000, 5),
        "linear_search_ms": round(lin_time / repeats * 1000, 5),
        "builtin_in_ms": round(builtin_time / repeats * 1000, 5)
    }
