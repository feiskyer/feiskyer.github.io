---
title: Troubleshooting Kubernetes Cloud Provider
date: 2018-01-27 20:11:07
layout: "post"
---

This chapter is about troubleshooting kubernetes clusters on public clouds (AWS, Azure, GCE etc).

For those clusters, kubernetes is usually configured with cloud provider. e.g. on Azure

```sh
--cloud-config=/etc/kubernetes/azure.json --cloud-provider=azure
```

It may be configured by cloud's managed kubernetes service (e.g. GKE, AKS or EKS). Or it may be configured directly on VM, which gains much more flexibility.

### Overview of failure modes

This is an incomplete list of things that could go wrong, and how to adjust your cluster setup to mitigate the problems.

* **AuthorizationFailure**, e.g. not authorized to operate network routes or persistent volumes. This failure could be easily found in kube-controller-manager or cloud-controller-manager logs.
* **Network routes not configured**. Normally, cloud provider will configure a network route for each nodes registered. If the configuration is wrong or not able to finish (e.g. quota limits), then pod connections will be abnormal.
* **Public IP not allocated for LoadBalancer Service**.
* **Security group rules error**, e.g. new rules couldn't be added (because of quota ) or conflicting with other rules.
* **Persistent volume not able to allocate or attach to VM**, e.g.
  * PV may not be able to allocate if exceeding quota
  * Most PVs doesn't allow to mount on multiple VMs
* **Network plugin configure error**. Network plugin may be configured with protocol not allowed by the cloud, e.g. Azure doesn't allow GRE and ipip in VM.
