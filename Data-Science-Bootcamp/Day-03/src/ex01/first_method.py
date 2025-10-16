class Research:
    def file_reader(self):
        try:
            with open('data.csv', 'r') as file:
                return file.read()
        except FileNotFoundError:
            print("File is not exist or not exist")

if __name__ == "__main__":
    research = Research()
    print(research.file_reader())