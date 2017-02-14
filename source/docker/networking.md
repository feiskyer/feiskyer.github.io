---
title: "docker networking"
layout: "post"
---



# Docker Networking

容器网络通常需要考虑：

* Portability
* Service Discovery
* Load Balancing
* Security
* Performance
* Scalability

![](/images/14779801387121.png)

## Container Networking Model (CNM)

CNM是docker内置的多主机通信网络模型，如下所示：

![](/images/14779726977544.png)

其中，

- Network Sandbox是一个网络命名空间，为容器隔离网络栈，并管理容器的网卡、路由和DNS。
- Endpoint将Sandbox连接到Network，对应容器的一块虚拟网卡。
- Network则是一组互通的Endpoint的集合，不同Network内的Endpoint不可以直接通信。

CNM提供了四种默认的网络插件

- Bridge: By default containers on a bridge will be able to communicate with each other. External access to containers can also be configured through the bridge driver.
- MACVLAN: It can be used to provide IP addresses to containers that are routable on the physical network. Additionally VLANs can be trunked to the macvlan driver to enforce Layer 2 container segmentation.
- Host: There is no namespace separation, and all interfaces on the host can be used directly by the container.
- None: The none driver gives a container its own networking stack and network namespace but does not configure interfaces inside the container. Without additional configuration, the container is completely isolated from the host networking stack.

**Control plane**

> The control plane uses a Gossip protocol based on SWIM to propagate network state information and topology across Docker container clusters. The Gossip protocol is highly efficient at reaching eventual consistency within the cluster while maintaining constant rates of message size, failure detection times, and convergence time across very large scale clusters. This that the network is able to scale across many nodes without introducing scaling issues such as slow convergence or false positive node failures.

1.  **Message Dissemination** updates nodes in a peer-to-peer fashion fanning out the information in each exchange to a larger group of nodes. Fixed intervals and size of peer groups ensures that network usage is constant even as the size of the cluster scales. Exponential information propagation across peers ensures that convergence is fast and bounded across any cluster size.
2.  **Failure Detection** utilizes direct and indirect hello messages to rule out network congestion and specific paths from causing false positive node failures.
3.  **Full State Syncs** occur periodically to achieve consistency faster and resolve network partitions.
4.  **Topology Aware** algorithms understand the relative latency between themselves and other peers. This is used to optimize the peer groups which makes convergence faster and more efficient.
5.  **Control Plane Encryption** protects against man in the middle and other attacks that could compromise network security.

### Default Bridge network

By default bridge will be assigned one subnet from the ranges 172.[17-31].0.0/16 or 192.168.[0-240].0/20 which does not overlap with any existing host interface. The default bridge network is the only network that supports legacy links. Name-based service discovery and user-provided IP addresses are not supported by the default bridge network.


![](/images/14779762459288.png)

### User-defined bridge network

![](/images/14779763239716.png)

**port mapping**

![](/images/14779764170554.png)

### Overlay network

VXLAN has been a part of the Linux kernel since version 3.7, and Docker uses the native VXLAN features of the kernel to create overlay networks. The Docker overlay datapath is entirely in kernel space. This results in fewer context switches, less CPU overhead, and a low-latency, direct traffic path between applications and the physical NIC.

VXLAN is defined as a MAC-in-UDP encapsulation that places container Layer 2 frames inside an underlay IP/UDP header. The underlay IP/UDP header provides the transport between hosts on the underlay network. The overlay is the stateless VXLAN tunnel that exists as point-to-multipoint connections between each host participating in a given overlay network. Because the overlay is independent of the underlay topology, applications become more portable. Thus, network policy and connectivity can be transported with the application whether it is on-premises, on a developer desktop, or in a public cloud.

![](/images/14779765021254.png)

```
#Create an overlay named "ovnet" with the overlay driver
$ docker network create -d overlay ovnet

#Create a service from an nginx image and connect it to the "ovnet" overlay network
$ docker service create --network ovnet --name container nginx
```

Two interfaces have been created inside the container that correspond to two bridges that now exist on the host. On overlay networks, each container will have at least two interfaces that connect it to the overlay and the docker_gwbridge:

