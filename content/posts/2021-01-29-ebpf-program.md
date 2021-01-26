---
title: "eBPF 入门之编程"
date: 2021-01-29
tags: []
draft: true
---

eBPF 提供了强大的跟踪、探测以及高效内核网络等功能，但由于其接口处于操作系统底层，新手入门起来还是有很大难度，特别是如何编写 eBPF 程序是入门的一大难点。本文将介绍一些常用的 eBPF 编程框架。

## BCC

上篇文章介绍的 BCC 其实就提供了对 eBPF 的封装，前端提供 Python API，而后端的 eBPF 程序还是通过 C 来实现。在运行的时候，BCC 会把 eBPF 程序编译成字节码、加载到内核执行，最后再通过用户空间的前端获取执行状态。

BCC 的优点就是简单易用，但也有很多缺点：

* 启动时编译，导致启动缓慢，且编译也需要耗费较高的 CPU 和内存资源。
* 编译 eBPF 要求所有主机上都安装内核头文件。
* 编译错误只有在运行的时候才能检测到，排错困难。

由于这些问题存在，BCC 正在基于 [libbpf](https://github.com/libbpf/libbpf) 将所有工具 [转换](http://www.brendangregg.com/blog/2020-11-04/bpf-co-re-btf-libbpf.html) 为可直接执行的二进制文件，无需外部依赖，从而更易分发到实际生产环境中。转换后的工具，因无需动态编译和接口转换，可以获得更高的性能和更少的资源占用。

除此之外，libbpf 还基于 BTF 和 CO-RE (Compile-Once Run-Everywhere) 提供了更好的便携性（兼容新旧内核版本）：

* BTF 是 BPF 类型格式，用于避免依赖 Clang 和内核头文件。
* CO-RE 则使得 BTF 字节码支持重定位，避免 LLVM 重新编译的需要。

借助于 BTF 和 CO-RE 的优势，你也可以在 `/sys/kernel/btf/vmlinux` 找到内核的 BTF 信息，甚至可以通过 bpftool 将其导出（一般放到文件 `vmlinux.h` 中）：

```sh
bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h
```

你可以在 [libbpf-tools](https://github.com/iovisor/bcc/tree/master/libbpf-tools) 找到 BCC 目前已迁移完成的工具。

## libbpf-bootstrap

[libbpf](https://github.com/libbpf/libbpf) 在使用上并不是很直观，所以 eBPF 维护者开发了一个脚手架项目 [libbpf-bootstrap](https://github.com/libbpf/libbpf-bootstrap)。它结合了 BPF 社区的最佳开发实践，为初学者提供了一个简单易用的上手框架。

在使用 libbpf-bootstrap 时，需要首先安装 LLVM 和依赖库文件：

```sh
sudo apt install -y bison build-essential cmake flex git libedit-dev pkg-config libmnl-dev \
   python zlib1g-dev libssl-dev libelf-dev libcap-dev libfl-dev llvm clang pkg-config \
   gcc-multilib luajit libluajit-5.1-dev libncurses5-dev libclang-dev clang-tools
```

然后检出其脚手架代码，检查示例代码是否可以编译通过：

```sh
# checkout libbpf-bootstrap
git clone https://github.com/libbpf/libbpf-bootstrap
# update submodules
git submodule update --init --recursive
# build existing samples
cd src && make
```

接下来，创建两个文件，分别是用户空间的 hello.c 以及 BPF 程序 hello.bpf.c（libbpf-bootstrap 要求 BPF 文件的格式总是 `<APP-NAME>.bpf.c`）。

```c
/* cat hello.bpf.c */
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

SEC("tracepoint/syscalls/sys_enter_execve")
int handle_tp(void *ctx)
{
    int pid = bpf_get_current_pid_tgid()>> 32;
    char fmt[] = "BPF triggered from PID %d.\n";
    bpf_trace_printk(fmt, sizeof(fmt), pid);
    return 0;
}

char LICENSE[] SEC("license") = "Dual BSD/GPL";
```

```c
/* cat hello.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/resource.h>
#include <bpf/libbpf.h>
#include "hello.skel.h"

#define DEBUGFS "/sys/kernel/debug/tracing/"

/* logging function used for debugging */
static int libbpf_print_fn(enum libbpf_print_level level, const char *format, va_list args)
{
#ifdef DEBUGBPF
    return vfprintf(stderr, format, args);
#else
    return 0;
#endif
}

/* read trace logs from debug fs */
void read_trace_pipe(void)
{
    int trace_fd;

    trace_fd = open(DEBUGFS "trace_pipe", O_RDONLY, 0);
    if (trace_fd < 0)
        return;

    while (1) {
        static char buf[4096];
        ssize_t sz;

        sz = read(trace_fd, buf, sizeof(buf) - 1);
        if (sz> 0) {
            buf[sz] = 0;
            puts(buf);
        }
    }
}

/* set rlimit (required for every app) */
static void bump_memlock_rlimit(void)
{
    struct rlimit rlim_new = {
        .rlim_cur	= RLIM_INFINITY,
        .rlim_max	= RLIM_INFINITY,
    };

    if (setrlimit(RLIMIT_MEMLOCK, &rlim_new)) {
        fprintf(stderr, "Failed to increase RLIMIT_MEMLOCK limit!\n");
        exit(1);
    }
}

int main(int argc, char **argv)
{
    struct hello_bpf *skel;
    int err;

    /* Set up libbpf errors and debug info callback */
    libbpf_set_print(libbpf_print_fn);

    /* Bump RLIMIT_MEMLOCK to allow BPF sub-system to do anything */
    bump_memlock_rlimit();

    /* Open BPF application */
    skel = hello_bpf__open();
    if (!skel) {
        fprintf(stderr, "Failed to open BPF skeleton\n");
        return 1;
    }

    /* Load & verify BPF programs */
    err = hello_bpf__load(skel);
    if (err) {
        fprintf(stderr, "Failed to load and verify BPF skeleton\n");
        goto cleanup;
    }

    /* Attach tracepoint handler */
    err = hello_bpf__attach(skel);
    if (err) {
        fprintf(stderr, "Failed to attach BPF skeleton\n");
        goto cleanup;
    }

    printf("Hello BPF started, hit Ctrl+C to stop!\n");

    read_trace_pipe();

cleanup:
    hello_bpf__destroy(skel);
    return -err;
}
```

更新 Makefile 的 APPS 列表

```sh
APPS = minimal bootstrap uprobe hello
```

最后，编译运行 hello 程序：

```sh
$ make
  BPF      .output/hello.bpf.o
  GEN-SKEL .output/hello.skel.h
  CC       .output/hello.o
  BINARY   hello
$ ./hello
Hello BPF started, hit Ctrl+C to stop!
<...>-241424  [006] d... 202520.596987: bpf_trace_printk: BPF triggered from PID 241424.
```

可以发现，用 libbpf-bootstrap 开发 BPF 程序非常方便。其源码库中三个示例的解析可以参考 [Building BPF applications with libbpf-bootstrap](https://nakryiko.com/posts/libbpf-bootstrap/)，而更多的示例则可以查看 BCC 中的 [libbpf-tools](https://github.com/iovisor/bcc/tree/master/libbpf-tools)。

> 注意： libbpf 需要开启内核选项 `CONFIG_DEBUG_INFO_BTF=y` 以及 `CONFIG_DEBUG_INFO=y`。在编译内核时，推荐安装 pahole 1.16+，否则的话，就无法生成 BTF。
> 或者，也可以从 <https://kernel.ubuntu.com/~kernel-ppa/mainline/> 直接下载已经默认开启这些选项的内核 DEB 包（比如 v5.10.9）。
## 内核源码

除了以上两种方法，最后一种门槛更高一些的方法是从内核源码中直接编译 BPF 程序。这种方法需要对内核编译有一定了解，且需要善于运用搜索引擎解决编译过程中的各种问题。

首先安装必要的依赖：

```sh
sudo apt install -y bison build-essential cmake flex git libedit-dev pkg-config libmnl-dev \
   python zlib1g-dev libssl-dev libelf-dev libcap-dev libfl-dev llvm clang pkg-config \
   gcc-multilib luajit libluajit-5.1-dev libncurses5-dev libclang-dev clang-tools
```

然后检出内核源码：

```sh
apt install linux-source
cd /usr/src/linux-source-5.4.0 # 版本取决于具体系统
tar jxf linux-source-5.4.0.tar.bz2
cd linux-source-5.4.0
```

最后编译内核 BPF 程序示例：

```sh
cp /boot/config-5.4.0-40-generic .config
make headers_install
make M=samples/bpf
```

而具体的 Hello World 可以参考 [eBPF 环境搭建](https://mp.weixin.qq.com/s?__biz=MzA3NjY2NzY1MA==&mid=2649740000&idx=1&sn=858ac279b00d2b70b39696018cdebf6f&chksm=8746bc8db031359bb891126ae0056c0ac00f3676f07ad68ce7aeddf242a312f3796108cb5f3e&token=1525812246&lang=zh_CN#rd)。

内核中的程序 `hello_kern.c`：

```c
#include <linux/bpf.h>
#include "bpf_helpers.h"

#define SEC(NAME) __attribute__((section(NAME), used))

SEC("tracepoint/syscalls/sys_enter_execve")
int bpf_prog(void *ctx)
{
    char msg[] = "Hello BPF!\n";
    bpf_trace_printk(msg, sizeof(msg));
    return 0;
}

char _license[] SEC("license") = "GPL";
```

用户态的程序 `hello_user.c`:

```c
#include <stdio.h>
#include "bpf_load.h"

int main(int argc, char **argv)
{
    if(load_bpf_file("hello_kern.o") != 0)
    {
        printf("The kernel didn't load BPF program\n");
        return -1;
    }

    read_trace_pipe();
    return 0;
}
```

在对应的位置修改 Makefile 文件，添加以下三行：

```Makefile
hostprogs-y += hello
hello-objs := bpf_load.o hello_user.o
always += hello_kern.o
```

最后编译运行：

```bash
# V=1 查看详细编译输出
make M=samples/bpf V=1
cd samples/bpf
./hello
```

## 小结

本文介绍了三种 eBPF 入门的编程方法，分别是 BCC、libbpf-bootstrap 以及内核源码。对于入门者来说，推荐用 libbpf-bootstrap 作为入门学习参考。

---

欢迎扫描下面的二维码关注**漫谈云原生**公众号，回复**任意关键字**查询更多云原生知识库，或回复**联系**加我微信。

![](/assets/mp.png)
