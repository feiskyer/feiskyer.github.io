# Google Cloud Datastore

在 2011 年，Google 发表了 Megastore 的论文，第一次描述了一个支持跨数据中心高可用 + 可以水平扩展 + 支持 ACID 事务语义的分布式存储系统。 Google Megastore 构建在 BigTable 之上，不同数据中心之间通过 Paxos 同步，数据按照 Entity Group 来进行分片。Entity Group 本身跨数据中心使用 Paxos 复制，跨 Entity Group 的 ACID 事务需要走两阶段的提交，实现了 Timestamp-based 的 MVCC。

不过也正是因为 Timstamp 的分配需要走一遍 Paxos，另外不同 Entity Groups 之间的 2PC 通信需要通过一个队列来进行异步的通信，所以实际的 Megastore 的 2PC 的延迟是比较大的，论文也提到大多数的写请求的平均响应延迟是 100~400ms 左右。据 Google 内部的朋友提到过，Megastore 用起来是挺慢的，秒级别的延迟也是常有的事情。

作为应该是 Google 内部第一个支持 ACID 事务和 SQL 的分布式数据库，还是有大量的应用跑在 Megastore 上，主要是用 SQL 和事务写程序确实能轻松得多。为什么说那么多 Megastore 的事情呢？因为 Google Cloud Datastore 的后端就是 Megastore。

其实 Cloud Datastore 在 2011 年就已经在 Google App Engine 中上线，也就是当年的 Data Engine 的 High Replication Datastore，现在改了个名字叫 Cloud Datastore，当时不知道背后原来就是大名鼎鼎的 Megastore 实在是失敬。

虽然功能看上去很牛，又是支持高可用，又支持 ACID，还支持 SQL（只不过是 Google 精简版的 GQL）但是从 Megastore 的原理上来看延迟是非常大的，另外 Cloud Datastore 提供的接口是一套类似的 ORM 的 SDK，对业务仍然是有一定的侵入性。

在 Spanner 论文中提到，2012 年大概已经有 300+ 的业务跑在 Megastore 上，在越来越多的业务在 BigTable 上造 ACID Transaction 实现的轮子后，Google 实在受不了了，开始造一个大轮子 Spanner，项目的野心巨大，和 Megastore 一样，ACID 事务 + 水平扩展 + SQL 支持。



