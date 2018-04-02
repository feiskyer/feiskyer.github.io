---
title: "Seccomp"
type: page
---

Seccomp是Secure computing mode的缩写，它是Linux内核提供的一个操作，用于限制一个进程可以执行的系统调用．Seccomp需要有一个配置文件来指明容器进程允许和禁止执行的系统调用。

```sh
$ cat profile.json
{
    "defaultAction": "SCMP_ACT_ALLOW",
    "syscalls": [
        {
            "name": "chmod",
            "action": "SCMP_ACT_ERRNO"
        }
    ]
}

$ docker run --rm -it --security-opt seccomp:$(pwd)/profile.json busybox chmod 400 /etc/hosts
chmod: /etc/hosts: Operation not permitted
```

运行容器时，可以设置`seccomp:unconfined`来允许容器执行全部系统调用

```sh
docker run --rm -it --security-opt seccomp:unconfined busybox chmod 400 /etc/hosts
```

## Kubernetes示例

```sh
$ cat /var/lib/kubelet/seccomp/chmod.json
{
    "defaultAction": "SCMP_ACT_ALLOW",
    "syscalls": [
        {
            "name": "chmod",
            "action": "SCMP_ACT_ERRNO"
        }
    ]
}

$ kubectl create -f /dev/stdin <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: trustworthy-pod
  annotations:
    seccomp.security.alpha.kubernetes.io/pod: localhost/chmod
spec:
  containers:
    - name: trustworthy-container
      image: sotrustworthy:latest
EOF
```
