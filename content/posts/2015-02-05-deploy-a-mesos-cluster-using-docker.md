---
layout: post
title: "Deploy a Mesos Cluster Using Docker"
description: ""
category: mesos
tags: [docker, mesos]
---

his tutorial will show you how to bring up a single node [Mesos](http://mesosphere.com/) cluster all provisioned out using [Docker](http://docker.io/) containers (a future post will show how to easily scale this out to multi nodes or see the update on the bottom). This means that you can startup an entire cluster with 7 commands! Nothing to install except for starting out with a working Docker server.

This will startup 4 containers:

1.  ZooKeeper
2.  Meso Master
3.  Marathon
4.  Mesos Slave Container

As mentioned the only prerequisite is to have a working Docker server. This means you can bring up a local [Vagrant box with Docker installed](https://docs.vagrantup.com/v2/provisioning/docker.html), use [Boot2Docker](http://boot2docker.io/), use [CoreOS](https://coreos.com/), instance on AWS, or however you like to get a Docker server.

The entire process is outlined in this Github repository: https://github.com/sekka1/mesosphere-docker

All of the Docker container build files used are there also. You can build each container locally or just use the pre-built containers located on the Docker Hub. The commands below will automatically download the needed pre-built containers for you.

ZooKeeper: https://registry.hub.docker.com/u/garland/zookeeper/

Meso Master: https://registry.hub.docker.com/u/garland/mesosphere-docker-mesos-master/

Marathon:  https://registry.hub.docker.com/u/garland/mesosphere-docker-marathon/

### Lets Get Started

**Step 1:** Get the IP of the Docker server and export it out to the environment. We will use this IP over and over again in subsequent Docker commands.

Just as a note, this is the IP address of the server and not docker0 or an IP address inside a Docker container. If you ssh into your server and run the command “ifconfig” use the eth0 interface’s address.

<pre name="feb0" id="feb0" class="graf--pre">
root@docker-server:/# HOST_IP=10.11.31.7
</pre>

**Step 2:** Start the ZooKeeper container.

<pre name="c73f" id="c73f" class="graf--pre">
docker run -d \  
-p 2181:2181 \  
-p 2888:2888 \  
-p 3888:3888 \  
garland/zookeeper
</pre>

**Step 3:** Start Mesos Master

<pre name="9331" id="9331" class="graf--pre">
docker run --net="host" \  
-p 5050:5050 \  
-e "MESOS_HOSTNAME=${HOST_IP}" \  
-e "MESOS_IP=${HOST_IP}" \  
-e "MESOS_ZK=zk://${HOST_IP}:2181/mesos" \  
-e "MESOS_PORT=5050" \  
-e "MESOS_LOG_DIR=/var/log/mesos" \  
-e "MESOS_QUORUM=1" \  
-e "MESOS_REGISTRY=in_memory" \  
-e "MESOS_WORK_DIR=/var/lib/mesos" \  
-d \  
garland/mesosphere-docker-mesos-master
</pre>

**Step 4:** Start Marathon

<pre name="a717" id="a717" class="graf--pre">
docker run \  
-d \  
-p 8080:8080 \  
garland/mesosphere-docker-marathon --master zk://${HOST_IP}:2181/mesos --zk zk://${HOST_IP}:2181/marathon
</pre>

**Step 5:** Start Mesos Slave in a container

<pre name="e983" id="e983" class="graf--pre">
docker run -d \  
--name mesos_slave_1 \  
--entrypoint="mesos-slave" \  
-e "MESOS_MASTER=zk://${HOST_IP}:2181/mesos" \  
-e "MESOS_LOG_DIR=/var/log/mesos" \  
-e "MESOS_LOGGING_LEVEL=INFO" \  
garland/mesosphere-docker-mesos-master:latest
</pre>

**Step 6:** Goto the Mesos’ webpage

Depending on how you brought up your Docker server and it’s IP address you might have to change the IP you point your browser to but the port will be the same.

The Mesos webpage will be at this address:

<pre name="0000" id="0000" class="graf--pre">
http://${HOST_IP}:5050
</pre>

Then you should get a page like this but probably at first without all the items in the “Tasks” tables.

<figure name="d978" id="d978" class="graf--figure">
    <div class="aspectRatioPlaceholder is-locked" style="max-width: 700px; max-height: 554px;">
        <div class="aspect-ratio-fill" style="padding-bottom: 79.2%;"></div>![](https://d262ilb51hltx0.cloudfront.net/max/1010/1*jaUBLpqWBgviqteTk4CuTQ.png)
    </div>
</figure>

**Step 7:** Goto Marathon’s webpage to start a job

The Marathon webpage lets you schedule long running tasks onto the Meso Slave container. This is a good test to see if your cluster is up and running. You can view the Marathon’s webpage at:

<pre name="d885" id="d885" class="graf--pre">
http://${HOST_IP}:8080
</pre>

<figure name="dbcb" id="dbcb" class="graf--figure">
    <div class="aspectRatioPlaceholder is-locked" style="max-width: 700px; max-height: 189px;">
        <div class="aspect-ratio-fill" style="padding-bottom: 27%;"></div>![](https://d262ilb51hltx0.cloudfront.net/max/1400/1*0dKOQ7S8Sc53dTK1tezVLA.png)
    </div>
</figure>

Clicking on the “New App” button on the top right gives you the following menu where you can create a new job/task. We are simply going to echo out hello to a file. We can go into the container and check if the file is created and if the job is continuously running.

<figure name="7586" id="7586" class="graf--figure">
    <div class="aspectRatioPlaceholder is-locked" style="max-width: 700px; max-height: 1096px;">
        <div class="aspect-ratio-fill" style="padding-bottom: 156.6%;"></div>![](https://d262ilb51hltx0.cloudfront.net/max/700/1*T2RuhLQE5xawA_whqbB7ig.png)
    </div>
</figure>

**Step 8:** Check if job/task is running

Lets check if the job/task is continuously running on the Mesos Slave.

On the Docker server run the following commands. It will place you inside the slave container and from there tail out the output.txt file.

<pre name="ff5e" id="ff5e" class="graf--pre">
docker exec -it mesos_slave_1 /bin/bash  
root@ca83bf0ea76a:/# tail -f /tmp/output.txt
</pre>

You will see “hello” being placed into this file about once a second.

Update: I just updated this projects doc to include how to setup a multi node environment: https://github.com/sekka1/mesosphere-docker#multi-node-setup

Here is the same article but translated to Chinese: http://dockerone.com/article/136

From [medium gargar454](https://medium.com/@gargar454/deploy-a-mesos-cluster-with-7-commands-using-docker-57951e020586)
