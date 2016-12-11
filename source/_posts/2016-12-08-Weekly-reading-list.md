---
title: Weekly reading list
date: 2016-12-08 14:00:22
category: Readings
tags:
---

# [Docker收购Infinit](https://blog.docker.com/2016/12/docker-acquires-infinit/) [PDF](/assets/infinit.pdf)

[Infinit](https://infinit.sh/)为容器提供了分布式存储，其特点包括

- 基于软件：可以部署在任何硬件之上，从遗留设备到消费级实体机、虚拟机，甚至容器。
- 可编程：开发者可以轻松地完成多个存储基础设施的自动化创建和部署，并且每个都能借助基于策略的能力进行自定义，适配上层应用的需求。
- 可伸缩：通过依靠一个去中心化的架构（即点对点），Infinit没有使用leader/follower模型，因而不会有瓶颈和单点失效的问题。
- 自愈合：Infinit的再平衡策略能让系统适应各种故障，包括拜占庭将军问题。
- 多用途：Infinit平台提供了块、对象和文件存储的接口：NFS、SMB、AWS S3、OpenStack Swift、iSCSI和FUSE等等。

![](/images/14811775178610.png)

基本原理：

• Federate all nodes in an overlay network for lookup and routing.• Store data as blocks in a distributed hashtable (key-value store) with a per-block consensus.• Use cryptographic access control to dispense from any leader.• Use symmetrical operations to ensure resilience and flexibility.

![](/images/14811780770073.jpg)

![](/images/14811782445452.jpg)

Infinit以volume的形式挂载到docker容器中：

![](/images/14811779192673.jpg)

## [Docker@Alibaba——超大规模Docker化的实战经验](https://yq.aliyun.com/articles/64256)

* AliDocker，并非阿里云，主要是阿里内部业务在用
* Swarm改造支持单swarm实例health nodes 2w+
    * 优化连接管理、最小化锁粒度、修改diff算法减少node刷新时的开销、减少连接线程
* Docker Engine增强
    * 磁盘配额、固定IP、Hooks、解决hyperd重启容器销毁问题等
* 镜像分发：流式分发、镜像分批预热、P2P等
* swarm-proxy HA

![](/images/14811788194621.jpg)7

## [微服务在微信后台的架构实践](http://ppt.geekbang.org/slide/show/607)

- 多地自治，园区互备：城市间RTT 30ms-400ms，园区间小于2ms
- RPC：protobuf/libco
- 调度：Yard，双层调度器（Mesos+Yard）
- 过载保护：轻重分离、队列式、组合命令式

![](/images/14811817178100.jpg)

- 数据存储：PaxosStore，同步复制、多主多写

![](/images/14811818656014.jpg)

## [Go:微服务架构的基石](http://ppt.geekbang.org/slide/show/615)

- 负载均衡：seesaw、caddy
- 服务网关：tyk、fabio、vulcand
- 进程间通信：RESTful、RPC、自定义
    - REST框架：beego、gin、Iris、micro、go-kit、goa
    - RPC框架：grpc、thrift、hprose
    - 自定义：协议，编解码
- 服务发现：etcd、consul、serf
- 调度系统：kubernetes、swarm、mesos
- 消息队列：NSQ、Nats
- APM（应用性能监控）：appdash、Cloudinsight、opentracing
- 配置管理：etcd、consul、mgmt
- 日志分析：Beats、Heka
- 服务监控：open-falcon、prometheus
- CI/CD：Drone
- 熔断器：gateway、Hystrix-go

## [基于万节点Kubernetes支撑大规模云应用实践](http://ppt.geekbang.org/slide/show/586)

- 基于OpenStack的IaaS：裁剪KVM镜像、优化启动流程，Openvswitch SDN、Ceph存储
- 容器与虚拟机共用一套虚拟化网络
- Ceph存储直接挂载到容器
- 统一的日志收集、分析、搜索
- Kubernetes调度器优化：将原来的串行队列改为多个优先级队列
- etcd集群扩展：将Pod/Node/ReplicationController拆分到不同的etcd集群

![](/images/14811811876614.jpg)

![](/images/14811813670269.jpg)

# [20 天持续压测，告诉你云存储性能哪家强](https://www.v2ex.com/t/326038?from=timeline&isappinstalled=0#reply7) [📈](http://www.codingpy.com/specials/cbs_test/)

对阿里云和腾讯云两种云存储产品（云盘）的性能和价格对比：

- 测试方法：SNIA发布的[企业级SSD评测规范](http://snia.org/sites/default/files/SSS_PTS_Enterprise_v1.1.pdf)及[实现](https://github.com/cloudharmony/block-storage)
- 阿里云 SSD 云盘必须搭配 I/O 优化实例才能给发挥最大性能
- 腾讯云高效云盘的读写操作可同时达到预期性能峰值（数据块 16KB 以下），而阿里云方面，读写无法同时达到预期性能峰值
- 腾讯云达到了预期的性能；阿里云部分没有达到， 400GB 容量的时延过高
- 腾讯云高效云盘的时延在 1ms 以下， IOPS 、吞吐量的优势更加突出
- 两家高效云盘的 IOPS 表现均比较稳定，几乎呈一条直线，只有阿里云的 400GB 云盘有些略微波动
- 容量越大，似乎闲置时间对性能恢复的影响越明显；阿里云 400GB 高效云盘的性能波动受闲置时间影响较明显

![](/images/14811840736214.jpg)

## [外卖的背后-饿了么基础架构从0到1的演进](http://ppt.geekbang.org/slide/show/619)

- 负载均衡
  - 最初：HAProxy部署在客户端本地，不需要考虑HAProxy的高可用；问题是部署规模大，维护客户列表复杂，并且配置不统一
  - 解决：
    - RPC+内置LB SDK，服务自注册/自发现，配置少，部署简单
    - Redis/DB解决方案GoProxy: DAL/Corvus作为服务自注册，GoProxy订阅注册事件并自带服务发现的Haproxy
    - 健康检查：心跳检测，进程在、端口活不代表服务可用
- 无损升级
  - 最初：发布前通知客户端停止请求，服务端将正在处理的请求处理完毕才能升级
  - 解决：
    - RPC调用：服务发现机制会在注销时通知客户端，直连情况下客户端从可用列表中剔除准备下线的服务
    - 数据库访问，客户端限制连接存活时间，DAL侧重连
- 基础架构：开放式架构
  - 基于组件，给业务开发团队最大的自由
  - 基于运行时，给业务开发团队最大限度的自由
  - 开放封闭原则：基础框架应该是可以扩展的，但是不可以“选择”的


