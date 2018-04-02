---
title: Zab
date: 2016-10-21 16:11:07
type: page
---

# Zab

Zab (Zookeeper atomic broadcast protocol)是Zookeeper内部用到的一致性协议。相比Paxos，Zab最大的特点是保证强一致性(strong consistency)。

 ![](/images/14803431609804.png)


和Raft一样，Zab要求唯一Leader参与决议，Zab可以分解成discovery、sync、broadcast三个阶段：

![](/images/14803408244633.jpg)


- 1) discovery: 选举产生PL(prospective leader)，PL收集Follower epoch(cepoch)，根据Follower的反馈PL产生newepoch(每次选举产生新Leader的同时产生新epoch，类似Raft的term)
- 2) sync: PL补齐相比Follower多数派缺失的状态、之后各Follower再补齐相比PL缺失的状态，PL和Follower完成状态同步后PL变为正式Leader(established leader)
- 3) broadcast: Leader处理Client的写操作，并将状态变更广播至Follower，Follower多数派通过之后Leader发起将状态变更落地(deliver/commit)

Leader和Follower之间通过心跳判别健康状态，正常情况下Zab处在broadcast阶段，出现Leader宕机、网络隔离等异常情况时Zab重新回到discovery阶段。

Zab通过约束事务先后顺序达到强一致性，先广播的事务先commit、FIFO，Zab称之为primary order。


**参考文档**

- [Zab: High-performance broadcast for primary-backup systems](http://www.cs.cornell.edu/courses/cs6452/2012sp/papers/zab-ieee.pdf)
- [ZooKeeper’s atomic broadcast protocol: Theory and practice](http://www.tcs.hut.fi/Studies/T-79.5001/reports/2012-deSouzaMedeiros.pdf)
- [Architecture of ZAB – ZooKeeper Atomic Broadcast protocol](https://distributedalgorithm.wordpress.com/2015/06/20/architecture-of-zab-zookeeper-atomic-broadcast-protocol/)
- http://www.cnblogs.com/bangerlee/p/5991417.html
- http://blog.xiaohansong.com/2016/08/25/zab/
