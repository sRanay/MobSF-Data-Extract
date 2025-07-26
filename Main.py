import subprocess
import time
import re
import strip_codes
import requests
import json

# Define ANSI escape codes for colors and reset
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'  # Resets all formatting

API_KEY = ''
MOBSF_URL = 'http://127.0.0.1:8000'
apk_file = './InsecureBankv2.apk'

def start_mobsf():
    # Start MobSF in detached mode using Docker
    print("[*] Starting MobSF container...")

    # Remove any existing container named 'mobsf' to avoid conflict
    subprocess.run(['docker', 'rm', '-f', 'mobsf'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Run the MobSF container
    subprocess.run([
        'docker', 'run', '-d', '-v', 'mobsf_data:/root/.MobSF',
        '-p', '8000:8000',
        '--name', 'mobsf',
        'opensecurity/mobile-security-framework-mobsf:latest'
    ], check=True)

def get_mobsf_api_key(retries=15, delay=4):
    for i in range(retries):
        result = subprocess.run(['docker', 'logs', 'mobsf'], capture_output=True, text=True)
        clean_log = strip_codes.strip_ansi_codes(result.stdout)
        match = re.search(r'REST API Key:\s*([a-fA-F0-9]+)', clean_log)
        if match:
            return match.group(1)
        time.sleep(delay)
    return None

def uploading_binary(binary):
    upload_url = f'{MOBSF_URL}/api/v1/upload'
    files = {'file': (binary, open(binary, 'rb'), 'application/octet-stream')}
    upload_resp = requests.post(upload_url, files=files, headers=headers)
    upload_data = upload_resp.json()
    scan_hash = upload_data['hash']
    return scan_hash

def generate_json_report(scan_hash):
    report_url = f'{MOBSF_URL}/api/v1/report_json'
    data = {'hash': scan_hash}
    report_resp = requests.post(report_url, data=data, headers=headers)
    report = report_resp.json()
    with open('mobsf_report.json', 'w') as f:
        json.dump(report, f, indent=4)
    print("JSON report saved as mobsf_report.json")

def scan_uploaded_file(scan_hash): 
    scan_endpoint = f"{MOBSF_URL}/api/v1/scan"
    data = {
        'hash': scan_hash
    }

    response = requests.post(scan_endpoint, headers=headers, data=data)

    if response.status_code == 200:
        print(f"{GREEN}[+] Scan initiated successfully.{RESET}")
        return response.json()
    else:
        print(f"❌ Failed to initiate scan: {response.status_code}")
        print("Response:", response.text)
        return None

start_mobsf()

API_KEY = get_mobsf_api_key()

if API_KEY:
    print(f"{GREEN}[+] MobSF REST API Key: {API_KEY}{RESET}")
else:
    print("[-] Failed to extract MobSF API Key from logs.")

headers={'Authorization': API_KEY}
print("[*] Starting MobSF. Please wait")
time.sleep(15)
print("[*] MobSF is running at http://127.0.0.1:8000")
scan_hash = uploading_binary(apk_file)
scan_uploaded_file(scan_hash)
