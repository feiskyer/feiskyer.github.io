---
title: Raft
date: 2016-10-21 16:11:07
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
- 2) 当收到来自集群中过半数节点的接受投票后，节点即成为 leader，开始接收保存 client 的数据并向其它的 follower 节点同步日志。
- 3) leader节点依靠定时向 follower 发送heartbeat来保持其地位。
- 4）任何时候如果其它 follower 在 election timeout 期间都没有收到来自 leader 的 heartbeat，同样会将自己的状态切换为 candidate 并发起选举。每成功选举一次，新 leader 的步进数（Term）都会比之前 leader 的步进数大1。

**日志复制**

当接Leader收到客户端的日志（事务请求）后先把该日志追加到本地的Log中，然后通过heartbeat把该Entry同步给其他Follower，Follower接收到日志后记录日志然后向Leader发送ACK，当Leader收到大多数（n/2+1）Follower的ACK信息后将该日志设置为已提交并追加到本地磁盘中，通知客户端并在下个heartbeat中Leader将通知所有的Follower将该日志存储在自己的本地磁盘中。

![](/images/14804284340920.jpg)


**安全性**

安全性是用于保证每个节点都执行相同序列的安全机制，如当某个Follower在当前Leader commit Log时变得不可用了，稍后可能该Follower又会倍选举为Leader，这时新Leader可能会用新的Log覆盖先前已committed的Log，这就是导致节点执行不同序列；Safety就是用于保证选举出来的Leader一定包含先前 commited Log的机制；

- 选举安全性（Election Safety）：每个Term只能选举出一个Leader
- Leader完整性（Leader Completeness）：指Leader日志的完整性，当Log在Term1被Commit后，那么以后Term2、Term3…等的Leader必须包含该Log；Raft在选举阶段就使用Term的判断用于保证完整性：当请求投票的该Candidate的Term较大或Term相同Index更大则投票，否则拒绝该请求。

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


**参考文档**

- [In Search of an Understandable Consensus Algorithm (Extended Version)](https://ramcloud.stanford.edu/raft.pdf)
- [CONSENSUS: BRIDGING THEORY AND PRACTICE](https://ramcloud.stanford.edu/~ongaro/thesis.pdf)
- [Raft Understandable Distributed Consensus](http://thesecretlivesofdata.com/raft/)
- [etcd raft实现](https://github.com/coreos/etcd/tree/master/raft)
- [raft publications and talks](https://raft.github.io/)
- http://www.infoq.com/cn/articles/etcd-interpretation-application-scenario-implement-principle
- http://www.cnblogs.com/bangerlee/p/5991417.html



