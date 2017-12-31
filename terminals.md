
# Linux Command Hijacking (Winter Wonder Landing)

With this terminal we are supposed to find the file elftalkd
and execute it, but locate and find don't seem to work

```
                                 |
                               \ ' /
                             -- (*) --
                                >*<
                               >0<@<
                              >>>@<<*
                             >@>*<0<<<
                            >*>>@<<<@<<
                           >@>>0<<<*<<@<
                          >*>>0<<@<<<@<<<
                         >@>>*<<@<>*<<0<*<
           \*/          >0>>*<<@<>0><<*<@<<
       ___\\U//___     >*>>@><0<<*>>@><*<0<<
       |\\ | | \\|    >@>>0<*<0>>@<<0<<<*<@<<  
       | \\| | _(UU)_ >((*))_>0><*<0><@<<<0<*<
       |\ \| || / //||.*.*.*.|>>@<<*<<@>><0<<<
       |\\_|_|&&_// ||*.*.*.*|_\\db//_               
       """"|'.'.'.|~~|.*.*.*|     ____|_
           |'.'.'.|   ^^^^^^|____|>>>>>>|
           ~~~~~~~~         '""""`------'
My name is Bushy Evergreen, and I have a problem for you.
I think a server got owned, and I can only offer a clue.
We use the system for chat, to keep toy production running.
Can you help us recover from the server connection shunning?

Find and run the elftalkd binary to complete this challenge.

elf@7e33d7981b0b:~$ ls -lhaR / |grep -B5 elftalkd
ls: cannot open directory '/proc/tty/driver': Permission denied
ls: cannot open directory '/root': Permission denied
/run/elftalk/bin:
total 7.1M
drwxr-xr-x 1 root root 4.0K Dec  4 14:32 .
drwxr-xr-x 1 root root 4.0K Dec  4 14:32 ..
-rwxr-xr-x 1 root root 7.1M Dec  4 14:29 elftalkd
ls: cannot open directory '/var/cache/apt/archives/partial': Permission denied
ls: cannot open directory '/var/cache/ldconfig': Permission denied
ls: cannot open directory '/var/lib/apt/lists/partial': Permission denied
elf@7e33d7981b0b:~$ /run/elftalk/bin/elftalkd
        Running in interactive mode
        --== Initializing elftalkd ==--
Initializing Messaging System!
Nice-O-Meter configured to 0.90 sensitivity.
Acquiring messages from local networks...
--== Initialization Complete ==--
      _  __ _        _ _       _ 
     | |/ _| |      | | |     | |
  ___| | |_| |_ __ _| | | ____| |
 / _ \ |  _| __/ _` | | |/ / _` |
