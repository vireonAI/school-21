import sys


def read_employees_file(filename):
    email_to_name = {}
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            header = next(file)
            
            for line_number, line in enumerate(file, 2):  
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split('\t')
                if len(parts) >= 3:
                    name = parts[0].strip()
                    surname = parts[1].strip()
                    email = parts[2].strip()
                    email_to_name[email.lower()] = name
                else:
                    print(f"Warning: Invalid format on line {line_number}")
                    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        print("Please run names_extractor.py first to create the employees.tsv file")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    return email_to_name


def generate_welcome_letter(email, email_to_name):
    email_lower = email.lower().strip()
    
    if email_lower not in email_to_name:
        print(f"Email '{email}' not found in employee database")
        return
    
    name = email_to_name[email_lower]
    
    welcome_text = (f"Dear {name}, welcome to our team! We are sure that it will be a "
                   f"pleasure to work with you. That's a precondition for the "
                   f"professionals that our company hires.")
    
    print(welcome_text)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 letter_starter.py <email_address>")
        return
    
    email = sys.argv[1]
    employees_file = "employees.tsv"
    email_to_name = read_employees_file(employees_file)
    
    if email_to_name is None:
        return
    
    generate_welcome_letter(email, email_to_name)


if __name__ == '__main__':
    main()