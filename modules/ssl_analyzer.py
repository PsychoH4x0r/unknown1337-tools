import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from colorama import Fore
from prettytable import PrettyTable
from datetime import datetime

def run():
    def get_cert(hostname):
        cert = ssl.get_server_certificate((hostname, 443))
        return x509.load_pem_x509_certificate(cert.encode(), default_backend())

    host = input("\n[+] Enter Domain: ").strip()
    
    try:
        cert = get_cert(host)
    except Exception as e:
        print(Fore.RED + f"[!] SSL Error: {str(e)}")
        return

    table = PrettyTable()
    table.field_names = [f"{Fore.CYAN}Attribute", f"{Fore.GREEN}Value"]
    table.align = "l"
    
    # Subject Info
    subject = {}
    for attr in cert.subject:
        subject[attr.oid._name] = attr.value
    table.add_row(["Subject", "\n".join([f"{k}: {v}" for k, v in subject.items()])])
    
    # Validity
    valid_from = cert.not_valid_before.strftime("%Y-%m-%d")
    valid_to = cert.not_valid_after.strftime("%Y-%m-%d")
    table.add_row(["Validity", f"{valid_from} to {valid_to}"])
    
    # Signature Algorithm
    table.add_row(["Signature Algorithm", cert.signature_algorithm_oid._name])
    
    # Extensions
    extensions = []
    for ext in cert.extensions:
        extensions.append(ext.oid._name)
    table.add_row(["Extensions", "\n".join(extensions)])
    
    print(Fore.MAGENTA + "\n=== SSL Certificate Details ===")
    print(table)