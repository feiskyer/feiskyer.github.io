---
title: SwarmKit
type: page
date: 2016-10-13 22:47:27
---

# SwarmKit

SwarmKit是随着docker 1.12发布的集群管理系统，并内置在docker daemon中，主要提供以下的功能：

- 容器调度、健康检查和滚动升级
- 服务发现和自动负载均衡
- 基于Raft协议的分布式存储
- 集成overlay网络
- TLS管理和加密通信
- 节点管理

配合SwarmKit的发布，docker也新增了`docker swarm`、`docker node`和`docker service`命令来提供上述的功能（即swarm mode），其使用方法可以参考[这里](http://feisky.xyz/2016/06/24/Play-with-docker-v1-12/)。

## 整体架构

![](/images/14773867932879.jpg)

## 服务发现

![](/images/14773925013757.jpg)


## 网络

每个service中的容器都会加入三个网络：

- Ingress: Ingress将服务开放的端口映射到每台机器的30000-32000直接的端口上，并通过ipvs将service vip负载均衡到后端的多个容器.
- docker_gwbridge: 为容器提供外网的访问通道.
- user-defined overlay network: 即用户创建的overlay网络，比如`docker network create -d overlay mynet`.

```sh
# docker exec c2e7fa656ce9 ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
11: eth0@if12: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP group default
    link/ether 02:42:0a:ff:00:06 brd ff:ff:ff:ff:ff:ff
    inet 10.255.0.6/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet 10.255.0.4/32 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:aff:feff:6/64 scope link
       valid_lft forever preferred_lft forever
13: eth1@if14: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:ac:12:00:03 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.3/16 scope global eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::42:acff:fe12:3/64 scope link
       valid_lft forever preferred_lft forever
16: eth2@if17: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP group default
    link/ether 02:42:0a:00:00:04 brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.4/24 scope global eth2
       valid_lft forever preferred_lft forever
    inet 10.0.0.2/32 scope global eth2
       valid_lft forever preferred_lft forever
    inet6 fe80::42:aff:fe00:4/64 scope link
       valid_lft forever preferred_lft forever
```

该容器内多个网卡跟其他部分的连接关系为：

![](/images/14773987193442.jpg)

## 负载均衡

每个Publish的Service都会开放端口到host上，并通过ingress_sbox内的ipvs负载均衡到后端容器的eth0上：

![3](/images/3-3.png)

而用户自定义网络也同样是通过ipvs复杂均衡的：

![4](/images/4-1.png)
