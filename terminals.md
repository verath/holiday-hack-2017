
# Linux Command Hijacking (Winter Wonder Landing)

```
My name is Bushy Evergreen, and I have a problem for you.
I think a server got owned, and I can only offer a clue.
We use the system for chat, to keep toy production running.
Can you help us recover from the server connection shunning?


Find and run the elftalkd binary to complete this challenge.
```

Unfortunately, it seemed like the `find` command could not be used:
```sh
$ find
bash: /usr/local/bin/find: cannot execute binary file: Exec format error
```

Instead, we use ls to recursively list all files and grep for the wanted binary:
```sh 
$ ls -R / | grep -n3 elftalkd
ls: cannot open directory '/proc/tty/driver': Permission denied
ls: cannot open directory '/root': Permission denied
5087-bin
5088-
5089-/run/elftalk/bin:
5090:elftalkd
5091-
5092-/run/lock:
5093-
ls: cannot open directory '/var/cache/apt/archives/partial': Permission denied
ls: cannot open directory '/var/cache/ldconfig': Permission denied
ls: cannot open directory '/var/lib/apt/lists/partial': Permission denied
```

And then we run it solving the terminal:

```
$ /run/elftalk/bin/elftalkd 
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
owner (see: [Run a binary owned by root without sudo](https://unix.stackexchange.com/a/157999)):

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
