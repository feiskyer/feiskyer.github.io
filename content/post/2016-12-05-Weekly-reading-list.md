---
title: Weekly reading list
date: 2016-12-05 07:59:01
category: Readings
tags: []
---

## [分布式后台毫秒服务引擎](http://mp.weixin.qq.com/s?__biz=MjM5MDE0Mjc4MA==&mid=2650994968&idx=1&sn=6713bb3b59e1fb38c70f7178de136cfc&scene=0#wechat_redirect)

> 腾讯QQ团队于12月4日开源了一个服务开发运营框架，叫做毫秒服务引擎（Mass Service Engine in Cluster，MSEC），它集RPC、名字发现服务、负载均衡、业务监控、灰度发布、容量管理、日志管理、Key-Value存储于一体，目的是提高开发与运营的效率和质量。

![](/images/14809236732969.jpg)

![](/images/14809236897310.jpg)


* 服务发现与负载均衡
    * 集中管理每个服务（包括异构服务）的IP地址
    * 服务之间RPC调用：服务名+接口名
    * 路由的同时统计过去一段时间的成功率和时延
* 支持多种编程语言（通过Protocol buffer生成不同语言的接口），如C/C++、Java、PHP等
* Web化的管理界面(Tomcat)
* 存储：Redis cluster
* 官方网站：http://haomiao.qq.com
* Github：https://github.com/Tencent/MSEC

## [Understanding SELinux Roles](http://danwalsh.livejournal.com/75683.html)

SELinux label包含4个部分`user_u:role_r:type_t:level`，每个用户可以访问的角色：

```
semanage user -l

         Labeling   MLS/       MLS/
SELinux User    Prefix     MCS Level  MCS Range       SELinux Roles

guest_u             user       s0         s0                             guest_r
root                    user       s0         s0-s0:c0.c1023        staff_r sysadm_r system_r unconfined_r
staff_u               user       s0         s0-s0:c0.c1023        staff_r sysadm_r system_r unconfined_r
sysadm_u         user       s0         s0-s0:c0.c1023        sysadm_r
system_u          user       s0         s0-s0:c0.c1023        system_r unconfined_r
unconfined_u    user       s0         s0-s0:c0.c1023        system_r unconfined_r
user_u               user       s0         s0                             user_r
xguest_u           user       s0         s0                             xguest_r
```

* system_r role is the default role for all processes started at boot
* You can not assign an SELinux user a role that is not listed
* object_r is not really a role, but more of a place holder.  Roles only make sense for processes, not for files
* on the file system.  But the SELinux label requires a role for all labels.  object_r is the role that we use to fill the objects on disks role.  Changing a process to run as object_r or trying to assign a different role to a file will always be denied by the kernel.

## [Kompose: a tool to go from Docker-compose to Kubernetes](http://blog.kubernetes.io/2016/11/kompose-tool-go-from-docker-compose-to-kubernetes.html)

- 把docker-compose.yml或dab转换为kubernetes service+deployment
- Github: https://github.com/kubernetes-incubator/kompose

```
$ kompose --bundle docker-compose-bundle.dab convert
WARN[0000]: Unsupported key networks - ignoring
file "redis-svc.json" created
file "web-svc.json" created
file "web-deployment.json" created
file "redis-deployment.json" created

$ kompose -f docker-compose.yml convert
WARN[0000]: Unsupported key networks - ignoring
file "redis-svc.json" created
file "web-svc.json" created
file "web-deployment.json" created
file "redis-deployment.json" created
```

## [2016年网络虚拟化趋势](http://www.sdnlab.com/18153.html)

* 市场持续升温：NV的市场已经是一个数十亿美元的市场，Cisco、Juniper、Nuage、VMware是NV市场的四大巨头，他们占据了NV市场的绝大多数收入
* 思科和VMware公布的数据显示其与NV相关的投资组合在2016年将近30亿美元
* 容器化：思科收购ContainerX，VMWare推出vSphere集成容器（VIC）

![](/images/14809260496846.jpg)


## Amazon发布一大波新产品

- [Amazon Lightsail](https://amazonlightsail.com/)：廉价VPS，价格跟LightSale, DO, VULTR, Linode相同。
- [F1 instance with FPGA](https://aws.amazon.com/cn/blogs/aws/developer-preview-ec2-instances-f1-with-programmable-hardware/)：VHDL和Verilog终于有出路了
- 今年是机器学习大火的一年，Amazon也随大流（微软、Google）推出了AI服务：
    * Amazon Rekognition图像处理和分析
    * Amazon Lex自然语言处理
    * Amazon Polly文本到语音的转换
- [AWS Snowmobile](https://aws.amazon.com/cn/snowmobile/)：带宽从来都不是问题
    ![](/images/14809265679834.jpg)

## [Linux bcc/BPF tcplife](http://www.brendangregg.com/blog/2016-11-30/linux-bcc-tcplife.html)

```
# ./tcplife -D 80
PID   COMM       LADDR           LPORT RADDR           RPORT TX_KB RX_KB MS
27448 curl       100.66.11.247   54146 54.154.224.174  80        0     1 263.85
27450 curl       100.66.11.247   20618 54.154.164.22   80        0     1 243.62
27452 curl       100.66.11.247   11480 54.154.43.103   80        0     1 231.16
27454 curl       100.66.11.247   31382 54.154.15.7     80        0     1 249.95
27456 curl       100.66.11.247   33416 52.210.59.223   80        0     1 545.72
27458 curl       100.66.11.247   16406 52.30.140.35    80        0     1 222.29
27460 curl       100.66.11.247   11634 52.30.133.135   80        0     1 217.52
27462 curl       100.66.11.247   25660 52.30.126.182   80        0     1 250.81
[...]

# ./tcplife -h
usage: tcplife [-h] [-T] [-t] [-w] [-s] [-p PID] [-L LOCALPORT]
               [-D REMOTEPORT]

Trace the lifespan of TCP sessions and summarize

optional arguments:
  -h, --help            show this help message and exit
  -T, --time            include time column on output (HH:MM:SS)
  -t, --timestamp       include timestamp on output (seconds)
  -w, --wide            wide column output (fits IPv6 addresses)
  -s, --csv             comma seperated values output
  -p PID, --pid PID     trace this PID only
  -L LOCALPORT, --localport LOCALPORT
                        comma-separated list of local ports to trace.
  -D REMOTEPORT, --remoteport REMOTEPORT
                        comma-separated list of remote ports to trace.

examples:
    ./tcplife           # trace all TCP connect()s
    ./tcplife -t        # include time column (HH:MM:SS)
    ./tcplife -w        # wider colums (fit IPv6)
    ./tcplife -stT      # csv output, with times & timestamps
    ./tcplife -p 181    # only trace PID 181
    ./tcplife -L 80     # only trace local port 80
    ./tcplife -L 80,81  # only trace local ports 80 and 81
    ./tcplife -D 80     # only trace remote port 80
```

## [cgroup namespace](http://hustcat.github.io/cgroup-namespace/)

之前，在一个容器查看/proc/$PID/cgroup，或者在容器挂载cgroup时，会看到整个系统的cgroup信息；在内核从4.6开始，支持cgroup namespace （<https://lwn.net/Articles/618873/>）。

> (1)可以限制容器的cgroup filesytem视图，使得在容器中也可以安全的使用cgroup；
> (2)此外，会使容器迁移更加容易；在迁移时，/proc/self/cgroup需要复制到目标机器，这要求容器的cgroup路径是唯一的，否则可能会与目标机器冲突。有了cgroupns，每个容器都有自己的cgroup filesystem视图，不用担心这种冲突。
