---
layout: post
title: "Installing nova docker on OpenStack Juno"
description: ""
category: Docker
tags: [Docker]
---

This post comes about indirectly by a request on IRC in #rdo for help getting nova-docker installed on Fedora 21. I ran through the process from start to finish and decided to write everything down for posterity.

Getting started
I started with the Fedora 21 Cloud Image, because I'm installing onto OpenStack and the cloud images include some features that are useful in this environment.

We'll be using OpenStack packages from the RDO Juno repository. Because there is often some skew between the RDO packages and the current Fedora selinux policy, we're going to start by putting SELinux into permissive mode (sorry, Dan):

    # setenforce 0
    # sed -i '/^SELINUX=/ s/=.*/=permissive/' /etc/selinux/config
Next, install the RDO Juno repository:

    # yum -y install \
  https://repos.fedorapeople.org/repos/openstack/openstack-juno/rdo-release-juno-1.noarch.rpm
And upgrade all our existing packages:

    # yum -y upgrade
Install OpenStack
We'll be using packstack to install OpenStack onto this host. Start by installing the package:

    # yum -y install openstack-packstack
And then run a --allinone install, which sets up all OpenStack services on a single host:

    # packstack --allinone
Install nova-docker prequisites
Once packstack has completed successfully, we need to install some prerequisites for nova-docker.

    # yum -y install git python-pip python-pbr \
  docker-io fedora-repos-rawhide
The fedora-repos-rawhide package provides a yum configuration for the rawhide repository (disabled by default). We're going to need that to pick up more recent versions of systemd (because of this bug) and python-six (because nova-docker needs the six.add_metaclass method):

    # yum --enablerepo=rawhide install python-six systemd
At this point, having upgraded systemd, you should probably reboot:

    # reboot
Configure Docker
Once things are up and running, we will expect the nova-compute service to launch Docker containers. In order for this to work, the nova user will need access to the Docker socket, /var/run/docker.sock. By default, this is owned by root:root and has mode 660:

    # ls -l /var/run/docker.sock
srw-rw----. 1 root root 0 Feb  1 12:43 /var/run/docker.sock
The nova-compute service runs as the nova user and will not have access to that socket. There are a few ways of resolving this; an expedient method is simply to make this socket owned by the nova group, which we can do with docker's -G option.

Edit /etc/sysconfig/docker, and modify the OPTIONS= line to look like:

OPTIONS='--selinux-enabled -G nova'
Then enable and start the docker service:

    # systemctl enable docker
    # systemctl start docker
Install nova-docker
Clone the nova-docker repository:

    # git clone http://github.com/stackforge/nova-docker.git
    # cd nova-docker
And check out the stable/juno branch, since we're operating with an OpenStack Juno environment:

    # git checkout stable/juno
Now install the driver:

    # python setup.py install
Configure Nova
Following the README from nova-docker, we need to modify the Nova configuration to use the nova-docker driver. Edit /etc/nova/nova.conf and add the following line to the DEFAULT section:

compute_driver=novadocker.virt.docker.DockerDriver
If there is already a line setting compute_driver, then comment it out or delete before adding the new one.

Modify the Glance configuration to permit storage of Docker images. Edit /etc/glance/glance-api.conf, and add the following line to the DEFAULT section:

container_formats=ami,ari,aki,bare,ovf,ova,docker
Next, we need to augment the rootwrap configuration such that nova-docker is able run the ln command with root privileges. We'll install the docker.filters file from the nova-docker source:

    # mkdir -p /etc/nova/rootwrap.d
    # cp etc/nova/rootwrap.d/docker.filters \
  /etc/nova/rootwrap.d/docker.filters
We've changed a number of configuration files, so we should restart the affected services:

    # openstack-service restart nova glance
Testing things out
Let's try starting a container! We need to select one that will run in the nova-docker environment. Generally, that means one that does not expect to have an interactive terminal and that will automatically start some sort of web-accessible service. I have a minimal thttpd container that fits the bill nicely:

    # docker pull larsks/thttpd
We need to store this image into Glance using the same name:

    # docker save larsks/thttpd |
  glance image-create --name larsks/thttpd \
  --container-format docker --disk-format raw --is-public true
And now we should be able to start a container:

    # nova boot --image larsks/thttpd --flavor m1.tiny test0
After a bit, nova list should show:

+------...+-------+--------+...+------------------+
| ID   ...| Name  | Status |...| Networks         |
+------...+-------+--------+...+------------------+
| 430a1...| test0 | ACTIVE |...| private=10.0.0.6 |
+------...+-------+--------+...+------------------+
And we should also see the container if we run docker ps:

    # docker ps
CONTAINER ID        IMAGE                  COMMAND                CREATED             STATUS              PORTS               NAMES
ee864da30cf1        larsks/thttpd:latest   "/thttpd -D -l /dev/   7 hours ago         Up 7 hours                              nova-430a197e-a0ca-4e72-a7db-1969d0773cf7
Getting connected
At this point, the container will not be network accessible; it's attached to a private tenant network. Let's assign it a floating ip address:

    # nova floating-ip-create public
+--------------+-----------+----------+--------+
| Ip           | Server Id | Fixed Ip | Pool   |
+--------------+-----------+----------+--------+
| 172.24.4.229 | -         | -        | public |
+--------------+-----------+----------+--------+
    # nova floating-ip-associate test0 172.24.4.229
This isn't going to be immediately accessible because Packstack left us without a route to the floating ip network. We can fix that temporarily like this:

    # ip addr add 172.24.4.225/28 dev br-ex
And now we can ping our Docker container:

    # ping -c2 172.24.4.229
PING 172.24.4.229 (172.24.4.229) 56(84) bytes of data.
64 bytes from 172.24.4.229: icmp_seq=1 ttl=63 time=0.291 ms
64 bytes from 172.24.4.229: icmp_seq=2 ttl=63 time=0.074 ms


--- 172.24.4.229 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 0.074/0.182/0.291/0.109 ms
And access the webserver:

        # curl http://172.24.4.229

    <!DOCTYPE html>
    <html>
      <head>
        <title>Your web server is working</title>
