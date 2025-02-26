import jwt
from tqdm import tqdm
from colorama import Fore

def run():
    token = input("\n[+] Enter JWT Token: ").strip()
    wordlist = input("[+] Wordlist Path: ").strip()
    
    try:
        with open(wordlist) as f:
            secrets = [line.strip() for line in f]
        
        print(Fore.YELLOW + f"[~] Testing {len(secrets)} secrets...")
        
        for secret in tqdm(secrets, desc=Fore.CYAN + "Cracking JWT"):
            try:
                jwt.decode(token, secret, algorithms=["HS256"])
                print(Fore.GREEN + f"\n[+] Secret Found: {secret}")
                return
            except:
                continue
        print(Fore.RED + "\n[!] Secret not found in wordlist")
        
    except Exception as e:
        print(Fore.RED + f"[!] Error: {str(e)}")