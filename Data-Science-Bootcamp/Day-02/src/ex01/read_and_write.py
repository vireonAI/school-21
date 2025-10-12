def read_csv():
    try:
        with open('ds.csv', 'r') as file:
            lines = file.readlines()
        return lines
    
    except FileNotFoundError:
        print("Error: The file 'ds.csv' was not found.")
        raise

def write_tsv(lines):
    with open('ds.tsv', 'w') as file:
        for line in lines:
            file.write(line)

def process_line(line):
    new_line = []
    inside_quotes = False
    i = 0
    for i in range(len(line)):
        char = line[i]
        if char == '"':
            inside_quotes = not inside_quotes
            new_line.append(char)
        elif char ==',' and not inside_quotes:
            new_line.append('\t')
        else:
            new_line.append(char)
    return ''.join(new_line)

def main():
    lines = read_csv()
    processed_lines = [process_line(line) for line in lines]
    write_tsv(processed_lines)

if __name__ == '__main__':
    main()
