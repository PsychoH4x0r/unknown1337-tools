import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style
from prettytable import PrettyTable
from tqdm import tqdm

def run():
    def get_target():
        target = input("\n[+] Enter Target IP/Domain: ").strip()
        try:
            return socket.gethostbyname(target)
        except socket.gaierror:
            print(Fore.RED + "[!] Invalid target or domain not resolved")
            return None

    def scan_port(target, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((target, port))
                return port
        except:
            return None

    target = get_target()
    if not target:
        return

    ports = [21, 22, 80, 443, 8080, 3306, 3389, 8000, 8008, 8888]
    open_ports = []

    print(Fore.YELLOW + f"\n[~] Scanning {target}...")
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, target, port): port for port in ports}
        
        for future in tqdm(as_completed(futures), total=len(ports), 
                        desc=Fore.CYAN + "Scanning Ports", 
                        bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.YELLOW, Fore.WHITE)):
            result = future.result()
            if result:
                open_ports.append(result)

    table = PrettyTable()
    table.field_names = [f"{Fore.CYAN}Port", f"{Fore.GREEN}Service", f"{Fore.YELLOW}Status"]
    for port in sorted(open_ports):
        try:
            service = socket.getservbyport(port)
        except:
            service = "Unknown"
        table.add_row([port, service, Fore.GREEN + "OPEN"])
    
    print(Fore.MAGENTA + "\n=== Port Scan Results ===")
    print(table)
    print(Fore.YELLOW + f"\nFound {len(open_ports)} open ports")