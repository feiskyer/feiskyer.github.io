---
layout: "post"
---

# 集群部署

## GCE/Azure

在GCE或者Azure上面可以利用cluster脚本方便的部署集群：

```
# gce,aws,gke,azure-legacy,vsphere,openstack-heat,rackspace,libvirt-coreos
export KUBERNETES_PROVIDER=gce
curl -sS https://get.k8s.io | bash
cd kubernetes
cluster/kube-up.sh
```

## AWS

在aws上建议使用[kops](https://kubernetes.io/docs/getting-started-guides/kops/)来部署。

## 物理机或虚拟机

在Linux物理机或虚拟机中，建议使用[kubeadm](https://kubernetes.io/docs/getting-started-guides/kubeadm/)来部署Kubernetes集群。

