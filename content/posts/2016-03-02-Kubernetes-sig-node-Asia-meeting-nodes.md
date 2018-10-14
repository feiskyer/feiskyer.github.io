---
title: Kubernetes sig-node (Asia) meeting notes
date: 2016-03-02 17:07:00
tags: [kubernetes, hyper, rkt]
---

## Kubernetes 1.2 Status Update (@dchen)

* Deployment object and HPA scale还有一些P0和P1的问题待解决
* aws还有挺多的问题（应该要超过20个）
* 整个v1.2还有超过100个issue，但大部分都不是block issue
* v1.2推荐使用Docker v1.9.1，Docker v1.10 validation <https://github.com/kubernetes/kubernetes/issues/19720>
* Docker v1.10最大的问题是镜像格式变化，需要某种转换镜像的管理机制

## Huawei Conformance Test (@liangchenye)

关于Pod运行和删除的PR已经merge，但是image的test还在开发中。主要的问题是没有文档指导rkt环境的搭建。

## Hyper integration (@feiskyer)

Hypernetes e2e test有一个单机环境的[测试结果](https://gist.github.com/feiskyer/ecb7eab17ef41f134353)，但由于GCE环境的问题，多机环境的搭建还没有完成。还有一个Hyper日志"\n"处理的bug需要修复。

## etcd

etcd计划在4月份发布v3.0 alpha，并争取kubernetes v1.3升级到etcd 3.0 stable。

## More notes taken by @lantao

Release Brain Storm

@hongchao: Over-commit? -> In 1.3 roadmap today, but not finalized.In fact we can do over-commit today, but reliablility and QoS should be guranteed.(@dchen)
Detect out of resource
Decide which pod should be killed
Well-defined eviction policy is needed.

Q&A
@dchen: Etcd v3.0 alpha version in April; stable version in May or June; Try to ship with kubernetes 1.3.

@xiang: 
New node metric api merged? Yeah.
Is the new metric api added for better scheduling? No, necessary information for scheduling is available on kubelet side from v1.0.
Hardware level metrics?

@feiskyer: Pod level data in cadvisor? At cgroup level, we could do that. But at API level, it is still in disicussion. Internally shareable resource between containers is very powerful but quite complex. If customers don’t ask for that now, we may want to defer it. @dchen: How to define extra overhide of rkt and hyper in api, should it be visible for user?
Related issue: https://github.com/coreos/rkt/issues/1788

Previous notes is recorded at <https://docs.google.com/document/d/1L8s6Nyu5hNJxCOZLqJsuVEFAScWKhbwcis0X-j-upDc/edit#heading=h.jgbd25swf99j>