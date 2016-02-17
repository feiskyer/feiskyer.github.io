---
layout: post
title: "Weekly reading list (20150626)"
description: ""
category: Readings
tags: []
---

这周最热的就是Dockercon了，列表里面很多都是docker相关的。

## Open Container Project (OCP)

> Today we’re pleased to announce that CoreOS, Docker, and a large group of industry leaders are working together on a standard container format through the formation of the Open Container Project (OCP). OCP is housed under the Linux Foundation, and is chartered to establish common standards for software containers. This announcement means we are starting to see the concepts behind the App Container spec and Docker converge. This is a win for both users of containers and our industry at large.

<https://coreos.com/blog/app-container-and-the-open-container-project/>

Docker is donating draft specifications and code for container image format and runtime for the new project. Docker’s [LibContainer project](https://github.com/docker/libcontainer) will become part of [the new RunC project](https://github.com/opencontainers/runc). CoreOS cofounder and chief executive Alex Polvi wrote in a [blog post](https://coreos.com/blog/app-container-and-the-open-container-project/) that he expects a good portion of its appc container specification to become part of the project, while his team will turn its rkt container runtime “into a leading container runtime around the new shared container format.”

<http://venturebeat.com/2015/06/22/docker-and-coreos-unite-to-start-the-open-container-project-and-standardize-runtime-image-format/>

runc <https://github.com/opencontainers/runc>

OCP <http://www.opencontainers.org/>

OCP spec <https://github.com/opencontainers/specs> 暂未公布，需要2-3周时间

## Docker hackathon

一些有趣的项目包括：

* [docker vlan](https://github.com/dockervlan/) implements the VLAN driver in libnetwork
* [swarm-sec](https://github.com/snrism/swarm-sec)  Swarm Security Assessment tool
* [libsecurity](https://github.com/advanderveer/libsecurity) A POC for using Docker to act on vulnerability releases in real time
* BenchRock 用来测试IaaS平台性能的工具
* [sherdock](https://github.com/rancherio/sherdock) Automatic GC of images based on regexp, Find and delete orphan Docker volumes

更多的项目见<http://www.dockercon.com/hackathon>

## Docker experimental binary

> Docker’s experimental binary gives you access to bleeding edge features that are not in, and may never make it into, Docker’s official release.  An experimental build allows users to try out features early and give feedback to the Docker maintainers.  In this way, we hope to refine our feature designs by exposing earlier to real-world usage.
>
> In all cases, experimental features have gone through the same level of refining and quality control than any code that makes it into Docker: the difference is that the user interface and APIs may change.
>
> Network and volume plugins are the very first experimental features introduced
>
> Unlike the regular Docker binary, the experimental channels is built and updated nightly on https://experimental.docker.com. From one day to the next, new features may appear, while existing experimental features may be refined or entirely removed.
>
> Each experimental feature is documented in a dedicated experimental section.  This section explains the feature’s function and design goals. Because your feedback is essential to refine and decide on a feature’s future, you will also find links to GitHub issues where you can leave your comments, look for reported problems, or report on your experience.

<http://blog.docker.com/2015/06/experimental-binary/>

## Docker plugins

The Docker plugins mechanism is now available in the new [Docker experimental channel](https://github.com/docker/docker/tree/master/experimental). Also available are the first Docker plugins, including [Flocker](http://clusterhq.com/docker-plugin) for portable volumes across hosts, and networking plugins available from [Weave](http://blog.weave.works/2015/06/22/weave-as-a-docker-network-plugin/), [Project Calico](http://www.projectcalico.org/calico-docker-1-7-libnetwork/), [Nuage Networks](http://www.nuagenetworks.net/libnetwork-is-license-to-hyper-scale-for-docker-and-sdn/), [Cisco](http://blogs.cisco.com/datacenter/docker-and-the-rise-of-microservices), [VMware](http://blogs.vmware.com/networkvirtualization/2015/06/vmware-docker-networking.html), Microsoft, and [Midokura](http://blog.midonet.org/docker-networking-midonet/).

* Network plugins**, which allow third-party container networking solutions to connect containers to container networks, making it easier for containers to talk to each other even if they are running on different machines.  
* Volume plugins**, which allow third-party container data management solutions to provide data volumes for containers which operate on data, such as databases, queues and key-value stores and other stateful applications that use the filesystem.

To demonstrate the value of plugins we are going to show you an example, that [anyone can replicate themselves today](https://plugins-demo-2015.github.io). The example two plugins to enable container migration for an application on the Docker platform.  We enhance an application with two extension points.

• [Weave](http://blog.weave.works/2015/06/18/weave-1-0-is-out-and-it-is-good/) for portable networking, discovery, monitoring.  
• [Flocker](https://clusterhq.com/) for portable volumes and data.  
• A Docker Swarm cluster runs the application described by Docker Compose  
• We start a database on node 1, then later reschedule it on node 2, and it keeps its volumes and network identity!  
• All of this is combined into one easy Docker experience via plugins.

See demo at <https://plugins-demo-2015.github.io/> 

<http://blog.docker.com/2015/06/extending-docker-with-plugins/>

## Disney docker deployment

Here are some of the components that are in use in the Disney environment:

* Chef: Chef handles the hosts and laying down the configuration for the Mesos master, the Marathon framework, the ZooKeeper endpoint configurations, etc. Chef also handles the initial setup of Consul and HAProxy.
* * Docker: Docker is the packaging solution. Services are packaged using Docker. The Dockerfile for an application resides in the application repo. Application builds include building the Docker image and pushing it to the appropriate registry.
* * Mesos: Mesos provides cluster scheduling, placing containers onto hosts. All interaction with Mesos comes through the frameworks (i.e., Marathon, spark, Cassandra, etc.). 
* * Marathon: The main framework in use is Marathon, which enables running Docker on Mesos. Marathon deployments (handled via JSON descriptions) will deploy Docker images and configure them appropriately (which image to use, which ports to expose, etc.). Health checks are also included in the Marathon deployment file. Marathon also allows Disney to define the upgrade strategy, which enables them to control how new images are deployed.
* * Consul: Disney only uses the distributed key-value store functionality of Consul (not the service discovery aspect). Containers use consul-template to pull information from Consul to customize the configuration at run-time.
* * HAProxy: HAProxy handles the routing of requests. Two health checks are involved: one on the HAProxy side, and one on the back-end service side. HAProxy is completely configured via Marathon’s service discovery mechanism.
* * Jenkins: Jenkins handles the Docker build/push/deploy.

<http://blog.scottlowe.org/2015/06/23/scaling-new-services/>

## Docker security

Docker能提供的安全保障将涵盖以下7点：

* namespace保障系统资源的隔离
* cgroup完成进程组资源的限制
* Linux的安全模块提供MAC（apparmor， SELinux）
* capabilities将root的权限细分为多种类型
* ulimit的功能更多维度的限制资源（docker 1.6之后支持）
* user namespace保障容器内部的root在host上并非root（预计docker 1.8支持）
* seccomp使得容器内进程受到系统调用权限的控制

Docker在安全方面还做了以下工作：

###降低镜像带来的安全风向

* 设置更为精简的Linux发行版：
* 移除不需要的package、用户以及二进制工具文件，

### 提出Tailored Profiles

* 容器可以创建least-privildge的文件
* 文件有能力随容器传递
* 通过独立的文件配置表明所有的权限
* 已经规划入runC
* 描述所有的隔离特性

Docker安全贡献的公司

* HuaWei在支持Docker的seccomp方面贡献有目共睹
* IBM大力贡献Docker的user namespace的支持
* Intel在Docker的bootchain方面投入效果可观
* RedHat则在SELinux方面的贡献受到社区的肯定

<http://blog.daocloud.io/dockercon-day-2-security/>

## Project Orca

Project Orca has a vision of providing a top-to-bottom integrated stack that takes all the tools and plumbing (Docker Engine, Docker Swarm, Networking, GUI, Docker Compose, security, plus tools for installation, deployment, configuration, etc.). Project Orca fits into the “run” portion of the “build-ship-run” triangle on which Docker focuses.

> The Orca demo starts out with a log in to a web-based UI. Hazlett shows how Orca integrates into directory services and provides role-based access controls, and shows the logging/auditing functionality, so that users can see what has happened. Orca will provide lists of images, as well as what’s inside the images (such as showing layers, and the sizes of layers). Orca has integration into Docker Swarm, to show the nodes in a Swarm cluster and manage the nodes in a Swarm cluster. Hazlett also shows how to see the images that are present in a cluster, pull updated images, and push them across the entire Swarm cluster. Naturally, Orca also shows the images that are running across the cluster, the images used by each container, and display the details for running containers (the node on which it’s running, the ports that are exposed, the resources that are in use, the volumes associated with the container). Viewing the logs from a Docker container is also readily accessible from within Orca, as is real-time streaming statistics for the containers. Orca introduces the idea of “stacks,” which correspond to a Docker Compose configuration (sounds a lot like OpenStack Heat to me). Deploying a stack is like docker-compose up, and application-specific (stack-specific) metrics are available within Orca. Orca also integrates the ability to scale the number of containers associated with a stack. Developers can update their application definitions (via changes to the Compose YAML definition), and Orca will allow those changes to be dynamically deployed to production without adverse affect to operations’ ability to scale up or scale down capacity.

<http://blog.scottlowe.org/2015/06/23/dockercon-day2-general-session/>

<http://blog.daocloud.io/dockercon-day-2-production-readiness/>

## Project Bonneville

> Bonneville is a Docker daemon with custom VMware graph, execution and network drivers that delivers a fully-compatible API to vanilla Docker clients. The pure approach Bonneville takes is that the container is a VM, and the VM is a container. There is no distinction, no encapsulation, and no in-guest virtualization. All of the necessary container infrastructure is outside of the VM in the container host. The container is an x86 hardware virtualized VM – nothing more, nothing less.

<http://blogs.vmware.com/cloudnative/introducing-project-bonneville>

<http://venturebeat.com/2015/06/22/everything-announced-at-dockercon-2015/>





