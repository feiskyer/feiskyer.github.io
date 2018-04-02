---
title: Raft
type: page
---

# Raft

Raft可以在高效的解决分布式系统中各个节点日志内容一致性问题的同时，也使得集群具备一定的容错能力。即使集群中出现部分节点故障、网络故障等问题，仍可保证其余大多数节点正确的步进。甚至当更多的节点（一般来说超过集群节点总数的一半）出现故障而导致集群不可用时，依然可以保证节点中的数据不会出现错误的结果。

**论文**

1. [In Search of an Understandable Consensus Algorithm (Extended Version)](https://ramcloud.stanford.edu/raft.pdf)
2. [CONSENSUS: BRIDGING THEORY AND PRACTICE](https://ramcloud.stanford.edu/~ongaro/thesis.pdf)

## raft算法

**3个角色**

- Leader：负责日志的同步管理，处理来自客户端的请求，与Follower保持heartBeat联系；
- Follower：刚启动时所有节点为Follower状态，响应Leader的日志同步请求，响应Candidate的请求，把请求到Follower的事务转发给Leader；
- Candidate：负责选举投票，Raft刚启动时由一个节点从Follower转为Candidate发起选举，选举出Leader后从Candidate转为Leader状态。

![](/images/14804284620225.jpg)


**Raft选举方法**

- 1) 初始启动时，节点处于follower状态并被设定一个election timeout，如果在这一时间周期内没有收到来自 leader 的 heartbeat，节点将发起选举：将自己切换为 candidate 之后，向集群中其它 follower 节点发送请求，询问其是否选举自己成为 leader。
- 2) 当收到来自集群中过半数节点的接受投票后，节点即成为 leader，开始接收保存 client 的数据并向其它的 follower 节点同步日志。如果没有达成一致，则candidate随机选择一个等待间隔（150ms ~ 300ms）再次发起投票，得到集群中半数以上follower接受的candidate将成为leader
- 3) leader节点依靠定时向 follower 发送heartbeat来保持其地位。
- 4）任何时候如果其它 follower 在 election timeout 期间都没有收到来自 leader 的 heartbeat，同样会将自己的状态切换为 candidate 并发起选举。每成功选举一次，新 leader 的任期（Term）都会比之前 leader 的任期大1。

**日志复制**

当接Leader收到客户端的日志（事务请求）后先把该日志追加到本地的Log中，然后通过heartbeat把该Entry同步给其他Follower，Follower接收到日志后记录日志然后向Leader发送ACK，当Leader收到大多数（n/2+1）Follower的ACK信息后将该日志设置为已提交并追加到本地磁盘中，通知客户端并在下个heartbeat中Leader将通知所有的Follower将该日志存储在自己的本地磁盘中。

![](/images/14804284340920.jpg)


**安全性**

安全性是用于保证每个节点都执行相同序列的安全机制，如当某个Follower在当前Leader commit Log时变得不可用了，稍后可能该Follower又会倍选举为Leader，这时新Leader可能会用新的Log覆盖先前已committed的Log，这就是导致节点执行不同序列；Safety就是用于保证选举出来的Leader一定包含先前 commited Log的机制；

- 选举安全性（Election Safety）：每个任期（Term）只能选举出一个Leader
- Leader完整性（Leader Completeness）：指Leader日志的完整性，当Log在任期Term1被Commit后，那么以后任期Term2、Term3…等的Leader必须包含该Log；Raft在选举阶段就使用Term的判断用于保证完整性：当请求投票的该Candidate的Term较大或Term相同Index更大则投票，否则拒绝该请求。

**失效处理**

- 1) **Leader失效**：其他没有收到heartbeat的节点会发起新的选举，而当Leader恢复后由于步进数小会自动成为follower（日志也会被新leader的日志覆盖）
- 2）**follower节点不可用**：follower 节点不可用的情况相对容易解决。因为集群中的日志内容始终是从 leader 节点同步的，只要这一节点再次加入集群时重新从 leader 节点处复制日志即可。
- 3）**多个candidate**：冲突后candidate将随机选择一个等待间隔（150ms ~ 300ms）再次发起投票，得到集群中半数以上follower接受的candidate将成为leader

