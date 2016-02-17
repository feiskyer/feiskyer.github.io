---
layout: post
title: "How enable OpenStack allinone vm to access external network"
description: ""
category: 
tags: [OpenStack]
---

首先需要为OpenStack添加一个公网网络，假设All-in-one环境建的公网网段为10.10.10.0/24，公网网关为10.10.10.1。这样为虚拟机绑定公网IP后，由于网关是不存在的，虚拟机无法访问外网。那虚拟机如果想访问外网怎么办呢？

```
#添加FAKE公网网关
ovs-vsctl add-port br-ex gwp -- set interface gwp type=internal
ifconfig gwp 10.10.10.1 netmask 255.255.255.0
#添加SNAT规则允许虚拟机访问外网 
iptables -t nat -A POSTROUTING -s 10.10.10.0/24 -j MASQUERADE
#允许转发，添加允许转发或者删除默认的REJECT规则都可以
#iptables -D FORWARD -j REJECT --reject-with icmp-host-prohibited
iptables -t filter -I FORWARD -j ACCEPT

#开启内核转发
sysctl -w net.ipv4.conf.eth0.rp_filter=0
sysctl -w net.ipv4.conf.gwp.rp_filter=0
sysctl -w net.ipv4.ip_forward=1
```

如果想从外部访问虚拟机的话，可以通过类似的方法将虚拟机的22端口映射到主机的eth0上来：

```
#假设eth0的ip地址为192.168.33.22
iptables -t nat -I OUTPUT -d 192.168.33.22/32 -p tcp -m tcp --dport 2222 -j DNAT --to-destination 10.10.10.5:22
iptables -t nat -I FORWORD ! -i enp1s0f0 ! -o enp1s0f0 -m conntrack ! --ctstate DNAT -j ACCEPT
iptables -t nat -I PREROUTING -d 192.168.33.22/32 -p tcp -m tcp --dport 2222 -j DNAT --to-destination 10.10.10.5:22

#iptables -t nat -I POSTROUTING -s 10.10.10.5/32 -p tcp -m tcp --sport 2222 -j SNAT --to-source 192.168.33.22:22
#iptables -t nat -I POSTROUTING -s 10.10.10.0/24 -j SNAT --to-source 192.168.33.22
```
