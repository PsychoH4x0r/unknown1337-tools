import re
import os
from colorama import Fore

def run():
    print(f"\n{Fore.CYAN}=== API Key Extractor ===")
    directories = input(f"{Fore.WHITE}[+] Enter directories to scan (comma separated): ").split(',')
    
    api_key_pattern = re.compile(r'(?i)(?:api|secret)[_-]?key\s*[:=]\s*[\'"]?([a-z0-9]{32,45})[\'"]?')
    found_keys = []

    for dir_path in directories:
        dir_path = dir_path.strip()
        if os.path.exists(dir_path):
            for root, _, files in os.walk(dir_path):
                for file in files:
                    if file.endswith(('.env', '.config', '.json', '.yaml', '.php', '.py')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r') as f:
                                content = f.read()
                                matches = api_key_pattern.findall(content)
                                if matches:
                                    found_keys.append((file_path, matches))
                        except:
                            continue

    print(f"\n{Fore.GREEN}[+] Found {len(found_keys)} API keys:")
    for path, keys in found_keys:
        print(f"{Fore.YELLOW}File: {path}")
        for key in keys:
            print(f"{Fore.RED}Key: {key}")