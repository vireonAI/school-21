import sys

class Research:
    def __init__(self, file_path):
        self.file_path = file_path

    def file_reader(self):
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()

                if not lines:
                    raise ValueError("File is empty")

                header = lines[0].strip()
                if header != "head,tail":
                    raise ValueError("Invalid header format. Expected 'head,tail'.")

                for line in lines[1:]:
                    clean = line.strip()
                    if clean not in ("0,1", "1,0"):
                        raise ValueError(f"Invalid data line: {clean}")

                return ''.join(lines)

        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self.file_path}' not found.")

if __name__ == "__main__":
    try:
        research = Research(sys.argv[1])
        print(research.file_reader())
    except IndexError:
        print("Usage: python3 first_constructor.py <path_to_csv>")
    except Exception as e:
        print(f"Error: {e}")

