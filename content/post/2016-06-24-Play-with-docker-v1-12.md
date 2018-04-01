---
title: Play with docker v1.12
date: 2016-06-24 12:39:49
tags: [docker]
---

[TOC]

Docker v1.12 brings in its integrated orchestration into docker engine.

> Starting with Docker 1.12, we have added features to the core Docker Engine to make multi-host and multi-container orchestration easy.  We’ve added new API objects, like Service and Node, that will let you use the Docker API to deploy and manage apps on a group of Docker Engines called a swarm. With Docker 1.12, the best way to orchestrate Docker is Docker!

![docker-v1 12](https://cloud.githubusercontent.com/assets/676637/16327966/a4f34346-3a07-11e6-8d21-153509596cec.png)

## Playing on GCE

Create swarm-manager:

```sh
gcloud init
docker-machine create swarm-manager --engine-install-url experimental.docker.com -d google --google-machine-type n1-standard-1 --google-zone us-central1-f --google-disk-size "500" --google-tags swarm-cluster --google-project k8s-dev-prj
```

Check what version has been installed:

```
$ eval $(docker-machine env swarm-manager)
$ docker version
Client:
 Version:      1.12.0-rc2
 API version:  1.24
 Go version:   go1.6.2
 Git commit:   906eacd
 Built:        Fri Jun 17 20:35:33 2016
 OS/Arch:      darwin/amd64
 Experimental: true

Server:
 Version:      1.12.0-rc2
 API version:  1.24
 Go version:   go1.6.2
 Git commit:   906eacd
 Built:        Fri Jun 17 21:07:35 2016
 OS/Arch:      linux/amd64
 Experimental: true
```

Create worker node:

```
docker-machine create swarm-worker-1 \
    --engine-install-url experimental.docker.com \
    -d google \
    --google-machine-type n1-standard-1 \
    --google-zone us-central1-f \
    --google-disk-size "500" \
    --google-tags swarm-cluster \
    --google-project k8s-dev-prj
```

Initialize swarm

```sh
# init manager
eval $(docker-machine env swarm-manager)
docker swarm init
```

> Under the hood this creates a Raft consensus group of one node.  This first node has the role of manager, meaning it accepts commands and schedule tasks.  As you join more nodes to the swarm, they will by default be workers, which simply execute containers dispatched by the manager.  You can optionally add additional manager nodes.  The manager nodes will be part of the Raft consensus group. We use an optimized Raft store in which reads are serviced directly from memory which makes scheduling performance fast.

```
# join worker
eval $(docker-machine env swarm-worker-1)
manager_ip=$(gcloud compute instances list | awk '/swarm-manager/{print $4}')
docker swarm join ${manager_ip}:2377
```

List all nodes:

```
$ eval $(docker-machine env swarm-manager)
$ docker node ls
ID                           NAME            MEMBERSHIP  STATUS  AVAILABILITY  MANAGER STATUS
0m2qy40ch1nqfpmhnsvj8jzch *  swarm-manager   Accepted    Ready   Active        Leader
4v1oo055unqiz9fy14u8wg3fn    swarm-worker-1  Accepted    Ready   Active
```

## Playing with service

```sh
eval $(docker-machine env swarm-manager)
docker service create --replicas 2 -p 80:80/tcp --name nginx nginx
```

> This command declares a desired state on your swarm of 2 nginx containers, reachable as a single, internally load balanced service on port 80 of any node in your swarm.  Internally, we make this work using Linux IPVS, an in-kernel Layer 4 multi-protocol load balancer that’s been in the Linux kernel for more than 15 years.  With IPVS routing packets inside the kernel, swarm’s routing mesh delivers high performance container-aware load-balancing.

> When you create services, can optionally create replicated or global services.  Replicated services mean any number of containers that you define will be spread across the available hosts.  Global services, by contrast, schedule one instance the same container on every host in the swarm.

> Let’s turn to how Docker provides resiliency.  Swarm mode enabled engines are self-healing, meaning that they are aware of the application you defined and will continuously check and reconcile the environment when things go awry.  For example, if you unplug one of the machines running an nginx instance, a new container will come up on another node.  Unplug the network switch for half the machines in your swarm, and the other half will take over, redistributing the containers amongst themselves.  For updates, you now have flexibility in how you re-deploy services once you make a change. You can set a rolling or parallel update of the containers on your swarm.

```sh
docker service scale nginx=3

$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
b51a902db8bc        nginx:latest        "nginx -g 'daemon off"   2 minutes ago       Up 2 minutes        80/tcp, 443/tcp     nginx.1.8yvwxbquvz1ptuqsc8hewwbau
```

```
# switch to worker
$ eval $(docker-machine env swarm-worker-1)
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS               NAMES
da6a8250bef4        nginx:latest        "nginx -g 'daemon off"   About a minute ago   Up About a minute   80/tcp, 443/tcp     nginx.2.bqko7fyj1nowwj1flxva3ur0g
54d9ffd07894        nginx:latest        "nginx -g 'daemon off"   About a minute ago   Up About a minute   80/tcp, 443/tcp     nginx.3.02k4d34gjooa9f8m6yhfi5hyu
```

As seen above, one container runs on swarm-manager, and the others run on swarm-worker-1.

## Expose services

### Visit by node node ip

```
gcloud compute firewall-rules create nginx-swarm \
  --allow tcp:80 \
  --description "nginx swarm service" \
  --target-tags swarm-cluster
```

Then use external IP (get by exec `gcloud compute instances list`) to visit nginx service.

### GCP Load Balancer (tcp)

```
gcloud compute addresses create network-lb-ip-1 --region us-central1
gcloud compute http-health-checks create basic-check
gcloud compute target-pools create www-pool --region us-central1 --health-check basic-check
gcloud compute target-pools add-instances www-pool --instances swarm-manager,swarm-worker-1 --zone us-central1-f

# Get lb addresses
STATIC_EXTERNAL_IP=$(gcloud compute addresses list | awk '/network-lb-ip-1/{print $3}')
# create forwarding rules
gcloud compute forwarding-rules create www-rule --region us-central1 --port-range 80 --address ${STATIC_EXTERNAL_IP} --target-pool www-pool
```

Now you could visit http://${STATIC_EXTERNAL_IP} for nginx service.

BTW, [Docker for aws and azure](https://blog.docker.com/2016/06/azure-aws-beta/) will do this more easily as integrated:

- Use an SSH key already associated with your IaaS account for access control
- Provision infrastructure load balancers and update them dynamically as apps are created and updated
- Configure security groups and virtual networks to create secure Docker setups that are easy for operations to understand and manage

> By default, apps deployed with bundles do not have ports publicly exposed. Update port mappings for services, and Docker will automatically wire up the underlying platform loadbalancers:`docker service update -p 80:80 <example-service>`

### Networking

#### Local networking

<img width="1239" alt="2016-06-24 12 05 13" src="https://cloud.githubusercontent.com/assets/676637/16327964/9dfd842a-3a07-11e6-9031-c79c9c43ec83.png">

Create local scope network and place containers in existing vlans:

```
docker network create -d macvlan --subnet=192.168.0.0/16 --ip-range=192.168.41.0/24 --aux-address="favoriate_ip_ever=192.168.41.2" --gateway=192.168.41.1 -o parent=eth0.41 macnet41
docker run --net=macnet41 -it --rm alpine /bin/sh
```

#### Multi-host networking

A typical two-tier (web+db) application runs on swarm scope network would be created like this:

```
docker network create -d overlay mynet
docker service create –name frontend –replicas 5 -p 80:80/tcp –network mynet mywebapp
docker service create –name redis –network mynet redis:latest
```

<img width="1133" alt="2016-06-26 10 27 20" src="https://cloud.githubusercontent.com/assets/676637/16362920/7dbd339e-3bed-11e6-9987-8d425480ba59.png">

<img width="1169" alt="2016-06-24 12 05 30" src="https://cloud.githubusercontent.com/assets/676637/16327980/c4af9432-3a07-11e6-93ed-9e94d12f0c9b.png">
<img width="1228" alt="2016-06-24 12 05 58" src="https://cloud.githubusercontent.com/assets/676637/16327982/c4b2a906-3a07-11e6-8e97-70a26c5fc701.png">
<img width="1235" alt="2016-06-24 12 06 11" src="https://cloud.githubusercontent.com/assets/676637/16327981/c4b14fc0-3a07-11e6-84f0-260a716044cb.png">

### Conclusion

Docker v1.12 indeeds introduced easy-of-use interface for orchestrating containers, but I'm concerned whether this way could scale for large clusters. Maybe we could see it on Docker's further iterations.

### Further more

- https://blog.docker.com/2016/06/docker-1-12-built-in-orchestration/
- http://www.slideshare.net/MadhuVenugopal2/dockercon-us-2016-docker-networking-deep-dive
- https://medium.com/google-cloud/docker-swarm-on-google-cloud-platform-c9925bd7863c#.3plkwmxss
- https://beta.docker.com/docs/


