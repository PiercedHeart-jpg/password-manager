import os
import base64
import random
import string
import time
from cryptography.fernet import Fernet

NEON_PURPLE = '\033[38;5;129m'  
DARK_PINK = '\033[38;5;204m'  
GOTHIC_BLACK = '\033[30m'      
RESET_COLOR = '\033[0m'        


ASCII_ART = """
  ▄▄█    █▄       ▄████████  ▄████████    ▄█   ▄█▄    ▄████████     ███      ▄█    ▄▄▄▄███▄▄▄▄      ▄████████
  ███    ███     ███    ███ ███    ███   ███ ▄███▀   ███    ███ ▀█████████▄ ███  ▄██▀▀▀███▀▀▀██▄   ███    ███
  ███    ███     ███    ███ ███    █▀    ███▐██▀     ███    ███    ▀███▀▀██ ███▌ ███   ███   ███   ███    █▀
 ▄███▄▄▄▄███▄▄   ███    ███ ███         ▄█████▀      ███    ███     ███   ▀ ███▌ ███   ███   ███  ▄███▄▄▄
▀▀███▀▀▀▀███▀  ▀███████████ ███        ▀▀█████▄    ▀███████████     ███     ███▌ ███   ███   ███ ▀▀███▀▀▀
  ███    ███     ███    ███ ███    █▄    ███▐██▄     ███    ███     ███     ███  ███   ███   ███   ███    █▄
  ███    ███     ███    ███ ███    ███   ███ ▀███▄   ███    ███     ███     ███  ███   ███   ███   ███    ███
  ███    █▀      ███    █▀  ████████▀    ███   ▀█▀   ███    █▀     ▄████▀   █▀    ▀█   ███   █▀    ██████████
                                         ▀
"""

