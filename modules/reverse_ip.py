import dns.resolver
import ipaddress
import requests
from datetime import datetime
from colorama import Fore, Style, init
from prettytable import PrettyTable

init(autoreset=True)

class FullReverseLookup:
    def __init__(self):
        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = ['8.8.8.8', '1.1.1.1', '9.9.9.9']
        self.api_url = "https://api.viewdns.info/reverseip/"
        self.api_key = "a304509c13bb5c04da194b190e9c156d0e175d9e"  # Daftar di viewdns.info untuk mendapatkan API key

    def show_header(self):
        print(f"\n{Fore.CYAN}┌{'─'*60}┐")
        print(f"│{Fore.YELLOW}{'FULL REVERSE IP LOOKUP':^60}{Fore.CYAN}│")
        print(f"├{'─'*60}┤")
        print(f"│{Fore.WHITE} Find ALL domains hosted on a target IP address {' '*17}{Fore.CYAN}│")
        print(f"└{'─'*60}┘")

    def get_api_results(self, ip):
        """Menggunakan API untuk mendapatkan semua domain"""
        try:
            params = {
                'host': ip,
                'apikey': self.api_key,
                'output': 'json'
            }
            response = requests.get(self.api_url, params=params)
            data = response.json()
            
            if data['response']['domain_count'] == 0:
                return []
                
            return [
                (domain['name'], domain['last_resolved']) 
                for domain in data['response']['domains']
            ]
        except Exception as e:
            print(f"{Fore.RED}API Error: {str(e)}")
            return []

    def get_dns_records(self, domain):
        """Verifikasi DNS record terbaru"""
        try:
            answers = self.resolver.resolve(domain, 'A')
            return [str(r) for r in answers]
        except Exception:
            return []

    def show_full_results(self, ip, results):
        print(f"\n{Fore.CYAN}Reverse IP results for {ip}")
        print(f"{Fore.YELLOW}Found {len(results)} domains hosted on this server")
        print(f"{Fore.CYAN}┌{'─'*35}┬{'─'*15}┬{'─'*20}┐")
        print(f"│{Fore.GREEN} Domain Name{' '*22} │ Last Resolved │ Current IP(s){' '*7} {Fore.CYAN}│")
        print(f"├{'─'*35}┼{'─'*15}┼{'─'*20}┤")
        
        for domain, last_resolved in results:
            current_ips = self.get_dns_records(domain)
            ips = ', '.join(current_ips) if current_ips else f"{Fore.RED}N/A"
            
            print(f"│ {domain[:34]:<34} │ {last_resolved} │ {ips[:18]:<18} {Fore.CYAN}│")
        
        print(f"└{'─'*35}┴{'─'*15}┴{'─'*20}┘")

    def main_menu(self):
        while True:
            self.show_header()
            print(f"\n{Fore.CYAN}1. Full Reverse Lookup")
            print(f"{Fore.CYAN}2. Set API Key")
            print(f"{Fore.RED}3. Exit")
            
            choice = input(f"\n{Fore.YELLOW}Select option (1-3): ")
            
            if choice == '1':
                target = input(f"\n{Fore.CYAN}Enter Domain/IP: ").strip()
                
                try:
                    # Resolve input ke IP
                    try:
                        ip_obj = ipaddress.ip_address(target)
                        ip = str(ip_obj)
                    except ValueError:
                        answers = self.resolver.resolve(target, 'A')
                        ip = str(answers[0])
                        print(f"{Fore.GREEN}Resolved to IP: {ip}")
                        
                    # Ambil data dari API
                    api_results = self.get_api_results(ip)
                    
                    if not api_results:
                        print(f"{Fore.YELLOW}No domains found via API, trying DNS lookup...")
                        ptr_results = self.resolver.resolve(dns.reversename.from_address(ip), 'PTR')
                        api_results = [(str(r), datetime.now().strftime('%Y-%m-%d')) for r in ptr_results]
                    
                    if api_results:
                        self.show_full_results(ip, api_results)
                    else:
                        print(f"{Fore.RED}No domains found for {ip}")
                        
                except Exception as e:
                    print(f"{Fore.RED}Error: {str(e)}")
                
            elif choice == '2':
                new_key = input(f"{Fore.CYAN}Enter new API key: ")
                self.api_key = new_key
                print(f"{Fore.GREEN}API key updated!")
            
            elif choice == '3':
                print(f"{Fore.GREEN}Exiting...")
                break
            
            else:
                print(f"{Fore.RED}Invalid choice!")

if __name__ == "__main__":
    tool = FullReverseLookup()
    tool.main_menu()
