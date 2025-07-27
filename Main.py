import subprocess
import time
import re
import strip_codes
import requests
import json
from pathlib import Path

# Define ANSI escape codes for colors and reset
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'  # Resets all formatting

API_KEY = ''
MOBSF_URL = 'http://127.0.0.1:8000'
binary_folder_path = Path('./Binary')
json_report_folder_path = Path('./Reports/JSON')


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

def uploading_binary(files):
    scan_hash = []
    for binary in files:
        upload_url = f'{MOBSF_URL}/api/v1/upload'
        files = {'file': (binary, open(binary, 'rb'), 'application/octet-stream')}
        upload_resp = requests.post(upload_url, files=files, headers=headers)
        upload_data = upload_resp.json()
        scan_hash.append(upload_data['hash'])
    return scan_hash

def generate_json_report(scan_hash):
    for hash in scan_hash:
        report_url = f'{MOBSF_URL}/api/v1/report_json'
        data = {'hash': hash}
        report_resp = requests.post(report_url, data=data, headers=headers)
        report = report_resp.json()
        file_name = './Reports/JSON/mobsf_report-'+hash+'.json'
        with open(file_name, 'w') as f:
            json.dump(report, f, indent=4)
        print(f"{GREEN}[+] JSON report saved as mobsf_report-{hash}.json{RESET}")

def generate_pdf_report(scan_hash):
    for hash in scan_hash:
        report_url = f'{MOBSF_URL}/api/v1/download_pdf'
        data = {'hash': hash}
        report_resp = requests.post(report_url, data=data, headers=headers)
        file_name = './Reports/PDF/mobsf_report-'+hash+'.pdf'
        with open(file_name, 'wb') as f:
            f.write(report_resp.content)
        print(f"{GREEN}[+] JSON report saved as mobsf_report-{hash}.pdf{RESET}")

def scan_uploaded_file(scan_hash):
    for hash in scan_hash: 
        scan_endpoint = f"{MOBSF_URL}/api/v1/scan"
        data = {
            'hash': hash
        }

        response = requests.post(scan_endpoint, headers=headers, data=data)

        if response.status_code == 200:
            print(f"{GREEN}[+] Scan finished successfully for {hash}.{RESET}")
        else:
            print(f"{RED}Failed to initiate scan: {response.status_code}{RESET}")
            print("Response:", response.text)
            return None
        
def process_json_file():
    json_files = ['./Reports/JSON/'+f.name for f in json_report_folder_path.iterdir() if f.is_file()]
    for json_file in json_files:
        with open(json_file, 'r') as file:
            data = json.load(file)
            if (data['file_name'][-3:] == "ipa"):
                print("It is an IPA file")
            if (data['file_name'][-3:] == "apk"):
                print("It is an APK file")


start_mobsf()

API_KEY = get_mobsf_api_key()

if API_KEY:
    print(f"{GREEN}[+] MobSF REST API Key: {API_KEY}{RESET}")
else:
    print("{RED}[-] Failed to extract MobSF API Key from logs.{RESET}")

headers={'Authorization': API_KEY}
print("[*] Starting MobSF. Please wait")
time.sleep(15)
print("[*] MobSF is running at http://127.0.0.1:8000")
files = ['./Binary/'+f.name for f in binary_folder_path.iterdir() if f.is_file()]
scan_hash = uploading_binary(files)
scan_uploaded_file(scan_hash)
generate_json_report(scan_hash)
generate_pdf_report(scan_hash)
process_json_file()
