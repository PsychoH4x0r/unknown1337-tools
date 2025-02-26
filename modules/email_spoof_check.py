import dns.resolver
from colorama import Fore

def run():
    domain = input(f"\n{Fore.WHITE}[+] Enter domain: ")
    
    try:
        records = dns.resolver.resolve(domain, 'TXT')
        for rdata in records:
            if 'v=spf1' in str(rdata):
                print(f"{Fore.GREEN}[+] SPF record found: {rdata}")
            if 'v=DMARC1' in str(rdata):
                print(f"{Fore.GREEN}[+] DMARC record found: {rdata}")
    except:
        print(f"{Fore.RED}[!] No SPF/DMARC records found")