**集群扩容**

集群中节点的变更，要么是故障，要么是业务需求扩容/缩容。 Raft使用联合一致性阶段（joint consensus）来作为过渡阶段实现配置从旧到新的变化。

集群中配置状态的转换：

- Cold 已提交，Cold,new 未提交
- Cold,new 已提交，Cnew 未提交 此时只有拥有 Cold,new 配置的server才会被选为leader。如果此时，Cold,new 提交失败，那么重新发送 Cold，回滚配置。
- Cnew 已提交 如果在这个阶段存在着Leader election，那么只有具有Cnew 配置的server才能被选为Leader，Leader将Cnew 配置复制到所有的follower，使得整个集群应用新的配置。 如果Cnew 提交时，leader并不包括在新的配置中，那么leader将降为为follower，且不参与大多数的投票。
- 如果Cnew 提交失败，则需要复制 Cold，回滚配置。如果在回滚配置之前发生了Leader Election，那么leader具有Cnew，则将其复制到新集群。如果leader没有Cnew，则会覆盖其他server中的新配置，回到joint consensus状态

![](/images/14804283965953.jpg)

## 与Paxos对比

raft中发送的请求（日志项）必须是连续的,而paxos中使可以并发的（就是说paxos可以同时发送日志项2,3，3不需要等待2处理完才能发送，但在状态集中日志顺序还是不变的，有点类似于TCP中的数据发送）
raft选主是有限制的, 必须有最新，最全的日志节点才可以当选. 而multi-paxos中是随意的。所以raft 可以看成是简化版本的multi-paxos(这里multi-paxos因为允许并发的写日志,因此不存在一个最新，最全的日志节点，因此只能这么做。这样带来的麻烦就是选主以后, 需要将主里面没有的日志给补全, 并执行commit 过程)
根据上面可以看出，raft更加的简单，paxos支持日志并发，更加的灵活。

## Raft常见问答一览

