def process_ipa_result(data):
    # Creating an export file to store all the issues
    output_file = open(f"./Export/{data['file_name']}-results.txt", "w")

    # Getting permissions
    permissions = data['permissions']
    output_file.write("---------------------Permissions Issues---------------------\n")

    # Process permissions
    dangerous_perms = {perm: details for perm, details in permissions.items() if details["status"] == "dangerous"}
    unknown_perms = {perm: details for perm, details in permissions.items() if details["status"] == "unknown"}

    for perm in dangerous_perms.items():
        output_file.write(f"[-] {perm[0]} is dangerous\n")

    for perm in unknown_perms.items():
        output_file.write(f"[-] {perm[0]} is unknown\n")
    
    # Checking ATS
    ats_findings = data['ats_analysis']['ats_findings']    
    output_file.write("\n---------------------ATS Issues---------------------\n")

    for findings in ats_findings:
        output_file.write(f"[-] {findings['issue']}\n")
    
    # Checking the binary analysis portion of the IPA
    macho_analysis = data['macho_analysis']
    output_file.write("\n---------------------Binary Analysis Issues---------------------\n")

    if (macho_analysis['nx']['has_nx'] == False):
        output_file.write(f"[-] NX bit is not set\n")
    
    if (macho_analysis['pie']['has_pie'] == False):
        output_file.write(f"[-] PIE is not enabled\n")
    
    if (macho_analysis['stack_canary']['has_canary'] == False):
        output_file.write(f"[-] Stack Canary is not enabled\n")
    
    if (macho_analysis['encrypted']['is_encrypted'] == False):
        output_file.write(f"[-] Application is not encrypted\n")
    
    if (macho_analysis['symbol']['is_stripped'] == False):
        output_file.write(f"[-] Debugging symbol is not stripped\n")
    
    # URL Scheme
    bundle_URL = data['bundle_url_types']
    output_file.write("\n---------------------URL Scheme Issues---------------------\n")

    for url in bundle_URL:
        output_file.write(f"[-] URL Scheme used ({url['CFBundleURLName']})\n")
    
    # Retrieve the Minimum OS version
    min_os_version = data['min_os_version']
    output_file.write("\n---------------------Version Issues---------------------\n")
    output_file.write(f"[*] Min OS Version is {min_os_version}\n")