---
title: VXLAN
layout: "post"
---

## VXLAN

Virtual eXtensible Local Area Network (VXLAN) 是一种将2层报文封装到UDP包(Mac in UDP)中进行传输的一种封装协议。VXLAN主要是由Cisco推出的，VXLAN的包头有一个24bit的ID段，即意味着1600万个独一无二的虚拟网段，这个ID通常是对UDP端口采取伪随机算法而生成的（UDP端口是由该帧中的原始MAC Hash生成的）。这样做的好处是可以保证基于5元组的负载均衡，保存VM之间数据包的顺序，具体做法是将数据包内部的MAC组映射到唯一的UDP端口组。将二层广播被转换成IP组播,VXLAN使用IP组播在虚拟网段中泛洪而且依赖于动态MAC学习。在VXLAN中，封装和解封的组件有个专有的名字叫做VTEP，VTEP之间通过组播发现对方。

![](media/14749886659589.png)
     
步骤    | 操作/封包        | 协议       | 长度                                              | MTU                                   
----- | ------------ | -------- | ----------------------------------------------- | -------------------------------------                         
1     | ping -s 1422 | ICMP     | 1430 = 1422 + 8 （ICMP header）                   |                                      
2     | L3           | IP       | 1450 = 1430 + 20 （IP header）                    | VxLAN Interface 的 MTU                
3     | L2           | Ethernet | 1464 = 1450 + 14 （Ethernet header）              |                                      
4     | VxLAN        | UDP      | 1480 = 1464 + 8 （VxLAN header） + 8 （UDP header） |                                      
5     | L3           | IP       | 1500 = 1480 + 20 （IP header）                    | 物理网卡的（IP）MTU，它不包括 Ethernet header 的长度
6     | L2           | Ethernet | 1514 = 1500 + 14 （Ethernet header）              |  最大可传输帧大小                            

因此，VxLAN 的 overhead 是1514- 1464 = 50 byte。

![](media/14749884705318.png)

## VXLAN Offload

一些新型号的网卡(Intel X540 or X710)，具备VXLAN硬件封包／解包能力。开启硬件VXLAN offload，并使用较大的MTU（如9000），可以明显提升虚拟网络的性能。

### 开启或关闭vxlan offload的方法

```
ethtool -k <eth0/eth1> tx-udp_tnl-segmentation <on/off>
```