def center_text(text, width=80):
    """Center the text in the terminal window."""
    return '\n'.join([line.center(width) for line in text.splitlines()])

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter_effect(text, speed=0.05):
    """Print text one character at a time for typewriter effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(speed)
    print()  

class PasswordManager:
    def __init__(self, key_file="secret.key", password_file="passwords.txt"):
        self.key_file = key_file
        self.password_file = password_file
        self.key = self.load_key()

    def generate_key(self):
        """Generate a new encryption key."""
        return Fernet.generate_key()

    def load_key(self):
        """Load an existing key or create a new one.""" 
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as key_file:
                return key_file.read()
        else:
            key = self.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)
            return key

    def encrypt_password(self, password):
        f = Fernet(self.key)
        encrypted = f.encrypt(password.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt_password(self, encrypted_password):
        f = Fernet(self.key)
        encrypted_password = base64.urlsafe_b64decode(encrypted_password)
        return f.decrypt(encrypted_password).decode()

    def add_password(self, service, password):
        encrypted_password = self.encrypt_password(password)
        with open(self.password_file, "a") as f:
            f.write(f"{service} | {encrypted_password}\n")
        print(f"{NEON_PURPLE}☆･ﾟ: *☆ Password for {service} added successfully. *:･ﾟ☆{RESET_COLOR}")

    def retrieve_password(self, service):
        if not os.path.exists(self.password_file):
            return None

        with open(self.password_file, "r") as f:
            for line in f:
                stored_service, encrypted_password = line.strip().split(" | ")
                if stored_service == service:
                    return self.decrypt_password(encrypted_password)
        return None

    def list_services(self):
        if not os.path.exists(self.password_file):
            print(f"{NEON_PURPLE}✦ No services stored. ✦{RESET_COLOR}")
            return

        with open(self.password_file, "r") as f:
            for line in f:
                service, _ = line.split(" | ")
                print(f"{DARK_PINK}✧{NEON_PURPLE} {service} {DARK_PINK}✧{RESET_COLOR}")

    def validate_password(self, password):
        """Check if the password meets basic strength requirements."""
        if len(password) < 8:
            print(f"{NEON_PURPLE}✦ Password must be at least 8 characters long. ✦{RESET_COLOR}")
            return False
        if not any(char.isdigit() for char in password):
            print(f"{NEON_PURPLE}✦ Password must contain at least one number. ✦{RESET_COLOR}")
            return False
        if not any(char.isupper() for char in password):
            print(f"{NEON_PURPLE}✦ Password must contain at least one uppercase letter. ✦{RESET_COLOR}")
            return False
        return True

    def generate_random_password(self):
        """Generate a random password based on user preferences."""
        print(f"{NEON_PURPLE}✦ Let's create a strong password! ✦{RESET_COLOR}")
        
        
        while True:
            try:
                length = int(input(f"{NEON_PURPLE}✦ Enter desired password length (e.g., 12): {RESET_COLOR}"))
                if length < 8:
                    print(f"{NEON_PURPLE}✦ Password must be at least 8 characters long. ✦{RESET_COLOR}")
                else:
                    break
            except ValueError:
                print(f"{NEON_PURPLE}✦ Please enter a valid number for password length. ✦{RESET_COLOR}")

       
        include_uppercase = input(f"{NEON_PURPLE}✦ Include uppercase letters? (y/n): {RESET_COLOR}").lower() == 'y'
        include_lowercase = input(f"{NEON_PURPLE}✦ Include lowercase letters? (y/n): {RESET_COLOR}").lower() == 'y'
        include_numbers = input(f"{NEON_PURPLE}✦ Include numbers? (y/n): {RESET_COLOR}").lower() == 'y'
        include_symbols = input(f"{NEON_PURPLE}✦ Include symbols? (y/n): {RESET_COLOR}").lower() == 'y'

       
        characters = ''
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_lowercase:
            characters += string.ascii_lowercase
        if include_numbers:
            characters += string.digits
        if include_symbols:
            characters += string.punctuation

        if not characters:
            print(f"{NEON_PURPLE}✦ You must select at least one type of character. ✦{RESET_COLOR}")
            return None
        
        
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def main_menu(self):
        try:
           
            clear_screen()
            typewriter_effect(f"{NEON_PURPLE}★ Welcome to pierce's Password Manager! ★{RESET_COLOR}", speed=0.1)
            time.sleep(1)  
            clear_screen()

            while True:
                clear_screen()
                print(f"{NEON_PURPLE}{center_text(ASCII_ART)}{RESET_COLOR}")
                print(f"{NEON_PURPLE}\n{GOTHIC_BLACK}●●●●●●●●●●●●●●●●●●●●●●●●●●{RESET_COLOR}")
                print(f"{NEON_PURPLE}{GOTHIC_BLACK}  ᕯ  {DARK_PINK}★ pierce's Password Manager ★{RESET_COLOR}")
                print(f"{NEON_PURPLE}●●●●●●●●●●●●●●●●●●●●●●●●●●{RESET_COLOR}")
                print(f"{NEON_PURPLE}1. Add a Password{RESET_COLOR}")
                print(f"{NEON_PURPLE}2. Retrieve a Password{RESET_COLOR}")
                print(f"{NEON_PURPLE}3. List Services{RESET_COLOR}")
                print(f"{NEON_PURPLE}4. Generate a Random Password{RESET_COLOR}")
                print(f"{NEON_PURPLE}5. Exit{RESET_COLOR}")

                choice = input(f"{NEON_PURPLE}✦ Choose an option: {RESET_COLOR}")

                if choice == "1":
                    service = input(f"{NEON_PURPLE}✦ Enter the service name: {RESET_COLOR}")
                    password = input(f"{NEON_PURPLE}✦ Enter the password: {RESET_COLOR}")
                    self.add_password(service, password)

                elif choice == "2":
                    service = input(f"{NEON_PURPLE}✦ Enter the service name: {RESET_COLOR}")
                    password = self.retrieve_password(service)
                    if password:
                        print(f"{NEON_PURPLE}✧ Password for {service}: {password} ✧{RESET_COLOR}")
                    else:
                        print(f"{NEON_PURPLE}✧ No password found for {service}. ✧{RESET_COLOR}")

                elif choice == "3":
                    print(f"{NEON_PURPLE}✦ Stored services: ✦{RESET_COLOR}")
                    self.list_services()

                elif choice == "4":
                    new_password = self.generate_random_password()
                    if new_password:
                        print(f"{NEON_PURPLE}✦ Your new password is: {new_password} ✦{RESET_COLOR}")
                    else:
                        print(f"{NEON_PURPLE}✦ Failed to generate a password. Please try again. ✦{RESET_COLOR}")

                elif choice == "5":
                    print(f"{NEON_PURPLE}✧ Exiting pierce's Password Manager. ✧{RESET_COLOR}")
                    break

                else:
                    print(f"{NEON_PURPLE}✦ Invalid choice. ✦{RESET_COLOR}")

                input(f"{NEON_PURPLE}✦ Press Enter to continue... {RESET_COLOR}")  
                clear_screen()  

        except KeyboardInterrupt:
            print(f"\n{NEON_PURPLE}✧ Exiting pierce's Password Manager. ✧{RESET_COLOR}")

if __name__ == "__main__":
    pm = PasswordManager()
    pm.main_menu()
