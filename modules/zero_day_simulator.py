import random
from colorama import Fore
from prettytable import PrettyTable

def run():
    print(f"\n{Fore.RED}=== ZERO-DAY EXPLOIT SIMULATOR ===")
    systems = ['Windows 11', 'Linux Kernel 6.x', 'iOS 16', 'Android 13']
    vuln_system = random.choice(systems)
    
    table = PrettyTable()
    table.field_names = [f"{Fore.CYAN}Component", f"{Fore.GREEN}Status"]
    table.add_row(["Memory Corruption", "Vulnerable"])
    table.add_row(["Privilege Escalation", "Possible"])
    table.add_row(["Target System", vuln_system])
    
    print(table)
    print(f"{Fore.YELLOW}[!] This is a simulation for training purposes!")