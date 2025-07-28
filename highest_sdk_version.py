import requests
import re

def get_highest_android_sdk_version():
    url = "https://dl.google.com/android/repository/repository2-1.xml"
    response = requests.get(url)
    response.raise_for_status()

    # Search for lines like: <remotePackage path="platforms;android-34">
    matches = re.findall(r'path="platforms;android-(\d+)"', response.text)

    sdk_versions = [int(match) for match in matches]
    return max(sdk_versions) if sdk_versions else None