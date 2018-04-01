---
layout: post
title: "Microservice Infrastructure"
description: ""
category:
tags: [Docker]
---

## Microservices Infrastructure

Modern platform for rapidly deploying globally distributed services provided by cisco.

<https://github.com/CiscoCloud/microservices-infrastructure>


## Features

* the ability to deploy applications utilizing resources across multiple datacenters (and even clouds),
* deploying in a decentralized control model,
* supporting intelligent endpoints,
* heavy automation, and
* the on-demand nature of deploying these services to support business requirements and scale.


## Architectural Overview

* Mesos cluster manager for efficient resource isolation and sharing across distributed services
* Marathon for cluster management of long running containerized services
* Consul for service discovery (By using Consul's inbuilt DNS server)
* Docker container runtime supported by Marathon
* Multi-datacenter support
* High availablity


## Single Data Center Architecture

The base platform contains control nodes that manage the cluster and any number of compute nodes. Containers automatically register themselves into DNS so that other services can locate them.

![](https://github.com/CiscoCloud/microservices-infrastructure/blob/master/docs/_static/single_dc.png)


## Multi Data Center

Each datacenter contains a set of control nodes and computes nodes.  The architecture is “share nothing” with the exception of Consul. Consul nodes for all datacenters are automatically joined together to form a single WAN gossip pool. This enables application to local instance in the same datacenter and instances other datacenters with DNS or the Consul exposed API.

![](https://github.com/CiscoCloud/microservices-infrastructure/raw/master/docs/_static/multi_dc.png)


## Control Nodes

The control nodes manage a single datacenter. Each control node runs Consul for service discovery, Mesos leaders for resource scheduling and Mesos frameworks like Marathon.

![](https://github.com/CiscoCloud/microservices-infrastructure/raw/master/docs/_static/control_node.png)


## Compute Nodes

The compute nodes launch containers and other Mesos-based workloads. Registrator is used to update Consul as containers are launched and exit.

![](https://github.com/CiscoCloud/microservices-infrastructure/raw/master/docs/_static/compute_node.png)

## Have a try

```
# checkout codes
git clone https://github.com/CiscoCloud/microservices-infrastructure.git
cd microservices-infrastructure

# start services
vagrant up

# start microservices via Marathon
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


## More

See more at <https://github.com/CiscoCloud/microservices-infrastructure>
