---
title: Reading notes of week 17
date: 2016-04-29 16:50:14
tags: [docker, blockchain, container]
---

**[SIG-Networking: Kubernetes Network Policy APIs Coming in 1.3](http://blog.kubernetes.io/2016/04/Kubernetes-Network-Policy-APIs.html)**

> One problem many users have is that the open access network policy of Kubernetes is not suitable for applications that need more precise control over the traffic that accesses a pod or service. Today, this could be a multi-tier application where traffic is only allowed from a tier’s neighbor. But as new Cloud Native applications are built by composing microservices, the ability to control traffic as it flows among these services becomes even more critical.

> From these scenarios several possible approaches were considered and a minimal policy specification was defined. The basic idea is that if isolation were enabled on a per namespace basis, then specific pods would be selected where specific traffic types would be allowed.

Network isolation is enabled by defining the network-isolation annotation on namespaces as shown below:

		net.alpha.kubernetes.io/network-isolation: [ on | off ]

Once network isolation is enabled, explicit network policies must be applied to enable pod communication.

A policy specification can be applied to a namespace to define the details of the policy as shown below:

```
POST /apis/net.alpha.kubernetes.io/v1alpha1/namespaces/tenant-a/networkpolicys/

{
"kind": "NetworkPolicy",
"metadata": {
"name": "pol1"
},
"spec": {
"allowIncoming": {
"from": [
{ "pods": { "segment": "frontend" } }
],
"toPorts": [
{ "port": 80, "protocol": "TCP" }
]
},
"podSelector": { "segment": "backend" }
}
}
```

![](https://lh5.googleusercontent.com/zMEpLMYmask-B-rYWnbMyGb0M7YusPQFPS6EfpNOSLbkf-cM49V7rTDBpA6k9-Zdh2soMul39rz9rHFJfL-jnEn_mHbpg0E1WlM-wjU-qvQu9KDTQqQ9uBmdaeWynDDNhcT3UjX5)

https://docs.google.com/document/d/1qAm-_oSap-f1d6a-xRTj6xaH1sYQBfK36VyjB5XOZug/edit

**[Build Your Own Container Using Less than 100 Lines of Go](http://www.infoq.com/articles/build-a-container-golang?utm_source=golangweekly&utm_medium=email)

> a super super simple container, in (way) less than 100 lines of go

```go
package main

import (
    "fmt"
    "os"
    "os/exec"
    "syscall"
)

func main() {
    switch os.Args[1] {
    case "run":
        parent()
    case "child":
        child()
    default:
        panic("wat should I do")
    }
}

func parent() {
    cmd := exec.Command("/proc/self/exe", append([]string{"child"}, os.Args[2:]...)...)
    cmd.SysProcAttr = &syscall.SysProcAttr{
        Cloneflags: syscall.CLONE_NEWUTS | syscall.CLONE_NEWPID | syscall.CLONE_NEWNS,
    }
    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr

    if err := cmd.Run(); err != nil {
        fmt.Println("ERROR", err)
        os.Exit(1)
    }
}

func child() {
    must(syscall.Mount("rootfs", "rootfs", "", syscall.MS_BIND, ""))
    must(os.MkdirAll("rootfs/oldrootfs", 0700))
    must(syscall.PivotRoot("rootfs", "rootfs/oldrootfs"))
    must(os.Chdir("/"))

    cmd := exec.Command(os.Args[2], os.Args[3:]...)
    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr

    if err := cmd.Run(); err != nil {
        fmt.Println("ERROR", err)
        os.Exit(1)
    }
}

func must(err error) {
    if err != nil {
        panic(err)
    }
}
```

**[Go性能优化技巧(By 雨痕)](http://mp.weixin.qq.com/s?src=3&timestamp=1461920086&ver=1&signature=dvsw--b6KnMYdRt43I2g4kMRIN37-tbcl2AnwpG58mxVaoZpqG24Aou2amIcFH1aIgXelirKZ0iSYJnPud*qh3uzFrbmeM*bcDNCVC0t*m4oEblW1GOp0FHTsG-lSzRzE67RaskRf7u4*B5NZlkmYhTbWJNF44Bvwz9D58*D-54=)

1. 字符串（string）作为一种不可变类型，在与字节数组（slice, [ ]byte）转换时需付出 “沉重” 代价，根本原因是对底层字节数组的复制。

```go
package main

import (
    "fmt"
    "unsafe"
)

func str2bytes(s string) []byte {
    ptr := (*[2]uintptr)(unsafe.Pointer(&s))
    btr := [3]uintptr{ptr[0], ptr[1], ptr[1]}
    return *(*[]byte)(unsafe.Pointer(&btr))
}

func bytes2str(b []byte) string {
    return *(*string)(unsafe.Pointer(&b))
}

func main() {
    s := "abcdefghi"
    b := str2bytes(s)
    s2 := bytes2str(b)

    fmt.Println(s, b, s2)
}
```

2. Go Proverbs: A little copying is better than a little dependency. 对于一些短小的对象，复制成本远小于在堆上分配和回收操作。

3. map预设容量：map 会按需扩张，但须付出数据拷贝和重新哈希成本。如有可能，应尽可能预设足够容量空间，避免此类行为发生。

4. map直接存储，对于小对象，直接将数据交由 map 保存，远比用指针高效。这不但减少了堆内存分配，关键还在于垃圾回收器不会扫描非指针类型 key/value 对象。

5. defer的代价:编译器通过 runtime.deferproc “注册” 延迟调用，除目标函数地址外，还会复制相关参数（包括 receiver）。在函数返回前，执行 runtime.deferreturn 提取相关信息执行延迟调用。这其中的代价自然不是普通函数调用一条 CALL 指令所能比拟的。可以考虑将内层处理逻辑转换为匿名函数.

6. 不合理的闭包会造成性能问题，比如闭包引用原环境变量会导致Data Race并变量逃逸到堆上，增加GC扫描和回收的负担.

**[基于组的策略（GBP）开启新型网络设计时代](http://www.sdnlab.com/16646.html)**

很早就玩过GBP，当时还是基于思科ACI的。GBP这个东西从概念上完全照搬了ACI的那套理论，将原有网络的概念转换成了面向应用的网络策策略。对大部分做网络的人来说，有一定的接受难度；但对应用开发人员挺友好的。不过ACI需要增加路由器的控制，才能算是一个完整的方案。

现在GBP也集成了ODL，终于有更多的玩家进来。

顺便说下，Kubernetes Network Policy跟GBP的概念很像，都是面向应用的接口.


