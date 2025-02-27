import whois
from colorama import Fore, Style, init
from prettytable import PrettyTable
import socket
import json
import os
import re
import requests
from ipwhois import IPWhois
from ipwhois.exceptions import ASNRegistryError

init(autoreset=True)

def clean_whois(data):
    """Cleans WHOIS data, handling data types and edge cases."""
    cleaned_data = {}
    for k, v in data.items():
        if v is None:
            cleaned_data[k] = ""
        elif isinstance(v, list):
            cleaned_data[k] = ", ".join(str(item) for item in v)
        elif isinstance(v, bytes):
            try:
                cleaned_data[k] = v.decode('utf-8', 'replace')
            except Exception:
                cleaned_data[k] = str(v)
        else:
            cleaned_data[k] = str(v).replace('\n', ' ')
    return cleaned_data


def extract_emails(text):
    """Extracts email addresses from text using regex."""
    if not isinstance(text, str):
        return []
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(email_regex, text)


def get_http_headers(target):
    """Retrieves HTTP headers from a website."""
    try:
        if not target.startswith("http"):
            target = "http://" + target
        response = requests.get(target, timeout=10)
        response.raise_for_status()
        return response.headers
    except requests.exceptions.RequestException as e:
        return f"Error retrieving headers: {e}"


def ip_geolocation(ip_address):
    """Performs geolocation lookup for an IP address."""
    try:
        obj = IPWhois(ip_address)
        results = obj.lookup_rdap(depth=1)
        return results
    except ASNRegistryError:
        return "ASN lookup failed."
    except Exception as e:
        return f"Geolocation error: {e}"

def get_dns_info(target):
    """Retrieves DNS information for a domain or IP address."""
    dns_data = {}
    try:
        dns_data['A Records'] = socket.gethostbyname_ex(target)[2]
    except socket.gaierror:
        dns_data['A Records'] = "No A records found."
    except Exception as e:
        dns_data['A Records'] = f"Error retrieving A records: {e}"

    try:
        ip_address = socket.gethostbyname(target)
        dns_data['PTR Record'] = socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        dns_data['PTR Record'] = "No PTR record found."
    except socket.gaierror:
        dns_data['PTR Record'] = "No PTR record found (Invalid domain/IP)."
    except Exception as e:
        dns_data['PTR Record'] = f"Error retrieving PTR record: {e}"

    return dns_data

def display_dns_info(dns_data):
    """Displays DNS information in a table."""
    print(Fore.MAGENTA + "\n=== Informasi DNS ===")
    table = PrettyTable()
    table.field_names = [f"{Fore.CYAN}Jenis Record", f"{Fore.GREEN}Nilai"]
    table.align = "l"

    for record_type, value in dns_data.items():
        if isinstance(value, list):
            for ip in value:
                table.add_row([record_type, ip])
        else:
            table.add_row([record_type, value])
    print(table)


def display_whois_table(cleaned_data):
    """Displays cleaned WHOIS data in a table, showing ALL info."""
    table = PrettyTable()
    table.field_names = [f"{Fore.CYAN}Field", f"{Fore.GREEN}Value"]
    table.align = "l"

    print(Fore.MAGENTA + "\n=== Semua Hasil WHOIS ===")
    for field, value in cleaned_data.items():
        display_value = str(value)[:100] + ('...' if len(str(value)) > 100 else '')
        table.add_row([field.replace('_', ' ').title(), display_value])

    if table.rows:
        print(table)
    else:
        print(Fore.WHITE + "Tidak ada informasi WHOIS yang tersedia.")


def display_http_headers(headers):
    """Displays HTTP headers in a table."""
    if isinstance(headers, str):
        print(Fore.RED + headers)
        return

    table = PrettyTable()
    table.field_names = [f"{Fore.CYAN}Header", f"{Fore.GREEN}Nilai"]
    table.align = "l"
    print(Fore.MAGENTA + "\n=== Header HTTP ===")
    for header, value in headers.items():
        table.add_row([header, value])
    print(table)

