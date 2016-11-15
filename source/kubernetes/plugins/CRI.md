# Container Runtime Interface

Container Runtime Interface (CRI)是本人负责的一块项目，它重新定义了Kubelet Container Runtime API，将原来完全面向Pod级别的API拆分成面向Sandbox和Container的API，并分离镜像管理和容器引擎到不同的服务。

CRI最早从从1.4版就开始设计讨论和开发，预计1.5发布第一个测试版。

## 目前的CRI实现

目前，有多家厂商都在基于CRI集成自己的容器引擎，其中包括

* Docker: 核心代码依然保留在kubelet内部
* HyperContainer: https://github.com/kubernetes/frakti
* Rkt: https://github.com/kubernetes-incubator/rktlet
* Runc: https://github.com/kubernetes-incubator/ocid
* Libvirt qcow2: https://github.com/Mirantis/virtlet
