import dns.resolver
from colorama import Fore
from prettytable import PrettyTable

def run():
    def reverse_lookup(ip):
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = ['8.8.8.8', '1.1.1.1']
            return [str(r).rstrip('.') for r in resolver.resolve(dns.reversename.from_address(ip), 'PTR')]
        except dns.resolver.NXDOMAIN:
            return []
        except Exception as e:
            print(Fore.RED + f"[!] DNS Error: {str(e)}")
            return []

    ip = input("\n[+] Enter IP Address: ").strip()
    
    if not ip.replace('.', '').isdigit():
        print(Fore.RED + "[!] Invalid IP address")
        return
    
    domains = reverse_lookup(ip)
    
    table = PrettyTable()
    table.field_names = [f"{Fore.CYAN}IP Address", f"{Fore.GREEN}Associated Domains"]
    table.align = "l"
    
    if domains:
        for domain in domains:
            table.add_row([ip, domain])
    else:
        table.add_row([ip, Fore.RED + "No domains found"])
    
    print(Fore.MAGENTA + "\n=== Reverse IP Results ===")
    print(table)