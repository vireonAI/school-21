#!/usr/bin/python3

import sys
import resource


def read_lines_generator(filename):
    """Read lines from a file using a generator."""
    with open(filename, 'r') as f:
        for line in f:
            yield line


def main():
    """Main function to read file using generator and display memory/time usage."""
    if len(sys.argv) != 2:
        print("Usage: ./generator.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        for line in read_lines_generator(filename):
            pass
        
        usage = resource.getrusage(resource.RUSAGE_SELF)
        
        peak_memory_kb = usage.ru_maxrss
        peak_memory_gb = peak_memory_kb / (1024 ** 3)
        
        total_time = usage.ru_utime + usage.ru_stime
        
        print(f"Peak Memory Usage = {peak_memory_gb:.3f} GB")
        print(f"User Mode Time + System Mode Time = {total_time:.2f}s")
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()