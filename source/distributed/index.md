---
title: Distributed
date: 2016-10-21 16:11:07
---

# Distributed

## 分布式系统的一致性

考虑在数据冗余情况下一致性和性能的问题，即：

1）要想让数据有高可用性，就得写多份数据。
2）写多份的问题会导致数据一致性的问题。
3）数据一致性的问题又会引发性能问题。
4）同时还要考虑两将军问题和拜占庭将军问题。

**[一致性模型](http://coolshell.cn/articles/10910.html)**

1）Weak 弱一致性：当你写入一个新值后，读操作在数据副本上可能读出来，也可能读不出来。比如：某些cache系统，网络游戏其它玩家的数据和你没什么关系，VOIP这样的系统，或是百度搜索引擎（呵呵）。
2）Eventually 最终一致性：当你写入一个新值后，有可能读不出来，但在某个时间窗口之后保证最终能读出来。比如：DNS，电子邮件、Amazon S3，Google搜索引擎这样的系统。
3）Strong 强一致性：新的数据一旦写入，在任意副本任意时刻都能读到新值。比如：文件系统，RDBMS，Azure Table都是强一致性的。

[CAP理论](http://www.read.seas.harvard.edu/~kohler/class/cs239-w08/decandia07dynamo.pdf)要求$W+R > N$。

**[一致性实现方法](http://coolshell.cn/articles/10910.html)**

1) Master-Slave（最终一致或强一致）：读写请求都由Master负责；写请求写到Master上后，再同步到Slave上（同步或异步）。
2）Master-Master（最终一致）：多个Master都负责读写。好处是一台Master挂了，别的Master可以正常做读写服务，但和Master-Slave一样，当数据没有被复制到别的Master上时，数据会丢失。同时，多个Master写还涉及到数据冲突的问题。
3）Two/Three Phase Commit：第一阶段做Vote，第二阶段做决定。第一阶段是同步阻塞，影响性能。另一个问题是如果第一阶段完成后，参与者在第二阶没有收到决策，那么数据结点会进入“不知所措”的状态，这个状态会block住整个事务。所以引入三段提交（在询问的时候并不锁定资源，除非所有人都同意了，才开始锁资源），把二段提交的第一个段break成了两段：询问，然后再锁资源，最后真正提交。
4）一致性协调算法：

- 4.1) [Paxos](paxos.html)
- 4.2) [Raft](raft.html)
- 4.3) [Zab](zab.html)


