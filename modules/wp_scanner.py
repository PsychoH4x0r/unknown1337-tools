import requests
from colorama import Fore

def run():
    url = input("\n[+] Enter WordPress Site: ").strip()
    print(Fore.YELLOW + "[~] Scanning WordPress...")
    
    checks = {
        'Version Exposure': '/wp-includes/version.php',
        'Readme File': '/readme.html',
        'User Enum': '/?author=1',
        'Config Backup': '/wp-config.php~'
    }
    
    vulns = []
    for name, path in checks.items():
        try:
            response = requests.get(url+path)
            if response.status_code == 200:
                vulns.append(f"{Fore.RED}[!] {name} Exposed")
        except:
            continue
    
    if vulns:
        print(Fore.MAGENTA + "\n=== WordPress Issues ===")
        for vuln in vulns:
            print(vuln)
    else:
        print(Fore.GREEN + "[+] No common vulnerabilities found")