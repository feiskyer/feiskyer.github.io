---
title: 从veth看虚拟网络设备的qdisc - feisky
tags: []
date: 2014-11-18 21:26:00
description: "结合一次 Docker 网络性能测试引发的 veth 问题，深入分析虚拟网络设备的 qdisc 队列机制，探讨 tx_queuelen 设置对容器网络吞吐的影响以及内核社区的讨论。"
---

【摘要】背景前段时间在测试docker的网络性能的时候，发现了一个veth的性能问题，后来给docker官方提交了一个PR，参考set tx_queuelen to 0 when create veth device，引起了一些讨论。再后来，RedHat的网络专家Jesper Brouer出来详细的讨论了一... [阅读全文](http://www.cnblogs.com/feisky/p/4105884.html)
