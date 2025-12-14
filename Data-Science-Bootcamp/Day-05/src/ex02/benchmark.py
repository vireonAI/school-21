#!/usr/bin/python3
import timeit
import sys


def filter_with_loop(emails):
    """Filter Gmail addresses using a loop with append."""
    result = []
    for email in emails:
        if email.endswith('@gmail.com'):
            result.append(email)
    return result


def filter_with_list_comprehension(emails):
    """Filter Gmail addresses using list comprehension."""
    return [email for email in emails if email.endswith('@gmail.com')]


def is_gmail(email):
    """Helper function to check if email is Gmail."""
    return email.endswith('@gmail.com')


def filter_with_map(emails):
    """Filter Gmail addresses using map and filter."""
    return list(map(is_gmail, emails))


def filter_with_filter(emails):
    """Filter Gmail addresses using filter function."""
    return list(filter(lambda email: email.endswith('@gmail.com'), emails))


def benchmark_function(func_name, emails, number):
    """Benchmark the specified function."""
    functions = {
        'loop': filter_with_loop,
        'list_comprehension': filter_with_list_comprehension,
        'map': filter_with_map,
        'filter': filter_with_filter
    }
    
    if func_name not in functions:
        raise ValueError(f"Unknown function: {func_name}")
    
    func = functions[func_name]
    time_result = timeit.timeit(
        lambda: func(emails),
        number=number
    )
    
    return time_result


def main():
    """Main function to run benchmark based on command line arguments."""
    if len(sys.argv) != 3:
        sys.exit(1)
    
    func_name = sys.argv[1]
    try:
        number = int(sys.argv[2])
    except ValueError:
        print("Error: number_of_calls must be an integer")
        sys.exit(1)
    
    base_emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
                   'anna@live.com', 'philipp@gmail.com']
    
    emails = base_emails * 5
    
    try:
        time_result = benchmark_function(func_name, emails, number)
        print(time_result)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()