---
title: Go performance optimize
date: 2016-05-06 20:40:06
tags: [go]
---

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

7. Channel： Don't communicate by sharing memory, share memory by communicating.

> 如果说 channel 适用于结构层面解耦，那么 mutex 则适合保护语句级别的数据安全。至于 atomic，虽然也可实现 lock-free 结构，但处理起来要复杂得多（比如 ABA 等问题），也未必就比 mutex 快很多。还有，sync.Mutex 本就没有使用内核实现，而是像 Futex 那样，直接在用户空间以 atomic 操作完成，因为 runtime 没有任何理由将剩余 CPU 时间片还给内核。

8. 关于interface:

> 接口的用途无需多言。但这并不意味着可在任何场合使用接口，要知道通过接口调用和普通调用存在很大差别。首先，相比静态绑定，动态绑定性能要差很多；其次，运行期需额外开销，比如接口会复制对象，哪怕仅是个指针，也会在堆上增加一个需 GC 处理的目标。

9. 尽管反射（reflect）存在性能问题，但依然被频繁使用，以弥补静态语言在动态行为上的不足。只是某些时候，我们须对此做些变通，以提升性能。利用指针类型转换实现性能优化，本就是 “非常手段”，是一种为了性能而放弃 “其他” 的做法。与其担心代码是否适应未来的变化，不如写个单元测试，确保在升级时做出必要的安全检查。 [Link](http://mp.weixin.qq.com/s?timestamp=1462538257&src=3&ver=1&signature=dth4TWXJxgxWRCAQDVFbKniJE-JCeVdqp0eMklk4f0kgrbb7QuS7xs5KDDFwmZg0ba6tMcn41JsyNZceCzyp5nErTGnWK-K9wlgOp9wAw5S3bbeBa3-BkGp3r*kN-ORevh9Iuo1UnjtFWtOoEoSX0vTH6uxMcP7*Ts0r0f4yhzE=)

10. 作为内置类型，通道（channel）从运行时得到很多支持，其自身设计也算得上精巧。但不管怎么说，它本质上依旧是一种队列，当多个 goroutine 并发操作时，免不了要使用锁。某些时候，这种竞争机制，会导致性能问题。[在研究 go runtime 源码实现过程中，会看到大量利用 “批操作” 来提升性能的样例)(http://mp.weixin.qq.com/s?timestamp=1462538257&src=3&ver=1&signature=dth4TWXJxgxWRCAQDVFbKniJE-JCeVdqp0eMklk4f0kgrbb7QuS7xs5KDDFwmZg0ba6tMcn41JsyNZceCzyp5pZfVq*Q5bYXUHM1nH0kMNsPL3e92xy5a0zTraWNTSnQ9u8Ie3b9rjnbg0blEE3NEoenRnmCV3MpZdqseFiuy*A=)

11. Goroutine Leak: 极简单的演示，我们注释掉数据读取方，让发送方全部进入休眠等待状态。按理说，当 test 执行结束后，通道 c 已超出作用域，理应被释放回收，但实际情况是：这些处于 “chan send” 状态的 G 对象（goroutine）会一直存在，直到唤醒或进程结束，这就是所谓的 “Goroutine Leak”。解决方法很简单，可设置 timeout。或定期用 runtime.Stack 扫描所有 goroutine 调用栈，如果发现某个 goroutine 长时间（阈值）处于 “chan send” 状态，可用一个类似 “/dev/null hole” 的接收器负责唤醒并 “处理” 掉相关数据。 [Link](http://mp.weixin.qq.com/s?timestamp=1462538257&src=3&ver=1&signature=dth4TWXJxgxWRCAQDVFbKniJE-JCeVdqp0eMklk4f0kgrbb7QuS7xs5KDDFwmZg0ba6tMcn41JsyNZceCzyp5o9mcQPs7Eqi*KhEEPKyOoiDvyJHFBWSxCetuDBLPPTsdi-SZQypc24ZMdm5qRs13Je5vyZgLwIlLqhUsErg9oI=)
