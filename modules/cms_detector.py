import requests
from colorama import Fore

CMS_SIGNATURES = {
    'WordPress': '/wp-content/',
    'Joomla': '/media/system/js/',
    'Drupal': '/sites/all/themes/'
}

def run():
    url = input("\n[+] Enter URL: ").strip()
    try:
        response = requests.get(url)
        for cms, sig in CMS_SIGNATURES.items():
            if sig in response.text:
                print(Fore.GREEN + f"[+] CMS Detected: {cms}")
                return
        print(Fore.RED + "[!] CMS Not Recognized")
    except Exception as e:
        print(Fore.RED + f"[!] Error: {str(e)}")