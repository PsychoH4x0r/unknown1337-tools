from scapy.all import *
from colorama import Fore

def packet_handler(packet):
    if IP in packet:
        print(f"{Fore.CYAN}{packet[IP].src} -> {Fore.GREEN}{packet[IP].dst}")

def run():
    print(Fore.YELLOW + "\n[~] Sniffing network traffic (Ctrl+C to stop)...")
    try:
        sniff(prn=packet_handler, filter="ip", store=0)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Sniffing stopped")