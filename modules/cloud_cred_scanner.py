import os
import re
from colorama import Fore

def run():
    print(f"\n{Fore.CYAN}=== Cloud Credential Scanner ===")
    aws_pattern = re.compile(r'(AKIA|ASIA)[A-Z0-9]{16}')
    gcp_pattern = re.compile(r'"type": "service_account"')
    azure_pattern = re.compile(r'InstrumentationKey=[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

    for root, _, files in os.walk('/'):
        for file in files:
            if file.endswith(('.json', '.pem', '.cfg')):
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        content = f.read()
                        if aws_pattern.search(content):
                            print(f"{Fore.RED}[!] AWS Creds in {os.path.join(root, file)}")
                        if gcp_pattern.search(content):
                            print(f"{Fore.RED}[!] GCP Creds in {os.path.join(root, file)}")
                        if azure_pattern.search(content):
                            print(f"{Fore.RED}[!] Azure Creds in {os.path.join(root, file)}")
                except:
                    continue