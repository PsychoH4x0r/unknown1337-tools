import os
import re
import requests
from colorama import Fore, Style
from prettytable import PrettyTable

def run():
    print(f"\n{Fore.CYAN}=== Wayback Machine Scraper ===")
    print(f"{Fore.YELLOW}Scraping historical data from archive.org\n")
    
    domain = input(f"{Fore.WHITE}[+] Enter domain (e.g example.com): ").strip()
    
    try:
        # Parameter untuk API Wayback Machine
        params = {
            'url': f'*.{domain}/*',
            'collapse': 'urlkey',
            'output': 'text',
            'fl': 'original'
        }
        
        # Ekstensi file yang akan difilter
        file_extensions = [
            'xls', 'xml', 'xlsx', 'json', 'pdf', 'sql', 'doc', 'docx',
            'pptx', 'txt', 'git', 'zip', 'tar.gz', 'tgz', 'bak', '7z',
            'rar', 'log', 'cache', 'secret', 'db', 'backup', 'yml', 'gz',
            'config', 'csv', 'yaml', 'md', 'md5', 'exe', 'dll', 'bin',
            'ini', 'bat', 'sh', 'tar', 'deb', 'rpm', 'iso', 'img', 'env',
            'apk', 'msi', 'dmg', 'tmp', 'crt', 'pem', 'key', 'pub', 'asc'
        ]
        regex_pattern = re.compile(r'.*\.(' + '|'.join(file_extensions) + ')$', re.IGNORECASE)
        
        # Ambil data dari Wayback Machine
        print(f"\n{Fore.YELLOW}[~] Fetching data from archive.org...")
        response = requests.get(
            "https://web.archive.org/cdx/search/cdx",
            params=params,
            timeout=15
        )
        
        if response.status_code != 200:
            print(f"{Fore.RED}[!] Error fetching data: HTTP {response.status_code}")
            return
            
        all_urls = [url for url in response.text.split('\n') if url]
        
        if not all_urls:
            print(f"{Fore.RED}[!] No URLs found for this domain")
            return
            
        # Filter URL sensitif
        print(f"{Fore.YELLOW}[~] Filtering sensitive files...")
        sensitive_urls = [url for url in all_urls if regex_pattern.search(url)]
        
        # Tampilkan hasil
        print(f"\n{Fore.GREEN}[+] Results:")
        print(f"{Fore.WHITE}Total URLs      : {Fore.CYAN}{len(all_urls)}")
        print(f"{Fore.WHITE}Sensitive Files : {Fore.RED}{len(sensitive_urls)}")
        
        # Tampilkan contoh dalam tabel
        table = PrettyTable()
        table.field_names = [f"{Fore.CYAN}Type", f"{Fore.GREEN}Example URLs"]
        table.add_row([f"{Fore.YELLOW}All URLs", all_urls[0]])
        
        if sensitive_urls:
            table.add_row([f"{Fore.RED}Sensitive Files", sensitive_urls[0]])
        
        print(f"\n{Fore.MAGENTA}=== Sample Results ===")
        print(table)
        
        # Simpan ke file
        save = input(f"\n{Fore.WHITE}[+] Save full results to files? (y/n): ").lower()
        if save == 'y':
            with open(f"{domain}_all_urls.txt", "w") as f:
                f.write("\n".join(all_urls))
            with open(f"{domain}_sensitive_urls.txt", "w") as f:
                f.write("\n".join(sensitive_urls))
            print(f"{Fore.GREEN}[+] Saved to:")
            print(f"  - {domain}_all_urls.txt")
            print(f"  - {domain}_sensitive_urls.txt")
            
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}")
    finally:
        input(f"\n{Fore.YELLOW}[!] Press Enter to return to menu...")