import requests
from colorama import Fore

def run():
    domain = input("\n[+] Enter Domain: ").strip()
    print(Fore.YELLOW + "[~] Searching S3 Buckets...")
    
    buckets = [
        f"https://s3.amazonaws.com/{domain}",
        f"https://{domain}.s3.amazonaws.com",
        f"https://assets.{domain}.s3.amazonaws.com"
    ]
    
    found = []
    for bucket in buckets:
        try:
            response = requests.get(bucket)
            if response.status_code == 200:
                found.append(bucket)
        except:
            continue
    
    if found:
        print(Fore.MAGENTA + "\n=== Open S3 Buckets ===")
        for bucket in found:
            print(Fore.GREEN + f"[+] {bucket}")
    else:
        print(Fore.RED + "[!] No open S3 buckets found")