import requests
from colorama import Fore

providers = {
    'github.io': 'https://github.com/404',
    'azurewebsites.net': 'https://azurewebsites.net/404'
}

def run():
    subdomain = input(f"\n{Fore.WHITE}[+] Enter subdomain: ")
    for provider, check_url in providers.items():
        if provider in subdomain:
            response = requests.get(f"http://{subdomain}", timeout=5)
            if response.status_code == 404:
                print(f"{Fore.GREEN}[+] Vulnerable to {provider} takeover")