def display_geolocation_data(geo_data):
    """Displays geolocation data in a readable format."""
    if isinstance(geo_data, str):
        print(Fore.RED + geo_data)
        return

    print(Fore.MAGENTA + "\n=== Data Geolocation IP ===")
    table = PrettyTable()
    table.field_names = [f"{Fore.CYAN}Field", f"{Fore.GREEN}Nilai"]
    table.align = "l"

    fields_to_display = {
        'ASN': 'asn',
        'Registri ASN': 'asn_registry',
        'Kode Negara ASN': 'asn_country_code',
        'Deskripsi ASN': 'asn_description',
        'Negara': 'country',
        'Kota': 'city',
        'Latitude': 'latitude',
        'Longitude': 'longitude'
    }

    for display_name, field_name in fields_to_display.items():
        if field_name in geo_data and geo_data[field_name]:
            table.add_row([display_name, geo_data[field_name]])

    if 'nets' in geo_data and geo_data['nets']:
        net_info = geo_data['nets'][0]
        for display_name, field_name in {
            'Alamat Jaringan': 'address',
            'Handle Jaringan': 'handle',
            'Nama Jaringan' : 'name',
            'Rentang Jaringan': 'range',
            'CIDR Jaringan' : 'cidr'

        }.items():
            if field_name in net_info and net_info[field_name]:
                table.add_row([display_name, net_info[field_name]])

    print(table)

def reverse_ip_lookup(ip_address):
    """Performs reverse IP lookup and handles errors."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        print(Fore.CYAN + "\n[+] Reverse IP Lookup:" + Fore.GREEN + f" Hostname: {hostname}")
    except socket.herror:
        print(Fore.CYAN + "\n[+] Reverse IP Lookup:" + Fore.RED + " No hostname found for this IP.")
    except Exception as e:
        print(Fore.RED + f"[!] Error Reverse IP Lookup: {str(e)}")


def save_output(data, filename):
    """Saves data to a JSON file, handling errors."""
    if not filename.endswith(".json"):
        filename += ".json"
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(Fore.GREEN + f"[+] Data saved to {filename}")
    except Exception as e:
        print(Fore.RED + f"[!] Error saving to file: {str(e)}")

def clear_screen():
    """Clears the console screen (cross-platform)."""
    os.system('cls' if os.name == 'nt' else 'clear')



def run():
    """Main function to run the WHOIS lookup tool."""
    while True:
        clear_screen()
        print(Fore.BLUE + """

