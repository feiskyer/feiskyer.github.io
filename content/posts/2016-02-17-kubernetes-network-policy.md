layout: "post"
title: "Kubernetes network policy"
date: "2016-02-17 18:53"
---

Kubernetes network policy

Kubernetes社区（确切的说是Kubernetes Network SIG [1]）正在讨论Network Policy Proposal，以实现SDN、网络隔离、IP Overlapping等[2]复杂的网络需求。

目前，正在讨论的Proposals有多个：

* **Consolidated Casey/RH Proposal** https://docs.google.com/document/d/1blfqiH4L_fpn33ZrnQ11v7LcYP0lmpiJ_RaapAPBbNU/edit
* Casey Davenport https://docs.google.com/document/d/16fg7Dc7K5m4bM2vGwyvkhPG_lcBKeOjaUSYBMwZlR_o/edit?usp=sharing
* Vipin Jain https://docs.google.com/a/insiemenetworks.com/document/d/1KKMOJSXKKQOzlblAzwYV72KGUlAuAaUuFqCWO8h4gd0/edit?usp=sharing
* Tim Hockin https://docs.google.com/document/d/1bXUO-Lp6smmLm7SMGwrwuvK23wgsaWvx6Mkt-Y0AtZ0/edit#

这几个Proposal都大同小异，主要的思想都是一致的：

* 默认情况下网络模型跟现在保持一致，只有定义了Network Policy并且实现了相应的Network Plugin的时候，这个Proposal才有意义
* Network Policy: 管理网络连通性策略，这些策略与具体的网络实现（如libnetwork等）无关
* Network Policy通过Label作用到Pod/Service上
* 需要Network Plugin配合实现Network Policy

下面就以**Consolidated Casey/RH Proposal**为例看看具体的Proposal都有啥。

#### 设计目标

* 不影响现有的网络架构，即未定义Network Policy时，保持Kubernetes现有的网络架构
* 基于ThirdPartyResource实现NetworkPolicy资源的管理

#### Namespaces

Namespace spec中增加`isolation`，默认关闭。当`isolation`打开后

