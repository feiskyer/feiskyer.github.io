---
layout: post
title: "Integrating Openstack and Kubernetes with Murano"
description: ""
category: OpenStack
tags: [OpenStack, Docker]
---

There’s a perceived competition between OpenStack and containers such as Docker, but in reality, the two technologies are a powerful combination. They both solve similar problems, but on different layers of the stack, so combining the two can give users more scalability and automation than ever before.

That containers app you wrote needs to run somewhere. This is particularly true for orchestrated container applications, such as those managed by Kubernetes. What’s more, if your application is complicated enough that it needs to scale up and down, you need to be running it in an environment that can, itself, scale up and down. This is where OpenStack comes in.

The idea of making OpenStack and Kubernetes work together might seem a little daunting, but as of today, it just got easier. &nbsp;A lot easier.

Today we are announcing a joint project with Google to integrate the Kubernetes container management application with the OpenStack Application Catalog, Murano. This project will enable you to click a few buttons and end up with a working, scalable Kubernetes application within minutes.

While that in itself is a pretty heady thought, let’s stop for a moment and think about what that means. &nbsp;Remember, Kubernetes lets you move workloads between different clouds, as long as they’re both running Kubernetes. &nbsp;That means that you will be able to move workloads between OpenStack and other clouds, such as Google Cloud Platform. &nbsp;Suddenly hybrid cloud — an OpenStack private cloud integrated with public cloud for scale — doesn’t sound so crazy anymore.

For example, you might construct an application environment in which your internal database lives in your private OpenStack cloud, but the web application component that presents it to the world lives in public cloud. &nbsp;Perhaps you have an external-facing application in the public cloud that sends analytics back to a big data application in the private cloud. Or you might simply have an application that runs on the private cloud but uses the public cloud as a bank of additional resources when needed.

But how does it actually work?

## How it works

Craig Peters and Georgy Okrokvertskhov will be doing a live demo at the [Kubernetes Gathering on Wednesday, February 25](http://www.meetup.com/Bay-Area-Kubernetes-Meetup/events/220167517/), but the idea here is to build on the fact that users can easily self-provision applications using Murano. Murano will provide a Kubernetes package, which provides an abstraction layer for Kubernetes and Pods. Developers can then package their applications for use as they normally would, easily adding them to the Kubernetes cluster.

Kubernetes does the same things you expect it to, such as providing Pods that implement the Docker service, monitoring availability and load of the Pods, and scaling Pods up and down based on the Kubernetes configuration. &nbsp;It also coordinates connectivity between the Pods and the underlying infrastructure.

Meanwhile, Murano manages and orchestrates that underlying infrastructure, which consists of OpenStack resources. It configures the virtual network for Kubernetes and the Pods, and uses OpenStack Orchestration (Heat) to provision the resources Kubernetes needs, such as virtual machines and interface connections, network and subnet configs, security groups, router configurations, and storage.

If you’re already using Kubernetes, you’re probably already familiar with how scaling works. &nbsp;Containers are grouped into Pods, and Kubernetes scales the Pods within a Kubernetes cluster, spawning containers on Kubernetes hosts. If you have multiple hosts, Kubernetes distributes the containers among them.

When your application grows to the point where the Kubernetes cluster itself needs to scale, however, the system needs some outside help; an external system needs to add resources. In this case, that “external system” is Murano, which uses OpenStack Telemetry (Ceilometer) to detect when additional resources are needed. Murano adds a new host to the Kubernetes cluster using the Kubernetes “add node” function, and Kubernetes redistributes the load. &nbsp;(Murano can also initiate scaling applications within a cluster, if necessary.)

## Kubernetes and OpenStack in Action

Well, that all sounds great in theory, but how do you actually do it? &nbsp;Fortunately, the process is pretty straightforward. &nbsp;

NOTE: &nbsp;The following steps are in development, and will be available will be available for technical preview use on [Mirantis OpenStack Express](http://express.mirantis.com/) in April 2015.

* Deploy an OpenStack cluster, and install Murano. &nbsp;(In Mirantis OpenStack, this is simply a matter of checking the “Murano” box in the “Create Environment” wizard.

![](https://www.mirantis.com/wp-content/uploads/2015/02/install-murano1.png)(https://www.mirantis.com/wp-content/uploads/2015/02/install-murano1.png)

* Open the OpenStack Dashboard (Horizon).

![](https://www.mirantis.com/wp-content/uploads/2015/02/open-the-openstack-dashboard1.png)(https://www.mirantis.com/wp-content/uploads/2015/02/open-the-openstack-dashboard1.png)

* Click Murano and create a new environment.

![](https://www.mirantis.com/wp-content/uploads/2015/02/Click-Murano-and-create-a-new-environment1.png)(https://www.mirantis.com/wp-content/uploads/2015/02/Click-Murano-and-create-a-new-environment1.png)

* Add the Kubernetes application to the environment.

![](https://www.mirantis.com/wp-content/uploads/2015/02/add-the-kubernetes-application-to-the-environment1.png)(https://www.mirantis.com/wp-content/uploads/2015/02/add-the-kubernetes-application-to-the-environment1.png)

* Add the Kubernetes Pod to the environment.

![](https://www.mirantis.com/wp-content/uploads/2015/02/add-kubernetes-pod-to-environment1.png)(https://www.mirantis.com/wp-content/uploads/2015/02/add-kubernetes-pod-to-environment1.png)

* Add an application to the Pod. &nbsp;In this case, we’ll add a web server just so we can see it work.

![](https://www.mirantis.com/wp-content/uploads/2015/02/add-application-to-pod1.png)(https://www.mirantis.com/wp-content/uploads/2015/02/add-application-to-pod1.png)

* Deploy the environment.

![](https://www.mirantis.com/wp-content/uploads/2015/02/deploy1.png)(https://www.mirantis.com/wp-content/uploads/2015/02/deploy1.png)

* Test.

![](https://www.mirantis.com/wp-content/uploads/2015/02/test.png)(https://www.mirantis.com/wp-content/uploads/2015/02/test.png)

That’s it.

From <https://www.mirantis.com/blog/integrating-openstack-and-kubernetes-with-murano/>.
