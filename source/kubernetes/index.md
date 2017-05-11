---
title: "Kubernetes笔记"
layout: "post"
---

Kubernetes是谷歌开源的容器集群管理系统，是Google多年大规模容器管理技术Borg的开源版本，也是CNCF最重要的组件之一，主要功能包括：

- 基于容器的应用部署、维护和滚动升级
- 负载均衡和服务发现
- 跨机器和跨地区的集群调度
- 自动伸缩
- 无状态服务和有状态服务
- 广泛的Volume支持
- 插件机制保证扩展性

Kubernetes发展非常迅速，已经成为容器编排领域的领导者。

![](CloudNativeLandscape.jpg)

(图片来自[CNCF](https://github.com/cncf/landscape))

## 目录

- [1. Kubernetes简介](introduction/)
  - [1.1 核心概念](introduction/concepts.html)
  - [1.2 Kubernetes 101](introduction/101.html)
  - [1.3 Kubernetes 201](introduction/201.html)
  - [1.4 Kubernetes集群](introduction/cluster.html)
  - [1.5 高阶使用方法](use-guide/)
- [2. 核心原理](architecture/)
  - [2.1 设计理念](architecture/concepts.html)
  - [2.2 主要概念](architecture/objects.html)
    - [Service](architecture/Service.html)
    - [Volume](architecture/Volume.html)
    - [Deployment](architecture/deployment.html)
    - [Secret](architecture/Secret.html)
    - [StatefulSet](architecture/statefulset.html)
    - [更多...](architecture/objects.html)
  - [2.3 核心组件的工作原理](components/)
    - Etcd
    - API Server
    - Scheduler
    - Controller Manager
    - Kubelet
    - Kube Proxy
    - Kube DNS
    - hyperkube
    - Federation
    - [kubeadm](architecture/kubeadm.html)
- [3. 插件指南](plugins/)
  - [3.1 认证和授权插件](plugins/auth.html)
  - [3.2 网络插件](plugins/network.html)
  - [3.3 Volume插件](plugins/volume.html)
  - [3.4 Container Runtime Interface](plugins/CRI.html)
  - 3.5 Network Policy
  - 3.6 Ingress Controller
  - 3.7 Cloud Provider
  - 3.8 Scheduler
  - [3.9 其他](plugins/other.html)
- [4. 常用技巧](deploy)
  - [4.1 部署](deploy)
    - [单机部署](deploy/single.html)
    - [集群部署](deploy/cluster.html)
    - [kubeadm](deploy/kubeadm.html)
    - [附加组件](addons)
  - [4.2 监控](monitor/)
  - [4.3 日志](deploy/logging.html)
  - [4.4 高可用](ha/)
  - [4.5 调试](debugging/)
- [5. 开发指南](dev/)
  - [5.1 开发环境搭建](dev/index.html)
  - [5.2 单元测试和集成测试](dev/testing.html)
  - [5.3 社区贡献](dev/contribute.html)
- [6. 应用管理](apps/)
  - [6.1 Helm](apps/helm-app.html)
  - [6.2 Deis workflow](apps/deis.html)
- [7. 附录](appendix/)
  - [awesome-docker](appendix/awesome-docker.html)
  - [awesome-kubernetes](appendix/awesome-kubernetes.html)
  - [Kubernetes ecosystem](ecosystem.html)

## 链接

- [Kubernetes官方网站](https://kubernetes.io/)
- [Kubernetes文档](https://kubernetes.io/docs/home/)
- Kubernetes project metrics
  - [https://cncf.biterg.io](https://cncf.biterg.io)
  - [http://velodrome.k8s.io](http://velodrome.k8s.io)
  - [http://submit-queue.k8s.io/#/e2e](http://submit-queue.k8s.io/#/e2e)
  - [https://cloud.google.com/bigquery/public-data/github](https://cloud.google.com/bigquery/public-data/github)
