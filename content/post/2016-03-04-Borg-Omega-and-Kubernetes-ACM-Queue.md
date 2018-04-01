---
title: 'Borg, Omega, and Kubernetes (ACM Queue)'
date: 2016-03-04 15:46:28
tags: [kubernetes, borg]
---

Brendan Burns, Brian Grant等在[Borg, Omega, and Kubernetes - Lessons learned from three container-management systems over a decade](http://queue.acm.org/detail.cfm?id=2898444)分享了Google在容器管理的经验教训。

在谷歌的历史上，开发了三种容器管理调度系统：

- Borg：管理both long-running services and batch jobs，它们以前是由两个不同系统来管理的，分别是Babysitter和the Global Work Queue；而Borg基于Linux container开发，提高了资源的利用率，并衍生了大量的上层的配置管理工具。
- Omega：Borg的后代，集群状态维护在 a centralized Paxos-based transaction-oriented store中，并且using optimistic concurrency control to handle the occasional conflicts，去除了单master的问题
- Kubernetes：开源的容器调度系统，design goal is to make it easy to deploy and manage complex distributed systems, while still benefiting from the improved utilization that containers enable.

论文全文见[Borg, Omega, and Kubernetes](/assets/Borg-Omega-and-Kubernetes.pdf).
