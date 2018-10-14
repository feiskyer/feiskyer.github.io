---
layout: post
title: Azure Container Service（ACS）简介
date: 2017-11-20 21:00:00
tags: [Azure, Kubernetes]
category: "Kubernetes"
---

Azure Container Service（ACS）是 Microsoft Azure 在2015年推出的容器服务，支持 Kubernetes、DCOS 以及 Dockers Swarm 等多种容器编排工具。并且 ACS 的核心功能是开源的，用户可以通过<https://github.com/Azure/acs-engine>来查看和下载使用。

> 注意，AKS （预览版）是 ACS 的下一代产品，提供了一个托管的 Kubernetes 集群，并且集群管理本身是免费的。AKS未来会提供更丰富的功能和更完善的用户体验，比如
>
> - 简单一致的使用体验，包括CLI、PowerShell、Rest API、Dashboard等
> - 支持自定义VNET
> - 支持持久化存储
> - 支持 Linux 容器和 Windows 容器
> - [Azure managed applications](https://azure.microsoft.com/en-us/blog/azure-managed-applications/) 集成
>
> ACS 目前支持的 Swarm 和 DC/OS 未来还会继续支持，并且它们会进入  Azure Marketplace 中。而现有的 Kubernetes 集群也将可以通过 [heptio/Ark](https://github.com/heptio/ark) 等工具迁移到 AKS。

由于 ACS 未来会被 AKS 所取代，这里就不再详细介绍 ACS 的原理了。其使用也是比较简单的

```sh
# 创建集群
az acs create --orchestrator-type kubernetes --resource-group myResourceGroup --name myK8sCluster --generate-ssh-keys
# 安装 kubectl 命令行工具
az acs kubernetes install-cli 
# 配置 kubectl 用户和证书
az acs kubernetes get-credentials --resource-group=myResourceGroup --name=myK8sCluster
# 然后就可以正常使用了
kubectl get nodes
```

## acs-engine

虽然未来 AKS 是 Azure 容器服务的下一代主打产品，但用户可能还是希望可以自己管理容器集群以保证足够的灵活性（比如自定义master服务等）。这时用户可以使用开源的 [acs-engine](https://github.com/Azure/acs-engine) 来创建和管理自己的集群。acs-engine 其实就是 ACS 的核心部分，提供了一个部署和管理 Kubernetes、Swarm和DC/OS 集群的命令行工具。它通过将容器集群描述文件转化为一组ARM（Azure Resource Manager）模板来建立容器集群。 

在 acs-engine 中，每个集群都通过一个json文件来描述，比如一个Kubernetes集群可以描述为

```sh
{
  "apiVersion": "vlabs",
  "properties": {
    "orchestratorProfile": {
      "orchestratorType": "Kubernetes"
    },
    "masterProfile": {
      "count": 1,
      "dnsPrefix": "",
      "vmSize": "Standard_D2_v2"
    },
    "agentPoolProfiles": [
      {
        "name": "agentpool1",
        "count": 3,
        "vmSize": "Standard_D2_v2",
        "availabilityProfile": "AvailabilitySet"
      }
    ],
    "linuxProfile": {
      "adminUsername": "azureuser",
      "ssh": {
        "publicKeys": [
          {
            "keyData": ""
          }
        ]
      }
    },
    "servicePrincipalProfile": {
      "clientId": "",
      "secret": ""
    }
  }
}
```

orchestratorType 指定了部署集群的类型，目前支持三种

- Kubernetes
- Swarm
- DCOS

而创建集群的步骤也很简单

```sh
# create a new resource group.
az group create --name myResourceGroup  --location "centralus"

# start deploy the kubernetes
acs-engine deploy --resource-group myResourceGroup --subscription-id <subscription-id> --auto-suffix --api-model kubernetes.json

# setup kubectl
export KUBECONFIG="$(pwd)/_output/<name-with-suffix>/kubeconfig/kubeconfig.centralus.json"
kubectl get node
```

### 开启RBAC

RBAC默认是不可以开启的，可以通过设置enableRbac开启

```json
     "kubernetesConfig": {
        "enableRbac": true
      }
```

### 自定义Kubernetes版本

acs-engine基于 hyperkube 来部署Kubernetes服务，所以只需要使用自定义的 hyperkube 镜像即可。

```json
"kubernetesConfig": {
    "customHyperkubeImage": "docker.io/dockerhubid/hyperkube-amd64:sometag"
}
```

### 添加Windows节点

可以通过设置 osType 来添加Windows节点（完整示例见[这里](https://github.com/Azure/acs-engine/blob/master/examples/windows/kubernetes.json)）

```json
    "agentPoolProfiles": [
      {
        "name": "windowspool2",
        "count": 2,
        "vmSize": "Standard_D2_v2",
        "availabilityProfile": "AvailabilitySet",
        "osType": "Windows"
      }
    ],
    "windowsProfile": {
      "adminUsername": "azureuser",
      "adminPassword": "replacepassword1234$"
    },
```

### 使用GPU

设置 vmSize 为`Standard_NC*` 或  `Standard_NV*` 会自动配置GPU，并自动安装所需要的 NVDIA 驱动。

### 自定义网络插件

acs-engine 默认使用 kubenet 网络插件，并通过用户自定义的路由以及IP-forwarding转发Pod网络。此时，Pod网络与Node网络在不同的子网中，Pod不受VNET管理。

用户还可以使用 [Azure CNI plugin](https://github.com/Azure/azure-container-networking) 插件将Pod连接到Azure VNET中

```json
"properties": {
    "orchestratorProfile": {
      "orchestratorType": "Kubernetes",
      "kubernetesConfig": {
        "networkPolicy": "azure"
      }
    }
}
```

也可以使用calico网络插件

```json
"properties": {
    "orchestratorProfile": {
      "orchestratorType": "Kubernetes",
      "kubernetesConfig": {
        "networkPolicy": "calico"
      }
    }
}
```

## 参考文档

- [AKS – Managed Kubernetes on Azure](https://www.reddit.com/r/AZURE/comments/7d7diz/ama_aks_managed_kubernetes_on_azure/) 
- [Azure Container Service (AKS)](https://docs.microsoft.com/en-us/azure/aks/)
- [Azure/acs-engine Github](https://github.com/Azure/acs-engine)
- [acs-engine/examples](https://github.com/Azure/acs-engine/tree/master/examples) 
