---
layout: post
title: "Stateless Floating IPs"
description: ""
category: Networking
tags: []
---

Neutron里面的Floating IPs目前是基于iptables NAT来实现的，它使用ip_conntrack来跟踪所有连接（五元组），而ip_conntrack会大大降低NAT的性能，并且也有一些安全问题（比如[conntrack未释放问题](https://review.openstack.org/#/c/124375/)）。从Floating IPs的作用来看，它只需要完成源目的IP地址的转换即可，完全可以不需要conntrack，因而就有了一个[Stateless Floating IPs](https://blueprints.launchpad.net/neutron/+spec/stateless-floatingips)的BP, 

Stateless Floating IPs的大致实现方法是使用iptables将特定的包跳过conntrack，然后再用tc执行源目的地址的转换：

```
iptables -t raw -A PREROUTING -d 212.201.100.135/32 -j NOTRACK
iptables -t raw -A PREROUTING -s 199.181.132.25/32 -j NOTRACK

###### ingress
# to do once
tc qdisc add dev qg-xxxx ingress handle ffff:
# to do for each floating-ip,fixed-ip tuple
tc filter add dev qg-xxxx parent ffff: protocol ip prio 10 u32 match ip dst 212.201.100.135/32 action nat ingress 212.201.100.135/32 199.181.132.250

###### egress
# to do once
tc qdisc add dev qg-xxxx root handle 10: htb
# to do for each floating-ip,fixed-ip tuple
tc filter add dev qg-xxxx parent 10: protocol ip prio 10 u32 match ip src 199.181.132.25/32 action nat egress 199.181.132.250/32 212.201.100.135
```

当然，这种方法也还是有很多限制的：

> stateless NAT always rewrites egress packets;
> an external machine sending packets to the fixed-ip of a natted vm/port will
> receive packets with the floating-ip as source ip.  So external machines must
> use floating-ips of natted vms/ports.
>
> There is a shared SNAT feature of neutron routers for ports which do not have
> an associated floating ip.  This shared SNAT will still use conntrack (i.e. it
> will still use the iptables nat table with SNAT and DNAT targets).  It is
> necessary to demultiplex return traffic back to the various ports using it.


对于较老的内核，还可以使用下面的方法来实现stateless nat：

The kernel once had stateless nat built in to the routing rules feature [#]_.
This was removed (or deprecated) long ago and so it is not viable::

    --> ip rule add nat 205.254.211.17 from 192.168.100.17
         Warning: route NAT is deprecated

    --> ip route add nat 205.254.211.17 via 192.168.100.17
        RTNETLINK answers: Invalid argument

<http://linux-ip.net/html/nat-stateless.html>

The Xtables-addons project [#]_ had an implementation for performing stateless
NAT in the iptables raw table::

    -t raw -A PREROUTING -i lan0 -d 212.201.100.135 -j RAWDNAT --to-destination 199.181.132.250
    -t rawpost -A POSTROUTING -o lan0 -s 199.181.132.250 -j RAWSNAT --to-source 212.201.100.135

But RAWSNAT/RAWDNAT were removed in recent xtable-addons (for kernel >= 3.13)
because the feature was unmaintained.
