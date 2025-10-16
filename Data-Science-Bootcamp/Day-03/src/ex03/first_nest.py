import sys

class Research:
    class Calculations:
        def counts(self, data):
            heads = sum(1 for pair in data if pair == [0, 1])
            tails = sum(1 for pair in data if pair == [1, 0])
            return heads, tails

        def fractions(self, heads, tails):
            total = heads + tails
            if total == 0:
                return 0, 0
            return heads/total, tails/total


    def __init__(self, file_path):
        self.file_path = file_path

    def file_reader(self, has_header=True):
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()

                if has_header:
                    lines = lines[1:]

                data = []
                for line in lines:
                    clean = line.strip()  
                    parts = clean.split(',')  
                    row = [int(x) for x in parts]
                    data.append(row)

                return data

        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self.file_path}' not found.")

if __name__ == "__main__":
    try:
        research = Research(sys.argv[1])
        data = research.file_reader()
        print(data)

        calc = Research.Calculations()
        heads, tails = calc.counts(data)
        print(heads, tails)

        head_frac, tail_frac = calc.fractions(heads, tails)
        print(head_frac, tail_frac)
    except IndexError:
        print("Usage: python3 first_nest.py <path_to_csv>")
    except Exception as e:
        print(f"Error: {e}")

