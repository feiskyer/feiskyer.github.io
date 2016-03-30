layout: "post"
title: "Upgrade CentOS kernel"
date: "2016-03-30 22:25"
tags: [linux]
---

终于耐不住要升级下kernel了，目前epel提供两个版本: kernel-lt (4.4)和kernel-ml (4.5)。升级步骤很简单：

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
