---
title: PV Calls
date: 2016-10-14 14:03:04
type: page
---

PV Calls is a paravirtualized protocol that allows the implementation of
a set of POSIX functions in a different domain. The PV Calls frontend
sends POSIX function calls to the backend, which implements them and
returns a value to the frontend.

![1](/images/1-1.png)

This version of the document covers networking function calls, such as
connect, accept, bind, release, listen, poll, recvmsg and sendmsg; but
the protocol is meant to be easily extended to cover different sets of
calls. Unimplemented commands return ENOTSUPP.

PV Calls provide the following benefits:
* full visibility of the guest behavior on the backend domain, allowing
  for inexpensive filtering and manipulation of any guest calls
* excellent performance

Specifically, PV Calls for networking offer these advantages:
* guest networking works out of the box with VPNs, wireless networks and
  any other complex configurations on the host
* guest services listen on ports bound directly to the backend domain IP
  addresses
* localhost becomes a secure namespace for inter-VMs communications

PV Calls to forward POSIX calls from DomU to Dom0. The initial set of calls covers socket, connect, accept, listen, recvmsg, sendmsg and poll. The frontend driver forwards syscalls requests over a ring. The backend implements the syscalls, then returns success or failure to the caller. The protocol creates a new ring for each active socket. The ring size is configurable on a per socket basis. Receiving data is copied to the ring by the backend, while sending data is copied to the ring by the frontend. An event channel per ring is used to notify the other end of any activity.

![](/images/14764251600989.png)

![2](/images/2-1.png)

![3](/images/3-1.png)

## Performance

![](/images/14764251844248.png)

![](/images/14764251911897.png)


**参考文档**

[1] https://blog.xenproject.org/tag/pv-calls/
[2] http://www.slideshare.net/xen_com_mgr/xpds16-a-paravirtualized-interface-for-socket-syscalls-dimitri-stiliadis-aporeto?ref=https://blog.xenproject.org/tag/pv-calls/
[3] https://patchwork.kernel.org/patch/9332691/