* **Raft中一个Term（任期）是什么意思？** Raft算法中，从时间上，一个任期讲即从一次竞选开始到下一次竞选开始。从功能上讲，如果Follower接收不到Leader节点的心跳信息，就会结束当前任期，变为Candidate发起竞选，有助于Leader节点故障时集群的恢复。发起竞选投票时，任期值小的节点不会竞选成功。如果集群不出现故障，那么一个任期将无限延续下去。而投票出现冲突也有可能直接进入下一任再次竞选。

    ![](http://cdn3.infoqstatic.com/statics_s1_20170221-0307u1/resource/articles/etcd-interpretation-application-scenario-implement-principle/zh/resources/0129012.jpg)

    **Term示意图**

* **Raft状态机是怎样切换的？** Raft刚开始运行时，节点默认进入Follower状态，等待Leader发来心跳信息。若等待超时，则状态由Follower切换到Candidate进入下一轮term发起竞选，等到收到集群多数节点的投票时，该节点转变为Leader。Leader节点有可能出现网络等故障，导致别的节点发起投票成为新term的Leader，此时原先的老Leader节点会切换为Follower。Candidate在等待其它节点投票的过程中如果发现别的节点已经竞选成功成为Leader了，也会切换为Follower节点。

    ![](http://cdn3.infoqstatic.com/statics_s1_20170221-0307u1/resource/articles/etcd-interpretation-application-scenario-implement-principle/zh/resources/0129013.jpg)

    **Raft状态机**

* **如何保证最短时间内竞选出Leader，防止竞选冲突？** 在Raft状态机一图中可以看到，在Candidate状态下， 有一个times out，这里的times out时间是个随机值，也就是说，每个机器成为Candidate以后，超时发起新一轮竞选的时间是各不相同的，这就会出现一个时间差。在时间差内，如果Candidate1收到的竞选信息比自己发起的竞选信息term值大（即对方为新一轮term），并且新一轮想要成为Leader的Candidate2包含了所有提交的数据，那么Candidate1就会投票给Candidate2。这样就保证了只有很小的概率会出现竞选冲突。
* **如何防止别的Candidate在遗漏部分数据的情况下发起投票成为Leader？** Raft竞选的机制中，使用随机值决定超时时间，第一个超时的节点就会提升term编号发起新一轮投票，一般情况下别的节点收到竞选通知就会投票。但是，如果发起竞选的节点在上一个term中保存的已提交数据不完整，节点就会拒绝投票给它。通过这种机制就可以防止遗漏数据的节点成为Leader。
* **Raft某个节点宕机后会如何？** 通常情况下，如果是Follower节点宕机，如果剩余可用节点数量超过半数，集群可以几乎没有影响的正常工作。如果是Leader节点宕机，那么Follower就收不到心跳而超时，发起竞选获得投票，成为新一轮term的Leader，继续为集群提供服务。**需要注意的是；etcd目前没有任何机制会自动去变化整个集群总共的节点数量**，即如果没有人为的调用API，etcd宕机后的节点仍然被计算为总节点数中，任何请求被确认需要获得的投票数都是这个总数的半数以上。

    ![](http://cdn3.infoqstatic.com/statics_s1_20170221-0307u1/resource/articles/etcd-interpretation-application-scenario-implement-principle/zh/resources/0129014.jpg)

    **节点宕机**

* **为什么Raft算法在确定可用节点数量时不需要考虑拜占庭将军问题？** 拜占庭问题中提出，允许n个节点宕机还能提供正常服务的分布式架构，需要的总节点数量为3n+1，而Raft只需要2n+1就可以了。其主要原因在于，拜占庭将军问题中存在数据欺骗的现象，而etcd中假设所有的节点都是诚实的。etcd在竞选前需要告诉别的节点自身的term编号以及前一轮term最终结束时的index值，这些数据都是准确的，其他节点可以根据这些值决定是否投票。另外，etcd严格限制Leader到Follower这样的数据流向保证数据一致不会出错。
* **用户从集群中哪个节点读写数据？** Raft为了保证数据的强一致性，所有的数据流向都是一个方向，从Leader流向Follower，也就是所有Follower的数据必须与Leader保持一致，如果不一致会被覆盖。即所有用户更新数据的请求都最先由Leader获得，然后存下来通知其他节点也存下来，等到大多数节点反馈时再把数据提交。一个已提交的数据项才是Raft真正稳定存储下来的数据项，不再被修改，最后再把提交的数据同步给其他Follower。因为每个节点都有Raft已提交数据准确的备份（最坏的情况也只是已提交数据还未完全同步），所以读的请求任意一个节点都可以处理。

_以上转自<http://www.infoq.com/cn/articles/etcd-interpretation-application-scenario-implement-principle>_

## 参考文档

- [In Search of an Understandable Consensus Algorithm (Extended Version)](https://ramcloud.stanford.edu/raft.pdf)
- [CONSENSUS: BRIDGING THEORY AND PRACTICE](https://ramcloud.stanford.edu/~ongaro/thesis.pdf)
- [Raft Understandable Distributed Consensus](http://thesecretlivesofdata.com/raft/)
- [etcd raft实现](https://github.com/coreos/etcd/tree/master/raft)
- [raft publications and talks](https://raft.github.io/)
- http://www.infoq.com/cn/articles/etcd-interpretation-application-scenario-implement-principle
- http://www.cnblogs.com/bangerlee/p/5991417.html
- [Raft: The Understandable Distributed Consensus Protocol](https://speakerdeck.com/benbjohnson/raft-the-understandable-distributed-consensus-protocol)
