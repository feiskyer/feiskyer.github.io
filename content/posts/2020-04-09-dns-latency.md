---
title: "如何解决 Kubernetes 的 DNS 延迟问题"
date: 2020-04-09
tags: [Kubernetes, Networking]
draft: false
---



由于 Linux 内核中的缺陷，在 Kubernetes 集群中你很可能会碰到恼人的 DNS 间歇性 5 秒延迟问题（社区 issue 为 **#56903**[1]）。虽然 issue 已经关闭了，但并不是说这个问题已经完全解决了，所以在管理和维护 Kubernetes 集群时，我们需要注意绕开这个缺陷。

### 为什么会有 DNS 间歇性延迟问题

为什么在 Kubernetes 集群会碰到这个间歇性 5 延迟的问题呢？Weave works 发布了一篇博客**Racy conntrack and DNS lookup timeouts**[2]详细介绍了问题的原因。

简单来说，由于 UDP 是无连接的，内核 netfilter 模块在处理同一个 socket 上的并发 UDP 包时就可能会有三个竞争问题。以下面的 conntrack 和 DNAT 工作流程为例：

![图片](640-20210121125028619)

由于 UDP 的 connect 系统调用不会立即创建 conntrack 记录，而是在 UDP 包发送之后才去创建，这就可能会导致下面三种问题：

1. 两个 UDP 包在第一步 `nf_conntrack_in` 中都没有找到 conntrack 记录，所以两个不同的包就会去创建相同的 conntrack 记录（注意五元组是相同的）。
2. 一个 UDP 包还没有调用 `get_unique_tuple` 时 conntrack 记录就已经被另一个 UDP 包确认了。
3. 两个 UDP 包在 `ipt_do_table` 中选择了两个不同端点的 DNAT 规则。

所有这三种场景都会导致最后一步 `__nf_conntrack_confirm` 失败，从而一个 UDP 包被丢弃。由于 GNU C 库和 musl libc 库在查询 DNS 时，都会同时发出 A 和 AAAA DNS 查询，由于上述的内核竞争问题，就可能会发生其中一个包被丢掉的问题。丢弃之后客户端会超时重试，超时时间通常是 5 秒。

上述的第三个问题至今还没有修复，而前两个问题则已经修复了，分别包含在 5.0 和 4.19 中：

1. **netfilter: nf_nat: skip nat clash resolution for same-origin entries**[3] (包含在内核 v5.0 中)
2. **netfilter: nf_conntrack: resolve clash for matching conntracks**[4] (包含在内核 v4.19 中)

> 在公有云中，这些补丁有可能也会包含在旧的内核版本中。比如在 Azure 上，这两个问题已经包含在 v4.15.0-1030.31 和 v4.18.0-1006.6 中。

### 如何避免这个问题

要避免 DNS 延迟的问题，就要设法绕开上述三个问题，所以就有下面几种方法：

1. 禁止并发 DNS 查询，比如在 Pod 配置中开启 `single-request-reopen` 选项强制 A 查询和 AAAA 查询使用相同的 socket：

```
dnsConfig:
  options:
    - name: single-request-reopen
```

1. 禁用 IPv6 从而避免 AAAA 查询，比如可以给 Grub 配置 `ipv6.disable=1` 来禁止 ipv6（需要重启节点才可以生效）。
2. 使用 TCP 协议，比如在 Pod 配置中开启 `use-vc` 选项强制 DNS 查询使用 TCP 协议：

```
dnsConfig:
  options:
    - name: single-request-reopen
    - name: ndots
      value: "5"
    - name: use-vc
```

1. 使用 **Nodelocal DNS Cache**[5]，所有 Pod 的 DNS 查询都通过本地的 DNS 缓存查询，避免了 DNAT，从而也绕开了内核中的竞争问题。你可以执行下面的命令来部署它（注意它会修改 Kubelet 配置并重启 Kubelet）：

```
kubectl apply -f https://github.com/feiskyer/kubernetes-handbook/raw/master/examples/nodelocaldns/nodelocaldns-kubenet.yaml
```

### 参考资料

- [1] 56903: *https://github.com/kubernetes/kubernetes/issues/56903*
- [2] Racy conntrack and DNS lookup timeouts: *https://www.weave.works/blog/racy-conntrack-and-dns-lookup-timeouts*
- [3] netfilter: nf_nat: skip nat clash resolution for same-origin entries: *https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=4e35c1cb9460240e983a01745b5f29fe3a4d8e39*
- [4] netfilter: nf_conntrack: resolve clash for matching conntracks: *https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ed07d9a021df6da53456663a76999189badc432a*
- [5] Nodelocal DNS Cache: *https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/dns/nodelocaldns*




---

欢迎扫描下面的二维码关注**漫谈云原生**公众号，回复**任意关键字**查询更多云原生知识库，或回复**联系**加我微信。

![](/assets/mp.png)
