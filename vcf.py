import re
import sys
from ascii import opening,closing


# For Windows
if sys.platform.startswith('win'):
    import msvcrt
    def get_char():
        return msvcrt.getch().decode().upper()
# For Unix (Linux, macOS)
else:
    import tty
    import termios
    def get_char():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1).upper()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def read_vcf(filename='contacts.vcf'):
    contacts = []
    try:
        with open(filename, 'r') as file:
            content = file.read()
            vcards = content.split('BEGIN:VCARD')
            for vcard in vcards[1:]:  # Skip the first empty split
                name = re.search(r'FN:(.*)', vcard)
                tel = re.search(r'TEL:(.*)', vcard)
                if name and tel:
                    contacts.append((name.group(1).strip(), tel.group(1).strip()))
    except FileNotFoundError:
        pass
    return contacts

def append_to_vcf(name, number, filename='contacts.vcf'):
    existing_contacts = read_vcf(filename)

    for contact in existing_contacts:
        if contact[0].lower() == name.lower():
            print(f"A contact with the name '{name}' already exists.")
            return False
        if contact[1] == number:
            print(f"A contact with the number '{number}' already exists.")
            return False

    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TEL:{number}
END:VCARD
"""
    
    with open(filename, 'a') as file:
        file.write(vcard)
    
    print(f"Contact {name} added to {filename}")
    return True

def get_input(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    return input()

def main():
    print(opening)  # Print the ASCII art banner
    print("              WELCOME TO THE VCF CONTACT SAVER!!!                    ")
    print("=====================================================================")

    while True:
        name = get_input("Enter the contact's name: ")
        number = get_input("Enter the contact's phone number: ")

        append_to_vcf(name, number)

        sys.stdout.write("Do you want to add another contact? (Y/N): ")
        sys.stdout.flush()
        
        while True:
            choice = get_char()
            if choice in ['Y', 'N']:
                print(choice)  # Print the user's choice
                break
            
        if choice == 'N':
            break

    print(closing)

if __name__ == "__main__":
    main()