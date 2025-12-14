#!/usr/bin/python3
import timeit
import random
from collections import Counter


def generate_random_list():
    """Generate a list with one million random values from 0 to 100."""
    return [random.randint(0, 100) for _ in range(1000000)]


def my_counter(numbers):
    """Create a dictionary with counts using manual approach."""
    counts = {}
    for num in numbers:
        if num in counts:
            counts[num] += 1
        else:
            counts[num] = 1
    return counts


def counter_approach(numbers):
    """Create a dictionary with counts using Counter."""
    return dict(Counter(numbers))


def my_top_ten(numbers):
    """Return top ten most common numbers using manual approach."""
    counts = my_counter(numbers)
    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_items[:10])


def counter_top_ten(numbers):
    """Return top ten most common numbers using Counter."""
    return dict(Counter(numbers).most_common(10))


def main():
    """Main function to benchmark and compare approaches."""
    numbers = generate_random_list()
    
    my_counter_time = timeit.timeit(
        lambda: my_counter(numbers),
        number=1
    )
    
    counter_time = timeit.timeit(
        lambda: counter_approach(numbers),
        number=1
    )
    
    my_top_time = timeit.timeit(
        lambda: my_top_ten(numbers),
        number=1
    )
    
    counter_top_time = timeit.timeit(
        lambda: counter_top_ten(numbers),
        number=1
    )
    
    print(f"my function: {my_counter_time}")
    print(f"Counter: {counter_time}")
    print(f"my top: {my_top_time}")
    print(f"Counter's top: {counter_top_time}")


if __name__ == '__main__':
    main()