---
title: docker底层技术概览 - feisky
tags: []
date: 2014-11-19 21:11:00
---

【摘要】docker解决了云计算环境难于分发并且管理复杂，而用KVM、Xen等虚拟化又浪费系统资源的问题。Docker最初是基于lxc构建了容器引擎，为了提供跨平台支持，后又专门开发了libcontainer来抽象容器引擎。但无论是libcontainer还是lxc，其底层所依赖的内核特性都是相同的。我们来... [阅读全文](http://www.cnblogs.com/feisky/p/4105739.html)![](http://counter.cnblogs.com/blog/rss/4105739)