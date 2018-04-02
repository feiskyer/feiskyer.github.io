---
title: bcc
date: 2016-12-14 17:27:47
type: page
---

# BPF Compiler Collection (BCC) - Tools for BPF-based Linux IO analysis, networking, monitoring

* Website: https://github.com/iovisor/bcc

![](https://github.com/iovisor/bcc/raw/master/images/bcc_tracing_tools_2016.png)

## Basic usage of bcc （[tutorial](https://github.com/iovisor/bcc/blob/master/docs/tutorial.md)）

Install bcc:

```
echo -e '[iovisor]\nbaseurl=https://repo.iovisor.org/yum/nightly/f23/$basearch\nenabled=1\ngpgcheck=0' | sudo tee /etc/yum.repos.d/iovisor.repo
yum install bcc-tools
```

Now bcc is installed at `/usr/share/bcc/tools`.

```
# ls /usr/share/bcc/tools
argdist       cachestat  ext4dist        hardirqs        offwaketime  softirqs    tcpconnect  vfscount
bashreadline  cachetop   ext4slower      killsnoop       old          solisten    tcpconnlat  vfsstat
biolatency    capable    filelife        llcstat         oomkill      sslsniff    tcplife     wakeuptime
biosnoop      cpudist    fileslower      mdflush         opensnoop    stackcount  tcpretrans  xfsdist
biotop        dcsnoop    filetop         memleak         pidpersec    stacksnoop  tcptop      xfsslower
bitesize      dcstat     funccount       mountsnoop      profile      statsnoop   tplist      zfsdist
btrfsdist     doc        funclatency     mysqld_qslower  runqlat      syncsnoop   trace       zfsslower
btrfsslower   execsnoop  gethostlatency  offcputime      slabratetop  tcpaccept   ttysnoop
```

**capable**

capable checks Linux security capabilities of processes:

```
# capable
TIME      UID    PID    COMM             CAP  NAME                 AUDIT
22:11:23  114    2676   snmpd            12   CAP_NET_ADMIN        1
22:11:23  0      6990   run              24   CAP_SYS_RESOURCE     1
22:11:23  0      7003   chmod            3    CAP_FOWNER           1
22:11:23  0      7003   chmod            4    CAP_FSETID           1
22:11:23  0      7005   chmod            4    CAP_FSETID           1
22:11:23  0      7005   chmod            4    CAP_FSETID           1
22:11:23  0      7006   chown            4    CAP_FSETID           1
22:11:23  0      7006   chown            4    CAP_FSETID           1
22:11:23  0      6990   setuidgid        6    CAP_SETGID           1
22:11:23  0      6990   setuidgid        6    CAP_SETGID           1
22:11:23  0      6990   setuidgid        7    CAP_SETUID           1
22:11:24  0      7013   run              24   CAP_SYS_RESOURCE     1
22:11:24  0      7026   chmod            3    CAP_FOWNER           1
[...]
```

**tcpconnect**

tcpconnect prints one line of output for every active TCP connection (eg, via connect()), with details including source and destination addresses.

```
 ./tcpconnect
 PID    COMM         IP SADDR            DADDR            DPORT
 2462   curl         4  192.168.1.99       74.125.23.138    80
```

**tcptop**

tcptop summarize TCP send/recv throughput by host.

```
# ./tcptop -C 1 3
Tracing... Output every 1 secs. Hit Ctrl-C to end

08:06:45 loadavg: 0.04 0.01 0.00 2/174 3099

PID    COMM         LADDR                 RADDR                  RX_KB  TX_KB
1740   sshd         192.168.1.99:22         192.168.0.29:60315         0      0

08:06:46 loadavg: 0.04 0.01 0.00 2/174 3099

PID    COMM         LADDR                 RADDR                  RX_KB  TX_KB
1740   sshd         192.168.1.99:22         192.168.0.29:60315         0      0

08:06:47 loadavg: 0.04 0.01 0.00 2/174 3099

PID    COMM         LADDR                 RADDR                  RX_KB  TX_KB
1740   sshd         192.168.1.99:22         192.168.0.29:60315         0      0
```

## Write your own

**helloworld**

```python
#!/usr/bin/env python
from __future__ import print_function
from bcc import BPF

text='int kprobe__sys_sync(void *ctx) { bpf_trace_printk("Hello, World!\\n"); return 0; }'
prog="""
int hello(void *ctx) {
        bpf_trace_printk("Hello, World!\\n");
        return 0;
}
"""

b = BPF(text=prog)
b.attach_kprobe(event="sys_clone", fn_name="hello")

print("%-18s %-16s %-6s %s" % ("TIME(s)", "COMM", "PID", "MESSAGE"))
while True:
        try:
                (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        except ValueError:
                continue
        print("%-18.9f %-16s %-6d %s" % (ts, task, pid, msg))
```

**using BPF_PERF_OUTPUT**

```python
from __future__ import print_function
from bcc import BPF
import ctypes as ct

# load BPF program
b = BPF(text="""
struct data_t {
    u64 ts;
};

BPF_PERF_OUTPUT(events);

void kprobe__sys_sync(void *ctx) {
    struct data_t data = {};
    data.ts = bpf_ktime_get_ns() / 1000;
    events.perf_submit(ctx, &data, sizeof(data));
};
""")

class Data(ct.Structure):
    _fields_ = [
        ("ts", ct.c_ulonglong)
    ]

# header
print("%-18s %s" % ("TIME(s)", "CALL"))

# process event
def print_event(cpu, data, size):
    event = ct.cast(data, ct.POINTER(Data)).contents
    print("%-18.9f sync()" % (float(event.ts) / 1000000))

# loop with callback to print_event
b["events"].open_perf_buffer(print_event)
while True:
    b.kprobe_poll()
```

More python turorials <https://github.com/iovisor/bcc/blob/master/docs/tutorial_bcc_python_developer.md>.

## bcc user-level probes

```python
from __future__ import print_function
from bcc import BPF
from time import strftime
import ctypes as ct

# load BPF program
bpf_text = """
#include <uapi/linux/ptrace.h>

struct str_t {
    u64 pid;
    char str[80];
};

BPF_PERF_OUTPUT(events);

int printret(struct pt_regs *ctx) {
    struct str_t data  = {};
    u32 pid;
    if (!PT_REGS_RC(ctx))
        return 0;
    pid = bpf_get_current_pid_tgid();
    data.pid = pid;
    bpf_probe_read(&data.str, sizeof(data.str), (void *)PT_REGS_RC(ctx));
    events.perf_submit(ctx,&data,sizeof(data));

    return 0;
};
"""
STR_DATA = 80

class Data(ct.Structure):
    _fields_ = [
        ("pid", ct.c_ulonglong),
        ("str", ct.c_char * STR_DATA)
    ]

b = BPF(text=bpf_text)
b.attach_uretprobe(name="/bin/bash", sym="readline", fn_name="printret")

# header
print("%-9s %-6s %s" % ("TIME", "PID", "COMMAND"))

def print_event(cpu, data, size):
    event = ct.cast(data, ct.POINTER(Data)).contents
    print("%-9s %-6d %s" % (strftime("%H:%M:%S"), event.pid, event.str))

b["events"].open_perf_buffer(print_event)
while 1:
    b.kprobe_poll()
```

```
# ./bashreadline
TIME      PID    COMMAND
08:22:44  2070   ls /
08:22:56  2070   ping -c3 google.com

# ./gethostlatency
TIME      PID    COMM                  LATms HOST
08:23:26  3370   ping                   2.00 google.com
08:23:37  3372   ping                  56.00 baidu.com
```

## Networking

* https://github.com/iovisor/bcc/tree/master/examples/networking
* [tc eBPF](http://borkmann.ch/talks/2016_fosdem.pdf)

## BPF

BPF, as in Berkeley Packet Filter, was initially conceived in 1992 so as to provide a way to filter packets and to avoid useless packet copies from kernel to userspace. It initially consisted in a simple bytecode that is injected from userspace into the kernel, where it is checked by a verifier—to prevent kernel crashes or security issues—and attached to a socket, then run on each received packet.The simplicity of the language as well as the existence of an in-kernel Just-In-Time (JIT) compiling machine for BPF were factors for the excellent performances of this tool.

Then in 2013, Alexei Starovoitov completely reshaped it, started to add new functionalities and to improve the performances of BPF. This new version is designated as eBPF (for “extended BPF”), while the former becomes cBPF (“classic” BPF). New features such as maps and tail calls appeared. The JIT machines were rewritten.

## IO Visor

The IO Visor Project is an open source project and a community of developers to accelerate the innovation, development, and sharing of virtualized in-kernel IO services for tracing, analytics, monitoring, security and networking functions.

XDP or eXpress Data Path provides a high performance, programmable network data path in the Linux kernel as part of the IO Visor Project. XDP provides bare metal packet processing at the lowest point in the software stack which makes it ideal for speed without compromising programmability. Furthermore, new functions can be implemented dynamically with the integrated fast path without kernel modification.

![](https://www.iovisor.org/wp-content/uploads/2016/09/xdp-packet-processing-1024x560.png)

**Links**

- https://www.iovisor.org/
- https://www.iovisor.org/technology/ebpf
- https://www.iovisor.org/technology/xdp
- https://github.com/iovisor/bpf-docs
- https://www.kernel.org/doc/Documentation/networking/filter.txt
- https://events.linuxfoundation.org/sites/events/files/slides/iovisor-lc-bof-2016.pdf
- https://suchakra.wordpress.com/2015/08/12/bpf-internals-ii/
- https://qmonnet.github.io/whirl-offload/2016/09/01/dive-into-bpf/
- https://github.com/cilium/cilium
