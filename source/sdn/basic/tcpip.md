# TCP/IP标准模型

TCP/IP模型是互联网的基础，它是一系列网络协议的总称。这些协议可以划分为四层，分别为链路层、网络层、传输层和应用层。

* 链路层：负责封装和解封装IP报文，发送和接受ARP/RARP报文等。
* 网络层：负责路由以及把分组报文发送给目标网络或主机。
* 传输层：负责对报文进行分组和重组，并以TCP或UDP协议格式封装报文。
* 应用层：负责向用户提供应用程序，比如HTTP、FTP、Telnet、DNS、SMTP等。

在网络体系结构中网络通信的建立必须是在通信双方的对等层进行，不能交错。 在整个数据传输过程中，数据在发送端时经过各层时都要附加上相应层的协议头和协议尾（仅数据链路层需要封装协议尾）部分，也就是要对数据进行协议封装，以标识对应层所用的通信协议。


## OSI七层模型

当然在理论上，还有一个OSI七层模型：物理层、数据链路层、网络层、传输层、会话层、表示层和应用层。这是一个理想模型，由于其复杂性并没有被大家广泛采用。

![](media/tcpip.png)

## TCP/IP详解

- [tcpip详解笔记(1) 概述](http://www.cnblogs.com/feisky/archive/2012/10/21/2732919.html)
- [tcpip详解笔记(2) 链路层](http://www.cnblogs.com/feisky/archive/2012/10/21/2732924.html)
- [tcpip详解笔记(3) IP网际协议](http://www.cnblogs.com/feisky/archive/2012/10/21/2732931.html)
- [tcpip详解笔记(4) arp协议](http://www.cnblogs.com/feisky/archive/2012/10/21/2732939.html)
- [tcpip详解笔记(5) RARP协议](http://www.cnblogs.com/feisky/archive/2012/10/21/2732947.html)
- [tcpip详解笔记(6) icmp协议](http://www.cnblogs.com/feisky/archive/2012/10/21/2732957.html)
- [tcpip详解笔记(7) ping](http://www.cnblogs.com/feisky/archive/2012/10/21/2732959.html)
- [tcpip详解笔记(8) traceroute](http://www.cnblogs.com/feisky/archive/2012/10/21/2732962.html)
- [tcpip详解笔记(9) IP选路](http://www.cnblogs.com/feisky/archive/2012/10/21/2732966.html)
- [tcpip详解笔记(10) udp协议](http://www.cnblogs.com/feisky/archive/2012/10/21/2732977.html)
- [tcpip详解笔记(11) 广播和多播](http://www.cnblogs.com/feisky/archive/2012/10/21/2732982.html)
- [tcpip详解笔记(12) DNS](http://www.cnblogs.com/feisky/archive/2012/10/21/2732985.html)
- [tcpip详解笔记(13) tftp](http://www.cnblogs.com/feisky/archive/2012/10/21/2732986.html)
- [tcpip详解笔记（14） TCP协议简介](http://www.cnblogs.com/feisky/archive/2012/10/21/2732989.html)
- [tcpip详解笔记（15） TCP协议连接过程](http://www.cnblogs.com/feisky/archive/2012/10/21/2733132.html)
- [tcpip详解笔记（16） TCP的交互数据流](http://www.cnblogs.com/feisky/archive/2012/10/21/2733175.html)
- [tcpip详解笔记（17） TCP的成块数据流](http://www.cnblogs.com/feisky/archive/2012/10/23/2735475.html)
- [tcpip详解笔记（18）TCP的超时与重传](http://www.cnblogs.com/feisky/archive/2012/10/23/2735680.html)
- [tcpip详解笔记（19） persist定时器](http://www.cnblogs.com/feisky/archive/2012/10/23/2735738.html)
- [tcpip详解笔记（20） TCP的Keepalive定时器](http://www.cnblogs.com/feisky/archive/2012/10/23/2735942.html)
- [tcpip详解笔记（21） TCP的路径MTU探测与长肥管道](http://www.cnblogs.com/feisky/archive/2012/10/24/2737633.html)
- [tcpip详解笔记（22） telnet协议](http://www.cnblogs.com/feisky/archive/2012/10/27/2742982.html)
