---
layout: post
title: "Apache的Mesos和Google的Kubernetes 有什么区别"
description: ""
category: 
tags: [docker, mesos]
---

Kubernetes是一个开源项目，它把谷歌的集群管理工具引入到虚拟机和裸机场景中。它可以完美运行在现代的操作系统环境（比如CoreOS和Red Hat Atomic），并提供可以被你管控的轻量级的计算节点。Kubernetes使用Golang开发，具有轻量化、模块化、便携以及可扩展的特点。我们（Kubernetes开发团队）正在和一些不同的技术公司（包括维护着Mesos项目的MesoSphere）合作来把Kubernetes升级为一种与计算集群交互的标准方式。Kubernetes重新实现了Google在构建集群应用时积累的经验。这些概念包括如下内容：  

* Pods：一种将容器组织在一起的方法；
* Replication Controllers：一种控制容器生命周期的方法（译者注：Replication Controller确保任何时候Kubernetes集群中有指定数量的pod副本(replicas)在运行）；
* Labels：一种可以找到和查询容器的方法；
* Services：一个用于实现某一特定功能的容器组；  

因此，只要使用Kubernetes你就能够简单并快速的启动、移植并扩展集群。在这种情况下，集群就像是类似虚拟机一样灵活的资源，它是一个逻辑运算单元。打开它，使用它，调整它的大小，然后关闭它，就是这么快，就是这么简单。  

Mesos和Kubernetes的愿景差不多，但是它们在不同的生命周期中各有不同的优势。Mesos是分布式系统内核，它可以将不同的机器整合在一个逻辑计算机上面。当你拥有很多的物理资源并想构建一个巨大的静态的计算集群的时候，Mesos就派上用场了。有很多的现代化可扩展性的数据处理应用都可以在Mesos上运行，包括Hadoop、Kafka、Spark等，同时你可以通过容器技术将所有的数据处理应用都运行在一个基础的资源池中。在某个方面来看，Mesos是一个比Kubernetes更加重量级的项目，但是得益于那些像Mesosphere一样的贡献者，Mesos正在变得更加简单并且容易管理。  

有趣的是Mesos正在接受Kubernetes的理念，并已经开始支持Kubernetes API。因此如果你需要它们的话，它将是对你的Kubernetes应用去获得更多能力的一个便捷方式（比如高可用的主干、更加高级的调度命令、去管控很大数目结点的能力），同时能够很好的适用于产品级工作环境中（毕竟Kubernetes仍然还是一个初始版本）。  

当被问到区别的时候，我会这样回答：  

1.    
    如果你是一个集群世界的新手，那Kubernetes是一个很棒的开始。它可以用最快的、最简单的、最轻量级的方式来解决你的问题，并帮助你进行面向集群的开发。它提供了一个高水平的可移植方案，因为很多厂商已经开始支持Kubernetes，例如微软、IBM、Red Hat、CoreOS、MesoSphere、VMWare等。
2.    
    如果你拥有已经存在的工作任务（Hadoop、Spark、Kafka等），那Mesos可以给你提供了一个将不同工作任务相互交错的框架，然后还可以加入一些新的东西，比如Kubernetes应用。
3.    
    如果你想使用的功能Kuberntes还没实现，那Mesos是一个不错的替代品，毕竟它已经成熟。  

**原文链接：[Whats the difference between Apaches Mesos and Googles Kubernetes](http://stackoverflow.com/questions/26705201/whats-the-difference-between-apaches-mesos-and-googles-kubernetes) （翻译：刘凯宁 校对：李颖杰）**
