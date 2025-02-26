import whois
from colorama import Fore
from prettytable import PrettyTable

def run():
    def clean_whois(data):
        return {k: str(v).replace('\n', ' ') for k, v in data.items()}

    target = input("\n[+] Enter Domain/IP: ").strip()
    
    try:
        w = whois.whois(target)
        cleaned = clean_whois(w)
    except Exception as e:
        print(Fore.RED + f"[!] WHOIS Error: {str(e)}")
        return

    table = PrettyTable()
    table.field_names = [f"{Fore.CYAN}Field", f"{Fore.GREEN}Value"]
    table.align = "l"
    
    for key, value in cleaned.items():
        if value and value not in ['None', '']:
            table.add_row([key, value[:100] + ('...' if len(value) > 100 else '')])
    
    print(Fore.MAGENTA + "\n=== WHOIS Results ===")
    print(table)