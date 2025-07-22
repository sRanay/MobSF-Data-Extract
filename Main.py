import subprocess
import time
import re
import strip_codes

API_KEY = ""

def start_mobsf():
    # Start MobSF in detached mode using Docker
    print("[*] Starting MobSF container...")

    # Remove any existing container named 'mobsf' to avoid conflict
    subprocess.run(['docker', 'rm', '-f', 'mobsf'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Run the MobSF container
    subprocess.run([
        'docker', 'run', '-d',
        '-p', '8000:8000',
        '--name', 'mobsf',
        'opensecurity/mobile-security-framework-mobsf:latest'
    ], check=True)

def get_mobsf_api_key(retries=15, delay=4):
    for i in range(retries):
        print(f"Checking logs, attempt {i+1}...")
        result = subprocess.run(['docker', 'logs', 'mobsf'], capture_output=True, text=True)
        
        clean_log = strip_codes.strip_ansi_codes(result.stdout)
        
        match = re.search(r'REST API Key:\s*([a-fA-F0-9]+)', clean_log)
        if match:
            return match.group(1)
        time.sleep(delay)
    return None


def main():
    start_mobsf()

    API_KEY = get_mobsf_api_key()

    if API_KEY:
        print(f"[+] MobSF REST API Key: {API_KEY}")
    else:
        print("[-] Failed to extract MobSF API Key from logs.")

    print("[*] MobSF is running at http://127.0.0.1:8000")

if __name__ == "__main__":
    main()
