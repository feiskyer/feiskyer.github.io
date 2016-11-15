# Kubernetes架构

Kubernetes最初源于谷歌内部的Borg[1]，提供了面向应用的集群管理系统

## Borg简介

Borg[2]是谷歌内部的大规模集群管理系统，负责对谷歌内部很多核心服务的调度和管理。Borg的目的是让用户能够不必操心资源管理的问题，让他们专注于自己的核心业务，并且做到跨多个数据中心的资源利用率最大化。

Borg主要由BorgMaster、Borglet、borgcfg和Scheduler组成，如下图所示

![borg](media/borg.png)

* BorgMaster是整个集群的大脑，负责维护整个集群的状态，并将数据持久化到Paxos存储中；
* Scheduer负责任务的调度，根据应用的特点将其调度到具体的机器上去；
* Borglet负责真正运行任务（在容器中）；
* borgcfg是Borg的命令行工具，用于跟Borg系统交互，一般通过一个配置文件来提交任务。

## Kubernetes架构

Kubernetes借鉴了Borg的设计理念，比如Pod、Service、Labels和单Pod单IP等。Kubernetes的整体架构跟Borg非常像，如下图所示

![architecture](media/architecture.png)

Kubernetes主要由以下几个组件组成： 

- etcd保存了整个集群的状态；
- apiserver提供了资源操作的唯一入口，并提供认证、授权等机制；
- controller manager负责维护集群的状态，比如故障检测、自动扩展、滚动更新等；
- scheduler负责资源的调度，按照预定的调度策略将Pod调度到相应的机器上；
- kubelet负责维护容器的生命周期，同时也负责Volume和网络的管理；
- kube-proxy负责为Service提供cluster内部的负载均衡；
- kube-dns负责为整个集群提供DNS服务。

![](/images/14791969222306.png)

![](/images/14791969311297.png)


[1] http://queue.acm.org/detail.cfm?id=2898444
[2] http://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/43438.pdf
[3] http://thenewstack.io/kubernetes-an-overview

