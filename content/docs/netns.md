---
title: "net-ns"
type: page
---

### 简介

在Linux协议栈中引入网络命名空间，是为了支持网络协议栈的多个实例，而这些协议栈的隔离就是由命名空间来实现的(有点像进程的线性地址空间，协议栈不能访问其他协议栈的私有数据)。需要纳入命名空间的元素包括进程，套接字，网络设备。进程创建的套接字必须属于某个命名空间，套接字的操作也必须在命名空间内进行，网络设备也必须属于某个命名空间，但可能会改变，因为网络设备属于公共资源.

### 创建命名空间

    root@precise32:~# ip netns list
    root@precise32:~# ip netns add blue
    root@precise32:~# ip netns list
    blue

### 加入虚拟网卡

    Creating the network namespace is only the beginning; the next part is to assign interfaces to the namespaces, and then configure those interfaces for network connectivity. One thing that threw me off early in my exploration of network namespaces was that you couldn’t assign physical interfaces to a namespace. How in the world were you supposed to use them, then?

    It turns out you can only assign virtual Ethernet (veth) interfaces to a network namespace. Virtual Ethernet interfaces are an interesting construct; they always come in pairs, and they are connected like a tube—whatever comes in one veth interface will come out the other peer veth interface. As a result, you can use veth interfaces to connect a network namespace to the outside world via the “default” or “global” namespace where physical interfaces exist.

创建虚拟网卡对

    root@precise32:~# ip link add veth0 type veth peer name veth1
    root@precise32:~# ip link list
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue state UNKNOWN
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        link/ether 08:00:27:12:96:98 brd ff:ff:ff:ff:ff:ff
    5: veth1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN qlen 1000
        link/ether 22:16:92:b3:1b:d2 brd ff:ff:ff:ff:ff:ff
    6: veth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN qlen 1000
        link/ether 32:36:54:0b:ce:dd brd ff:ff:ff:ff:ff:ff

