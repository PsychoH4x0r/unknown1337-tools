import requests
from tqdm import tqdm
from colorama import Fore

def run():
    domain = input("\n[+] Enter Domain: ").strip()
    wordlist = input("[+] Wordlist Path: ").strip()
    
    try:
        with open(wordlist) as f:
            subdomains = [line.strip() for line in f]
        
        print(Fore.YELLOW + f"[~] Brute-forcing {len(subdomains)} subdomains...")
        
        valid = []
        for sub in tqdm(subdomains, desc=Fore.CYAN + "Checking Subdomains"):
            url = f"http://{sub}.{domain}"
            try:
                requests.get(url, timeout=3)
                valid.append(url)
            except:
                continue
        
        print(Fore.MAGENTA + "\n=== Valid Subdomains ===")
        for sub in valid:
            print(Fore.GREEN + f"[+] {sub}")
            
    except Exception as e:
        print(Fore.RED + f"[!] Error: {str(e)}")