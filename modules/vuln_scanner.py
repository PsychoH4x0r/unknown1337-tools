import requests
from colorama import Fore

VULN_PATHS = [
    '/.git/HEAD',
    '/.env',
    '/phpinfo.php',
    '/admin/config.php'
]

def run():
    url = input("\n[+] Enter Base URL: ").strip()
    print(Fore.YELLOW + "[~] Scanning for common vulnerabilities...")
    
    for path in VULN_PATHS:
        try:
            response = requests.get(url + path)
            if response.status_code == 200:
                print(Fore.RED + f"[!] Found exposed {path}")
        except:
            continue
    print(Fore.GREEN + "[+] Basic vulnerability scan completed")