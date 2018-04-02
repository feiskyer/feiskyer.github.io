---
title: Google BigTable
type: page
---

Google 作为大数据的祖宗一样的存在，对于云真是错过了一波又一波：虚拟化错过一波让 VMWare 和 Docker 抢先了（Google 早在十年前就开始容器的方案，要知道容器赖以生存的 cgroups 的 patch 就是 Google 提交的）；云服务错过一波让 Amazon 抢先了（Google App Engine 真是可惜）：大数据存储错过一波让开源的 Hadoop 拿下了事实标准，以至于我觉得 Google Cloud BigTable 服务中兼容 Hadoop HBase API 的决定，当时实现这些 Hadoop API for BigTable 的工程师心中应该是滴血的 :)

不过在被 Amazon / Docker / Hadoop 刺激到以后，Google 终于意识到社区和云化的力量，开始对 Google Cloud 输出 Google 内部各种牛逼的基础设施，2015 年终于在 Google Cloud Platform 上正式亮相。对于 BigTable 的架构相信大多数分布式存储系统工程师都比较了解，毕竟 BigTable 的论文也是和 Amazon Dynamo 一样是必读的经典，我就不赘述了。

BigTable 云服务的 API 和 HBase 兼容，所以也是 `{Key : 二维表格结构}`，由于在 Tablet Server 这个层次还是一个主从的结构，对一个 Tablet 的读写默认都只能通过 Tablet Master 进行，这样使得 BigTable 是一个强一致的系统。这里的强一致指的是对于单 Key 的写入，如果服务端返回成功，接下来发生的读取，都能是最新的值。

由于 BigTable 仍然不支持 ACID 事务，所以这里的强一致只是对于单 Key 的操作而言的。对于水平扩展能力来说， BigTable 其实并没有什么限制，文档里很嚣张的号称 Incredible scalability，但是 BigTable 并没有提供跨数据中心（Zone）高可用和跨 Zone 访问的能力。

也就是说，一个 BigTable 集群只能部署在一个数据中心内部。这其实看得出 BigTable 在 Google 内部的定位，就是一个高性能低延迟的分布式存储服务，如果需要做跨 Zone 高可用需要业务层自己做复制在两个 Zone 之间同步，构建一个镜像的 BigTable 集群。

其实 Google 很多业务在  MegaStore 和 Spanner 出来之前，就是这么搞的。对于 BigTable 来说，如果需要搞跨数据中心高可用，强一致，还要保证低延迟那是不太可能的，也不符合 BigTable 的定位。另外值得吐槽的是 BigTable 团队发过一个 Blog ：
（https://cloudplatform.googleblog.com/2015/05/introducing-Google-Cloud-Bigtable.html）。里面把 HBase 的延迟黑得够呛，一个 .99 的响应延迟 6 ms, HBase 280ms。其实看平均响应延迟的差距不会那么大....BigTable 由于是 C++ 写的，优势就是延迟是相当平稳的。但是据我所知 HBase 社区也在做很多工作将 GC 带来的影响降到最小，比如 off-heap 等优化做完以后，HBase 的延迟表现会好一些。
