import sys


def contains_cyrillic(text):
    for char in text:
        if '\u0400' <= char <= '\u04FF' or '\u0500' <= char <= '\u052F':
            return True
    return False


def caesar_shift_char(char, shift, encode=True):
    if not char.isalpha():
        return char
    
    is_upper = char.isupper()
    char = char.lower()
    
    if encode:
        shifted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
    else:
        shifted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
    
    return shifted_char.upper() if is_upper else shifted_char


def caesar_cipher(text, shift, encode=True):
    if contains_cyrillic(text):
        raise ValueError("The script does not support your language yet.")
    
    result = ""
    for char in text:
        result += caesar_shift_char(char, shift, encode)
    
    return result


def encode_text(text, shift):
    return caesar_cipher(text, shift, encode=True)


def decode_text(text, shift):
    return caesar_cipher(text, shift, encode=False)


def validate_arguments():
    if len(sys.argv) != 4:
        raise ValueError("Usage: python3 caesar.py <encode|decode> '<text>' <shift>")
    
    operation = sys.argv[1].lower()
    text = sys.argv[2]
    
    try:
        shift = int(sys.argv[3])
    except ValueError:
        raise ValueError("Shift must be a valid integer")
    
    if operation not in ['encode', 'decode']:
        raise ValueError("Operation must be 'encode' or 'decode'")
    
    return operation, text, shift


def main():
    try:
        operation, text, shift = validate_arguments()
        
        if operation == 'encode':
            result = encode_text(text, shift)
        else:  # operation == 'decode'
            result = decode_text(text, shift)
        
        print(result)
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()