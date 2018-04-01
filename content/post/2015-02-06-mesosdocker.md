---
layout: post
title: "使用Mesos来管理Docker集群"
description: ""
category: docker
tags: [docker, mesos]
---

### Introduction

Apache Mesos能够在同样的集群机器上运行多种分布式系统类型，更加动态有效率低共享资源。提供失败侦测，任务发布，任务跟踪，任务监控，低层次资源管理和细粒度的资源共享，可以扩展伸缩到数千个节点。Mesos已经被Twitter用来管理它们的数据中心。

![](/assets/mesos_1.png)

Mesos架构图如下：

![](/assets/mesos_2.png)

Mesos框架是一个在Mesos上运行分布式应用的应用程序，它有两个组件：

1.  调度器 : 与Mesos交互，订阅资源，然后在mesos从服务器中加载任务。  
2.  执行器 :  从框架的环境变量 配置中获得信息，在mesos从服务器中运行任务。

下面看看其是如何实现资源调用？Mesos通过"resources offers" 分配资源，资源其实是当前可用资源的一个快照，调度器将使用这些资源在mesos从服务器上运行任务。

Mesos主从服务器调度资源的顺序图如下：

![](/assets/mesos_3.png)

首先由Mesos主服务器查询可用资源给调度器，第二步调度器向主服务器发出加载任务，主服务器再传达给从服务器，从服务器向执行器命令加载任务执行，执行器执行任务以后，将状态反馈上报给从服务器，最终告知调度器 。

从服务器下管理多个执行器，每个执行器是一个容器，以前可以使用Linux容器LXC，现在使用Docker容器。

![](/assets/mesos_4.png)

### 失败恢复和高可用性

Mesos主服务器使用Zookeeper进行服务选举和发现。它有一个注册器记录了所有运行任何和从服务器信息，使用MultiPaxos进行日志复制实现一致性。

Mesos有一个从服务器恢复机制，无论什么时候一个从服务器死机了，用户的任务还是能够继续运行，从服务器会将一些关键点信息如任务信息 状态更新持久化到本地磁盘上，重新启动时可以从磁盘上恢复运行这些任务(类似Java中的钝化和唤醒)

### 什么是Marathon 

它是一个mesos框架，能够支持运行长服务，比如web应用等。是集群的分布式Init.d，能够原样运行任何Linux二进制发布版本，如Tomcat Play等等，可以集群的多进程管理。也是一种私有的Pass，实现服务的发现，为部署提供提供REST API服务，有授权和SSL、配置约束，通过HAProxy实现服务发现和负载平衡。  

![](/assets/mesos_5.png)

这样，我们可以如同一台Linux主机一样管理数千台服务器，它们的对应原理如下图，使用Marathon类似Linux主机内的init Systemd等外壳管理，而Mesos则不只包含一个Linux核，可以调度数千台服务器的Linux核，实际是一个数据中心的内核：

![](/assets/mesos_6.png)


### 部署方法

首先安装Mesos和Marathon，并配置slave使用docker：

```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E56151BF
DISTRO=$(lsb_release -is | tr '[:upper:]' '[:lower:]')
CODENAME=$(lsb_release -cs)
echo "deb http://repos.mesosphere.io/${DISTRO} ${CODENAME} main" | \
  sudo tee /etc/apt/sources.list.d/mesosphere.list
sudo apt-get -y update
sudo apt-get -y install mesos marathon
echo 'docker,mesos' > /etc/mesos-slave/containerizers
echo '5mins' > /etc/mesos-slave/executor_registration_timeout
```

启动所有服务

```
sudo service zookeeper restart
sudo service mesos-master start
sudo service mesos-slave start
sudo service marathon start
```

现在打开浏览器，访问`http://localhost:8080`和`http://localhost:5050`就可以分别看到Mesos和Marathon的界面了. 

![](/assets/mesos1.png)

执行下面的命令，来运行一个简单的任务确认Mesos部署正常：

```
MASTER=$(mesos-resolve `cat /etc/mesos/zk` 2>/dev/null)
mesos-execute --master=$MASTER --name="cluster-test" --command="sleep 5"
```

### 部署docker容器

通过Marathon提供了RestAPI，方便管理和部署各种应用，并支持通过HAProxy实现负载均衡。下面我们就通过Rest API来创建docker容器：

```
curl -X POST -H "Accept: application/json" -H "Content-Type: application/json" http://localhost:8080/v2/apps -d '{
  "container": {
    "type": "DOCKER",
    "docker": {
      "image": "centos"
    }
  },
  "id": "cent",
  "instances": 1,
  "cpus": 0.5,
  "mem": 512,
  "uris": [],
  "cmd": "while sleep 10; do date -u +%T; done"
}'
```

返回数据为：

```
{
    "id": "/cent",
    "cmd": "while sleep 10; do date -u +%T; done",
    "args": null,
    "user": null,
    "env": {
    },
    "instances": 1,
    "cpus": 0.5,
    "mem": 512.0,
    "disk": 0.0,
    "executor": "",
    "constraints": [
    ],
    "uris": [
    ],
    "storeUrls": [
    ],
    "ports": [
        0
    ],
    "requirePorts": false,
    "backoffSeconds": 1,
    "backoffFactor": 1.15,
    "maxLaunchDelaySeconds": 3600,
    "container": {
        "type": "DOCKER",
        "volumes": [
        ],
        "docker": {
            "image": "centos",
            "network": null,
            "portMappings": null,
            "privileged": false,
            "parameters": [
            ]
        }
    },
    "healthChecks": [
    ],
    "dependencies": [
    ],
    "upgradeStrategy": {
        "minimumHealthCapacity": 1.0,
        "maximumOverCapacity": 1.0
    },
    "labels": {
    },
    "version": "2015-02-06T01:25:27.392Z"
}
```

此时，通过Marathon的界面<http://localhost:8080>就可以看到已经有一个app在Deploying了，稍等一会该状态会变成Running。在Slave上执行`docker ps`也可以看到正在运行的容器。

Mesos也支持通过端口映射将容器内部的服务开放出来：

```
curl -X POST -H "Accept: application/json" -H "Content-Type: application/json" http://localhost:8080/v2/apps -d '{
  "id": "webserver",
  "cmd": "python -m SimpleHTTPServer 8080",
  "cpus": 0.5,
  "mem": 64.0,
  "instances": 1,
  "container": {
    "type": "DOCKER",
    "docker": {
      "image": "centos",
      "network": "BRIDGE",
      "portMappings": [
        { "containerPort": 8080, "hostPort": 0, "servicePort": 9000, "protocol": "tcp" }
      ]
    }
  }
}'
```

![](/assets/mesos2.png)

### 部署其他应用

前面是通过单机来测试了Mesos部署docker的功能的，而Mesos通常都是用在集群中，关于Mesos集群的部署请参考<http://mesosphere.com/docs/getting-started/datacenter/install/>.

Mesos支持部署各种集群应用，如Kubernets、Hadoop、Spark、Chronos、Storm等，具体部署方法参考<http://mesosphere.com/docs/tutorials/>.

### 参考文档

* <http://mesosphere.com/docs/getting-started/developer/single-node-install/>
* <http://mesosphere.com/docs/tutorials/>
* <http://mesosphere.com/docs/getting-started/datacenter/install/>

