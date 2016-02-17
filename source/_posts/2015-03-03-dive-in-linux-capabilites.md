---
layout: post
title: "Dive in Linux capabilites"
description: ""
category:
tags: [Linux]
---

### Introduction

Capabilities in Linux are flags that tell the kernel what the application is allowed to do, If you have no additional security mechanism in place, the Linux root user has all capabilities assigned to it. As capabilities are a way for running processes with some privileges, without having the need to grant them root privileges, it is important to understand that they exist.

Consider the ping utility. It is marked setuid root on some distributions, because the utility requires the (cap)ability to send raw packets. This capability is known as CAP_NET_RAW. However, thanks to capabilities, you can now mark the ping application with this capability and drop the setuid from the file. As a result, the application does not run with full root privileges anymore, but with the restricted privileges of the user plus one capability, namely the CAP_NET_RAW.

```
➜  ~  cp /bin/ping .
➜  ~  ll ping
-rwxr-xr-x 1 fei fei 44K  3月  3 14:42 ping
➜  ~  ll /bin/ping
-rwsr-xr-x 1 root root 44K  5月  8  2014 /bin/ping
➜  ~  ./ping -c 1 www.baidu.com
ping: icmp open socket: Operation not permitted
➜  ~  sudo setcap cap_net_raw+p ping
➜  ~  getcap ping
ping = cap_net_raw+p
➜  ~  ./ping -c 1 www.baidu.com
PING www.a.shifen.com (115.239.211.112) 56(84) bytes of data.
64 bytes from 115.239.211.112: icmp_seq=1 ttl=51 time=6.83 ms

--- www.a.shifen.com ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 6.833/6.833/6.833/0.000 ms
```

### Useful Tools

Install capability tools by `sudo apt-get install libcap-ng-utils`.

* filecap - a program to see file capabilities
* pscap - a program to see process capabilities
* netcap - a program to see network capabilities

### Another exmaple

Use following program for test cap_setuid and cap_setgid.

```
/*
 * gcc cap_test.c -o test -lcap
**/
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <sys/capability.h>
#include <sys/prctl.h>
#include <sys/types.h>

int main(int argc, char **argv)
{
    printf("cap_setuid and cap_setgid: %d\n", prctl(PR_CAPBSET_READ, CAP_SETUID | CAP_SETGID, 0, 0, 0));
    printf("File cap: %s\n", cap_to_text(cap_get_file(argv[0]), NULL));
    printf("Process cap: %s\n", cap_to_text(cap_get_proc(), NULL));
    if (setresuid(0, 0, 0))
    {
        printf("setresuid(): %s\n", strerror(errno));
    }
    else
    {
        char *args[] = {NULL};
        char *env[] = {NULL};
        execve("/bin/sh", args, env);
    }
}
```

Since `test` has no capabilities of cap_setuid and cap_setgid, `test` program is not permitted to setresuid().

```
➜  gcc cap_test.c -o test -lcap
➜  ./test
cap_setuid and cap_setgid: 1
File cap: (null)
Process cap: =
setresuid(): Operation not permitted
```

Now, we add cap_setuid and cap_setgid to `test`:

```
➜  sudo setcap cap_setuid,cap_setgid+ep test
➜  ./test
cap_setuid and cap_setgid: 1
File cap: = cap_setgid,cap_setuid+ep
Process cap: = cap_setgid,cap_setuid+ep
# cat /etc/shadow   # We are in sh now and we have root priviledge
root:!:11111:0:99999:7:::
daemon:*:12232:0:99999:7:::
...
```

### Reference

See more at [man](http://man7.org/linux/man-pages/man7/capabilities.7.html) and [faq](https://www.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.2/capfaq-0.2.txt).
