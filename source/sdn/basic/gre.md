# Generic Routing Encapsulation (GRE)

GRE提供了IP in IP的封装技术:

![](media/14749889550729.jpg)

步骤    | 操作/封包        | 协议       | 长度                                           | 备注            
----- | ------------ | -------- | -------------------------------------------- | ----------------        
1     | ping -s 1448 | ICMP     | 1456 = 1448 + 8 （ICMP header）                |  ICMP MSS       
2     | L3           | IP       | 1476 = 1456 + 20 （IP header）                 | GRE Tunnel MTU  
3     | L2           | Ethernet | 1490 = 1476 + 14 （Ethernet header）           | 经过 bridge 到达 GRE
4     | GRE          | IP       | 1500 = 1476 + 4 （GRE header）+ 20 （IP header） |  物理网卡 （IP）MTU   
5     | L2           | Ethernet | 1514 = 1500 + 14 （Ethernet header）           | 最大可传输帧大小        

因此，GRE 的 overhead 是 1514 - 1490 = 24 byte。

可见，使用 GRE 可以比使用 VxLAN 每次可以多传输 1448 - 1422 = 26 byte 的数据。

![](media/14749884486520.png)

由于GRE没有提供加密和防止窃听的技术，故而经常跟IPSEC一起配合实现对数据的加密传输。
