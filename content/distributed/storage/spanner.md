---
title: spanner
type: page
---

[Spanner](https://research.google.com/archive/spanner.html)是Google提供的跨区域/跨数据中心的关系型分布式数据库，在满足事务一致性的同时还具备极强的可扩展性，结合了传统关系数据库和NoSQL数据库的优点。

![](/images/14871461131101.jpg)

在 Spanner 论文中提到，2012 年大概已经有 300+ 的业务跑在 Megastore 上，在越来越多的业务在 BigTable 上造 ACID Transaction 实现的轮子后，Google 实在受不了了，开始造一个大轮子 Spanner，项目的野心巨大，和 Megastore 一样，ACID 事务 + 水平扩展 + SQL 支持。

- 和 Megastore 不一样的是，Spanner 没有选择在 BigTable 之上构建事务层，而是直接在 Google 的第二代分布式文件系统 Colossus 之上开始构建 Paxos-replicated tablet。
- 不像 Megastore 实现事务那样通过各个协调者通过 Paxos 来决定事务的 timestamp，而是引入了硬件，也就是 GPS 时钟和原子钟组成的 TrueTime API 来实现事务。这样一来，不同数据中心发起的事务就不需要跨数据中心协调时间戳，而是直接通过本地数据中心的 TrueTime API 来分配，这样延迟就降低了很多。

Spanner 近乎完美的一个分布式存储，在 Google 内部也是的 BigTable 的互补，想做跨数据中心高可用和强一致和事务的话，用 Spanner，代价是可能牺牲一点延迟，但是并没有Megastore 牺牲那么多；想高性能（低延迟）的话，用 BigTable。

在 12 年底发布 Spanner 的论文后，社区也有开源的实现，比如目前比较成熟的 TiDB 和 CockroachDB。

## Spanner与CAP

[CAP理论](https://en.wikipedia.org/wiki/CAP_theorem)指出，分布式系统最多只能满足一致性、可用性和分区容忍性中的两个，而不能同时满足三者。所以，常见的分布式系统都需要根据实际场景对这三者作相应的取舍，比如对一个大规模分布式系统来说，网络分区通常是不可避免的，所以要么牺牲一致性保证可用性（AP），要么牺牲可用性，保证一致性（CP）。

而Google Cloud Spanner同时满足了一致性和可用性（CA）：

- 网络分区是不可避免的，在分区出现时，Spanner实际上优先保证一致性，也就是严格意义上来说这是一个CP系统
- 但是Spanner实现了高达5个9的可用性，对大部分用户来说，这个可以认为是一个CA系统

那Google是如何实现这么高的可用性的呢

- 最重要的高可靠和低延迟的SDN网络[B4](http://cseweb.ucsd.edu/~vahdat/papers/b4-sigcomm13.pdf)尽量避免了发生网络分区
    - 链路冗余和快速故障切换（毫秒级）
    - 限制故障影响的范围，比如由于配置错误或者软件更新错误导致的故障只会影响极少的链路
    - 低延迟链路，region之间round-trip time在2ms内
    - 即便真的发生了网络分区，两阶段提交（2PC）+ Paxos也保证了事务一致性，而此时网络分区很可能会导致的其他更严重的服务故障，比如失去网络链接等
    - Spanner还支持快照读（snapshot read），进一步降低了网络分区的影响
- Google’s TrueTime system实现无锁的全局一致性读
    - 全局同步时钟提供了事务之间的外部一致性，避免了不同服务之间的通信开销（实际上会引入一个非常短的延迟，保证时间戳递增）
    - 基于GPS和原子钟保证可靠性（节点之间的时间差控制在10ms以内）

## Spanner实现

[Paper](https://static.googleusercontent.com/media/research.google.com/zh-CN//archive/spanner-osdi2012.pdf)

## Cloud Spanner

近日，Google还宣布了杀手级服务[Cloud Spanner](https://cloudplatform.googleblog.com/2017/02/introducing-Cloud-Spanner-a-global-database-service-for-mission-critical-applications.html)，具备spanner论文里的各种优点：

* 强一致、高性能（毫秒级延迟 single-digit millisecond latencies）
* RDBMS关系数据库的使用体验，ACID事务，SQL查询
* 自动水平扩展
* 高可用（99.999%）
* 默认加密和权限控制保证数据安全
* 多种语言（Java、Go、Python、Node.js等）的客户端

## 参考文档

- [Spanner: Google’s Globally-Distributed Database](https://research.google.com/archive/spanner.html)
- [Cloud Spanner](https://cloud.google.com/spanner/)
- [Inside Cloud Spanner and the CAP Theorem](https://cloudplatform.googleblog.com/2017/02/inside-Cloud-Spanner-and-the-CAP-Theorem.html)
- [Spanner, TrueTime and the CAP Theorem](https://research.google.com/pubs/pub45855.html)
- [Hacker News讨论](https://news.ycombinator.com/item?id=13644959)
