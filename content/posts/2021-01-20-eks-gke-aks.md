---
title: "三大公有云托管 Kubernetes 服务 (EKS、GKE、AKS) 评估"
date: 2021-01-20
tags: [CloudNative, Kubernetes]
draft: false
---

作为发展最快的开源项目，Kubernetes 已经在越来越多的企业落地。而作为全球三大公有云提供商，AWS、Azure 和 GCP 都提供了托管 Kubernetes 集群服务，即 Elastic Kubernetes Service (EKS)、Azure Kubernetes Service (AKS) 和 Google Kubernetes Engine (GKE)。

这些托管 Kubernetes 集群服务在标准的 Kubernetes 开源项目之上，构建了一系列的增强特性，形成了云平台独特的生态。了解它们的最新发展以及独特的生态圈，可以帮助我们更好的了解 Kubernetes 生态现状，并可以作为基于 Kubernetes 构建新服务时的最佳实践参考。

以下数据基于 2021 年 1 月三大平台的最新官方文档。

## 基本信息

- AKS 提供了更新的 Kubernetes 版本支持，通常比 GKE 和 EKS 新两到三个版本。
- AKS 和 GKE 都提供了控制平面的自动更新机制（AKS 还在预览版），而 EKS 不支持自动更新。
- AKS 和 GKE 都提供了 Node 健康检测和自动恢复机制，而 EKS 需要用户自己负责。
- GKE 和 EKS 的控制平面都是收费的，而 AKS 还是继续免费。
- 在运行时上，三大平台都同时支持 Docker 和 containerd，所以上游社区 Docker 弃用不影响这些平台。除此之外，GKE 还支持独有的 gVisor，适用于安全要求更高的场景。

![图片](640-20210121134820060.png)

综合这些基本信息，AKS 和 GKE 相对于 EKS 来说，托管服务提供了更多的自动诊断和自动恢复机制，具有明显的优势。而 AKS 的控制平面还是免费的，这对小型客户来说，具有不小的吸引力。

## 服务限制

- 在集群节点数量上，GKE 最多支持 15000 个节点，EKS 支持 3000 个节点，而 AKS 暂时只支持 1000 个节点。
- 在节点池数量上，AKS 支持 100 个节点池，EKS 支持 100，而 GKE 没有明确的文档。
- 在每个节点池支持的节点数量上，AKS 和 EKS 都支持 100，而 GKE 支持 1000。
- 在每个节点支持的 Pod 数量上，AKS 支持 250，GKE 支持 110， 而 EKS 需要用户根据具体网络配置计算。

![图片](640-20210121134819903.png)

综合这些服务限制，GKE 单集群支持更多的节点数，超过 5000 节点时，GKE 是唯一的选择。

## 网络和安全

- 在网络和安全上，三大平台都默认开启了 RBAC，都支持 PodSecurityPolicy。AKS 还支持 Azure Policy，在涵盖 PodSecurityPolicy 基础上，还支持配置 Azure 平台相关的策略。
- 在 Kubernetes API 的访问限制上，三大平台都提供了白名单机制和私有 API 地址的功能。
- 在网络策略（Network Policy）的支持上，EKS 需要用户手动去安装 Calico，而 AKS 和 GKE 都支持内置开启。
- 虽然 EKS 提供了托管节点池的功能，但这个功能要求每个节点都绑定一个公网 IP，这对网络安全来说是个很大的挑战。

![图片](640-20210121134819976.png)

综合这些网络和安全特性，AKS 和 GKE 提供了更完善的安全控制机制，而 EKS 还有很多配置需要用户自己管理。

## 镜像服务

- 在镜像服务上，三大平台都提供了镜像仓库服务，支持匿名或私有的镜像托管。ECR 和 ACR 都同时支持 Docker 镜像格式、OCI 镜像格式以及 Helm Chart，而 GKE 已经从大家熟知的 GCR 迁移到了 Artifact Registry （AR），支持 Docker 镜像格式、OCI 镜像格式以及 Maven 和 npm 等。
- 在镜像安全上，三大平台都提供了镜像安全扫描服务。
- 在镜像可用性上，三大平台都提供了跨地域冗余的机制，自动把镜像数据复制到其他地域。

![图片](640-20210121134819963.png)

综合这些镜像服务的特性，可以发现三个平台提供的镜像服务基本类似，AKS 和 EKS 支持托管 Helm Charts，是相对于 GKE 的优势。

**参考文档**

- StackRox 报告：https://www.stackrox.com/post/2021/01/eks-vs-gke-vs-aks-jan2021/
- AKS 文档：https://aka.ms/aks/docs
- GKE 文档：https://cloud.google.com/kubernetes-engine
- EKS 文档：https://aws.amazon.com/eks/


---

欢迎扫描下面的二维码关注**漫谈云原生**公众号，回复**任意关键字**查询更多云原生知识库，或回复**联系**加我微信。

![](/assets/mp.png)

