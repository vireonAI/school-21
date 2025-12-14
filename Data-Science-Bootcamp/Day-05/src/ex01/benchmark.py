#!/usr/bin/python3
import timeit


def filter_with_loop(emails):
    """Filter Gmail addresses using a loop with append."""
    result = []
    for email in emails:
        if email.endswith('@gmail.com'):
            result.append(email)
    return result


def filter_with_comprehension(emails):
    """Filter Gmail addresses using list comprehension."""
    return [email for email in emails if email.endswith('@gmail.com')]


def is_gmail(email):
    """Helper function to check if email is Gmail."""
    return email.endswith('@gmail.com')


def filter_with_map(emails):
    """Filter Gmail addresses using filter (functional programming approach)."""
    return list(map(is_gmail, emails))


def main():
    """Main function to benchmark and compare approaches."""
    base_emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
                   'anna@live.com', 'philipp@gmail.com']
    
    emails = base_emails * 5
    
    loop_time = timeit.timeit(
        lambda: filter_with_loop(emails),
        number=9000000
    )
    
    comprehension_time = timeit.timeit(
        lambda: filter_with_comprehension(emails),
        number=9000000
    )
    
    map_time = timeit.timeit(
        lambda: filter_with_map(emails),
        number=9000000
    )
    
    times_dict = {
        'loop': loop_time,
        'list comprehension': comprehension_time,
        'map': map_time
    }
    
    best_method = min(times_dict, key=times_dict.get)
    
    print(f"it is better to use a {best_method}")
    
    times = sorted([loop_time, comprehension_time, map_time])
    print(f"{times[0]} vs {times[1]} vs {times[2]}")


if __name__ == '__main__':
    main()