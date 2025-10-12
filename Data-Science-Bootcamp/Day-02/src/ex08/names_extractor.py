import sys


def extract_name_surname_from_email(email):

    email = email.strip().lower()
    
    if '@corp.com' not in email:
        return None, None
    
    local_part = email.split('@')[0]
    
    if '.' not in local_part:
        return None, None
    
    parts = local_part.split('.')
    if len(parts) != 2:
        return None, None
    
    name, surname = parts
    name = name.capitalize()
    surname = surname.capitalize()
    
    return name, surname


def process_email_file(input_filename, output_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8') as input_file:
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                output_file.write("Name\tSurname\tE-mail\n")
                
                for line_number, line in enumerate(input_file, 1):
                    email = line.strip()
                    
                    if not email:  
                        continue
                    
                    name, surname = extract_name_surname_from_email(email)
                    
                    if name and surname:
                        original_email = email.lower()
                        output_file.write(f"{name}\t{surname}\t{original_email}\n")
                    else:
                        print(f"Warning: Invalid email format on line {line_number}: {email}")
                        
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found")
        return False
    except Exception as e:
        print(f"Error processing file: {e}")
        return False
    
    return True


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 names_extractor.py <email_file_path>")
        return
    
    input_filename = sys.argv[1]
    output_filename = "employees.tsv"
    
    if process_email_file(input_filename, output_filename):
        print(f"Employee data extracted successfully to '{output_filename}'")
    else:
        print("Failed to process email file")


if __name__ == '__main__':
    main()