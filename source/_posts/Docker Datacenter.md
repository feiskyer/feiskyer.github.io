layout: "post"
title: "Docker Datacenter"
date: "2016-02-26 17:38"
category: docker
tags: [docker, cluster]
---

Docker annonced `Docker Datacenter (DDC)` at Februrary 23. It is an integrated, end-to-end platform for agile application development and management from the datacenter to the cloud.

With Docker Datacenter, organizations are empowered to deploy a Containers as a Services (CaaS) on-premises or in your virtual private cloud. A CaaS provides an IT managed and secured application environment of content and infrastructure where developers can build and deploy applications in a self service manner.

DDC includes severial Docker projects:

* Commercially supported Docker engine
* Universal Control Plane (UCP) with embedded Swarm for management and orchestration
* Trusted Registry (DTR) for image management

> Docker Trusted Registry allows you to store and manage your Docker images on-premise or in your virtual private cloud to support security or regulatory compliance requirements. Simply install and configure Docker Trusted Registry through the web admin console, integrate to your preferred storage, authenticate to your Active Directory / LDAP services and integrate into key software development workflows like Continuous Integration (CI) and Continuous Delivery (CD).
>
> Universal Control Plane enables enterprises to manage and deploy their Dockerized distributed applications, all from within the firewall.

![](/images/docker_platform.png)

DDC conforms to same API with docker and swarm, so it works completely same with `docker-compose up` on swarm cluster.

The feature of DDC including:

- Docker native with engine, networking and swarm
- Built in HA and security (TLS)
- Integrated content security (DTR)
- User management
- Plugins (networking, volumes, logging)

### Free Trial

You can get a free trial at <http://www.docker.com/products/docker-datacenter#/demo>. The installation of Docker Datacenter including severial steps:

- Install commercially supported Docker engine
- Install Docker Universal Control Plane (UCP)
    - docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock --name ucp docker/ucp install -i --swarm-port 3376 --host-address $(ifconfig eth0 | awk '/inet /{print $2}' | awk -F: '{print $2}')
    - Follow the tips and enter the password
    - Join more nodes: `docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock --name ucp docker/ucp join -i --host-address $(docker-machine ip node2)`
- Install Docker Trusted Registry: `docker run docker/trusted-registry install | bash`
- Open ucp dashboard at https://server-ip and upload your license


![](/images/ucp.png)

### Comparsion with kubernetes

DDC provides deep integration with docker tools (docker, swarm, compose). Because most developers are farmiliar with those tools, there is none learning cost for switching to DDC. This is the best advantage of DDC. Other advantages including:

- Easily to deploy: just a few containers
- Docker commercially support
- User-friendly UI for managing containers togather

On the other side, kubernetes is more difficult to deploy and the dashboard is still on developing at https://github.com/kubernetes/dashboard.

There is no official release about what size of cluster DDC can support, while kubernetes has officially cluster size supporting plan for each release.

Kubernetes supports much more features and much more learning curve than DDC.

Both DDC and kubernetes are in the quick evolving way. Currently I think DDC is much more easy to use, but Kubernetes is much more mature for production, because only kubernetes provides the key features like service-discovering, monitoring, logging, replication controllers and so on.

See more at http://www.docker.com/products/docker-datacenter.
