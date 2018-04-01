---
title: Virtio vsock
date: 2016-10-14 13:55:34
---

virtio-vsock is a host/guest communications device. It allows applications in the guest and host to communicate. This can be used to implement hypervisor services and guest agents (like qemu-guest-agent or SPICE vdagent).

Unlike virtio-serial, virtio-vsock supports the POSIX Sockets API so existing networking applications require minimal modification. The Sockets API allows N:1 connections so multiple clients can connect to a server simultaneously.

The device has an address assigned automatically so no configuration is required inside the guest.

Sockets are created with the AF_VSOCK address family. The SOCK_STREAM socket type is currently implemented.

![vhost-vsock](/images/vhost-vsock.png)

**NFS over vsock**

![nfs-over-vsock](/images/nfs-over-vsock.png)


**参考文档**

[1] http://qemu-project.org/Features/VirtioVsock
[2] http://vmsplice.net/~stefan/stefanha-kvm-forum-2015.pdf