- overlay: The ingress and egress point to the overlay network that VXLAN encapsulates and (optionally) encrypts traffic going between containers on the same overlay network. It extends the overlay across all hosts participating in this particular overlay. One will exist per overlay subnet on a host, and it will have the same name that a particular overlay network is given.
- docker_gwbridge: 	The egress bridge for traffic leaving the cluster. Only one docker_gwbridge will exist per host. Container-to-Container traffic is blocked on this bridge allowing ingress/egress traffic flows only.

![](/images/14779765196939.png)

### MACVLAN network

MACVLAN offers a number of unique features and capabilities. It has positive performance implications by virtue of having a very simple and lightweight architecture. Rather than port mapping, the MACVLAN driver provides direct access between containers and the physical network. It also allows containers to receive routable IP addresses that are on the subnet of the physical network.

```
$ docker network create -d macvlan --subnet 192.168.0.0/24 --gateway 192.168.0.1 -o parent=eth0 mvnet
```

![](/images/14779766291554.png)

### VLAN Trunking with MACVLAN

When the macvlan driver is instantiated with sub-interfaces it allows VLAN trunking to the host and segments containers at L2. The macvlan driver automatically creates the sub-interfaces and connects them to the container interfaces. As a result each container will be in a different VLAN, and communication will not be possible between them unless traffic is routed in the physical network.

```
#Creation of  macvlan10 network that will be in VLAN 10
$ docker network create -d macvlan --subnet 192.168.10.0/24 --gateway 192.168.10.1 -o parent=eth0.10macvlan10

#Creation of  macvlan20 network that will be in VLAN 20
$ docker network create -d macvlan --subnet 192.168.20.0/24 --gateway 192.168.20.1 -o parent=eth0.20 macvlan20

#Creation of containers on separate MACVLAN networks
$ docker run -itd --name c1--net macvlan10 --ip 192.168.10.2 busybox sh
$ docker run -it --name c2--net macvlan20 --ip 192.168.20.2 busybox sh
```

![](/images/14779767087981.png)

### Host Network

The host network driver connects a container directly to the host networking stack. containers will have native bare-metal network performance at the cost of namespace isolation.

### None network

Similar to the host network driver, the none network driver is essentially an unmanaged networking option. Docker Engine will not create interfaces inside the container, establish port mapping, or install routes for connectivity. A container using --net=none will be completely isolated from other containers and the host. The networking admin or external tools must be responsible for providing this plumbing. In the following example we see that a container using none only has a loopback interface and no other interfaces.

## Service discovery

Docker uses embedded DNS to provide service discovery for containers running on a single Docker Engine and tasks running in a Docker Swarm. Docker Engine has an internal DNS server that provides name resolution to all of the containers on the host in user-defined bridge, overlay, and MACVLAN networks. Each Docker container ( or task in Swarm mode) has a DNS resolver that forwards DNS queries to Docker Engine, which acts as a DNS server. 

```
$ docker network create -d overlay --subnet 10.1.0.0/24 --gateway 10.1.0.1 dognet
$ docker service create --network dognet --name dog-db redis
#Create the frontend service and expose it on port 8000 externally
$ docker service create --network dognet -p 8000:5000 -e 'DB=dog-db' -e 'ROLE=dog' --name dog-web chrch/web
```

![](/images/14779799677032.png)

![](/images/14779799476052.png)

**Routing mesh**

1.  A service is created with two replicas, and it is port mapped externally to port `8000`.
2.  The routing mesh exposes port `8000` on each host in the cluster.
3.  Traffic destined for the `app` can enter on any host. In this case the external LB sends the traffic to a host without a service replica.
4.  The kernel's IPVS load balancer redirects traffic on the `ingress` overlay network to a healthy service replica.

![](/images/14779800057981.png)

**Secure by IPsec**

![](/images/14779800658754.png)


**References:**

- http://success.docker.com/Datacenter/Apply/Docker_Reference_Architecture%3A_Designing_Scalable%2C_Portable_Docker_Container_Networks

