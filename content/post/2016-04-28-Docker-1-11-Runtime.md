---
title: Container runtime in Docker v1.11
date: 2016-04-28 10:07:23
tags: [docker, runc, container]
---

Docker v1.11正式集成了runc（终于支持OCI了），并将原来的一个二进制文件拆分为多个，同时还保持docker CLI和API不变：

* docker
* docker-containerd
* docker-containerd-shim
* docker-runc
* docker-containerd-ctr

![](/images/docker-v11.png)

这么做的好处很明显：

* 最重要的可以在docker或者containerd重启的时候container还保持running
* container runtime pluggable，比如以后可以选择用runV（当然默认肯定是runc）
* 性能，新的containerd没有历史包袱，一开始就针对性能做了优化（100 containers in 1.64 seconds）
* docker daemon的角色变化，docker只需要做少量的准备工作，把真正运行容器的工作交给containerd：
	* Image management
	* Generate OCI bundle for containers
	* Mount the container’s root filesystem inside the bundle
	* Call containerd to start container

**[Containerd](https://github.com/docker/containerd)**

containerd is a daemon to control runC, built for performance and density. containerd leverages runC's advanced features such as seccomp and user namespace support as well as checkpoint and restore for cloning and live migration of containers:

![](/images/containerd.png)

**docker-containerd-ctr**

docker-containerd-ctr is the CLI for docker-containerd, which is based on gPRC APIs.

```
$ docker-containerd-ctr --address "/var/run/docker/libcontainerd/docker-containerd.sock" containers
ID                                                                 PATH                                                                                             STATUS              PROCESSES
346c1b7bbb04b760032557e1324a4027ec0055ea84dca109134c02e03dc1242c   /var/run/docker/libcontainerd/346c1b7bbb04b760032557e1324a4027ec0055ea84dca109134c02e03dc1242c   running             init
bca15f3420e3218987314e1cbbf440120ff880af44844778293c4130526c85cc   /var/run/docker/libcontainerd/bca15f3420e3218987314e1cbbf440120ff880af44844778293c4130526c85cc   running             init
$ docker-containerd-ctr --address "/var/run/docker/libcontainerd/docker-containerd.sock" containers exec --id=346c1b7bbb04b760032557e1324a4027ec0055ea84dca109134c02e03dc1242c --pid=20 --cwd=/ -a /bin/ps aux
PID   USER     TIME   COMMAND
    1 root       0:00 sh
   51 root       0:00 /bin/ps aux
$ docker-containerd-ctr --address "/var/run/docker/libcontainerd/docker-containerd.sock" state 346c1b7bbb04b760032557e1324a4027ec0055ea84dca109134c02e03dc1242c
{"containers":[{"id":"346c1b7bbb04b760032557e1324a4027ec0055ea84dca109134c02e03dc1242c","bundlePath":"/var/run/docker/libcontainerd/346c1b7bbb04b760032557e1324a4027ec0055ea84dca109134c02e03dc1242c","processes":[{"pid":"init","terminal":true,"user":{"additionalGids":[10]},"args":["sh"],"env":["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin","HOSTNAME=346c1b7bbb04","TERM=xterm"],"cwd":"/","systemPid":3716,"stdin":"/var/run/docker/libcontainerd/346c1b7bbb04b760032557e1324a4027ec0055ea84dca109134c02e03dc1242c/init-stdin","stdout":"/var/run/docker/libcontainerd/346c1b7bbb04b760032557e1324a4027ec0055ea84dca109134c02e03dc1242c/init-stdout","stderr":"/var/run/docker/libcontainerd/346c1b7bbb04b760032557e1324a4027ec0055ea84dca109134c02e03dc1242c/init-stderr","capabilities":["CAP_CHOWN","CAP_DAC_OVERRIDE","CAP_FSETID","CAP_FOWNER","CAP_MKNOD","CAP_NET_RAW","CAP_SETGID","CAP_SETUID","CAP_SETFCAP","CAP_SETPCAP","CAP_NET_BIND_SERVICE","CAP_SYS_CHROOT","CAP_KILL","CAP_AUDIT_WRITE"]}],"status":"running","pids":[3716],"runtime":"docker-runc"}],"machine":{"cpus":2,"memory":7982}}
```

**containerd-shim**

containerd-shim is a small shim that sits in front of a runtime implementation that allows it to be repartented to init and handle reattach from the caller.

The cwd of the shim should be the bundle for the container.  Arg1 should be the path to the state directory where the shim can locate fifos and other information.

**[runc](https://github.com/opencontainers/runc.git)**

runc is a CLI tool for spawning and running containers according to the OCI specification.

**cgroups结构**

从cgroups里面可以直接看到这几个进程之间的管理关系，比如启动两个container之后：

```
│ ├─docker.service
│ │ ├─ 961 /usr/bin/docker daemon -H fd://
│ │ ├─ 967 docker-containerd -l /var/run/docker/libcontainerd/docker-containerd.sock --runtime docker-runc
│ │ ├─1063 docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 27017 -container-ip 172.17.0.2 -container-port 27017
│ │ ├─1070 docker-containerd-shim bca15f3420e3218987314e1cbbf440120ff880af44844778293c4130526c85cc /var/run/docker/libcontainerd/bca15f3420e3218987314e1cbbf440120ff880af44844778293c4130526c85cc docker-runc
│ │ └─3703 docker-containerd-shim 346c1b7bbb04b760032557e1324a4027ec0055ea84dca109134c02e03dc1242c /var/run/docker/libcontainerd/346c1b7bbb04b760032557e1324a4027ec0055ea84dca109134c02e03dc1242c docker-runc
```
