import re
import highest_sdk_version

def process_apk_result(data):
    # Creating an export file to store all the issues
    output_file = open(f"./Export/{data['file_name']}-results.txt", "w")
    
    # Get permission list
    permissions = data['permissions']
    output_file.write("---------------------Permissions Issues---------------------\n")

    # Process permissions
    dangerous_perms = {perm: details for perm, details in permissions.items() if details["status"] == "dangerous"}
    unknown_perms = {perm: details for perm, details in permissions.items() if details["status"] == "unknown"}

    for perm in dangerous_perms.items():
        output_file.write(f"[-] {perm[0]} is dangerous\n")

    for perm in unknown_perms.items():
        output_file.write(f"[-] {perm[0]} is unknown\n")

    # Getting highest SDK
    highest_sdk = highest_sdk_version.get_highest_android_sdk_version()
    output_file.write("\n---------------------SDK Version Issues---------------------\n")
    
    # Check if the min SDK is the same level as the latest SDK version
    if (int(data['min_sdk']) < int(highest_sdk)):
        output_file.write(f"[-] {data['min_sdk']} is not the highest SDK version. (Latest SDK is {highest_sdk})\n")

    output_file.write("\n---------------------Certificate Issues---------------------\n")
    # Check if v1 signature is signed
    if re.search(r'v1 signature:\s*True', data['certificate_analysis']['certificate_info']):
        output_file.write("[-] v1 Signature is enabled\n")
        
    # Get bit size
    match = re.search(r'Bit Size:\s*(\d+)', data['certificate_analysis']['certificate_info'])
    if match:
        bit_size = int(match.group(1))
        if bit_size < 2048:
            output_file.write(f"[-] Bit size is weak: {bit_size} bits (< 2048)\n")

    # Checking the binary analysis portion of the APK
    
    # Getting shared library portion
    shared_library = data['binary_analysis']
    output_file.write("\n---------------------Binary Analysis Issues---------------------\n")

    nx_output_string = f""
    pie_output_string = f""
    stack_canary_output_string = f""
    debugging_symbol_output_string = f""

    for single_library in shared_library:
        # Check NX bit
        if (single_library['nx']['is_nx'] == False):
            nx_output_string += f"[-] {single_library['name']}\n"
            #output_file.write(f"[-] {single_library['name']} does not have NX bit set\n")
        
        # Check PIE
        if (single_library['pie']['is_pie'] == False):
            pie_output_string += f"[-] {single_library['name']}\n"
            #output_file.write(f"[-] {single_library['name']} does not have PIE set\n")
        
        # Check Stack Canary
        if (single_library['stack_canary']['has_canary'] == False):
            stack_canary_output_string += f"[-] {single_library['name']}\n"
            #output_file.write(f"[-] {single_library['name']} does not have Stack Canary set\n")

        # Check debugging symbols
        if (single_library['symbol']['is_stripped'] == False):
            debugging_symbol_output_string += f"[-] {single_library['name']}\n"
            #output_file.write(f"[-] {single_library['name']} still have debugging symbols enabled\n")
    
    if (nx_output_string != ""):
        output_file.write("NX Bit not set:\n")
        output_file.write(nx_output_string)
    if (pie_output_string != ""):
        output_file.write("PIE not set:\n")
        output_file.write(pie_output_string)
    if (stack_canary_output_string != ""):
        output_file.write("Stack Canary not set:\n")
        output_file.write(stack_canary_output_string)
    if (debugging_symbol_output_string != ""):
        output_file.write("Debugging Symbols are enabled:\n")
        output_file.write(debugging_symbol_output_string)