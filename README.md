This is a simple password manager I made in Python!
Disclaimer: Please don't use this as a real password manager (unless you're just messing around). There are much better options out there like KeePass XC (offline, free) and LastPass (cloud-based, not free).

This app uses Fernet encryption from the cryptography library to securely encrypt passwords before saving them. They can only be decrypted with the correct key.

How to Use:

passwordmanager.py: View the code and run it in your terminal.

passwordmanager.exe: Easier to run (Windows users).

Make sure to install the cryptography library first by running:

pip install cryptography

<!-- All praise the ommisiah spirit of the machine -->

or using venv for

python -m venv .venv

source .venv/bin/activate  # or activate.fish or what ever your system uses.
<!-- .ps1 for powershell? -->

then

pip install cryptography

