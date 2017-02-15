---
title: 负载均衡
---

## 经典Linux负载均衡

- Haproxy
- LVS
- Nginx (反向代理)

## 硬件负载均衡

- F5

## 其他

### Google Maglev

[Maglev](https://research.google.com/pubs/pub44824.html)是Google自研的负载均衡方案，在2008年就已经开始用于生产环境。Maglev安装后不需要预热5秒内就能处理每秒100万次请求。谷歌的性能基准测试中，Maglev实例运行在一个8核CPU下，网络吞吐率上限为12M PPS（数据包每秒）。如果Maglev使用Linux内核网络堆栈则速度会慢下来，吞吐率小于4M PPS。

![](maglev.png)

- 路由器ECMP (Equal Cost Multipath) 转发包到Maglev（而不是传统的主从结构)
- Kernel Bypass, CPU绑定，共享内存
- 一致性哈希保证连接不中断

### UCloud [Vortex](http://mp.weixin.qq.com/s?src=3&timestamp=1484623935&ver=1&signature=ifj0PRCsXKHVPiVcl-dNxhSlKKKcX6hwO1rz-hbipIrL2weMxHv0bSysMyY-yB-AXJrUZix9kjQCpvsRJnxF1grXi*O6nZZjaUFFEdA6ROfgicdAvfEFDM4-i42kY*58GHuAFkhGvMzovPTmTYY*Eg==)

Vortex参考了Maglev，大致的架构和实现跟Maglev类似：

- ECMP实现集群的负载均衡
- 一致性哈希保证连接不中断
    - 即使是不同的Vortex服务器收到了数据包，仍然能够将该数据包转发到同一台后端服务器
    - 后端服务器变化时，通过连接追踪机制保证当前活动连接的数据包被送往之前选择的服务器，而所有新建连接则会在变化后的服务器集群中进行负载分担
- DPDK提升单机性能 (14M PPS，10G, 64字节线速)
    - 通过RSS直接将网卡队列和CPU Core绑定，消除线程的上下文切换带来的开销
    - Vortex线程间采用高并发无锁的消息队列通信
- DR模式避免额外开销