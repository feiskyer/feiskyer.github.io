---
title: Setup hyperd with flannel network
date: 2016-07-19 15:58:26
tags: [flannel, hyper, container]
---

[TOC]

# Flannel

Flannel is a virtual network that gives a subnet to each host for use with container runtimes.

Platforms like Google's Kubernetes assume that each container (pod) has a unique, routable IP inside the cluster. The advantage of this model is that it reduces the complexity of doing port mapping.

flannel runs an agent, flanneld, on each host and is responsible for allocating a subnet lease out of a preconfigured address space. flannel uses etcd to store the network configuration, allocated subnets, and auxiliary data (such as host's IP). The forwarding of packets is achieved using one of several strategies that are known as backends. The simplest backend is udp and uses a TUN device to encapsulate every IP fragment in a UDP packet, forming an overlay network. The following diagram demonstrates the path a packet takes as it traverses the overlay network:

![](/images/14689151388980.jpg)

# Flannel install

First install etcd:

```sh
curl -L https://github.com/coreos/etcd/releases/download/v3.0.3/etcd-v3.0.3-linux-amd64.tar.gz -o etcd-v3.0.3-linux-amd64.tar.gz
tar xzvf etcd-v3.0.3-linux-amd64.tar.gz
cp etcd-v3.0.3-linux-amd64/{etcd,etcdctl} /usr/bin
rm -rf etcd-v3.0.3-linux-amd64 etcd-v3.0.3-linux-amd64.tar.gz
```

Then, install flannel:

```sh
curl -L https://github.com/coreos/flannel/releases/download/v0.5.5/flannel-0.5.5-linux-amd64.tar.gz -o flannel-0.5.5-linux-amd64.tar.gz
tar zxvf flannel-0.5.5-linux-amd64.tar.gz
cp flannel-0.5.5/flanneld /usr/bin
rm -rf flannel-0.5.5*
```

Start etcd and setup default network:

```sh
nohup etcd --advertise-client-urls 'http://192.168.33.10:2379' --listen-client-urls 'http://192.168.33.10:2379' &
etcdctl --endpoints=192.168.33.10:2379 set /coreos.com/network/config  '{ "Network": "172.168.0.0/16", "Backend": { "Type": "vxlan", "VNI": 2000 } }'
```

Start flanneld on all nodes:

```sh
nohup flanneld -etcd-endpoints=http://192.168.33.10:2379 -iface=eth1 &
```

# Hyperd install

```sh
apt-get install qemu-system-x86 -y
curl -sSL http://hypercontainer.io/install | bash
```

Configure hyperd to use subnet provided by flannel：

```sh
source /run/flannel/subnet.env
brctl addbr docker0
ip addr add dev docker0 ${FLANNEL_SUBNET}
ip link set docker0 up

cat >/etc/hyper/config <<EOF
Kernel=/var/lib/hyper/kernel
Initrd=/var/lib/hyper/hyper-initrd.img
Hypervisor=qemu
StorageDriver=devicemapper
Bridge=docker0
BridgeIP=${FLANNEL_SUBNET}
EOF

nohup hyperd --nondaemon --v=3 &
```

# Test

```sh
root@s2:~# hyper run -d busybox
POD id is pod-hZviZLulsb
Time to run a POD is 3648 ms
root@s2:~# hyper exec pod-hZviZLulsb ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast qlen 1000
    link/ether 52:54:51:e5:db:2f brd ff:ff:ff:ff:ff:ff
    inet 172.168.12.3/24 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::5054:51ff:fee5:db2f/64 scope link
       valid_lft forever preferred_lft forever

root@s1:~# hyper run -d busybox
POD id is pod-GbccOdYKjK
Time to run a POD is 3631 ms
root@s1:~# hyper exec pod-GbccOdYKjK ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast qlen 1000
    link/ether 52:54:da:0c:b6:cd brd ff:ff:ff:ff:ff:ff
    inet 172.168.95.3/24 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::5054:daff:fe0c:b6cd/64 scope link
       valid_lft forever preferred_lft forever
root@s1:~# hyper exec pod-GbccOdYKjK ping -c3 172.168.12.3
PING 172.168.12.3 (172.168.12.3): 56 data bytes
64 bytes from 172.168.12.3: seq=0 ttl=62 time=57.400 ms
64 bytes from 172.168.12.3: seq=1 ttl=62 time=6.563 ms
64 bytes from 172.168.12.3: seq=2 ttl=62 time=1.580 ms

--- 172.168.12.3 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 1.580/21.847/57.400 ms
```

# Reference

* <https://github.com/coreos/flannel>
* <http://docs.hypercontainer.io/get_started/install/linux.html>