██╗░░░██╗███╗░░██╗██╗░░██╗███╗░░██╗░█████╗░░██╗░░░░░░░██╗███╗░░██╗░░███╗░░██████╗░██████╗░███████╗
██║░░░██║████╗░██║██║░██╔╝████╗░██║██╔══██╗░██║░░██╗░░██║████╗░██║░████║░░╚════██╗╚════██╗╚════██║
██║░░░██║██╔██╗██║█████═╝░██╔██╗██║██║░░██║░╚██╗████╗██╔╝██╔██╗██║██╔██║░░░█████╔╝░█████╔╝░░░░██╔╝
██║░░░██║██║╚████║██╔═██╗░██║╚████║██║░░██║░░████╔═████║░██║╚████║╚═╝██║░░░╚═══██╗░╚═══██╗░░░██╔╝░
╚██████╔╝██║░╚███║██║░╚██╗██║░╚███║╚█████╔╝░░╚██╔╝░╚██╔╝░██║░╚███║███████╗██████╔╝██████╔╝░░██╔╝░░
░╚═════╝░╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░╚══╝░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝░░╚══╝╚══════╝╚═════╝░╚═════╝░░░╚═╝░░░

        Alat Lookup WHOIS By Unknown1337 r
        """)
        print(Fore.CYAN + "1. WHOIS Lookup (Kategori)")
        print(Fore.CYAN + "2. WHOIS Lookup (Semua Data)")
        print(Fore.CYAN + "3. Reverse IP Lookup")
        print(Fore.CYAN + "4. Simpan Output ke JSON")
        print(Fore.CYAN + "5. Bersihkan Layar")
        print(Fore.CYAN + "6. Keluar")
        print(Fore.CYAN + "7. Dapatkan Header HTTP")
        print(Fore.CYAN + "8. IP Geolocation")
        print(Fore.CYAN + "9. Informasi DNS")


        choice = input(Fore.GREEN + "Pilih opsi: ").strip()

        if choice == '1':
            target = input(Fore.CYAN + "\n[+] Masukkan Domain/IP: ").strip()
            try:
                w = whois.whois(target)
                cleaned = clean_whois(w)
                display_whois_table_categorized(cleaned)
                all_text = str(w)
                emails = extract_emails(all_text)
                if emails:
                    print(Fore.YELLOW + "\n--- Email yang Diekstrak ---")
                    for email in emails:
                        print(Fore.GREEN + email)

            except Exception as e:
                print(Fore.RED + f"[!] Error WHOIS: {str(e)}")
            input(Fore.YELLOW + "\nTekan Enter untuk melanjutkan...")

        elif choice == '2':
            target = input(Fore.CYAN + "\n[+] Masukkan Domain/IP: ").strip()
            try:
                w = whois.whois(target)
                cleaned = clean_whois(w)
                display_whois_table(cleaned)
                all_text = str(w)
                emails = extract_emails(all_text)
                if emails:
                    print(Fore.YELLOW + "\n--- Email yang Diekstrak ---")
                    for email in emails:
                        print(Fore.GREEN + email)

            except Exception as e:
                print(Fore.RED + f"[!] Error WHOIS: {str(e)}")
            input(Fore.YELLOW + "\nTekan Enter untuk melanjutkan...")


        elif choice == '3':
            ip_target = input(Fore.CYAN + "\n[+] Masukkan Alamat IP untuk Reverse Lookup: ").strip()
            reverse_ip_lookup(ip_target)
            input(Fore.YELLOW + "\nTekan Enter untuk melanjutkan...")

        elif choice == '4':
            if 'cleaned' in locals() and cleaned:
                filename = input(Fore.CYAN + "\n[+] Masukkan nama file untuk menyimpan output (JSON): ")
                save_output(cleaned,filename)
            else:
                print(Fore.RED + "[!] Silakan lakukan WHOIS lookup terlebih dahulu.")
            input(Fore.YELLOW + "\nTekan Enter untuk melanjutkan...")

        elif choice == '5':
            clear_screen()

        elif choice == '6':
            break

        elif choice == '7':
            target = input(Fore.CYAN + "\n[+] Masukkan Domain/URL: ").strip()
            headers = get_http_headers(target)
            display_http_headers(headers)
            input(Fore.YELLOW + "\nTekan Enter untuk melanjutkan...")

        elif choice == '8':
            ip_address = input(Fore.CYAN + "\n[+] Masukkan Alamat IP: ").strip()
            geo_data = ip_geolocation(ip_address)
            display_geolocation_data(geo_data)
            input(Fore.YELLOW + "\nTekan Enter untuk melanjutkan...")

        elif choice == '9':
            target = input(Fore.CYAN + "\n[+] Masukkan Domain/IP untuk DNS Lookup: ").strip()
            dns_data = get_dns_info(target)
            display_dns_info(dns_data)
            input(Fore.YELLOW + "\nTekan Enter untuk melanjutkan...")


        else:
            print(Fore.RED + "[!] Pilihan tidak valid. Silakan pilih opsi yang valid.")
            input(Fore.YELLOW + "\nTekan Enter untuk melanjutkan...")

def display_whois_table_categorized(cleaned_data):
    """Displays categorized WHOIS data in a table."""
    table = PrettyTable()
    table.field_names = [f"{Fore.CYAN}Field", f"{Fore.GREEN}Nilai"]
    table.align = "l"

    categories = {
        "Informasi Domain": ["domain_name", "registrar", "whois_server", "referral_url",
                                   "updated_date", "creation_date", "expiration_date", "status"],
        "Kontak Registrant": ["registrant_name", "registrant_organization", "registrant_address",
                                   "registrant_city", "registrant_state", "registrant_postal_code",
                                   "registrant_country", "registrant_phone", "registrant_fax",
                                   "registrant_email"],
        "Kontak Admin": ["admin_name", "admin_organization", "admin_address", "admin_city",
                                   "admin_state", "admin_postal_code", "admin_country", "admin_phone",
                                   "admin_fax", "admin_email"],
        "Kontak Teknis": ["tech_name", "tech_organization", "tech_address", "tech_city",
                                   "tech_state", "tech_postal_code", "tech_country", "tech_phone",
                                   "tech_fax", "tech_email"],
        "Server Nama": ["name_servers"],
        "DNSSEC": ["dnssec"],
    }

    print(Fore.MAGENTA + "\n=== Hasil WHOIS (Berkategori) ===")
    for category, fields in categories.items():
        print(Fore.YELLOW + f"\n--- {category} ---")
        category_added = False
        for field in fields:
            if field in cleaned_data and cleaned_data[field]:
                value = cleaned_data[field]
                display_value = value[:100] + ('...' if len(value) > 100 else '')
                table.add_row([field.replace('_', ' ').title(), display_value])
                category_added = True
        if category_added:
            print(table)
            table.clear_rows()
        else:
            print(Fore.WHITE + "Tidak ada informasi yang tersedia dalam kategori ini.")


if __name__ == "__main__":
    run()
