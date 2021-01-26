---
title: "eBPF 入门之初体验"
date: 2021-01-27
tags: [eBPF]
draft: true
---

eBPF 提供了强大的跟踪、探测以及高效内核网络等功能，但由于其接口处于操作系统底层，新手入门起来还是有很大难度。幸好，eBPF 的维护者也看到了这个问题，并开发了一系列的工具来简化 eBPF 程序的开发和使用。这其中，最常用的两个工具是 BCC 和 bpftrace。

## BCC

[BCC](https://github.com/iovisor/bcc)(BPF Compiler Collection) 在 eBPF 编程接口之上封装了 eBPF 程序的构建过程，提供了 Python、C++ 和 Lua 等高级语言接口，并基于 Python 接口实现了大量的工具，是新手入门体验 eBPF 的最好项目。

BCC 的安装比较简单，比如 Ubuntu 和 RHEL 直接运行下面的命令就可以（其他发行版可以参考 [INSTALL](https://github.com/iovisor/bcc/blob/master/INSTALL.md) 安装）：

```sh
# Ubuntu
sudo apt-get install bpfcc-tools linux-headers-$(uname -r) linux-tools-common

# RHEL
sudo yum install bcc-tools
```

安装后，BCC 会把所有示例（包括 Python 和 lua），放到 /usr/share/bcc/examples 目录中。

不过发行版自带的 BCC 版本通常比较旧，并不包含很多已经修复的问题或者新的特性，在运行时可能会碰到意想不到的错误。比如，在 Ubuntu 18.04 中，执行 /usr/sbin/tcpconnect-bpfcc 你会碰到下面的'asm goto' 问题：

```sh
error: 'asm goto' constructs are not supported yet
```

这是一个已知的问题，BCC Github 上面对应的 issue 是 [#2119](https://github.com/iovisor/bcc/issues/2119)。

所以，在学习的时候，更推荐从源码安装最新版本：

```sh
apt-get install -y build-essential git bison cmake flex  libedit-dev libllvm6.0 llvm-6.0-dev libclang-6.0-dev python zlib1g-dev libelf-dev python3-distutils libfl-dev
git clone https://github.com/iovisor/bcc.git
mkdir bcc/build && cd bcc/build
cmake ..
make && make install
cmake -DPYTHON_CMD=python3 .. # build python3 binding
pushd src/python/
make && make install
```

这样，所有的 BCC 工具会安装到 `/usr/share/bcc` 目录中。比如，你可以通过 `/usr/share/bcc/tools/tcpconnect` 命令来执行 tcpconnect 工具。

```sh
$ /usr/share/bcc/tools/tcpconnect
Tracing connect ... Hit Ctrl-C to end
PID    COMM         IP SADDR            DADDR            DPORT
192664 curl         4  10.240.1.2       39.156.69.79     80
```

## bpftrace

[bpftrace](https://github.com/iovisor/bpftrace) 类似于 DTrace 或 SystemTap，它在 eBPF 之上构建了一个简化的跟踪语言，通过简单的几行脚本，就可以达到复杂的跟踪功能。多行的跟踪指令也可以放到脚本文件中执行，脚本后缀通常为 `.bt`。

![](2021-01-25-14-44-55.png)

Ubuntu 19.04 或者更新的系统可以直接通过 apt-get 命令安装 bpftrace：

```sh
# Ubuntu
sudo apt-get install -y bpftrace
```

而在其他系统或者生产环境中，推荐使用 docker 来运行 bpftrace。比如：

```sh
$ docker run -ti --rm -v /usr/src:/usr/src:ro \
       -v /lib/modules/:/lib/modules:ro \
       -v /sys/kernel/debug/:/sys/kernel/debug:rw \
       --net=host --pid=host --privileged \
       quay.io/iovisor/bpftrace:latest \
       tcplife.bt
Attaching 3 probes...
PID    COMM       LADDR           LPORT RADDR           RPORT TX_KB RX_KB MS
192855 curl       10.240.1.2      44790 220.181.38.148  80        0     0 233
```

[bpftrace 文档](https://github.com/iovisor/bpftrace/blob/master/docs/tutorial_one_liners.md) 提供了很多的单行示例，可以作为学习 bpftrace 的入门教程：

```sh
# Files opened by process
bpftrace -e 'tracepoint:syscalls:sys_enter_open {printf("%s %s\n", comm, str(args->filename)); }'

# Syscall count by program
bpftrace -e 'tracepoint:raw_syscalls:sys_enter {@[comm] = count(); }'

# Read bytes by process:
bpftrace -e 'tracepoint:syscalls:sys_exit_read /args->ret/ {@[comm] = sum(args->ret); }'

# Read size distribution by process:
bpftrace -e 'tracepoint:syscalls:sys_exit_read {@[comm] = hist(args->ret); }'

# Show per-second syscall rates:
bpftrace -e 'tracepoint:raw_syscalls:sys_enter {@ = count(); } interval:s:1 { print(@); clear(@); }'

# Trace disk size by process
bpftrace -e 'tracepoint:block:block_rq_issue {printf("%d %s %d\n", pid, comm, args->bytes); }'

# Count page faults by process
bpftrace -e 'software:faults:1 {@[comm] = count(); }'
```

在 Kubernetes 集群中，你可以通过 [kubectl trace](https://github.com/iovisor/kubectl-trace) 简化 bpftrace 的调度和运行。其运行原理如下图所示：

![](2021-01-25-14-49-01.png)

kubectl trace 支持单行方式或者脚本文件方式，比如

```sh
# Run a program from string literal
kubectl trace run node-1 -e "tracepoint:syscalls:sys_enter_* {@[probe] = count(); }"
# Run a program from file
kubectl trace run node-1 -f read.bt
```

![](2021-01-25-14-45-25.png)

kubectl trace 也可以通过 uprobe 直接跟踪一个 Pod：

![](2021-01-25-14-54-41.png)

## 小结

BCC 和 bpftrace 是两个最简单易用的 eBPF 跟踪工具，推荐初学者先学会它们的使用方法，并作为排错和性能调优的工具应用到实际系统中。

---

欢迎扫描下面的二维码关注**漫谈云原生**公众号，回复**任意关键字**查询更多云原生知识库，或回复**联系**加我微信。

![](/assets/mp.png)
