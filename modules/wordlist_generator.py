import itertools
from colorama import Fore
from tqdm import tqdm

def run():
    base_words = input("\n[+] Enter Base Words (comma separated): ").split(',')
    year_range = range(2000, 2025)
    
    with open("custom_wordlist.txt", "w") as f:
        print(Fore.YELLOW + "[~] Generating combinations...")
        for combo in tqdm(itertools.product(base_words, map(str, year_range)), 
                        desc=Fore.CYAN + "Creating Wordlist"):
            f.write(''.join(combo) + '\n')
    
    print(Fore.GREEN + f"[+] Wordlist saved to custom_wordlist.txt ({len(base_words)*25} entries)")