将其中一个虚拟网卡veth1加入命名空间\`blue·中，加入后veth1会在默认网络命名空间中消失，只能在blue命名空间中看到它：

    root@precise32:~# ip link set veth1 netns blue
    root@precise32:~# ip link list
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue state UNKNOWN
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        link/ether 08:00:27:12:96:98 brd ff:ff:ff:ff:ff:ff
    6: veth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN qlen 1000
        link/ether 32:36:54:0b:ce:dd brd ff:ff:ff:ff:ff:ff
    root@precise32:~# ip netns exec blue ip link list
    4: lo: <LOOPBACK> mtu 16436 qdisc noop state DOWN
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    5: veth1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN qlen 1000
        link/ether 22:16:92:b3:1b:d2 brd ff:ff:ff:ff:ff:ff

### 配置并启动虚拟网卡 {#_4}

    root@precise32:~# ifconfig veth0 10.0.2.16/24 up
    root@precise32:~# ip netns exec blue ifconfig veth1 10.0.2.100 up
    root@precise32:~# ip netns exec blue ifconfig
    lo        Link encap:Local Loopback
              inet addr:127.0.0.1  Mask:255.0.0.0
              inet6 addr: ::1/128 Scope:Host
              UP LOOPBACK RUNNING  MTU:16436  Metric:1
              RX packets:0 errors:0 dropped:0 overruns:0 frame:0
              TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:0
              RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

    veth1     Link encap:Ethernet  HWaddr d6:e8:04:c4:54:94
              inet addr:10.0.2.100  Bcast:10.255.255.255  Mask:255.0.0.0
              inet6 addr: fe80::d4e8:4ff:fec4:5494/64 Scope:Link
              UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
              RX packets:17 errors:0 dropped:0 overruns:0 frame:0
              TX packets:10 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:1000
              RX bytes:1258 (1.2 KB)  TX bytes:748 (748.0 B)

上面启动了虚拟网卡后，就可以和主机之间的ip通信了：

    root@precise32:~# ping 10.0.2.100
    PING 10.0.2.100 (10.0.2.100) 56(84) bytes of data.
    64 bytes from 10.0.2.100: icmp_req=1 ttl=64 time=1.63 ms
    64 bytes from 10.0.2.100: icmp_req=2 ttl=64 time=0.311 ms
    ^C
    --- 10.0.2.100 ping statistics ---
    2 packets transmitted, 2 received, 0% packet loss, time 1002ms
    rtt min/avg/max/mdev = 0.311/0.970/1.630/0.660 ms
    root@precise32:~# ip netns exec blue ping 10.0.2.15
    PING 10.0.2.15 (10.0.2.15) 56(84) bytes of data.
    64 bytes from 10.0.2.15: icmp_req=1 ttl=64 time=1.52 ms
    64 bytes from 10.0.2.15: icmp_req=2 ttl=64 time=0.427 ms
    ^C
    --- 10.0.2.15 ping statistics ---
    2 packets transmitted, 2 received, 0% packet loss, time 1001ms
    rtt min/avg/max/mdev = 0.427/0.974/1.521/0.547 ms

### 安装Open vSwitch {#open-vswitch}

    # apt-get install openvswitch-controller openvswitch-brcompat openvswitch-switch openvswitch-datapath-source
    # sed -i 's/# BRCOMPAT=no/BRCOMPAT=yes/g' /etc/default/openvswitch-switch
    # module-assistant auto-install openvswitch-datapath
    # service openvswitch-switch start
    # service openvswitch-switch status
    # lsmod | grep brcom
    brcompat               13229  0
    openvswitch            72964  1 brcompat
    # ovs-vsctl show

    # 修改默认网络配置
    root@precise32:~# cat /etc/network/interfaces
    # This file describes the network interfaces available on your system
    # and how to activate them. For more information, see interfaces(5).

    # The loopback network interface
    auto lo
    iface lo inet loopback

    auto br0
    iface br0 inet dhcp
    dns-nameservers 8.8.8.8
    bridge_ports eth0
    bridge_hello 2
    bridge_maxage 12
    bridge_stp off

    # The primary network interface
    auto eth0
    iface eth0 inet manual
    up ifconfig $IFACE 0.0.0.0 up
    down ifconfig $IFACE down

    # 创建网桥
    root@precise32:~# ovs-vsctl add-br br0

    root@precise32:~# ovs-vsctl show
    20ccb33b-8544-4778-97d6-bac3be70a1ca
        Bridge "br0"
            Port "br0"
                Interface "br0"
                    type: internal
            Port "eth0"
                Interface "eth0"
        ovs_version: "1.4.6"

### 两个命名空间之间通信 {#_5}

再创建一个命名空间red：

    ip netns add red
    ip link add veth2 type veth peer name veth3
    ip link set veth3 netns red
    ip netns exec red ip addr add 10.0.2.101/24 dev veth3
    ovs-vsctl add-port br0 veth2
    ifconfig veth2 10.0.2.17 up
    ip netns exec red ip link set veth3 up

red内部可以ping通blue命名空间

    root@precise32:~# ip netns exec red ifconfig
    lo        Link encap:Local Loopback
              inet addr:127.0.0.1  Mask:255.0.0.0
              inet6 addr: ::1/128 Scope:Host
              UP LOOPBACK RUNNING  MTU:16436  Metric:1
              RX packets:2 errors:0 dropped:0 overruns:0 frame:0
              TX packets:2 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:0
              RX bytes:168 (168.0 B)  TX bytes:168 (168.0 B)

    veth3     Link encap:Ethernet  HWaddr 2e:a5:51:89:9d:1c
              inet addr:10.0.2.101  Bcast:10.255.255.255  Mask:255.0.0.0
              inet6 addr: fe80::2ca5:51ff:fe89:9d1c/64 Scope:Link
              UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
              RX packets:36 errors:0 dropped:0 overruns:0 frame:0
              TX packets:11 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:1000
              RX bytes:1896 (1.8 KB)  TX bytes:846 (846.0 B)

    root@precise32:~# ip netns exec red ping 10.0.2.100
    PING 10.0.2.100 (10.0.2.100) 56(84) bytes of data.
    64 bytes from 10.0.2.100: icmp_req=1 ttl=64 time=1.29 ms
    64 bytes from 10.0.2.100: icmp_req=2 ttl=64 time=0.483 ms
    ^C
    --- 10.0.2.100 ping statistics ---
    2 packets transmitted, 2 received, 0% packet loss, time 1004ms
    rtt min/avg/max/mdev = 0.483/0.887/1.291/0.404 ms

### 两个网桥之间通信 {#_6}

创建一个新的网桥，并把veth2挪到新的网桥上

    ovs-vsctl add-br br1
    ifconfig br1 10.0.2.22 up
    ovs-vsctl del-port br0 veth2
    ovs-vsctl add-port br1 veth2

    # 此时，两个网桥之间是不通的
    root@precise32:~# ip netns exec red ping 10.0.2.100
    PING 10.0.2.100 (10.0.2.100) 56(84) bytes of data.
    From 10.0.2.101 icmp_seq=1 Destination Host Unreachable
    From 10.0.2.101 icmp_seq=2 Destination Host Unreachable
    From 10.0.2.101 icmp_seq=3 Destination Host Unreachable

创建一个虚拟网卡对，用于连接两个网桥：

    root@precise32:~# ip link add veth7 type veth peer name veth8
    root@precise32:~# ovs-vsctl add-port br0 veth7
    root@precise32:~# ovs-vsctl add-port br1 veth8
    root@precise32:~# ifconfig veth8 10.0.2.182 up
    root@precise32:~# ifconfig veth7 10.0.2.181 up

然后再测试，两个命名空间的网络是通的了

    root@precise32:~# ip netns exec red ping 10.0.2.100
    PING 10.0.2.100 (10.0.2.100) 56(84) bytes of data.
    64 bytes from 10.0.2.100: icmp_req=1 ttl=64 time=4.25 ms
    64 bytes from 10.0.2.100: icmp_req=2 ttl=64 time=0.668 ms
    64 bytes from 10.0.2.100: icmp_req=3 ttl=64 time=0.658 ms

参考链接：

1
<http://blog.scottlowe.org/2013/09/04/introducing-linux-network-namespaces/>

2 <http://www.opencloudblog.com/?p=42>

3
<http://blog.scottlowe.org/2013/09/09/namespaces-vlans-open-vswitch-and-gre-tunnels/>
