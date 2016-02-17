---
layout: post
title: "Use kubectl to connect kubernetes cluster"
description: ""
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
