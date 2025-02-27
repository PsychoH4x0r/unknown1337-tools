import dns.resolver
import ipaddress
import requests
from colorama import Fore, Style, init
from prettytable import PrettyTable

init(autoreset=True)

class ReverseIPLookup:
    def __init__(self):
        self.api_url = "https://ip.0x1999.tech/"
        self.api_key = "0x1999"
        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = ['8.8.8.8', '1.1.1.1', '9.9.9.9']

    def show_banner(self):
        print(f"""
        {Fore.CYAN}Reverse IP Lookup Tool - UNKNOWN1337 WASS HERE!!! 
        {Style.RESET_ALL}
        """)

    def get_api_data(self, ip):
        try:
            response = requests.get(f"{self.api_url}?apikey={self.api_key}&ip={ip}")
            print(f"DEBUG: API Response ({response.status_code}): {response.text}")  # Debugging
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"{Fore.RED}Error: Received status code {response.status_code}")
                return None
        except Exception as e:
            print(f"{Fore.RED}API Error: {str(e)}")
            return None

    def show_results(self, ip, data):
        if not data or "domains" not in data:
            print(f"{Fore.RED}Error: Unexpected response format or missing 'domains' key")
            return
        
        table = PrettyTable()
        table.field_names = ["No", "Domain Name"]
        table.align = "l"
        
        for idx, domain in enumerate(data.get('domains', []), 1):
            table.add_row([idx, domain])
        
        print(f"\n{Fore.YELLOW}Reverse IP Results for {ip}:")
        print(f"{Fore.CYAN}Total Domains Found: {len(data.get('domains', []))}")
        print(table)

    def run(self):
        while True:
            self.show_banner()
            print(f"{Fore.CYAN}1. Start Reverse Lookup")
            print(f"{Fore.CYAN}2. Set Custom API Key")
            print(f"{Fore.RED}3. Exit\n")

            choice = input(f"{Fore.YELLOW}[?] Select option (1-3): ")

            if choice == '1':
                target = input(f"\n{Fore.CYAN}[+] Enter IP/Domain: ").strip()

                try:
                    try:
                        ip = str(ipaddress.ip_address(target))
                    except ValueError:
                        answers = self.resolver.resolve(target, 'A')
                        ip = str(answers[0])
                        print(f"{Fore.GREEN}Resolved to IP: {ip}")
                    
                    data = self.get_api_data(ip)
                    if data:
                        self.show_results(ip, data)
                except Exception as e:
                    print(f"{Fore.RED}Error: {str(e)}")
                
                input(f"\n{Fore.CYAN}[Press Enter to continue...]")

            elif choice == '2':
                self.api_key = input(f"\n{Fore.CYAN}[+] Enter new API key: ")
                print(f"{Fore.GREEN}API key updated successfully!")

            elif choice == '3':
                print(f"{Fore.GREEN}Exiting...")
                break

            else:
                print(f"{Fore.RED}Invalid selection!")

if __name__ == "__main__":
    tool = ReverseIPLookup()
    tool.run()
