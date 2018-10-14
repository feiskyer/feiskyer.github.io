---
layout: post
title: "Something about kubernetes authentication"
description: ""
category: kubernetes
tags: [kubernetes]
---

You can enable kubernetes authentication by through [this documentation](https://github.com/kubernetes/kubernetes/blob/master/docs/admin/authentication.md). Then you happily access kube-apiserve by curl: 

```
# curl -k -N -X GET -H "Authorization: Basic XXXXXXXXXX" http://localhost:8080/api/v1/namespaces/default/pods
{
  "kind": "PodList",
  "apiVersion": "v1",
  "metadata": {
    "selfLink": "/api/v1/namespaces/default/pods",
    "resourceVersion": "74034"
  },
  "items": []
}
```

Nothing blocks this request! What is wrong? Wait a moment and checkout kubernetes documentation, I find this:

> The Kubernetes API is served by the Kubernetes apiserver process.  Typically,
> there is one of these running on a single kubernetes-master node.

By default the Kubernetes APIserver serves HTTP on 2 ports:

  1. Localhost Port

    - serves HTTP
    - default is port 8080, change with `--insecure-port` flag.
    - defaults IP is localhost, change with `--insecure-bind-address` flag.
    - no authentication or authorization checks in HTTP
    - protected by need to have host access

  2. Secure Port

    - default is port 6443, change with `--secure-port` flag.
    - default IP is first non-localhost network interface, change with `--bind-address` flag.
    - serves HTTPS.  Set cert with `--tls-cert-file` and key with `--tls-private-key-file` flag.
    - uses token-file or client-certificate based [authentication](authentication.md).
    - uses policy-based [authorization](authorization.md).

  3. Removed: ReadOnly Port

    - For security reasons, this had to be removed. Use the [service account](../user-guide/service-accounts.md) feature instead.

So authn and authz are only enable by https port, let's get a try:

```
# curl -k -N -X GET -H "Authorization: Basic YWRtaW46YWRtaW4=" https://localhost:6443/api/v1/namespaces/default/pods
Unauthorized
```

It works.

