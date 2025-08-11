# MobSF-Data-Extract
This repository contains a main python script (`Main.py`) that automates the extraction and analysis of security data from Mobile applications using the MobSF REST API.

## Prerequisite
1. Install the libraries to be used inside `requirements.txt`
2. Ensure that Docker Desktop is installed for Windows devices or Docker can be run on Linux/MacOS devices

## Usage
1. Put the binaries into the `Binary` folder
2. Delete the folder content inside `Reports/JSON`, `Report/PDF` and `Export`
3. Run `python Main.py` to generate the reports and information for penetration testing report

## Example output
```
PS .... > python .\Main.py
[*] Starting MobSF container...
[*] Starting MobSF. Please wait for a minute
[*] MobSF is running at http://127.0.0.1:8000
[*] Uploading Binaries
[*] Scanning Binaries
[+] Scan finished successfully for 82ab8b2193b3cfb1c737e3a786be363a.
[+] Scan finished successfully for b919e84e7d35f68e16b6cd05d8e3b1ce.
[*] Generating JSON Report
[+] JSON report saved as mobsf_report-82ab8b2193b3cfb1c737e3a786be363a.json
[+] JSON report saved as mobsf_report-b919e84e7d35f68e16b6cd05d8e3b1ce.json
[*] Generating PDF Report
[+] PDF report saved as mobsf_report-82ab8b2193b3cfb1c737e3a786be363a.pdf
[+] PDF report saved as mobsf_report-b919e84e7d35f68e16b6cd05d8e3b1ce.pdf
[*] Processing for DivaApplication.apk
[+] Done reviewing result for DivaApplication.apk
[*] Processing for DVIA-v2.ipa
[+] Done reviewing result for DVIA-v2.ipa
[*] Please check the results in the Exports Folder
```

## Checks being done

**Note: Might have some checks that I might have missed out**

**For iOS**:
- Checking application permissions used
- ATS analysis
- Binary analysis
- URL Schemes used
- Retrieve the Minimum iOS version for the application

**For Android:**
- Checking application permissions used
- Retrieving the Minimum SDK version for the application
- Checking v1 Signature if it is true
- Checking Bit Size of the Signature
- Binary Analysis
- Manifest Analysis