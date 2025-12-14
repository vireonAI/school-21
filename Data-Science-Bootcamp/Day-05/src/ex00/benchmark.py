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
    
    if comprehension_time <= loop_time:
        print("it is better to use a list comprehension")
    else:
        print("it is better to use a loop")
    
    times = sorted([loop_time, comprehension_time])
    print(f"{times[0]} vs {times[1]}")


if __name__ == '__main__':
    main()

