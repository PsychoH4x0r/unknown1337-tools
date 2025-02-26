import getpass
from impacket import smbconnection
from colorama import Fore

def run():
    target = input(f"\n{Fore.WHITE}[+] Enter DC IP: ")
    username = input("[+] Username: ")
    password = getpass.getpass("[+] Password: ")
    domain = input("[+] Domain: ")

    try:
        conn = smbconnection.SMBConnection(target, target)
        conn.login(username, password, domain)
        print(f"{Fore.GREEN}[+] Successful login!")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed: {str(e)}")