* 所有访问该Namespace内部Pods的请求都被拒绝(也包括该Namespace内部的Pods访问内部的其他Pods）
* 例外：为了不影响Health Check，从Node上访问Pods均允许

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: IsolatedApp
spec:
 isolation: [ yes | no ]
```

#### **NetworkPolicy Objects**

当Namespace的isolation打开的时候，需要NetworkPolicy来控制访问策略。访问策略的规则为：

* 访问策略`allowFrom`仅对进入的请求有效，当策略满足的时候放行
* 所有不匹配Policy的入请求均拒绝
* 所有从Pods向外部发出的请求均放行（当然以后也有可能增加`allowTo`）
* 定义Namespace和Pod时需要添加`tier`标签

一个简单的NetworkPolicy示例为

```yaml
kind: NetworkPolicy
 metadata:
  name: database-policy
spec:
  selector:
	 tier: database
  allowFrom:
  * namespaces:
	  foo: bar  [ allows from namespaces with label “foo:bar” ]
  * pods:
	  tier: database   [ allows east-west traffic on TCP 4001 ]
	protocol: TCP [ One of: TCP, UDP, ICMP ]
	ports: [4001]
```

### 简单的示例

现在就看一下如何通过ThirdPartyResource来管理NetworkPolicy资源。

```sh
[root@linux kubernetes]# # start k8s with thirdpartyresources enabled
[root@linux kubernetes]# cd $GOPATH/src/k8s.io/kubernetes
[root@linux kubernetes]# export RUNTIME_CONFIG="extensions/v1beta1=true,extensions/v1beta1/thirdpartyresources=true"
[root@linux kubernetes]# hack/local-up-cluster.sh


[root@linux ~]# # create a ThirdPartyResource whose type is NetworkPolicy
[root@linux ~]# cat network-policy.yaml
metadata:
  name: "network-policy.experimental.kubernetes.io"
apiVersion: "extensions/v1beta1"
kind: "ThirdPartyResource"
description: "An experimental specification of network policy"
versions:
  * name: v1
[root@linux ~]# kubectl create -f network-policy.yaml
thirdpartyresource "network-policy.experimental.kubernetes.io" created
[root@linux ~]# kubectl get thirdpartyresource
NAME                                        DESCRIPTION                                       VERSION(S)
network-policy.experimental.kubernetes.io   An experimental specification of network policy   extensions/v1

[root@linux ~]# # new experimental.kubernetes.io and networkpolicys APIs is visitable
[root@linux ~]# curl http://localhost:8080/apis/experimental.kubernetes.io/
{
  "kind": "APIGroup",
  "apiVersion": "v1",
  "name": "experimental.kubernetes.io",
  "versions": [
	{
	  "groupVersion": "experimental.kubernetes.io/v1",
	  "version": "v1"
	}
  ],
  "preferredVersion": {
	"groupVersion": "",
	"version": ""
  }
}[root@linux ~]# curl http://localhost:8080/apis/experimental.kubernetes.io/v1/namespaces/default/networkpolicys/
{
  "kind": "NetworkPolicyList",
  "items": [  ]
}


[root@linux ~]# # create a new network policy
[root@linux ~]# cat network-policy.json
{
  "kind": "NetworkPolicy",
  "metadata": {
	"name": "awesome-policy"
  },
  "allowIncoming": {
	"pods": [
	  {
		"tier": "database"
	  }
	],
	"ports": [
	  {
		"protocol": "TCP",
		"port": 4001
	  }
	],
	"namespaces": [
	  {
		"foo": "bar"
	  }
	]
  },
  "apiVersion": "experimental.kubernetes.io/v1",
  "selector": {
	"tier": "database"
  }
}
[root@linux ~]# # kubectl supporting with 3rd party objects is on reviewing at https://github.com/kubernetes/kubernetes/pull/18835
[root@linux ~]# # so just post directly here
[root@linux ~]# curl -X POST -H "Content-Type: application/json" -d @network-policy.json http://localhost:8080/apis/experimental.kubernetes.io/v1/namespaces/default/networkpolicys
{
  "allowIncoming": {
	"namespaces": [
	  {
		"foo": "bar"
	  }
	],
	"pods": [
	  {
		"tier": "database"
	  }
	],
	"ports": [
	  {
		"port": 4001,
		"protocol": "TCP"
	  }
	]
  },
  "apiVersion": "experimental.kubernetes.io/v1",
  "kind": "NetworkPolicy",
  "metadata": {
	"name": "awesome-policy",
	"namespace": "default",
	"selfLink": "/apis/experimental.kubernetes.io/v1/namespaces/default/networkpolicys/awesome-policy",
	"uid": "63d53b48-d248-11e5-85b1-064a4ed57913",
	"resourceVersion": "29",
	"creationTimestamp": "2016-02-13T11:53:25Z"
  },
  "selector": {
	"tier": "database"
  }
}
[root@linux ~]# curl http://localhost:8080/apis/experimental.kubernetes.io/v1/namespaces/default/networkpolicys/
{
  "kind": "NetworkPolicyList",
  "items": [
	{
	  "allowIncoming": {
		"namespaces": [
		  {
			"foo": "bar"
		  }
		],
		"pods": [
		  {
			"tier": "database"
		  }
		],
		"ports": [
		  {
			"port": 4001,
			"protocol": "TCP"
		  }
		]
	  },
	  "apiVersion": "experimental.kubernetes.io/v1",
	  "kind": "NetworkPolicy",
	  "metadata": {
		"name": "awesome-policy",
		"namespace": "default",
		"selfLink": "/apis/experimental.kubernetes.io/v1/namespaces/default/networkpolicys/awesome-policy",
		"uid": "63d53b48-d248-11e5-85b1-064a4ed57913",
		"resourceVersion": "29",
		"creationTimestamp": "2016-02-13T11:53:25Z"
	  },
	  "selector": {
		"tier": "database"
	  }
	}
  ]
}

[root@linux ~]# # clear
[root@linux ~]# kubectl delete thirdpartyresource network-policy.experimental.kubernetes.io
thirdpartyresource "network-policy.experimental.kubernetes.io" deleted
```

当然了，上面只是API部分的demo，具体的网络Plugin还需要做很多工作实现这些策略。Kubernetes Meetup [3] 上Romana有一个关于Network Policy的演示，[4] 这里有更多的说明。

**Consolidated Casey/RH Proposal**还有一些未解决的问题还在讨论中，如

* Service的访问策略怎么定义，如何处理跟Pod访问策略冲突的问题
* 如何定义Kubernetes外部服务的访问策略，是不是要在`allowFrom`中增加`CIDR`等


当然，这些Proposal都还在讨论中，虽然最终的Design和实现还没有确定，但大致的思想肯定不会有太大的变化了。


[1] https://docs.google.com/document/d/1_w77-zG_Xj0zYvEMfQZTQ-wPP4kXkpGD8smVtW_qqWM
[2] https://docs.google.com/document/d/1ZCz_MZILzKCbFwF9gjU1YNA1YbNaw0NDsESh1P6Vcnc
[3] https://www.youtube.com/watch?v=ab7mXAddaX8
[4] https://docs.google.com/document/d/1qAm-_oSap-f1d6a-xRTj6xaH1sYQBfK36VyjB5XOZug
