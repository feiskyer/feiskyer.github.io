---
layout: post
title: "Hypernetes   The multi tenant Kubernetes distribution"
description: ""
category: Kubernetes
tags: [Kubernetes]
---


"[The Caas Revolution](https://hyper.sh/blog/post/2015/07/06/the-caas-revolution.html)". This is what we believe is happening today in the Cloud ecosystem. This revolution has been started by the now famous project (and company) [Docker](http://www.docker.com/), and embraced by Cloud providers like [Google](https://cloud.google.com/container-engine/) and [AWS](https://aws.amazon.com/ecs/).

However, most multi-tenant CaaS solutions today run on a public IaaS, and use fully isolated virtual machine clusters to schedule containers. This is in contrast to the solely container-based implementation provided in private CaaS deployments. The public “hybrid” VM/container isolation approach is a direct result from the shared kernel architecture in container technology.

Which got us thinking... do users really need to configure a cluster of full-blown virtual machines to ship containers in a secure cloud? Isn’t there a native container approach to perform true isolation?

When we introduced [Hyper](http://hyper.sh/), we wanted to show that it is actually possible to run truly isolated containers applications without any guest OS configuration required. We claimed that Hyper unlocks the possibility to build app-centric secure and isolated public CaaS platform, and now want to show you its power with a real-world implementation.

Today, we are happy to announce **[Hypernetes](http://hypernetes.com)*: the Secure, Multi-tenant Kubernetes distribution**.

Simply put:

	   Hypernetes = Bare-metal + Hyper + Kubernetes + Cinder(Ceph) + Neutron + Keystone

![Hypernetes](https://github.com/hyperhq/hypernetes/raw/master/architecture.png?raw=true)

- Hyper (Hyperd) runs directly on all your bare-metal machines to provision HyperVM (with Docker images) in milliseconds
- Within the VM, the "Hyperstart" init process is launched on top of the Hyper Kernel (or any compatible Linux kernel) to run Docker images as Pod
- Kubelet agent runs on each bare-metal host and manages HyperVM with Hyperd’s APIs
- The formed cluster of "Kubelets" is managed with the help of a "Kubernetes Master" server
- Hypernetes also makes uses of several OpenStack components
	- [Keystone](http://docs.openstack.org/developer/keystone/) for identities management and authentication
	- [Neutron](https://wiki.openstack.org/wiki/Neutron) for virtual networks management and isolation
	- [Cinder](https://wiki.openstack.org/wiki/Cinder) + [Ceph](http://ceph.com/) for persistent storage volume management

With Hypernetes, you are ready to offer your users an easy and straightforward way to deploy their Containers in the Cloud, with a maximum level of security, efficiency, and compatibility, but without the complexity introduced by nesting the Linux containers in full-blown VMs. Indeed, Hypernetes leverages the same old secure, reliable, battle tested, robust hypervisor virtualization to natively run all of your new Container applications, maximizing the ROI of your virtual infrastructure.

You can check it out and try Hypernetes today as a [open-source project](http://github.com/hyperhq/hypernetes). Please, don't hesitate to join our [Slack community](http://slack.hyper.sh/), [users](https://groups.google.com/forum/#!forum/hyper-user) and [developers](https://groups.google.com/forum/#!forum/hyper-dev) mailing lists if you would like to discuss about Hyper or Hypernetes with us.

Also, as an open-source project, we warmly welcome PR contributions and issues, directly on our [Github](https://github.com/hyperhq/hypernetes).

As a last word, we are presenting Hypernetes this week at the [OpenStack Tokyo Summit](https://www.openstack.org/summit/tokyo-2015/) and [DockerCon Europe](http://europe-2015.dockercon.com/) next month. If you're around, please come by our booth ;-)

From <https://hyper.sh/blog/post/2015/10/27/announcing-hypernetes-the-multitenant-kubernetes-distribution.html>
