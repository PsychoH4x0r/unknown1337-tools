from googlesearch import search
from colorama import Fore

def run():
    dork = input("\n[+] Enter Google Dork: ").strip()
    print(Fore.YELLOW + "[~] Searching with Google Dork...")
    
    try:
        results = []
        for url in search(dork, num=10, stop=10, pause=2):
            results.append(url)
            print(Fore.CYAN + f"[+] Found: {url}")
            
        if not results:
            print(Fore.RED + "[!] No results found")
            
    except Exception as e:
        print(Fore.RED + f"[!] Error: {str(e)}")