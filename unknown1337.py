#!/usr/bin/env python3
import os
import sys
from colorama import Fore, Style, init

# Import semua modul yang diperlukan
from modules.reverse_ip import ReverseIPLookup
from modules.ddos_tool import DDoSTool
from modules import (
    port_scanner,
    vsftpd_exploit,
    whois_lookup,
    ssl_analyzer,
    cve_2021_41773,
    shellshock_exploit,
    wordlist_generator,
    hash_cracker,
    network_sniffer,
    cms_detector,
    ssh_bruteforce,
    vuln_scanner,
    metasploit_generator,
    wayback_scraper,
    google_dorking,
    laravel_exploit,
    subdomain_brute,
    wp_scanner,
    jwt_cracker,
    git_exposer,
    s3_finder,
    xxe_tester,
    crlf_injection,
    api_key_extractor,
    log4j_scanner,
    deserialization_exploit,
    cloud_cred_scanner,
    ad_password_spray,
    dns_axfr,
    subdomain_takeover,
    email_spoof_check,
    fastcgi_exploit,
    zero_day_simulator
)

init(autoreset=True)

class Unknown1337Tools:
    def __init__(self):
        # Dictionary untuk semua tools
        self.modules = {
            '1': ("Port Scanner", port_scanner.run),
            '2': ("Reverse IP Lookup", ReverseIPLookup().run),
            '3': ("VS-FTPD 2.3.4 Exploit", vsftpd_exploit.run),
            '4': ("WHOIS Lookup", whois_lookup.run),
            '5': ("SSL/TLS Analyzer", ssl_analyzer.run),
            '6': ("CVE-2021-41773 Exploit", cve_2021_41773.run),
            '7': ("Shellshock Exploit", shellshock_exploit.run),
            '8': ("Wordlist Generator", wordlist_generator.run),
            '9': ("Hash Cracker", hash_cracker.run),
            '10': ("Network Sniffer", network_sniffer.run),
            '11': ("CMS Detector", cms_detector.run),
            '12': ("SSH Bruteforce", ssh_bruteforce.run),
            '13': ("Vulnerability Scanner", vuln_scanner.run),
            '14': ("DDoS Tool", DDoSTool().run),
            '15': ("Metasploit Generator", metasploit_generator.run),
            '16': ("Wayback Scraper", wayback_scraper.run),
            '17': ("Google Dorking", google_dorking.run),
            '18': ("Laravel RCE Exploit", laravel_exploit.run),
            '19': ("Subdomain Bruteforce", subdomain_brute.run),
            '20': ("WordPress Scanner", wp_scanner.run),
            '21': ("JWT Cracker", jwt_cracker.run),
            '22': ("Git Exposer", git_exposer.run),
            '23': ("S3 Bucket Finder", s3_finder.run),
            '24': ("XXE Tester", xxe_tester.run),
            '25': ("CRLF Injection", crlf_injection.run),
            '26': ("API Key Extractor", api_key_extractor.run),
            '27': ("Log4j Scanner", log4j_scanner.run),
            '28': ("Deserialization Exploit", deserialization_exploit.run),
            '29': ("Cloud Cred Scanner", cloud_cred_scanner.run),
            '30': ("AD Password Spray", ad_password_spray.run),
            '31': ("DNS Zone Transfer", dns_axfr.run),
            '32': ("Subdomain Takeover", subdomain_takeover.run),
            '33': ("Email Spoof Check", email_spoof_check.run),
            '34': ("FastCGI Exploit", fastcgi_exploit.run),
            '35': ("Zero-Day Simulator", zero_day_simulator.run)
        }

    def show_banner(self):
        print(Fore.MAGENTA + r"""
██╗░░░██╗███╗░░██╗██╗░░██╗███╗░░██╗░█████╗░░██╗░░░░░░░██╗███╗░░██╗░░███╗░░██████╗░██████╗░███████╗
██║░░░██║████╗░██║██║░██╔╝████╗░██║██╔══██╗░██║░░██╗░░██║████╗░██║░████║░░╚════██╗╚════██╗╚════██║
██║░░░██║██╔██╗██║█████═╝░██╔██╗██║██║░░██║░╚██╗████╗██╔╝██╔██╗██║██╔██║░░░█████╔╝░█████╔╝░░░░██╔╝
██║░░░██║██║╚████║██╔═██╗░██║╚████║██║░░██║░░████╔═████║░██║╚████║╚═╝██║░░░╚═══██╗░╚═══██╗░░░██╔╝░
╚██████╔╝██║░╚███║██║░╚██╗██║░╚███║╚█████╔╝░░╚██╔╝░╚██╔╝░██║░╚███║███████╗██████╔╝██████╔╝░░██╔╝░░
░╚═════╝░╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░╚══╝░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░╚══╝╚══════╝╚═════╝░╚═════╝░░░╚═╝░░░
        """)
        print(Fore.CYAN + "═════════════════════════════════════════════════════════════════════════")
        print(Fore.RED + "GITHUB: " + Fore.WHITE + "https://github.com/PsychoH4x0r/ultimate-tools")
        print(Fore.YELLOW + "WARNING: " + Fore.WHITE + "F0r H4x0r p3n3tr4ti0n t3st1n9 0nly!\n")

    def main_menu(self):
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            self.show_banner()
            print(Fore.GREEN + "🛠️  MAIN MENU - 35 PENTESTING TOOLS")
            print(Fore.CYAN + "───────────────────────────────────")

            # Tampilan dua kolom untuk 35 tools
            modules = list(self.modules.items())
            half = (len(modules) + 1) // 2

            for i in range(half):
                col1 = modules[i]
                col2 = modules[i + half] if (i + half) < len(modules) else (None, None)

                left = f"{Fore.YELLOW}{col1[0].rjust(2)}. {col1[1][0]}"
                right = f"{Fore.YELLOW}{col2[0].rjust(2)}. {col2[1][0]}" if col2[0] else ""

                print(f"{left.ljust(45)}{right}")

            print(Fore.YELLOW + "\n 0. Exit")
            print(Fore.CYAN + "──────────────────────────────────────────────────────")

            choice = input("\n[+] Select Tool (1-35): ")

            if choice == '0':
                sys.exit()
            elif choice in self.modules:
                os.system('clear' if os.name == 'posix' else 'cls')
                try:
                    self.modules[choice][1]()
                except Exception as e:
                    print(Fore.RED + f"\n[!] Critical Error: {str(e)}")
                    import traceback
                    traceback.print_exc()
                input("\nPress Enter to return to main menu...")
            else:
                print(Fore.RED + "[!] Invalid selection!")
                input("Press Enter to continue...")

if __name__ == '__main__':
    try:
        tool = Unknown1337Tools()
        tool.main_menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Operation terminated!")
        sys.exit(1)
