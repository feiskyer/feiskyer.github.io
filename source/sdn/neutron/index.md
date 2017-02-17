---
title: OpenStack Neutron
layout: "post"
---

## 目录

* [前言](index.html)
* [概述](intro/index.html)
* [基本概念](concept/index.html)
* [常用命令](tool/)
   * [手动创建vm网卡](tool/tap.html)
   * [监听Notifications消息](tool/notification.html)
   * [Python neutron client](tool/client.html)
   * [REST API](tool/rest.html)
* [GRE 模式](gre_mode/index.html)
   * [计算节点](gre_mode/compute_node.html)
   * [网络节点](gre_mode/network_node.html)
* [VLAN 模式](vlan_mode/index.html)
   * [计算节点](vlan_mode/compute_node.html)
   * [网络节点](vlan_mode/network_node.html)
* [VXLAN 模式](vxlan_mode/index.html)
   * [计算节点](vxlan_mode/compute_node/index.html)
       * [br-int](vxlan_mode/compute_node/br-int.html)
       * [br-tun](vxlan_mode/compute_node/br-tun.html)
   * [网络节点](vxlan_mode/network_node/index.html)
       * [br-tun](vxlan_mode/network_node/br-tun.html)
       * [br-int](vxlan_mode/network_node/br-int.html)
       * [br-ex](vxlan_mode/network_node/br-ex.html)
* [网络命名空间](namespace/index.html)
   * [DHCP 服务](namespace/dhcp.html)
   * [路由服务](namespace/router.html)
* [安全组](security_group/index.html)
   * [INPUT](security_group/input.html)
   * [OUTPUT](security_group/output.html)
   * [FORWARD](security_group/forward.html)
   * [整体逻辑](security_group/global_logic.html)
   * [快速查找安全组规则](security_group/quick_find.html)
   * [其它](security_group/other.html)
* [LBaaS（负载均衡即服务）](lbaas/index.html)
   * [典型场景](lbaas/scenario.html)
   * [实现细节](lbaas/arch.html)
   * [其它问题](lbaas/other.html)
* [FWaaS（防火墙即服务）](fwaas/index.html)
   * [典型场景](fwaas/scenario.html)
   * [实现细节](fwaas/arch.html)
   * [其它问题](fwaas/other.html)
* [DVR（分布式路由）](dvr/index.html)
   * [典型场景](dvr/scenario.html)
   * [网络节点](dvr/network_node.html)
   * [计算节点](dvr/compute_node.html)
   * [配置](dvr/config.html)
   * [工作流程](dvr/workflow.html)
   * [实现细节](dvr/implementation.html)
* [参考](ref/index.html)
   * [easyOVS](tool/easyovs.html)
   * [监听notification消息](tool/notification.html)
   * [Python Client](tool/client.html)
   * [Rest API](tool/rest.html)
   * [手动创建Tap网卡](tool/tap.html)
* [附：安装配置](appendix_install/index.html)

## 链接

- [OpenStack Networking Guide](https://docs.openstack.org/newton/networking-guide/)
- [Neutron developer guide](https://docs.openstack.org/developer/neutron/)
- [UMCloud Neutron性能与扩展性测试报告](http://mp.weixin.qq.com/s?__biz=MzAwNjgxNTY5MQ==&mid=2651153920&idx=1&sn=2c87ba7e7af607315a1383be64778a35&chksm=80f66ca4b781e5b234523512e7fb631e18163a683a6b65d58bdc46f776af74a2577daa99dc8c&mpshare=1&scene=1&srcid=0215U0PpXs7khAvyW925ljJH#rd)
- [OpenStack Architecture Design Guide](https://docs.openstack.org/arch-design/)

---

备注: _基于[yeasy/openstack_understand_Neutron](https://github.com/yeasy/openstack_understand_Neutron)修改。_


