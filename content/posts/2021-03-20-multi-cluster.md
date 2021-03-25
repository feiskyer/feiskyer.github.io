---
title: "基于Kubernetes的多集群实践"
date: 2021-03-20
tags: [Kubernetes]
draft: false
---

在 [基于Kubernetes的多云和混合云](https://mp.weixin.qq.com/s/uM4d3_fwLIdQ95fBWcmRjw) 文章中，我介绍了多云和混合云的由来以及常用方案。多云和混合云的目的主要有以下几个：

* 解除云服务商锁定，避免服务单纯依赖于某一家云服务商。
* 提高服务可用性，不仅可以跨地区和跨地域，更可以在某个云服务商故障时继续在其他正常的云服务商中运行。
* 优化基础设施成本，根据云服务商的价格选择成本较低的方案。
* 保障业务突发的弹性扩展，在某个云服务商容量不足时扩展到其他云服务商中。

有了这么多好处，多云和混合云的缺点也很多，特别是提高了基础架构的复杂度。而 Kubernetes 的诞生则是解决了云平台异构的问题：无论是在哪家云服务上中运行 Kubernetes，其底层的云平台异构问题都被封装为相同的 Kubernetes API。这样，对用户来说，只需要在部署 Kubernetes 集群本身的时候考虑每家云平台的不同，而其上的管理平台和业务应用都可以用相同的 Kubernetes API 进行操作。本文就给大家介绍一下多 Kubernetes 集群的常用实践。

## 集群部署

多集群的第一步就是 Kubernetes  集群的部署。由于各家云厂商的 API 并不相同，在管理各个云平台的资源时一般需要借助额外的 CMP（云管理平台）或者  [terraform](https://www.terraform.io/) 等进行统一管理。既然常见的公有云平台都提供了托管 Kubernetes 服务，部署这些托管集群一般并不需要很复杂的操作，所以使用 Terraform 就可以满足大部分需要。

![image-20210321155207074](image-20210321155207074.png)

使用 Terraform 的好处是它是声明式的，在使用时只需要声明预期的基础架构是什么样子，具体的执行步骤会有 Terraform 自动完成，包括下载云服务商模块、与云服务商 API 对接以及执行具体的部署等。

比如，下图就是一个使用 Terraform 部署 AWS 资源的示例：

![](oss-cli-demo-20210321154457049.mp4)

Kubernetes 集群部署完成之后，剩下的就是多集群的应用管理了，包括配置管理、服务治理以及对外服务的负载均衡等等。

## 配置管理

对于同一个应用，部署到多集群时，绝大部分配置都是相同的。所以，可以把应用的配置通过 Helm Charts、Kustomize 甚至是放在不同目录的 Kubernetes YAML 文件等管理起来。多集群不同的地方可通过变量进行区分，如使用 Helm Charts 可以根据 Values 的不同设置不同的 YAML 配置：

```yaml
{{/* Returns Horizontal Pod Autoscaler replicas for GraphQL*/}}
{{- define "graphql.hpaReplicas" -}}
{{- if eq .Values.global.env "prod" }}
{{- if eq .Values.global.region "europe-west1" }}
minReplicas: 40
{{- else }}
minReplicas: 150
{{- end }}
maxReplicas: 1400
{{- else }}
minReplicas: 4
maxReplicas: 20
{{- end }}
{{- end -}}
```

这样，将应用配置部署到不同集群的时候，给 `.Values.global.region` 设置不同的值就可以实现多集群的区分部署。

应用配置准备好之后，接下来就可以结合 gitops、CI/CD 等将其融入 Devops 流水线中。比如，一个最简单的 Jenkins 部署步骤如下图所示：

![img](1*aVw14rBd5nyCOIeuX2nMRg.png)

（图片来自 [Medium](https://medium.com/dailymotion/deploying-apps-on-multiple-kubernetes-clusters-with-helm-19ee2b06179e)）

这个图式就是一个常规的 CI/CD 流水线，包括单元测试、集成测试、镜像发布、生产环境部署等几个步骤。其中，最后一个部署步骤会把应用部署到多个不同的集群中。

## 负载均衡

应用部署完成之后，对于需要暴露到集群外部的服务来说，通常可以通过 LoadBalancer 或 NodePort 类型的 Service 为每个集群内部的应用分配公网 IP 并结合 DNS 绑定一个子域名。

但由于单个集群有可能会发生故障，在这些集群之上还应该再加一层跨集群的负载均衡。这一般有两种实现方法：

* DNS 负载均衡：即在 DNS 服务器中给同一个主机名配置多个 IP 地址，分别指向单个集群中对应服务的公网 IP。这种方式简单灵活，常用在 Web 服务中，缺点是不支持高可靠性，即便单个集群出现了故障，DNS 服务器仍然会为其分配请求。
* 全局负载均衡（GSLB）：即使用跨地区的负载均衡服务，根据后端各个服务的健康状况以及客户端的位置，选择最佳的后端服务器进行转发。GSLB 的优点是会进行后端服务的健康检查，确保请求只转发给健康的服务器；缺点是自建复杂，一般推荐使用云服务商提供的 GSLB 。下图是一个 Azure 全局负载均衡器的示例：

![img](68747470733a2f2f646f63732e6d6963726f736f66742e636f6d2f656e2d75732f617a7572652f6c6f61642d62616c616e6365722f6d656469612f63726f73732d726567696f6e2d6f766572766965772f63726f73732d726567696f6e2d6c6f61642d62616c616e6365722e706e67.png)

## 服务治理

通常说到服务治理，是指服务的注册、发现、观测、流控、安全控制等。在多集群场景中，还包括跨集群访问服务的能力。

不同集群的网络可以通过 Service Mesh 打通，实现网络流量的灵活调度和故障转移。常见的 Service Mesh 项目均提供了多集群打通的能力，如下图是 Linkerd 多集群的示意图：

![image-20210321174651279](image-20210321174651279.png)

（图片来自 [Linkerd multi-cluster communication](https://linkerd.io/2.10/features/multicluster/)）

这个示意图等价于下面的命令，即把 `east` 集群的服务暴露到 `west `集群中：

```sh
linkerd --context=east multicluster link --cluster-name east |
  kubectl --context=west apply -f -
```

当 `east`  集群中的 Service 加上 `mirror.linkerd.io/exported=true` 标签之后，Linkerd 会自动在 `west` 集群中创建其镜像 Service。之后，在 `west` 集群中就可以通过镜像 Service 访问 `east` 集群中的 Service：

```sh
# 在east集群中为服务打开多集群镜像支持
kubectl --context=east label svc -n test podinfo mirror.linkerd.io/exported=true
# 查询west集群中的镜像服务
kubectl --context=west -n test get svc podinfo-east
```

当然，只有镜像还是不够的，更重要的是故障转移。在 Linkerd 中可以创建 `TrafficSplit` 对象，确保集群故障时自动把流量调度到健康的后端中：

```sh
cat <<EOF | kubectl --context=west apply -f -
apiVersion: split.smi-spec.io/v1alpha1
kind: TrafficSplit
metadata:
  name: podinfo
  namespace: test
spec:
  service: podinfo
  backends:
  - service: podinfo
    weight: 50
  - service: podinfo-east
    weight: 50
EOF
```

![image-20210321175202202](image-20210321175202202.png)

除了 Service Mesh，如果多集群之间的网络配置并不冲突（如 IP 网段不重合），还可以通过专线打通，实现更低延迟的跨集群访问。

## 小结

虽然多云多集群可以解决云服务商锁定、跨地域跨云高可靠以及跨云弹性突发等诸多的问题，但从前面的这些方案可以看出来，多云多集群中不同的功能还都需要不同的服务来提供，并非一个完整的解决方案。故而主流的云服务商也都提供了相应的解决方案，如 Azure Arc、GKE Anthos、AWS Outposts 等。各大云服务商和开源社区也在着力解决多云多集群中的各种挑战，如网络延迟、跨地域数据同步、统一安全等等，多云多集群依然还有很长的路要走。




---

欢迎长按下面的二维码关注**漫谈云原生**公众号，输入**任意关键字**查询更多云原生知识库。

![](https://feisky.xyz/assets/mp.png)
