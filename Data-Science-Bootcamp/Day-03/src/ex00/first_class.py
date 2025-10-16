class Must_Read:
    try:
        with open('data.csv', 'r') as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("Error: 'data.csv' file not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    Must_Read()
