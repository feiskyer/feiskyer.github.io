---
title: SELinux
date: 2016-10-21 16:41:20
layout: "post"
---

SELinux (Security-Enhanced Linux) 是一种强制访问控制（mandatory access control）的实现。它的作法是以最小权限原则（principle of least privilege）为基础，在Linux核心中使用Linux安全模块（Linux Security Modules）。SELinux主要由美国国家安全局开发，并于2000年12月22日发行给开放源代码的开发社区。

可以通过`runcon`来为进程设置安全策略，`ls`和`ps`的`-Z`参数可以查看文件或进程的安全策略。

## 安装 SELinux

```sh
apt install selinux
reboot
```

## 开启与关闭SELinux

修改`/etc/selinux/config`文件方法：

- 开启：`SELINUX=enforcing`
- 关闭：`SELINUX=disabled`

通过命令临时修改：

- 开启：`setenforce 1`
- 关闭：`setenforce 0`

查询SELinux状态：

```
$ getenforce
```

## 基本操作

```sh
# List
$ mkdir /html
$ touch /html/index.html
$ ls -Z /html/index.html
-rw-r--r--  root root user_u:object_r:default_t        /html/index.html
$ ls -Z | grep html
drwxr-xr-x  root root user_u:object_r:default_t        html 

# Relabel
$ chcon -v --type=httpd_sys_content_t /html
context of /html changed to user_u:object_r:httpd_sys_content_t
$ chcon -v --type=httpd_sys_content_t /html/index.html
context of /html/index.html changed to user_u:object_r:httpd_sys_content_t
$ ls -Z /html/index.html
-rw-r--r--  root root user_u:object_r:httpd_sys_content_t    /html/index.html
$ ls -Z | grep html
drwxr-xr-x  root root user_u:object_r:httpd_sys_content_t    html 
```

## Docker中的SELinux

默认情况下，dockerd 启动时禁止了 selinux。如果要使用 SELinux，需要修改 dockerd 的启动命令，添加 `--selinux-enabled `。

Docker可以通过`--security-opt label:xxxx`选项为容器设置SELinux，默认为`svirt_sandbox_file_t`；当然，也可以通过`--security-opt label:disable`来为某些容器禁止SELinux。

在需要Volume的情况下，docker还支持自动relabel volume，只需要加上`:Z`即可：

```sh
$docker run -v /data:/data:Z --security-opt label:level:s0:c2,c3 -itd busybox
$ ls -Z /data
-rw-r--r--. root root system_u:object_r:svirt_sandbox_file_t:s0:c2,c3 test
```

## Kubernetes中的SELinux

Kubernetes也已经通过SecurityContext支持SELinux：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hello-world
spec:
  containers:
  - image: gcr.io/google_containers/busybox:1.24
    name: test-container
    command:
    - sleep
    - "6000"
    volumeMounts:
    - mountPath: /mounted_volume
      name: test-volume
  restartPolicy: Never
  hostPID: false
  hostIPC: false
  securityContext:
    seLinuxOptions:
      level: "s0:c2,c3"
  volumes:
  - name: test-volume
    emptyDir: {}
```

这会自动给容器生成如下的`HostConfig.Binds`: 

- `/var/lib/kubelet/pods/f734678c-95de-11e6-89b0-42010a8c0002/volumes/kubernetes.io~empty-dir/test-volume:/mounted_volume:Z`
- `/var/lib/kubelet/pods/f734678c-95de-11e6-89b0-42010a8c0002/volumes/kubernetes.io~secret/default-token-88xxa:/var/run/secrets/kubernetes.io/serviceaccount:ro,Z`
- `/var/lib/kubelet/pods/f734678c-95de-11e6-89b0-42010a8c0002/etc-hosts:/etc/hosts`

对应的volume也都会正确设置SELinux：

```sh
$ ls -Z /var/lib/kubelet/pods/f734678c-95de-11e6-89b0-42010a8c0002/volumes
drwxr-xr-x. root root unconfined_u:object_r:svirt_sandbox_file_t:s0:c2,c3 kubernetes.io~empty-dir
drwxr-xr-x. root root unconfined_u:object_r:svirt_sandbox_file_t:s0:c2,c3 kubernetes.io~secret
```

**参考文档**

- <https://wiki.centos.org/HowTos/SELinux>
- <http://kubernetes.io/docs/user-guide/security-context/>
- <https://access.redhat.com/documentation/en/red-hat-enterprise-linux-atomic-host/7/single/getting-started-with-containers/#kubernetes_and_selinux_permissions>
