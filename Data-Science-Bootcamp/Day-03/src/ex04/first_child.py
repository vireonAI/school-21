import sys
from random import randint

class Research:
    class Calculations:
        def __init__(self, data):
            self.data = data

        def counts(self):

            heads = sum(1 for pair in self.data if pair == [0, 1])
            tails = sum(1 for pair in self.data if pair == [1, 0])
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

class Analytics(Research.Calculations):
    def predict_random(self, n):
        predictions = []
        for _ in range(n):
            head = randint(0, 1)
            tail = 1-head
            predictions.append([head, tail])
        return predictions

    def predict_last(self):
        if not self.data:
            return None
        return self.data[-1]


if __name__ == "__main__":
    try:
        research = Research(sys.argv[1])
        data = research.file_reader()
        print(data)

        analytics = Analytics(data)

        heads, tails = analytics.counts()
        print(heads, tails)

        h_frac, t_frac = analytics.fractions(heads, tails) 
        print(h_frac, t_frac)

        print(analytics.predict_random(3))   

        print(analytics.predict_last())

    except IndexError:
        print("Usage: python3 first_child.py <path_to_csv>")
    except Exception as e:
        print(f"Error: {e}")

