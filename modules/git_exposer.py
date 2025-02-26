import requests
from colorama import Fore

def run():
    url = input("\n[+] Enter Target URL: ").strip()
    paths = ['/.git/HEAD', '/.git/config', '/.git/logs/HEAD']
    
    print(Fore.YELLOW + "[~] Checking Git Exposure...")
    
    exposed = []
    for path in paths:
        try:
            response = requests.get(url+path)
            if response.status_code == 200:
                exposed.append(path)
        except:
            continue
    
    if exposed:
        print(Fore.RED + "\n[!] Exposed Git Paths:")
        for path in exposed:
            print(Fore.CYAN + f"- {path}")
    else:
        print(Fore.GREEN + "[+] No exposed Git repositories found")