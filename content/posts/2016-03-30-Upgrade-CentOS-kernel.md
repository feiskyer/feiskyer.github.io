---
title: "Upgrade CentOS kernel"
date: 2016-03-30T12:20:15+08:00
---

终于耐不住要升级下kernel了，目前epel提供两个版本: kernel-lt (4.4)和kernel-ml (4.5):

- The kernel-ml packages are built from the sources available from the "mainline stable" branch of The Linux Kernel Archives (external link). The kernel configuration is based upon the default RHEL-7 configuration with added functionality enabled as appropriate. The packages are intentionally named kernel-ml so as not to conflict with the RHEL-7 kernels and, as such, they may be installed and updated alongside the regular kernel.
- The kernel-lt packages are built from the sources available from The Linux Kernel Archives (external link), just like the kernel-ml packages. The difference is that kernel-lt is based on a "long term support" branch and kernel-ml is based on the "mainline stable" branch.


升级到lt的步骤很简单：

```sh
rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
yum install -y http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm
yum --enablerepo=elrepo-kernel install -y kernel-lt
```

然后重启机器即可。

```sh
$  uname -r
4.4.6-1.el7.elrepo.x86_64
```

当然了，相应的内核头文件和开发库也需要安装下：

```sh
yum --enablerepo=elrepo-kernel install -y kernel-lt-headers kernel-lt-tools kernel-lt-devel
```

参考 http://elrepo.org/tiki/kernel-lt http://elrepo.org/tiki/kernel-ml
