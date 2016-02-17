---
layout: post
title: "Redhat Atomic Host"
description: ""
category:
tags: [Linux, docker]
---

### Introduction

Red Hat has announced first public beta of [Red Hat Enterprise Linux 7 Atomic Host](http://www.projectatomic.io/). The beta is available from Red Hat and on Amazon Web Services and Google Compute Platform.

What can you expect from the Red Hat Enterprise Linux 7 Atomic Host Beta?

#### Specifically Designed to Run Containers

Red Hat Enterprise Linux 7 Atomic Host Beta provides a streamlined host platform that is optimized to run application containers. The software components included in Red Hat Enterprise Linux 7 Atomic Host Beta, as well as the default system tunings, have been designed to enhance the performance, scalability and security of containers, giving you the optimal platform on which to deploy and run application containers.

#### The Confidence of Red Hat Enterprise Linux

Red Hat Enterprise Linux 7 Atomic Host Beta is built from Red Hat Enterprise Linux 7, enabling Red Hat Enterprise Linux 7 Atomic Host Beta to deliver open source innovation built on the stability and maturity of Red Hat Enterprise Linux. It also means that Red Hat Enterprise Linux 7 Atomic Host Beta inherits the hardware certifications of Red Hat Enterprise Linux 7, giving you a vast choice of certified hardware partners.

#### Atomic Updating and Rollback

Red Hat Enterprise Linux 7 Atomic Host Beta features a new update mechanism that operates in an image-like fashion. Based on rpm-ostree, updates are composed into “atomic” trees, which can be downloaded and deployed in a single step. The previous version of the operating system is retained, enabling you to easily rollback to an earlier state. This simplified upgrade and rollback capability reduces the time you spend “keeping the lights on.”

#### Container Orchestration

Through our [collaboration](http://www.redhat.com/en/about/blog/red-hat-and-google-collaborate-kubernetes-manage-docker-containers-scale)[ ](http://www.redhat.com/en/about/blog/red-hat-and-google-collaborate-kubernetes-manage-docker-containers-scale)[with](http://www.redhat.com/en/about/blog/red-hat-and-google-collaborate-kubernetes-manage-docker-containers-scale)[ ](http://www.redhat.com/en/about/blog/red-hat-and-google-collaborate-kubernetes-manage-docker-containers-scale)[Google](http://www.redhat.com/en/about/blog/red-hat-and-google-collaborate-kubernetes-manage-docker-containers-scale), Red Hat Enterprise Linux 7 Atomic Host Beta includes [<span style="text-decoration: underline;">Kubernetes</span>](https://github.com/GoogleCloudPlatform/kubernetes), a framework for managing clusters of containers. Kubernetes helps with horizontal scaling of multi-container deployments across a container host, and interconnecting multiple layers of the application stacks. This enables you to orchestrate services running in multiple containers into unified, large-scale business applications.

#### Secure Host by Default

Security is paramount when it comes to running applications. Containers alone do not contain, but you can more effectively isolate vulnerable containers with a secure host like Red Hat Enterprise Linux 7 Atomic Host Beta that implements a secure environment by default. First, applications are only run within containers, not directly on the host, creating a clear security boundary. Each container is then confined using a combination of SELinux in enforcing mode, control groups, and kernel namespaces. These technologies prevent a compromised container from affecting other containers or the host and are the same proven technologies that have been delivering military-grade security to Red Hat customers for more than 10 years.

#### Red Hat Enterprise Linux Container Images and Building Containers

Red Hat Enterprise Linux 7 Atomic Host Beta provides all of the required tools to build and run container images based on Red Hat Enterprise Linux, including Red Hat Enterprise Linux 6 and 7 container images as well as the docker services. This means that applications that run on Red Hat Enterprise Linux 6 and Red Hat Enterprise Linux 7 can be deployed in a container on Red Hat Enterprise Linux 7 Atomic Host Beta, opening access to a vast ecosystem of certified applications. Additionally, Red Hat Enterprise Linux 7 Atomic Host Beta<span style="font-weight: normal"> users will have access to the full breadth of their Red Hat subscriptions inside these containers, including the </span><span style="font-weight: normal">the popular programming language stacks and development tools delivered through Red Hat Software Collections.</span><span style="font-weight: normal">.</span>

#### Deploy Across the Open Hybrid Cloud

Red Hat Enterprise Linux 7 Atomic Host Beta extends container portability across the open hybrid cloud by enabling deployment on physical hardware; certified hypervisors, including Red Hat Enterprise Virtualization and VMware vSphere; private clouds such as Red Hat Enterprise Linux OpenStack Platform; and Amazon Web Services and Google Compute Platform public clouds. This ability to “deploy anywhere, deploy everywhere” enables you to choose the best platform for your container infrastructure.

### Demo of Atomic

First, Download an image of Atomic from [Atomic Download](http://www.projectatomic.io/download/):

```
curl http://buildlogs.centos.org/rolling/7/isos/x86_64/CentOS-7-x86_64-AtomicHost-20141129_02.qcow2.xz
xz -d CentOS-7-x86_64-AtomicHost-20141129_02.qcow2.xz
```

And then create an virtual machine with Atomic by virt-manager.  Create an metadata iso before starting it:

<pre>
$ cat meta-data
instance-id: id-local01
local-hostname: samplehost.example.org

$ cat user-data
#cloud-config
password: centos
ssh_pwauth: True
chpasswd: { expire: False }
#ssh_authorized_keys:
#  - ssh-rsa ... foo@bar.baz (insert ~/.ssh/id_rsa.pub here)

$ genisoimage -output init.iso -volid cidata -joliet -rock user-data meta-data
</pre>

Attach init.iso to Atomic virtual machine via virt-manager and start it. Note, if you enconter “hda-duplex not supported in this QEMU binary” problem, change the sound device model from default to ac97 and try again util you can login it by centos/centos.

### Manager docker containers in Atomic

First enable kubernetes:

<pre>
# For master
$ sudo systemctl enable etcd kube-apiserver kube-controller-manager kube-scheduler
$ sudo systemctl start etcd kube-apiserver kube-controller-manager kube-scheduler
# For minion
$ sudo systemctl enable flanneld kubelet kube-proxy
$ sudo systemctl start flanneld kubelet kube-proxy
</pre>

Check kubenetes is ok:

<pre>
$ kubectl get minions
NAME
127.0.0.1
</pre>

Now create pods/replicas/services:

<pre>
$ cat Dockerfile
FROM centos:latest
CMD python -m SimpleHTTPServer 80
EXPOSE 80

$ sudo docker build -t apache .

$ cat apache.json
{
  "id": "apache",
  "kind": "Pod",
  "apiVersion": "v1beta1",
  "desiredState": {
    "manifest": {
      "version": "v1beta1",
      "id": "apache",
      "containers": [{
        "name": "apache",
        "image": "apache",
        "ports": [{
          "containerPort": 80,
          "hostPort": 80
        }]
      }]
    }
  },
  "labels": {
    "name": "apache"
  }
}
$ cat replica.json
{
  "id": "apacheController",
  "kind": "ReplicationController",
  "apiVersion": "v1beta1",
  "labels": {"name": "apache"},
  "desiredState": {
    "replicas": 3,
    "replicaSelector": {"name": "apache"},
    "podTemplate": {
      "desiredState": {
         "manifest": {
           "version": "v1beta1",
           "id": "apache",
           "containers": [{
             "name": "apache",
             "image": "apache",
             "ports": [{
               "containerPort": 80,
             }]
           }]
         }
       },
       "labels": {"name": "apache"},
      },
  }
}

$ cat service.json
{
  "id": "apache",
  "kind": "Service",
  "apiVersion": "v1beta1",
  "labels": {
    "name": "apache"
  },
  "selector": {
    "name": "apache",
  },
  "protocol": "TCP",
  "containerPort": 80,
  "port": 8987
}

$ kubectl create -f apache.json
$ kubectl create -f replica.json
$ kubectl create -f service.json

$ kubectl get pods
NAME                                   IMAGE(S)            HOST                LABELS              STATUS
apache                                 apache              127.0.0.1/          name=apache         Running
a0575c0e-c3d4-11e4-9a23-5254000bef8a   apache              127.0.0.1/          name=apache         Running
a0581080-c3d4-11e4-9a23-5254000bef8a   apache              127.0.0.1/          name=apache         Running
$ kubectl get service
NAME                LABELS              SELECTOR                                  IP                  PORT
kubernetes-ro                           component=apiserver,provider=kubernetes   10.254.228.92       80
apache                                  name=apache                               10.254.91.251       8987
kubernetes                              component=apiserver,provider=kubernetes   10.254.42.232       443
$ kubectl get replicationController
NAME                IMAGE(S)            SELECTOR            REPLICAS
apacheController    apache              name=apache         3

</pre>

### Inter-Container Communications

Atomic uses [Geard](https://github.com/openshift/geard) to enable containers to connect to each other:

<pre>
/usr/sbin/sysctl -w net.ipv4.ip_forward=1
/usr/sbin/sysctl -w net.ipv4.conf.all.route_localnet=1
iptables -t nat -A PREROUTING -d ${local_ip}/32 -p tcp -m tcp \
    --dport ${local_port} -j DNAT --to-destination ${remote_ip}:${remote_port}
iptables -t nat -A OUTPUT -d ${local_ip}/32 -p tcp -m tcp \
    --dport ${local_port} -j DNAT --to-destination ${remote_ip}:${remote_port}
iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to-source ${container_ip}

gear link -n "127.0.0.1:3306:10.16.138.101:49153" server/application_container_1
</pre>

Two advantages of this approach are:

* The application code or configuration to connect to the database
    doesn’t have to change for all instances of the application container.
* The database container could be moved to any host and the application
    would just have to flush and rerun gear link to point to the new location.

### Atomic Upgrades

From a running host, start an upgrade with:

<pre>
# rpm-ostree upgrade
# systemctl reboot
</pre>

On the boot screen you'll see your new version. Hold down the
SHIFT key there to rollback to your previous tree.

### Try the New UI for Your Server

Administer the services on your system with Cockpit (Preview - not for production use)

```
# sudo systemctl enable cockpit.socket
# sudo systemctl start cockpit.socket
# visit http://<ipaddress>:9090 in a browser
```

![](/images/cockpit.png)

Cockpit is perfect for new sysadmins, allowing them to easily perform simple tasks such as storage
administration, inspecting journals and starting and stopping services.

The snapshot of Cockpit included in Atomic is a preview - do
not use in production environments.  Cockpit is under rapid
development.

[Visit cockpit-project.org](http://cockpit-project.org/)

### References

* <http://www.redhat.com/en/about/blog/small-footprint-big-impact-red-hat-enterprise-linux-7-atomic-host-beta-now-available>
* <http://www.projectatomic.io/download/>
* <https://www.technovelty.org//linux/running-cloud-images-locally.html>
* <http://cloudinit.readthedocs.org/en/latest/topics/datasources.html#no-cloud>
* <http://www.projectatomic.io/docs/inter-container-networking/>
* <http://www.cnblogs.com/feisky/p/4108477.html>

