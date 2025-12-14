#!/usr/bin/python3
import timeit
import sys
from functools import reduce


def sum_squares_loop(n):
    """Calculate sum of squares using a loop."""
    total = 0
    for i in range(1, n + 1):
        total = total + i * i
    return total


def sum_squares_reduce(n):
    """Calculate sum of squares using reduce."""
    return reduce(lambda acc, i: acc + i * i, range(1, n + 1), 0)


def benchmark_function(func_name, number, n):
    """Benchmark the specified function."""
    functions = {
        'loop': sum_squares_loop,
        'reduce': sum_squares_reduce
    }
    
    if func_name not in functions:
        raise ValueError(f"Unknown function: {func_name}")
    
    func = functions[func_name]
    time_result = timeit.timeit(
        lambda: func(n),
        number=number
    )
    
    return time_result


def main():
    """Main function to run benchmark based on command line arguments."""
    if len(sys.argv) != 4:
        print("Usage: ./benchmark.py <function_name> <number_of_calls> <n>")
        print("Functions: loop, reduce")
        sys.exit(1)
    
    func_name = sys.argv[1]
    try:
        number = int(sys.argv[2])
        n = int(sys.argv[3])
    except ValueError:
        print("Error: number_of_calls and n must be integers")
        sys.exit(1)
    
    try:
        time_result = benchmark_function(func_name, number, n)
        print(time_result)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()