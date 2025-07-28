import re
import highest_sdk_version

# Define ANSI escape codes for colors and reset
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
RESET = '\033[0m'  # Resets all formatting

def process_apk_result(data):
    # Get permission list
    permissions = data['permissions']
    print("[*] Checking permissions")

    # Process permissions
    dangerous_perms = {perm: details for perm, details in permissions.items() if details["status"] == "dangerous"}
    unknown_perms = {perm: details for perm, details in permissions.items() if details["status"] == "unknown"}

    for perm in dangerous_perms.items():
        print(f"{RED}[-] {perm[0]} is dangerous{RESET}")

    for perm in unknown_perms.items():
        print(f"{RED}[-] {perm[0]} is unknown{RESET}")

    # Getting highest SDK
    highest_sdk = highest_sdk_version.get_highest_android_sdk_version()
    print("[*] Checking SDK Version")
    
    # Check if the min SDK is the same level as the latest SDK version
    if(int(data['min_sdk']) < int(highest_sdk)):
        print(f"{RED}[-] {data['min_sdk']} is not the highest SDK version. (Latest SDK is {highest_sdk}){RESET}")

    # Check if v1 signature is signed
    if re.search(r'v1 signature:\s*True', data['certificate_analysis']['certificate_info']):
        print(f"{RED}[-] v1 Signature is enabled{RESET}")

    # Get bit size
    match = re.search(r'Bit Size:\s*(\d+)', data['certificate_analysis']['certificate_info'])
    print("[*] Checking Bit Size used")
    if match:
        bit_size = int(match.group(1))
        if bit_size < 2048:
            print(f"{RED}[-] Bit size is weak: {bit_size} bits (< 2048){RESET}")
        else:
            print(f"{GREEN}[+] Bit size is strong: {bit_size} bits{RESET}")
    else:
        print(f"{YELLOW}[*] Unable to find bit size in certificate information{RESET}")