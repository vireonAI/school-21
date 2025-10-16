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
    
    def save_file(self, data, file_name, extention):
        full_name = f"{file_name}.{extention}"
        try:
            with open(full_name, 'w') as f:
                f.write(str(data))
            return full_name
        except Exception as e:
            raise Exception(f"Could not save file: {e}")


