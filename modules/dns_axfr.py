import dns.zone
import dns.query
from colorama import Fore

def run():
    domain = input(f"\n{Fore.WHITE}[+] Enter domain: ")
    ns_server = input("[+] Enter NS server: ")
    
    try:
        zone = dns.zone.from_xfr(dns.query.xfr(ns_server, domain))
        print(f"{Fore.GREEN}[+] Zone transfer successful:")
        for name in zone.nodes:
            print(f"{Fore.CYAN}{name}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed: {str(e)}")