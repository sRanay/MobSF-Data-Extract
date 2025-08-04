import re

# Define ANSI escape codes for colors and reset
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
RESET = '\033[0m'  # Resets all formatting

def process_ipa_result(data):
    # Getting permissions
    permissions = data['permissions']
    print("[*] Checking permissions")

    # Process permissions
    dangerous_perms = {perm: details for perm, details in permissions.items() if details["status"] == "dangerous"}
    unknown_perms = {perm: details for perm, details in permissions.items() if details["status"] == "unknown"}

    for perm in dangerous_perms.items():
        print(f"{RED}[-] {perm[0]} is dangerous{RESET}")

    for perm in unknown_perms.items():
        print(f"{RED}[-] {perm[0]} is unknown{RESET}")
