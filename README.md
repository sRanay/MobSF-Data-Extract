# MobSF-Data-Extract
This repository contains a main python script (`Main.py`) that automates the extraction and analysis of security data from Mobile applications using the MobSF REST API. 

### Note
This project is still in the works, which I am trying to plan to finish by the end of the year if it is possible. 

## Usage
1. Put the binaries into the `Binary` folder
2. Delete the folder for `Reports/JSON` and `Report/PDF`
3. Run `python Main.py` to generate the reports and information for penetration testing report

## Example output
```
PS .... > python .\Main.py
[*] Starting MobSF container...
....
[*] Scanning Binaries
[+] Scan finished successfully for 82ab8b2193b3cfb1c737e3a786be363a.
[+] Scan finished successfully for b919e84e7d35f68e16b6cd05d8e3b1ce.
[*] Generating JSON Report
[+] JSON report saved as mobsf_report-82ab8b2193b3cfb1c737e3a786be363a.json
[+] JSON report saved as mobsf_report-b919e84e7d35f68e16b6cd05d8e3b1ce.json
[*] Generating PDF Report
[+] JSON report saved as mobsf_report-82ab8b2193b3cfb1c737e3a786be363a.pdf
[+] JSON report saved as mobsf_report-b919e84e7d35f68e16b6cd05d8e3b1ce.pdf

====================== Reviewing results for DivaApplication.apk ======================
....

====================== Reviewing results for DVIA-v2.ipa ======================
....
```