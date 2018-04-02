---
title: Paxos
date: 2016-10-21 16:11:07
type: page
---

# Paxos

Paxos算法是莱斯利·兰伯特于1990年提出的一种基于消息传递且具有高度容错特性的一致性算法。

**论文**

1. [The Part-Time Parliament](http://research.microsoft.com/en-us/um/people/lamport/pubs/lamport-paxos.pdf)
2. [Paxos Made Simple](http://research.microsoft.com/en-us/um/people/lamport/pubs/paxos-simple.pdf)
3. [Paxos Made Live](http://static.googleusercontent.com/media/research.google.com/zh-CN//archive/paxos_made_live.pdf)
3. [CONSENSUS: BRIDGING THEORY AND PRACTICE](https://ramcloud.stanford.edu/~ongaro/thesis.pdf)

## Paxos算法

**基本问题**

解决分布式系统中多个节点之间就某个值（提案）达成一致（决议）。

**基本假设**

- 集群中有多数派节点$(N/2+1)$存活并且他们之间的网络通信正常
- 存储是可靠的，没有数据丢失和错误
- 允许消息丢失和消息乱序

**基本原则**

安全原则---保证不能做错的事

1. 只能有一个值被批准，不能出现第二个值把第一个覆盖的情况
2. 每个节点只能学习到已经被批准的值，不能学习没有被批准的值

存活原则---只要有多数服务器存活并且彼此间可以通信最终都要做到的事

1. 最终会批准某个被提议的值
2. 一个值被批准了，其他服务器最终会学习到这个值

**4个角色**

- Proposer: 提议发起者，处理客户端请求，将客户端的请求发送到集群中，以便决定这个值是否可以被批准。
- Acceptor: 提议批准者，负责处理接收到的提议，他们的回复就是一次投票
- Learner: 不参与提议的处理，学习提议的处理结果，并相应客户端请求
- Client: 分布式系统的客户端，也不参与提议的处理

**协议内容**

```
Client   Proposer      Acceptor     Learner
   |         |          |  |  |       |  |
   X-------->|          |  |  |       |  |  Request
   |         X--------->|->|->|       |  |  Prepare(1)
   |         |<---------X--X--X       |  |  Promise(1,{Va,Vb,Vc})
   |         X--------->|->|->|       |  |  Accept!(1,Vn)
   |         |<---------X--X--X------>|->|  Accepted(1,Vn)
   |<---------------------------------X--X  Response
   |         |          |  |  |       |  |
```

1、第一阶段 Prepare

(1.1) Proposer发送Prepare: Proposer 生成全局唯一且递增的提案 ID（Proposal id，以高位时间戳 + 低位机器 IP 可以保证唯一性和递增性），向Paxos集群的所有机器发送PrepareRequest，这里无需携带提案内容，只携带 Proposal id 即可。
(1.2) Acceptor应答Prepare: Acceptor收到PrepareRequest后，做出“两个承诺，一个应答”。

两个承诺：

*第一，不再应答 Proposal id 小于等于当前请求的PrepareRequest*；
*第二，不再应答 Proposal id 小于当前请求的AcceptRequest*。

一个应答：

*返回自己已经Accept过的提案中ProposalID最大的那个提案的内容，如果没有则返回空值*;

注意：这“两个承诺”中，蕴含两个要点：**就是应答当前请求前，也要按照“两个承诺”检查是否会违背之前处理 PrepareRequest时做出的承诺；应答前要在本地持久化当前Propsal id**。

2、第二阶段 Accept

(2.1) Proposer发送Accept: Proposer收集到多数派应答的PrepareResponse后，从中选择proposal id最大的提案内容，作为要发起Accept的提案，如果这个提案为空值，则可以自己随意决定提案内容。然后携带上当前 Proposal id，向Paxos集群的所有机器发送 AccpetRequest。
(2.2) Acceptor应答Accept: Accpetor收到AccpetRequest后，检查不违背自己之前作出的“两个承诺”情况下，持久化当前 Proposal id 和提案内容。
(2.3) Proposer收集到多数派应答的AcceptResponse后，形成决议。

注意，*一条超时未形成多数派应答的提案，我们即不能认为它已形成决议，也不能认为它未形成决议。只有当你观察它（执行Paxos协议）的时候，你才能得到确定的结果。因此无论如何都对这条日志重新执行Paxos（这也是为什么在恢复的时候，我们要对每条日志都执行Paxos的原因）*。

## 错误处理

**Acceptor或者Learner失效**

这个时候不影响整个提议的处理过程，不需要任何额外恢复处理。

```
Client   Proposer      Acceptor     Learner
   |         |          |  |  |       |  |
   X-------->|          |  |  |       |  |  Request
   |         X--------->|->|->|       |  |  Prepare(1)
   |         |          |  |  !       |  |  !! FAIL !!
   |         |<---------X--X          |  |  Promise(1,{null,null})
   |         X--------->|->|          |  |  Accept!(1,V)
   |         |<---------X--X--------->|->|  Accepted(1,V)
   |<---------------------------------X--X  Response
   |         |          |  |          |  |
         (Quorum size = 2 Acceptors)
```

**Proposer失效**

Proposer在提议达成之前失效，这时另一个Proposer再次发起整个提议过程。

```
Client  Proposer        Acceptor     Learner
   |      |             |  |  |       |  |
   X----->|             |  |  |       |  |  Request
   |      X------------>|->|->|       |  |  Prepare(1)
   |      |<------------X--X--X       |  |  Promise(1,{null, null, null})
   |      |             |  |  |       |  |
   |      |             |  |  |       |  |  !! Leader fails during broadcast !!
   |      X------------>|  |  |       |  |  Accept!(1,Va)
   |      !             |  |  |       |  |
   |         |          |  |  |       |  |  !! NEW LEADER !!
   |         X--------->|->|->|       |  |  Prepare(2)
   |         |<---------X--X--X       |  |  Promise(2,{null, null, null})
   |         X--------->|->|->|       |  |  Accept!(2,V)
   |         |<---------X--X--X------>|->|  Accepted(2,V)
   |<---------------------------------X--X  Response
   |         |          |  |  |       |  |
```

**多个Proposers竞争**

当多个Proposers都觉得它们自己应该是leader的时候最为复杂。比如当前的leader可能失效后又恢复，而恢复之前已经有新的leader选举出来了，这个时候就有可能很难达成一致（这时Latency会非常高，解决方法时Multi Paxos）：

```
Client   Proposer        Acceptor     Learner
   |      |             |  |  |       |  |
   X----->|             |  |  |       |  |  Request
   |      X------------>|->|->|       |  |  Prepare(1)
   |      |<------------X--X--X       |  |  Promise(1,{null,null,null})
   |      !             |  |  |       |  |  !! LEADER FAILS
   |         |          |  |  |       |  |  !! NEW LEADER (knows last number was 1)
   |         X--------->|->|->|       |  |  Prepare(2)
   |         |<---------X--X--X       |  |  Promise(2,{null,null,null})
   |      |  |          |  |  |       |  |  !! OLD LEADER recovers
   |      |  |          |  |  |       |  |  !! OLD LEADER tries 2, denied
   |      X------------>|->|->|       |  |  Prepare(2)
   |      |<------------X--X--X       |  |  Nack(2)
   |      |  |          |  |  |       |  |  !! OLD LEADER tries 3
   |      X------------>|->|->|       |  |  Prepare(3)
   |      |<------------X--X--X       |  |  Promise(3,{null,null,null})
   |      |  |          |  |  |       |  |  !! NEW LEADER proposes, denied
   |      |  X--------->|->|->|       |  |  Accept!(2,Va)
   |      |  |<---------X--X--X       |  |  Nack(3)
   |      |  |          |  |  |       |  |  !! NEW LEADER tries 4
   |      |  X--------->|->|->|       |  |  Prepare(4)
   |      |  |<---------X--X--X       |  |  Promise(4,{null,null,null})
   |      |  |          |  |  |       |  |  !! OLD LEADER proposes, denied
   |      X------------>|->|->|       |  |  Accept!(3,Vb)
   |      |<------------X--X--X       |  |  Nack(4)
   |      |  |          |  |  |       |  |  ... and so on ...
```

## Multi Paxos

朴素Paxos算法的Latency很高，Multi-Paxos通过改变Promised的生效范围至全局的Instance（收到来自其他节点的Accept，则进行一段时间的拒绝提交请求），从而使得一些唯一节点的连续提交获得去Prepare的效果。这将原来2-Phase过程简化为了1-Phase，从而加快了提交速度。

Multi Paxos一边先运行一次完整的paxos算法选举出leader，有leader处理所有的读写请求，然后省略掉prepare过程：

```
Client   Proposer      Acceptor     Learner
   |         |          |  |  |       |  | --- First Request ---
   X-------->|          |  |  |       |  |  Request
   |         X--------->|->|->|       |  |  Prepare(N)
   |         |<---------X--X--X       |  |  Promise(N,I,{Va,Vb,Vc})
   |         X--------->|->|->|       |  |  Accept!(N,I,Vm)
   |         |<---------X--X--X------>|->|  Accepted(N,I,Vm)
   |<---------------------------------X--X  Response
   |         |          |  |  |       |  |
```

Multi Paxos要求在各个Proposer中有唯一的Leader，并由这个Leader唯一地提交value给各Acceptor进行表决，在系统中仅有一个Leader进行value提交的情况下，Prepare的过程就可以被跳过：

```
Client   Proposer       Acceptor     Learner
   |         |          |  |  |       |  |  --- Following Requests ---
   X-------->|          |  |  |       |  |  Request
   |         X--------->|->|->|       |  |  Accept!(N,I+1,W)
   |         |<---------X--X--X------>|->|  Accepted(N,I+1,W)
   |<---------------------------------X--X  Response
   |         |          |  |  |       |  |
```

## Fast Paxos

## Cheap Paxos

## Fast Paxos

## 与raft对比

从上面的描述中可以看出basic-paxos无法和raft进行比较，一次basic-paxos的过程只相当于同步raft算法中的一个日志项的过程。multi-paxos和raft的流程才是相似的。根据我上面的描述可以看出，raft算法其实是对multi-paxos的流程做了更加严格的限制：

raft中发送的请求（日志项）必须是连续的,而paxos中使可以并发的（就是说paxos可以同时发送日志项2,3，3不需要等待2处理完才能发送，但在状态集中日志顺序还是不变的，有点类似于TCP中的数据发送）
raft选主是有限制的, 必须有最新，最全的日志节点才可以当选. 而multi-paxos中是随意的。所以raft 可以看成是简化版本的multi-paxos(这里multi-paxos因为允许并发的写日志,因此不存在一个最新，最全的日志节点，因此只能这么做。这样带来的麻烦就是选主以后, 需要将主里面没有的日志给补全, 并执行commit 过程)
根据上面可以看出，raft更加的简单，paxos支持日志并发，更加的灵活。

## 主要应用

* Zookeeper
* Chubby
* [Wechat](https://github.com/tencent-wechat/phxpaxos)

Paxos的应用简明来讲就是由算法确定一个操作系列，通过编写这些操作系列的callback（也就是状态机的状态转移函数），使得节点进行相同顺序的callback，从而保证各个节点的状态一致。

![](/images/14803289545403.jpg)

**参考文档**

- [Paxos Made Simple](http://research.microsoft.com/en-us/um/people/lamport/pubs/paxos-simple.pdf)
- [CONSENSUS: BRIDGING THEORY AND PRACTICE](https://ramcloud.stanford.edu/~ongaro/thesis.pdf)
- [Wikipedia](https://en.wikipedia.org/wiki/Paxos_(computer_science))
- [分布式系统的事务处理](http://coolshell.cn/articles/10910.html)
- [一步一步理解Paxos算法](http://mp.weixin.qq.com/s?__biz=MjM5MDg2NjIyMA==&mid=203607654&idx=1&sn=bfe71374fbca7ec5adf31bd3500ab95a&key=8ea74966bf01cfb6684dc066454e04bb5194d780db67f87b55480b52800238c2dfae323218ee8645f0c094e607ea7e6f&ascene=1&uin=MjA1MDk3Njk1&devicetype=webwx&version=70000001&pass_ticket=2ivcW%2FcENyzkz%2FGjIaPDdMzzf%2Bberd36%2FR3FYecikmo%3D)
- [浅谈basic-paxos,multi-paxos和raft](http://lemon0910.github.io/2016/05/06/paxos-raft/)
