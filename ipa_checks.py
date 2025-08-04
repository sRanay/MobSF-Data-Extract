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
    
    # Checking ATS
    ats_findings = data['ats_analysis']['ats_findings']    
    print("[*] Checking ATS")

    for findings in ats_findings:
        print(f"{RED}[-] {findings['issue']}{RESET}")
    
    # Checking the binary analysis portion of the IPA
    macho_analysis = data['macho_analysis']
    print("[*] Checking Binary Analysis for the IPA")

    if (macho_analysis['nx']['has_nx'] == False):
        print(f"{RED}[-] NX bit is not set{RESET}")
    
    if (macho_analysis['pie']['has_pie'] == False):
        print(f"{RED}[-] PIE is not enabled{RESET}")
    
    if (macho_analysis['stack_canary']['has_canary'] == False):
        print(f"{RED}[-] Stack Canary is not enabled{RESET}")
    
    if (macho_analysis['encrypted']['is_encrypted'] == False):
        print(f"{RED}[-] Application is not encrypted{RESET}")
    
    if (macho_analysis['symbol']['is_stripped'] == False):
        print(f"{RED}[-] Debugging symbol is not stripped{RESET}")
    
    # URL Scheme
    bundle_URL = data['bundle_url_types']
    print("[*] Checking URL Scheme")

    for url in bundle_URL:
        print(f"{RED}[-] URL Scheme used ({url['CFBundleURLName']}){RESET}")
    
    # Retrieve the Minimum OS version
    min_os_version = data['min_os_version']
    print(f"{YELLOW}[*] Min OS Version is {min_os_version}{RESET}")