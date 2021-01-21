---
title: "BPF 学习路径总结"
date: 2021-01-06
tags: [ebpf]
draft: false
---

> 作者简介：狄卫华，趣头条资深架构师，主要关注云原生相关领域，目前聚焦在 BPF 技术及实践.

## 1. 为什么要学习 BPF

可以先从 [ebpf.io](https://ebpf.io/) 网站获取一个简单的了解，首页内容翻译如下。

Linux 内核一直是实现监控/可观察性、网络和安全性的理想场所。不幸的是，这往往是不切实际的，因为它需要改变内核源代码或加载内核模块，并导致层层抽象叠加。eBPF 是一项革命性的技术，它可以在 Linux 内核中运行沙盒程序，而无需改变内核源代码或加载内核模块。

通过使Linux内核可编程，基础架构软件可以利用现有的层，使其更加智能，功能更加丰富，而不会继续给系统增加额外的复杂度，也不会影响执行效率和安全性。

eBPF 开发了全新一代的软件，能够对 Linux 内核的行为进行重新编程，甚至在传统上完全独立的多个子系统中应用逻辑。

![bpf_arch](bpf_arch.png)

BPF 技术目前主要用于以下场景：

1. 追踪和性能分析（Tracing & Profiling）

   将 eBPF 程序附加到跟踪点以及内核和用户应用探针点的能力，使得应用程序和系统本身的运行时行为具有前所未有的可见性。通过赋予应用程序和系统两方面的检测能力，可以将两种视图结合起来，从而获得强大而独特的洞察力来排除系统性能问题。先进的统计数据结构允许以高效的方式提取有意义的可见性数据，而不需要像类似系统那样，通常需要导出大量的采样数据。

2. 观测和监控（Obervability & Monitoring）

   eBPF 不依赖于操作系统暴露的静态计数器和测量，而是实现了自定义指标的收集和内核内聚合，并基于广泛的可能来源生成可见性事件。这扩展了实现的可见性深度，并通过只收集所需的可见性数据，以及在事件源处生成直方图和类似的数据结构，而不是依赖样本的导出，大大降低了整体系统的开销。

3. 网络（Network）

   可编程性和效率的结合使得 eBPF 自然而然地满足了网络解决方案的所有数据包处理要求。eBPF 的可编程性使其能够在不离开 Linux内核的包处理上下文的情况下，添加额外的协议解析器，并轻松编程任何转发逻辑以满足不断变化的需求。JIT 编译器提供的效率使其执行性能接近于本地编译的内核代码。

4. 安全（Security）

   在看到和理解所有系统调用的基础上，将其与所有网络操作的数据包和套接字级视图相结合，可以采用革命性的新方法来确保系统的安全。虽然系统调用过滤、网络级过滤和进程上下文跟踪等方面通常由完全独立的系统处理，但 eBPF 允许将所有方面的可视性和控制结合起来，以创建在更多上下文上运行的、具有更好控制水平的安全系统。

> 在追踪方面细分为了两类：
>
> - 追踪和性能分析
> - 观测和监控
>
> 这两者的区别主要在于数据的搜集和聚合是否在内测层面进行的，观测和监控主要是侧重于在内核导出指标、直方图或相关事件。

| ![bpf_cls_trace](bpf_cls_trace.png)     | ![bpf_cls_monitor](bpf_cls_monitor.png)   |
| :-------------------------------------- | :---------------------------------------- |
| ![bpf_cls_network](bpf_cls_network.png) | ![bpf_cls_security](bpf_cls_security.png) |

BPF 技术的整体介绍请参见 [eBPF 结束简介](https://www.ebpf.top/post/bpf_intro_blog/)。

## 2. BPF 应该怎么学习

### 2.1 BPF 书籍

#### 2.1.1 书籍介绍

如果是想系统学习 BPF 技术，我的建议是先阅读相关的书籍，得到一个整体的认识，然后分方向单独深入。

目前 BPF 的书籍主要有以下两本：

- [《Linux Observability with BPF》](https://www.amazon.com/Linux-Observability-BPF-Programming-Performance/dp/1492050202)

  图书全名为：《Linux Observability with BPF: Advanced Programming for Performance Analysis and Networking》。

  早期该书的电子版可以在 sysdig 官网下载，国内可以在[此处下载](https://pan.baidu.com/s/10gYYVXOdTX4HQ-_dQfWfOQ)：链接: 提取码: bebt。

  本书两位作者合著：

  - [美] 大卫·卡拉维拉（David Calavera）Netlify 的 CTO，曾是 Docker 的维护者以及 Runc、Go 和 BCC 工具及其他开源项目的贡献者
  - [意] 洛伦佐·丰塔纳（Lorenzo Fontana）Sysdig 开源团队的成员，主要负责CNCF的 Falco 项目，该项目通过内核模块和 eBPF 实现了容器运行时安全和异常检测功能。

  当前图书已经翻译成中文，京东地址：[《Linux内核观测技术BPF》](https://item.jd.com/72110825905.html)。

- [《BPF Performance Tools》](http://www.brendangregg.com/bpf-performance-tools-book.html)

  图书全名为：《[BPF Performance Tools: Linux System and Application Observability](http://www.brendangregg.com/bpf-performance-tools-book.html)》

  作者为大名鼎鼎的性能大师 [Brendan Gregg](http://www.brendangregg.com/)，该书目前还没有中文版，如果购买英文版，可以从[外文书店](https://item.jd.com/64536164411.html)代购，2-3 周可以收到。

  他还写过一本性能优化的畅销书 《Systems Performance: Enterprise and the Cloud》，中文翻译版本为 [《性能之巅：洞悉系统、企业与云计算》](https://item.jd.com/11755695.html)。该书的第二版作者还在修订中，可参见：《[Systems Performance: Enterprise and the Cloud, Second Edition (2020)](http://www.brendangregg.com/systems-performance-2nd-edition-book.html)》。

  Brendan Gregg 的博客地址为： http://www.brendangregg.com/，里面有关于性能优化的诸多宝藏，值得仔细学习和研究。

  > update: 2021-1-6
  >
  > 该书的中文版本已经出版在售，中文名为 《BPF之巅：洞悉Linux系统和应用性能》， JD 购买地址：https://item.jd.com/12769029.html

#### 2.1.2 图书心得

- [《Linux Observability with BPF》](https://www.amazon.com/Linux-Observability-BPF-Programming-Performance/dp/1492050202)

  中文和英文版都在 180 页左右，整体的思路清晰，相关的技术面面俱到，如果定位是整体理解（而不是实践练习），整本书阅读一天内可以完成，能够实现快速对于 BPF 技术的整体了解，但是本书对于涉及的内容介绍基本上还是停留在基础知识介绍，基本上无深入知识介绍，**作为入门级别的书籍再合适不过**。主要内容包括以下方面：

  - BPF 基础知识
    - BPF 的历史及架构；
    - BPF 的程序类型和验证器：按照重要性依次介绍了各种程序类型；
    - BPF Map： BPF Map 类型，常见操作和以及 Map 相关虚拟系统；
  - BPF Trace
    - BPF Trace：Trace 的基础知识（kprobe、tracepoint、usdt等）和几个 BCC 使用的样例；
    - BPF 相关工具（BPFTool & BPFTrace & kubectl-trace & eBPF Exportor）；
  - BPF Network
    - Linux 网络和 BPF：涵盖数据包过滤和 cls_bpf 相关内容；
    - XDP：由于 XDP 在网络数据处理的特殊地位，单独成章，对于 XDP 进行了简单介绍和一个简单的原理实现，以及如何使用 BCC 进行 XDP 相关的验证；
  - 安全
    - 主要是 Seccomp（基于传统的 cBPF）和 LSM 钩子两个方面的内容，主要是简单的介绍，内容不多；
  - 真实的用户案例
    - 国外几大公司 Sysdig 、Floowmill 等在 BPF 的技术实践。

- [《BPF Performance Tools》](http://www.brendangregg.com/bpf-performance-tools-book.html)

  本书英文版 839 页，主要涉及的 BPF 技术的基础、BPF Trace 基础基础知识、**BPF 技术 Trace 方面的各种实践**，**本书无 BPF 在网络、安全上的详细介绍**。本书的**介绍侧重于基础知识和在 Trace 层面的实践**，可以理解为 《Systems Performance: Enterprise and the Cloud》图书的修订版本，重点引入了 BPF 技术的实践。

  全书主题分成四个部分：

  1. 技术

     在第一部分主要涉及的是 BPF 相关的技术和如何使用的总览。

     - BPF 技术介绍
     - 👍 技术背景
     - 性能分析总览
     - BCC 工具介绍
     - BPFTrace 工具介绍

     这个部分的内容介绍，重点在 `技术背景` 章节，介绍的了 Trace 相关的技术点及实现原理，总结的非常简练和准确，值得多阅读几遍； BCC 和 BPFTrace 工具的介绍更多是从原理和使用层面介绍，详细的知识可以从两者的 github 网址学习到，贵在章节内容总结的有图有条理，可以快速对于整体架构有个快速的认知。

  2. 使用 BPF 工具

     本章节主要是介绍了各种性能分析维度（CPU/Mem/Network/System等）的背景知识、传统工具和BPF 工具使用。

     这个章节可以理解是 《Systems Performance: Enterprise and the Cloud》的缩减（背景知识、传统工具）和BPF 工具的补充，但是也增加了一些多的内容比如安全、容器和虚拟化的内容。

     这部分的内容有方法论、基础知识和使用实践，可以作为日常问题排查的参考工具书。

  3. 附加主题

     作为 BPF 性能工具的补充，还有一些是使用 BPF 各种过程中的小知识、技巧和常见的问题。

  4. 附录

     虽然是作为附录的内容，但是却是我们学习深入技术点的重要参考，主要是 bpftrace 工具的一览表、BCC Tools 开发、使用原生的 C 编写 BPF 和 BPF 指令集等。

     这部分的内容面对的是希望对于 BPF 技术更加深入了解和希望参与到 BCC 工具开发的研发人员。

### 2.2 BPF 学习样例

如果是 BCC 的样例可以参考 [tools](https://github.com/iovisor/bcc/tree/master/tools) 目录下的全部文件； BPFTrace 也可以参考 [tools](https://github.com/iovisor/bpftrace/tree/master/tools) 目录。

内核中的 BPF 样例参见 [samples/bpf](https://elixir.bootlin.com/linux/v5.8/source/samples/bpf) 和 [testing/bpf](https://elixir.bootlin.com/linux/v5.8/source/tools/testing/selftests/bpf)，这部分的代码都是原生的 C 代码，比较适合对于 BPF 技术原理进一步深入的同学。

如果是一开始学习 BPF，我个人的建议是：

1. 先大体了解 BPF 技术的发展历史、优点、限制；
2. 使用 BCC 工具在环境中进行实践，并且初步了解相关工具的的运作机制；
3. 参考 BCC 样例，用原生的 C 代码进行实践并编写；
4. 通过 KubeCon 会议或者 [BPF Summit](https://ebpf.io/summit-2020) 峰会学习当前主要的进展并学习跟进最新的进展；

学习方式也可以参考的大卫李的一篇文章 [Linux超能力BPF技术介绍及学习分享](https://cloud.tencent.com/developer/article/1698426)，写的内容也比较齐全，可以参考。

## 3. BPF 资料汇总

> 如果有好的文章或者思路分析，可以到我的 [GitHub Repo](https://github.com/DavadDi/bpf_study) 提交 Issue，地址：https://github.com/DavadDi/bpf_study。

### 3.1 介绍系列

- 👍 [https://ebpf.io](https://ebpf.io/) 官方维护的站点，上面的资料还是比较完整和权威的
- 👍👍 [[译\] 大规模微服务利器：eBPF + Kubernetes（KubeCon, 2020）](http://arthurchiao.art/blog/ebpf-and-k8s-zh/) BPF Maintainer Daniel 的大作，非常详细，本文内容的时间跨度有 8 年，覆盖了 eBPF 发展的整个历史，非常值得一读。[pdf](https://github.com/DavadDi/bpf_study/blob/master/BPF-and-Kubernetes-Little-Helper-Minions-for-Scaling-Microservices/Aug19_eBPF_and_Kubernetes_Little_Helper_Minions_for_Scaling_Microservices_Daniel_Borkmann.pdf)
- 👍 [[译\] 如何基于 Cilium 和 eBPF 打造可感知微服务的 Linux（2019）](https://github.com/DavadDi/bpf_study/blob/master/how-to-make-linux-microservice-aware-with-cilium-ebpf/index.md) [pdf](https://github.com/DavadDi/bpf_study/blob/master/how-to-make-linux-microservice-aware-with-cilium-ebpf/bpf_-_turning_linux_into_a_microservices-aware_operating_system.pdf)
- An eBPF overview 系列
  - [part 1: Introduction](https://www.collabora.com/news-and-blog/blog/2019/04/05/an-ebpf-overview-part-1-introduction/)
  - [part 2: Machine & bytecode](https://www.collabora.com/news-and-blog/blog/2019/04/15/an-ebpf-overview-part-2-machine-and-bytecode/)
  - [part 3: Walking up the software stack](https://www.collabora.com/news-and-blog/blog/2019/04/26/an-ebpf-overview-part-3-walking-up-the-software-stack/)
  - [part 4: Working with embedded systems](https://www.collabora.com/news-and-blog/blog/2019/05/06/an-ebpf-overview-part-4-working-with-embedded-systems/)
  - [part 5: Tracing user processes](https://www.collabora.com/news-and-blog/blog/2019/05/14/an-ebpf-overview-part-5-tracing-user-processes/)
- [The art of writing eBPF programs: a primer](https://github.com/DavadDi/bpf_study/blob/master/the-art-of-writing-ebpf-programs-a-primer/index.md)
- [A Deep Dive into eBPF: The Technology that Powers Tracee](https://blog.aquasec.com/intro-ebpf-tracing-containers)
- [Linux Extended BPF (eBPF) Tracing Tools](http://www.brendangregg.com/ebpf.html) Brendan Gregg
- [A thorough introduction to eBPF](https://lwn.net/Articles/740157/)
- [iovisor](https://github.com/iovisor)/**[bpf-docs](https://github.com/iovisor/bpf-docs)**

### 3.2 深入系列

- [Linux 内核 BPF 文档](https://www.infradead.org/~mchehab/kernel_docs/bpf/index.html)
- bpf 归档的邮件列表 https://lore.kernel.org/bpf/， 完整列表 http://vger.kernel.org/vger-lists.html
- 👍 [Dive into BPF: a list of reading material](https://qmonnet.github.io/whirl-offload/2016/09/01/dive-into-bpf/)，中文参见[这里](https://www.zcfy.cc/article/dive-into-bpf-a-list-of-reading-material), 基于这个文档有作者整理了一个更加清晰的分类 [zoidbergwill/awesome-ebpf](https://github.com/zoidbergwill/awesome-ebpf) 和 [**awesome-ebpf **](https://github.com/icopy-site/awesome-cn/blob/master/docs/awesome/awesome-ebpf.md)- 中文
- 👍👍 [Cillum BPF and XDP Reference Guide](https://docs.cilium.io/en/v1.8/bpf/) [[译\] Cilium：BPF 和 XDP 参考指南（2019）](http://arthurchiao.art/blog/cilium-bpf-xdp-reference-guide-zh/)
- [lwn.net#Berkeley_Packet_Filter](https://lwn.net/Kernel/Index/#Berkeley_Packet_Filter) lwn.net 网站中与 BPF 相关的主题文章，对于了解 BPF 的历史非常有帮助
- 👍👍 Oracle Blog 系列教程，深入浅出，是深入学习的必学教程
  - [BPF program types](http://blogs.oracle.com/linux/notes-on-bpf-1)，配合 [eBPF features by Linux version](https://github.com/iovisor/bcc/blob/master/docs/kernel-versions.md) 效果更好
  - [BPF helper functions for those programs](http://blogs.oracle.com/linux/notes-on-bpf-2)
  - [BPF userspace communication](http://blogs.oracle.com/linux/notes-on-bpf-3)
  - [BPF program build environment](http://blogs.oracle.com/linux/notes-on-bpf-4)
  - [BPF bytecodes and verifier](http://blogs.oracle.com/linux/notes-on-bpf-5)
  - [BPF Packet Transformation](http://blogs.oracle.com/linux/notes-on-bpf-6)
  - [The Power of XDP](https://blogs.oracle.com/linux/the-power-of-xdp)
  - [Notes on BPF (7) - BPF, tc and Generic Segmentation Offload](https://blogs.oracle.com/linux/notes-on-bpf-7)
  - [Taming Tracepoints in the Linux Kernel](https://blogs.oracle.com/linux/taming-tracepoints-in-the-linux-kernel)
- 👍 [xdp-tutorial](https://github.com/xdp-project/xdp-tutorial) 里面有详细的 xdp 的源码，是学习 xdp 的好地方
- 👍 [[译\] 深入理解 Cilium 的 eBPF 收发包路径（datapath）（KubeCon, 2019）](http://arthurchiao.art/blog/understanding-ebpf-datapath-in-cilium-zh/) [pdf](https://github.com/DavadDi/bpf_study/blob/master/Understanding-the-eBPF-Datapath-in-Cilium/eBPF-and-the-Cilium-Datapath.pdf)

### 3.3 Linux 资源

- 在线内核源码 https://elixir.bootlin.com/

> 本文转自深入浅出 eBPF，点击[这里](https://www.ebpf.top/post/ebpf_learn_path/)查看原文。


---

欢迎扫描下面的二维码关注**漫谈云原生**公众号，回复**任意关键字**查询更多云原生知识库，或回复**联系**加我微信。

![](/assets/mp.png)