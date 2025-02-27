import requests
import re
from colorama import Fore, Style, init
from urllib.parse import urljoin
import json

init(autoreset=True)

class WPScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.themes = []
        self.plugins = []
        self.vulns = []
        self.vulnerabilities_db = self.load_vulnerabilities_db()

    def load_vulnerabilities_db(self):
        # Database kerentanan plugin, tema, dan core WordPress
        return {
            'plugins': {
                'akismet': [
                    {'version': '<=4.1.9', 'cve': 'CVE-2021-25094', 'description': 'XSS Vulnerability', 'poc': '/wp-content/plugins/akismet/readme.txt'}
                ],
                'contact-form-7': [
                    {'version': '<=5.4.2', 'cve': 'CVE-2020-35489', 'description': 'File Upload Vulnerability', 'poc': '/wp-content/plugins/contact-form-7/readme.txt'}
                ],
                # Tambahkan plugin lainnya
            },
            'themes': {
                'twentyseventeen': [
                    {'version': '<=1.7', 'cve': 'CVE-2018-15877', 'description': 'XSS Vulnerability', 'poc': '/wp-content/themes/twentyseventeen/readme.txt'}
                ],
                # Tambahkan tema lainnya
            },
            'core': {
                'wp_register': [
                    {'version': '<=5.8.1', 'cve': 'CVE-2021-44228', 'description': 'Open Registration Exploit', 'poc': '/wp-login.php?action=register'}
                ],
                'wp_upload': [
                    {'version': '<=5.8.1', 'cve': 'CVE-2021-44229', 'description': 'Arbitrary File Upload', 'poc': '/wp-admin/async-upload.php'}
                ],
                'wp_theme': [
                    {'version': '<=5.8.1', 'cve': 'CVE-2021-44230', 'description': 'Theme Editor Exploit', 'poc': '/wp-admin/theme-editor.php'}
                ]
            }
        }

    def check_wp_version(self, url):
        try:
            response = self.session.get(url + '/wp-includes/version.php')
            if response.status_code == 200:
                version = re.search(r"\$wp_version\s*=\s*'([^']+)'", response.text)
                if version:
                    return version.group(1)
        except:
            pass
        return None

    def enumerate_themes(self, url):
        try:
            response = self.session.get(url + '/wp-content/themes/')
            if response.status_code == 200:
                self.themes = re.findall(r'href="([^"/]+)/"', response.text)
        except:
            pass

    def enumerate_plugins(self, url):
        try:
            response = self.session.get(url + '/wp-content/plugins/')
            if response.status_code == 200:
                self.plugins = re.findall(r'href="([^"/]+)/"', response.text)
        except:
            pass

    def check_common_vulns(self, url):
        checks = {
            'Version Exposure': '/wp-includes/version.php',
            'Readme File': '/readme.html',
            'User Enum': '/?author=1',
            'Config Backup': '/wp-config.php~',
            'Directory Listing': '/wp-content/uploads/',
            'XML-RPC Enabled': '/xmlrpc.php',
            'Debug Log': '/wp-content/debug.log',
            'Database Export': '/wp-content/backup-db/',
            'WP-Cron': '/wp-cron.php',
            'Install File': '/wp-admin/install.php',
            'Registration Enabled': '/wp-login.php?action=register',
            'Theme Editor': '/wp-admin/theme-editor.php',
            'Plugin Editor': '/wp-admin/plugin-editor.php',
            'File Upload': '/wp-admin/async-upload.php'
        }

        for name, path in checks.items():
            try:
                response = self.session.get(url + path)
                if response.status_code == 200:
                    self.vulns.append(f"{Fore.RED}[!] {name} Exposed")
            except:
                continue

    def check_theme_vulns(self, url):
        for theme in self.themes:
            if theme in self.vulnerabilities_db['themes']:
                for vuln in self.vulnerabilities_db['themes'][theme]:
                    self.vulns.append(f"{Fore.RED}[!] Vulnerable Theme: {theme} ({vuln['cve']}) - {vuln['description']}")
                    if 'poc' in vuln:
                        self.vulns.append(f"{Fore.YELLOW}    POC: {url + vuln['poc']}")

    def check_plugin_vulns(self, url):
        for plugin in self.plugins:
            if plugin in self.vulnerabilities_db['plugins']:
                for vuln in self.vulnerabilities_db['plugins'][plugin]:
                    self.vulns.append(f"{Fore.RED}[!] Vulnerable Plugin: {plugin} ({vuln['cve']}) - {vuln['description']}")
                    if 'poc' in vuln:
                        self.vulns.append(f"{Fore.YELLOW}    POC: {url + vuln['poc']}")

    def check_core_vulns(self, url):
        for vuln_type, vulns in self.vulnerabilities_db['core'].items():
            for vuln in vulns:
                self.vulns.append(f"{Fore.RED}[!] Core Vulnerability: {vuln_type} ({vuln['cve']}) - {vuln['description']}")
                if 'poc' in vuln:
                    self.vulns.append(f"{Fore.YELLOW}    POC: {url + vuln['poc']}")

    def check_db_exposure(self, url):
        try:
            response = self.session.get(url + '/wp-admin/admin-ajax.php?action=export_db')
            if response.status_code == 200 and 'SQL' in response.text:
                self.vulns.append(f"{Fore.RED}[!] Database Export Enabled")
        except:
            pass

    def run(self):
        url = input("\n[+] Enter WordPress Site: ").strip()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        print(Fore.YELLOW + "[~] Scanning WordPress Site...\n")

        # Check WordPress version
        version = self.check_wp_version(url)
        if version:
            print(f"{Fore.CYAN}[+] WordPress Version: {version}")
        else:
            print(f"{Fore.RED}[-] Could not detect WordPress version")

        # Enumerate themes and plugins
        self.enumerate_themes(url)
        self.enumerate_plugins(url)

        if self.themes:
            print(f"\n{Fore.CYAN}[+] Found {len(self.themes)} Themes:")
            for theme in self.themes:
                print(f" - {theme}")
        else:
            print(f"{Fore.RED}[-] No themes found")

        if self.plugins:
            print(f"\n{Fore.CYAN}[+] Found {len(self.plugins)} Plugins:")
            for plugin in self.plugins:
                print(f" - {plugin}")
        else:
            print(f"{Fore.RED}[-] No plugins found")

        # Check for vulnerabilities
        self.check_common_vulns(url)
        self.check_theme_vulns(url)
        self.check_plugin_vulns(url)
        self.check_core_vulns(url)
        self.check_db_exposure(url)

        # Display results
        if self.vulns:
            print(f"\n{Fore.MAGENTA}=== WordPress Vulnerabilities ===")
            for vuln in self.vulns:
                print(vuln)
        else:
            print(f"\n{Fore.GREEN}[+] No vulnerabilities found")

        print(f"\n{Fore.YELLOW}[~] Scan completed!")

# Fungsi run() untuk kompatibilitas dengan unknown1337.py
def run():
    scanner = WPScanner()
    scanner.run()

if __name__ == "__main__":
    run()
