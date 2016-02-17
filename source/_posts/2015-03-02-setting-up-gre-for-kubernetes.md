---
layout: post
title: "Setting up GRE for Kubernetes"
description: ""
category: 
tags: [Docker]
---

首先修改Docker的默认网桥：

```
#停止Docker Daemon进程
systemctl stop docker

#设置默认网桥docker0为down，并删除
ip link set dev docker0 down
brctl delbr docker0

#新建Linux网桥localbr0
brctl addbr localbr0

#在每台主机上更改10.10.x.0/24，注意各台主机之间不要重复
ip addr add 10.10.2.1/24 dev localbr0
ip link set dev localbr0 up

echo 'OPTIONS="--bridge localbr0 --iptables=false"'>>/etc/sysconfig/docker
systemctl start Docker
```

为上述网桥添加GRE连接

```
#新建Openvswitch网桥
ovs-vsctl add-br ovsbr

#启用STP协议防止网桥环路
ovs-vsctl set bridge ovsbr stp_enable=true

#添加ovsbr到本地localbr0，使得容器流量通过OVS流经GRE Tunnel
brctl addif localbr0 ovsbr
ip link set dev ovsbr up

#创建GRE
ovs-vsctl add-port ovsbr tep0 -- set interface tep0 type=internal

#需在每个主机上修改tep0 IP地址
ip addr add 192.168.1.1/24 dev tep0
ip addr add 192.168.1.2/24 dev tep0
ip link set dev tep0 up

#使用GRE隧道连接每个主机上的Openvswitch网桥
#192.168.0.127
ovs-vsctl add-port ovsbr gre0 -- set interface gre0 type=gre options:remote_ip=192.168.0.128

#192.168.0.128
ovs-vsctl add-port ovsbr gre0 -- set interface gre0 type=gre options:remote_ip=192.168.0.127

#配置路由使得跨主机间容器的通信
ip route add 10.10.0.0/16 dev tep0

#为了使得容器访问Internet，在两台主机上配置NAT
iptables -t nat -A POSTROUTING -s 10.10.0.0/16 -o eth0 -j MASQUERADE
```

