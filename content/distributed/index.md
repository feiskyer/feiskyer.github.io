---
title: 分布式系统
date: 2016-10-21 16:11:07
---

## 目录

- 一、分布式理论
    - 1.1 CAP
    - [1.2 一致性](consistent/)
        - 2PC/3PC
        - [Paxos](paxos/)
        - [Raft](raft/)
        - [Zab](zab/)
    - 1.3 可用性和扩展性
    - 1.4 网络分区
- 二、分布式存储系统
    - 2.1 Google - [Spanner](spanner/), GFS, [F1](F1/), Chubby, [BigTable](BigTable/), Omega, Dapper, [Datastore](Datastore/)
    - 2.2 AWS - [RDS](aws-rds/), [DynamoDB](DynamoDB/), [Aurora](aurora/)
    - 2.3 阿里云 - [阿里云RDS](aliyun-rds/), PetaData, OceanBase
    - 2.4 [TiDB](TiDB/)
    - 2.5 [CockroachDB](CockroachDB/)
    - 2.6 [Azure Cosmos DB](https://docs.microsoft.com/en-us/azure/cosmos-db/introduction)
    - 2.7 Cassandra, MongoDB, HBase
- 三、分布式通信系统
    - 3.1 消息队列
    - 3.2 [ZooKeeper](zookeeper/)
    - 3.3 [Etcd](etcd/)
    - 3.4 [Kafka](kafka/)
- 四、分布式计算系统
    - 4.1 Google: Cloud Dataflow
    - 4.2 Hadoop, Spark, Beam
    - 4.3 Kubernetes
- 五、分布式系统实践
- 六、经验教训
    - [6.1 aws s3故障回顾和教训](lessons/aws-s3-2.28/)
    - [6.2 gitlab故障回顾和教训](lessons/gitlab-1.31/)


## 资源

- [Distributed systems for fun and profit](http://book.mixu.net/distsys/)
- [Distributed Systems](https://pdos.csail.mit.edu/6.824/)
- [分布式系统资料](https://github.com/ty4z2008/Qix/blob/master/ds/)
- [阿里云、Amazon、Google 云数据库方案架构与技术分析](http://mp.weixin.qq.com/s?__biz=MjM5ODE1NDYyMA==&mid=2653381622&idx=2&sn=de2ca1807a8a15214f2154bd01bc0cdc&scene=0#wechat_redirect)