|  __/ | | | || (_| | |   < (_| |
 \___|_|_|  \__\__,_|_|_|\_\__,_|
-*> elftalkd! <*-
Version 9000.1 (Build 31337) 
By Santa Claus & The Elf Team
Copyright (C) 2017 NotActuallyCopyrighted. No actual rights reserved.
Using libc6 version 2.23-0ubuntu9
LANG=en_US.UTF-8
Timezone=UTC
Commencing Elf Talk Daemon (pid=6021)... done!
Background daemon...
elf@7e33d7981b0b:~$ 

```

# Troublesome Process (Winconceivable: The Cliffs of Winsanity)

```
My name is Sparkle Redberry, and I need your help.
My server is atwist, and I fear I may yelp.
Help me kill the troublesome process gone awry.
I will return the favor with a gift before nigh.
Kill the "santaslittlehelperd" process to complete this challenge.
```

Looking at the running processes we see PID 8 is what we want to kill:
```sh
$ elf@55f83966318c:~$ ps -aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
elf          1  0.2  0.0  18028  2828 pts/0    Ss   19:39   0:00 /bin/bash /sbin/init
elf          8  0.0  0.0   4224   648 pts/0    S    19:39   0:00 /usr/bin/santaslittlehelperd
elf         11  0.3  0.0  13528  6404 pts/0    S    19:39   0:00 /sbin/kworker
elf         12  0.0  0.0  18248  3216 pts/0    S    19:39   0:00 /bin/bash
elf         18  1.2  0.0  71468 26520 pts/0    S    19:39   0:00 /sbin/kworker
elf         48  0.0  0.0  34424  2860 pts/0    R+   19:40   0:00 ps -aux
```

Simply running `kill 8` doesn't work though, and gives us no message back:

```sh
$ kill 8
```

Looking at the .bashrc file in our current (home) directory we find that `kill` has been aliased to `true`:

```sh
$ cat .bashrc
...
# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'
    alias kill='true'
    alias killall='true'
    alias pkill='true'
    alias skill='true'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi
...
```

Not a very helpful alias... Running the kill binary in /bin works and completes the challenge:

```sh
$ /bin/kill 8
$ ps -aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
elf          1  0.5  0.0  18028  2888 pts/0    Ss   19:44   0:00 /bin/bash /sbin/init
elf         12  0.0  0.0  18248  3220 pts/0    S    19:44   0:00 /bin/bash
elf         33  0.0  0.0  34424  2872 pts/0    R+   19:44   0:00 ps -aux
```


# Candy Cane Striper (Cryokinetic Magic)

For this terminal we are tasked with executing a binary file in our home
directory called `CandyCaneStriper`. The file is owned by root, and does
not have any execute permissions. We are allowed to read it though, 
meaning that we can copy the binary to a new file and thereby becoming the
owner (see: [Run a binary owned by root without sudo](https://unix.stackexchange.com/a/157999))

Alternative method would've been to execute:
/lib64/ld-linux-x86-64.so.2 ./CandyCaneStriper

```
My name is Holly Evergreen, and I have a conundrum.
I broke the candy cane striper, and I'm near throwing a tantrum.
Assembly lines have stopped since the elves can't get their candy cane fix.
We hope you can start the striper once again, with your vast bag of tricks.


Run the CandyCaneStriper executable to complete this challenge.

elf@f3da6d0fa193:~$ ls -la
total 68
drwxr-xr-x 1 elf  elf   4096 Dec 15 20:00 .
drwxr-xr-x 1 root root  4096 Dec  5 19:31 ..
-rw-r--r-- 1 elf  elf    220 Aug 31  2015 .bash_logout
-rw-r--r-- 1 root root  3143 Dec 15 19:59 .bashrc
-rw-r--r-- 1 elf  elf    655 May 16  2017 .profile
-rw-r--r-- 1 root root 45224 Dec 15 19:59 CandyCaneStriper

elf@f3da6d0fa193:~$ cp CandyCaneStriper CandyCaneStriper1
```

Having done that we still notice that we are unable to run `chmod`. We can
work around this by instead using perl to invoke the `chmod()` system call
(see: [How to chmod without /usr/bin/chmod?](https://unix.stackexchange.com/a/83864)):

```
elf@f3da6d0fa193:~$ chmod +x CandyCaneStriper1

elf@f3da6d0fa193:~$ ls -la
total 116
drwxr-xr-x 1 elf  elf   4096 Dec 16 14:16 .
drwxr-xr-x 1 root root  4096 Dec  5 19:31 ..
-rw-r--r-- 1 elf  elf    220 Aug 31  2015 .bash_logout
-rw-r--r-- 1 root root  3143 Dec 15 19:59 .bashrc
-rw-r--r-- 1 elf  elf    655 May 16  2017 .profile
-rw-r--r-- 1 root root 45224 Dec 15 19:59 CandyCaneStriper
-rw-r--r-- 1 elf  elf  45224 Dec 16 14:16 CandyCaneStriper1

elf@f3da6d0fa193:~$ perl -e 'chmod 0755, "CandyCaneStriper1"'

elf@f3da6d0fa193:~$ ls -la
total 116
drwxr-xr-x 1 elf  elf   4096 Dec 16 14:16 .
drwxr-xr-x 1 root root  4096 Dec  5 19:31 ..
-rw-r--r-- 1 elf  elf    220 Aug 31  2015 .bash_logout
-rw-r--r-- 1 root root  3143 Dec 15 19:59 .bashrc
-rw-r--r-- 1 elf  elf    655 May 16  2017 .profile
-rw-r--r-- 1 root root 45224 Dec 15 19:59 CandyCaneStriper
-rwxr-xr-x 1 elf  elf  45224 Dec 16 14:16 CandyCaneStriper1
```

We now have execute permissions to the binary, so we run it to complete
the terminal:
```
elf@f3da6d0fa193:~$ ./CandyCaneStriper1 
                   _..._
                 .'\\ //`,      
                /\\.'``'.=",
               / \/     ;==|
              /\\/    .'\`,`
             / \/     `""`
            /\\/
           /\\/
          /\ /
         /\\/
        /`\/
        \\/
         `
The candy cane striping machine is up and running!
```


# Shadow file restoration

In this challenge we are tasked with restoring the 
/etc/shadow file from the /etc/shadow.bak but we 
have limited sudo privileges on the server. 

```
              \ /
            -->*<--
              /o\
             /_\_\
            /_/_0_\
           /_o_\_\_\
          /_/_/_/_/o\
         /@\_\_\@\_\_\
        /_/_/O/_/_/_/_\
       /_\_\_\_\_\o\_\_\
      /_/0/_/_/_0_/_/@/_\
     /_\_\_\_\_\_\_\_\_\_\
    /_/o/_/_/@/_/_/o/_/0/_\
   jgs       [___]  
My name is Shinny Upatree, and I've made a big mistake.
I fear it's worse than the time I served everyone bad hake.
I've deleted an important file, which suppressed my server access.
I can offer you a gift, if you can fix my ill-fated redress.
Restore /etc/shadow with the contents of /etc/shadow.bak, then run "inspect_da_box" to complete this challenge.
Hint: What commands can you run with sudo?
elf@812104749e7e:~$ sudo -l -l
Matching Defaults entries for elf on 812104749e7e:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin
User elf may run the following commands on 812104749e7e:
Sudoers entry:
    RunAsUsers: elf
    RunAsGroups: shadow
    Options: !authenticate
    Commands:
        /usr/bin/find
```
So, we can run find as the group shadow. Luckily 
/etc/shadow is writable for the group.
Simple -exec parameter for find should do the trick!
```
elf@812104749e7e:~$ ls -lh /etc/shadow*            
-rw-rw---- 1 root shadow   0 Dec 15 20:00 /etc/shadow
-rw------- 1 root root   652 Nov 14 13:48 /etc/shadow-
-rw-r--r-- 1 root root   677 Dec 15 19:59 /etc/shadow.bak
elf@812104749e7e:~$ sudo -g shadow find /etc -name shadow.bak -exec cp {} /etc/shadow \;
find: '/etc/ssl/private': Permission denied
elf@812104749e7e:~$ inspect_da_box 
                     ___
                    / __'.     .-"""-.
              .-""-| |  '.'.  / .---. \
             / .--. \ \___\ \/ /____| |
            / /    \ `-.-;-(`_)_____.-'._
           ; ;      `.-" "-:_,(o:==..`-. '.         .-"-,
           | |      /       \ /      `\ `. \       / .-. \
           \ \     |         Y    __...\  \ \     / /   \/
     /\     | |    | .--""--.| .-'      \  '.`---' /
     \ \   / /     |`        \'   _...--.;   '---'`
      \ '-' / jgs  /_..---.._ \ .'\\_     `.
       `--'`      .'    (_)  `'/   (_)     /
                  `._       _.'|         .'
                     ```````    '-...--'`
/etc/shadow has been successfully restored!
elf@812104749e7e:~$ 
```

# Troublesome process 

In this challenge we are tasked to kill a process
but someone has created an alias kill='true'
Removing the alias seems to work!

```
                ___,@
               /  <
          ,_  /    \  _,
      ?    \`/______\`/
   ,_(_).  |; (e  e) ;|
    \___ \ \/\   7  /\/    _\8/_
        \/\   \'=='/      | /| /|
         \ \___)--(_______|//|//|
          \___  ()  _____/|/_|/_|
             /  ()  \    `----'
            /   ()   \
           '-.______.-'
   jgs   _    |_||_|    _
        (@____) || (____@)
         \______||______/
My name is Sparkle Redberry, and I need your help.
My server is atwist, and I fear I may yelp.
Help me kill the troublesome process gone awry.
I will return the favor with a gift before nigh.
Kill the "santaslittlehelperd" process to complete this challenge.
elf@ea96bcf6ac17:~$ alias
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s
*alert$//'\'')"'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias grep='grep --color=auto'
alias kill='true'
alias killall='true'
alias l='ls -CF'
alias la='ls -A'
alias ll='ls -alF'
alias ls='ls --color=auto'
alias pkill='true'
alias skill='true'
elf@ea96bcf6ac17:~$ unalias kill
elf@ea96bcf6ac17:~$ ps aux |grep santaslittle 
elf          8  0.0  0.0   4224   636 pts/0    S    13:23   0:00 /usr/bin/santaslittlehelperd
elf        128  0.0  0.0  11284   972 pts/0    S+   13:25   0:00 grep --color=auto santaslittle
elf@ea96bcf6ac17:~$ kill 8
elf@ea96bcf6ac17:~$ 
elf@ea96bcf6ac17:~$ ps aux |grep santaslittle
elf        175  0.0  0.0  11284   948 pts/0    S+   13:26   0:00 grep --color=auto santaslittle
elf@ea96bcf6ac17:~$ 
```

# Web Log Terminal

In this terminal we are tasked with parsing an
nginx access log file and finding out the least
popular browser. Some awk, sort and cut magic
coming up (stolen from https://serverfault.com/questions/89773/get-list-of-user-agents-from-nginx-log)

ps. a tail would've been a good idea!

```
                           ._    _.
                           (_)  (_)                  <> \  / <>
                            .\::/.                   \_\/  \/_/ 
           .:.          _.=._\\//_.=._                  \\//
      ..   \o/   ..      '=' //\\ '='             _<>_\_\<>/_/_<>_
      :o|   |   |o:         '/::\'                 <> / /<>\ \ <>
       ~ '. ' .' ~         (_)  (_)      _    _       _ //\\ _
           >O<             '      '     /_/  \_\     / /\  /\ \
       _ .' . '. _                        \\//       <> /  \ <>
      :o|   |   |o:                   /\_\\><//_/\
      ''   /o\   ''     '.|  |.'      \/ //><\\ \/
           ':'        . ~~\  /~~ .       _//\\_
jgs                   _\_._\/_._/_      \_\  /_/ 
                       / ' /\ ' \                   \o/
       o              ' __/  \__ '              _o/.:|:.\o_
  o    :    o         ' .'|  |'.                  .\:|:/.
    '.\'/.'                 .                 -=>>::>o<::<<=-
    :->@<-:                 :                   _ '/:|:\' _
    .'/.\'.           '.___/*\___.'              o\':|:'/o 
  o    :    o           \* \ / */                   /o\
       o                 >--X--<
                        /*_/ \_*\
                      .'   \*/   '.
                            :
                            '
Minty Candycane here, I need your help straight away.
We're having an argument about browser popularity stray.
Use the supplied log file from our server in the North Pole.
Identifying the least-popular browser is your noteworthy goal.
total 28704
-rw-r--r-- 1 root root 24191488 Dec  4 17:11 access.log
-rwxr-xr-x 1 root root  5197336 Dec 11 17:31 runtoanswer
elf@5e61884a1077:~$ 
elf@5e61884a1077:~$ awk -F'"' '/GET/ {print $6}' access.log | cut -d' ' -f1 | sort | uniq -c | sort -rn
  96551 Mozilla/5.0
    422 Slack-ImgProxy
    353 Mozilla/4.0
     76 -
     34 Googlebot-Image/1.0
     25 ZmEu
     16 slack/2.47.1.7358
     13 slack/2.47.0.7352
     12 sysscan/1.0
     11 facebookexternalhit/1.1
     11 Wget(linux)
      8 ltx71
      8 Slack/370354
      7 Slack/370342
      4 slack/2.46.0.7100
      4 Python-urllib/2.7
      3 null
      3 Slack/370136
      3 Mozilla/5.0(WindowsNT6.1;rv:31.0)Gecko/20100101Firefox/31.0
      3 MobileSafari/604.1
      3 GarlikCrawler/1.2
      2 masscan/1.0
      2 WhatWeb/0.4.9
      2 WhatWeb/0.4.8-dev
      2 Twitterbot/1.0
      2 Twitter/7.11.1
      2 Telesphoreo
      2 Slackbot-LinkExpanding
      2 Slack/370007
      2 (KHTML,
      1 www.probethenet.com
      1 curl/7.35.0
      1 curl/7.19.7
      1 Dillo/3.0.5
elf@5e61884a1077:~$ ./runtoanswer 
Starting up, please wait......
Enter the name of the least popular browser in the web log: Dillo
That is the least common browser in the web log! Congratulations!
elf@5e61884a1077:~$ 

```

# Christmas Songs Data Analysis Terminal

This time we are given access to a sqlite3 database file and
we need to determine the most popular song in the database.
We need to count all the likes and check which song matches
the songid.

```
                       *
                      .~'
                     O'~..
                    ~'O'~..
                   ~'O'~..~'
                  O'~..~'O'~.
                 .~'O'~..~'O'~
                ..~'O'~..~'O'~.
               .~'O'~..~'O'~..~'
              O'~..~'O'~..~'O'~..
             ~'O'~..~'O'~..~'O'~..
            ~'O'~..~'O'~..~'O'~..~'
           O'~..~'O'~..~'O'~..~'O'~.
          .~'O'~..~'O'~..~'O'~..~'O'~
         ..~'O'~..~'O'~..~'O'~..~'O'~.
        .~'O'~..~'O'~..~'O'~..~'O'~..~'
       O'~..~'O'~..~'O'~..~'O'~..~'O'~..
      ~'O'~..~'O'~..~'O'~..~'O'~..~'O'~..
     ~'O'~..~'O'~..~'O'~..~'O'~..~'O'~..~'
    O'~..~'O'~..~'O'~..~'O'~..~'O'~..~'O'~.
   .~'O'~..~'O'~..~'O'~..~'O'~..~'O'~..~'O'~
  ..~'O'~..~'O'~..~'O'~..~'O'~..~'O'~..~'O'~.
 .~'O'~..~'O'~..~'O'~..~'O'~..~'O'~..~'O'~..~'
O'~..~'O'~..~'O'~..~'O'~..~'O'~..~'O'~..~'O'~..
Sugarplum Mary is in a tizzy, we hope you can assist.
Christmas songs abound, with many likes in our midst.
The database is populated, ready for you to address.
Identify the song whose popularity is the best.
total 20684
-rw-r--r-- 1 root root 15982592 Nov 29 19:28 christmassongs.db
-rwxr-xr-x 1 root root  5197352 Dec  7 15:10 runtoanswer
elf@e15e256f745b:~$ sqlite3 christmassongs.db 
SQLite version 3.11.0 2016-02-15 17:29:24
Enter ".help" for usage hints.
sqlite> .schema
CREATE TABLE songs(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  artist TEXT,
  year TEXT,
  notes TEXT
);
CREATE TABLE likes(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  like INTEGER,
  datetime INTEGER,
  songid INTEGER,
  FOREIGN KEY(songid) REFERENCES songs(id)
);
sqlite> select count(like) likes ,title from likes join songs on songs.id = songid group by songid order by likes desc limit 1;
11325|Stairway to Heaven
sqlite> 
elf@e15e256f745b:~$ ./runtoanswer 
Starting up, please wait......
Enter the name of the song with the most likes: Stairway to Heaven
That is the #1 Christmas song, congratulations!
elf@e15e256f745b:~$ 
```

# Train startup terminal

Now we need to start a program, which isn't compatible with
our linux architecture (x86_64). Qemu FTW!

```
                             ______
                          .-"""".._'.       _,##
                   _..__ |.-"""-.|  |   _,##'`-._
                  (_____)||_____||  |_,##'`-._,##'`
                  _|   |.;-""-.  |  |#'`-._,##'`
               _.;_ `--' `\    \ |.'`\._,##'`
              /.-.\ `\     |.-";.`_, |##'`
              |\__/   | _..;__  |'-' /
              '.____.'_.-`)\--' /'-'`
               //||\\(_.-'_,'-'`
             (`-...-')_,##'`
      jgs _,##`-..,-;##`
       _,##'`-._,##'`
    _,##'`-._,##'`
      `-._,##'`
My name is Pepper Minstix, and I need your help with my plight.
I've crashed the Christmas toy train, for which I am quite contrite.
I should not have interfered, hacking it was foolish in hindsight.
If you can get it running again, I will reward you with a gift of delight.
total 444
-rwxr-xr-x 1 root root 454636 Dec  7 18:43 trainstartup
elf@bf702257c7b6:~$ ./trainstartup 
bash: ./trainstartup: cannot execute binary file: Exec format error
elf@bf702257c7b6:~$ file trainstartup 
trainstartup: ELF 32-bit LSB  executable, ARM, EABI5 version 1 (GNU/Linux), statically linked, for GNU/Linux 3.2.0, BuildID[sha1]=005de4685e8563d10b
3de3e0be7d6fdd7ed732eb, not stripped
elf@bf702257c7b6:~$ qemu-arm ./trainstartup 

    Merry Christmas
    Merry Christmas
v
>*<
^
/o\
/   \               @.·
/~~   \                .
/ ° ~~  \         · .    
/      ~~ \       ◆  ·    
/     °   ~~\    ·     0
/~~           \   .─··─ · o
             /°  ~~  .*· · . \  ├──┼──┤                                        
              │  ──┬─°─┬─°─°─°─ └──┴──┘                                        
≠==≠==≠==≠==──┼──=≠     ≠=≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠===≠
              │   /└───┘\┌───┐       ┌┐                                        
                         └───┘    /▒▒▒▒                                        
≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠=°≠=°≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠==≠
You did it! Thank you!
elf@bf702257c7b6:~$ 

```

# isit42 challenge Terminal

This time we are faced with a different task: We have a binary
file, which calls the rand-function and we have to make it
return 42. We could try to simply run the binary over and over
again, but luckily we don't have to, since we can create our
own shared object (so) file:

```
                 .--._.--.--.__.--.--.__.--.--.__.--.--._.--.
               _(_      _Y_      _Y_      _Y_      _Y_      _)_
              [___]    [___]    [___]    [___]    [___]    [___]
              /:' \    /:' \    /:' \    /:' \    /:' \    /:' \
             |::   |  |::   |  |::   |  |::   |  |::   |  |::   |
             \::.  /  \::.  /  \::.  /  \::.  /  \::.  /  \::.  /
         jgs  \::./    \::./    \::./    \::./    \::./    \::./
               '='      '='      '='      '='      '='      '='
Wunorse Openslae has a special challenge for you.
Run the given binary, make it return 42.
Use the partial source for hints, it is just a clue.
You will need to write your own code, but only a line or two.
total 88
-rwxr-xr-x 1 root root 84824 Dec 16 16:59 isit42
-rw-r--r-- 1 root root   654 Dec 16 16:57 isit42.c.un
elf@a24f62092afe:~$ cat isit42.c.un 
#include <stdio.h>
// DATA CORRUPTION ERROR
// MUCH OF THIS CODE HAS BEEN LOST
// FORTUNATELY, YOU DON'T NEED IT FOR THIS CHALLENGE
// MAKE THE isit42 BINARY RETURN 42
// YOU'LL NEED TO WRITE A SEPERATE C SOURCE TO WIN EVERY TIME
int getrand() {
    srand((unsigned int)time(NULL)); 
    printf("Calling rand() to select a random number.\n");
    // The prototype for rand is: int rand(void);
    return rand() % 4096; // returns a pseudo-random integer between 0 and 4096
}
int main() {
    sleep(3);
    int randnum = getrand();
    if (randnum == 42) {
        printf("Yay!\n");
    } else {
            printf("Boo!\n");
    }
    return randnum;
}
elf@a24f62092afe:~$ cat <<EOF |tee unrandom.c
> int rand() {
> return 42;
> }
> EOF
int rand() {
return 42;
}
elf@a24f62092afe:~$ gcc -fPIC unrandom.c -shared -o unrandom.so
elf@a24f62092afe:~$ LD_PRELOAD=./unrandom.so ./isit42
Starting up ... done.
Calling rand() to select a random number.
                 .-. 
                .;;\ ||           _______  __   __  _______    _______  __    _  _______  _     _  _______  ______ 
               /::::\|/          |       ||  | |  ||       |  |   _   ||  |  | ||       || | _ | ||       ||    _ |
              /::::'();          |_     _||  |_|  ||    ___|  |  |_|  ||   |_| ||  _____|| || || ||    ___||   | ||
            |\/`\:_/`\/|           |   |  |       ||   |___   |       ||       || |_____ |       ||   |___ |   |_||_ 
        ,__ |0_..().._0| __,       |   |  |       ||    ___|  |       ||  _    ||_____  ||       ||    ___||    __  |
         \,`////""""\\\\`,/        |   |  |   _   ||   |___   |   _   || | |   | _____| ||   _   ||   |___ |   |  | |
         | )//_ o  o _\\( |        |___|  |__| |__||_______|  |__| |__||_|  |__||_______||__| |__||_______||___|  |_|
          \/|(_) () (_)|\/ 
            \   '()'   /            ______    _______  _______  ___      ___      __   __    ___   _______ 
            _:.______.;_           |    _ |  |       ||   _   ||   |    |   |    |  | |  |  |   | |       |
          /| | /`\/`\ | |\         |   | ||  |    ___||  |_|  ||   |    |   |    |  |_|  |  |   | |  _____|
         / | | \_/\_/ | | \        |   |_||_ |   |___ |       ||   |    |   |    |       |  |   | | |_____ 
        /  |o`""""""""`o|  \       |    __  ||    ___||       ||   |___ |   |___ |_     _|  |   | |_____  |
       `.__/     ()     \__.'      |   |  | ||   |___ |   _   ||       ||       |  |   |    |   |  _____| |
       |  | ___      ___ |  |      |___|  |_||_______||__| |__||_______||_______|  |___|    |___| |_______|
       /  \|---|    |---|/  \ 
       |  (|42 | () | DA|)  |       _   ___  _______ 
       \  /;---'    '---;\  /      | | |   ||       |
        `` \ ___ /\ ___ / ``       | |_|   ||____   |
            `|  |  |  |`           |       | ____|  |
      jgs    |  |  |  |            |___    || ______| ___ 
       _._  |\|\/||\/|/|  _._          |   || |_____ |   |
      / .-\ |~~~~||~~~~| /-. \         |___||_______||___|
      | \__.'    ||    '.__/ |
       `---------''---------` 
Congratulations! You've won, and have successfully completed this challenge.
elf@a24f62092afe:~$ 
```
