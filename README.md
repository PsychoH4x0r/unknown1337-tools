git clone https://github.com/PsychoH4x0r/unknown1337-tools
cd unknown1337-tools
pip install -r requirements.txt
python3 unknown1337.py


>[35 TOOLS]=====>

=== SSL Certificate Analysis ===
+---------------------+-----------------------------------+
| Attribute           | Value                             |
+---------------------+-----------------------------------+
| Issuer              | CN=R3, O=Let's Encrypt            |
| Subject             | CN=example.com                    |
| Expiration          | 2024-12-31 23:59:59               |
| Signature Algorithm | sha256WithRSAEncryption           |
+---------------------+-----------------------------------+



Copy
=== Scan Results ===
Total URLs Found: 1245
Sensitive Files Found: 23

=== Sample Results ===
+------------------------------------------+
| All URLs                                 |
+------------------------------------------+
| http://example.com/old_config.zip        |
| http://example.com/archive.tar.gz        |
| http://example.com/2021_backup.sql       |
+------------------------------------------+

+------------------------------------------+
| Sensitive Files                          |
+------------------------------------------+
| http://example.com/secret_keys.pem       |
| http://example.com/database_backup.sql   |
| http://example.com/config.yml            |
+------------------------------------------+



=== Port Scan Results ===
+------+--------+----------+
| Port | Status | Service  |
+------+--------+----------+
| 21   | OPEN   | ftp      |
| 80   | OPEN   | http     |
| 443  | OPEN   | https    |
+------+--------+----------+

=== VS-FTPD Exploit Results ===
+-------------+-----------------+----------+---------------------------+
| IP          | Domains         | Vuln     | Shell Output              |
+-------------+-----------------+----------+---------------------------+
| 192.168.1.5 | example.com     | YES!     | uid=0(root) gid=0(root)...|
+-------------+-----------------+----------+---------------------------+





