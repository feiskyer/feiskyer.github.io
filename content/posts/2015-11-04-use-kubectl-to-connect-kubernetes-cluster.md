---
layout: post
title: "Use kubectl to connect kubernetes cluster"
description: "介绍如何配置 kubectl 以带认证方式连接 Kubernetes 集群，通过 set-credentials 等命令替代默认的无鉴权本地访问。"
category: kubernetes
tags: [kubernetes]
---

`kubectl` is the main tool to interact with Kubernetes cluster. It connects to `http://localhost:8080` with no auth by default. But how can we use `kubectl` with auth?

Pretty simple, just config `kubectl` with dedicated cluster:

```
kubectl config set-credentials default --username=username --password=password
kubectl config set-cluster default --server=https://kubernetes-master:6443 --insecure-skip-tls-verify=true
kubectl config set-context default --cluster=default --user=default
kubectl config use-context default
```
