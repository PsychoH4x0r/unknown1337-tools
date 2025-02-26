import hashlib
from colorama import Fore

def run():
    hash_type = input("\n[+] Hash Type (md5/sha1/sha256): ").strip()
    hash_value = input("[+] Enter Hash: ").strip()
    wordlist = input("[+] Wordlist Path: ").strip()

    try:
        with open(wordlist, 'r') as f:
            for line in tqdm(f, desc=Fore.YELLOW + "Cracking Hash"):
                plain = line.strip()
                if hash_type == 'md5' and hashlib.md5(plain.encode()).hexdigest() == hash_value:
                    print(Fore.GREEN + f"\n[+] Password Found: {plain}")
                    return
                # Tambahkan jenis hash lainnya...
        print(Fore.RED + "\n[!] Password not found in wordlist")
    except Exception as e:
        print(Fore.RED + f"[!] Error: {str(e)}")