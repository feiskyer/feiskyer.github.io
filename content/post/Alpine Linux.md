layout: "post"
title: "Alpine Linux"
date: "2016-03-26 14:27"
---

Alpine Linux

随着Alpine Linux被越来越多的官方镜像使用，我们有必要了解一下Alpine Linux到底是个什么鬼。

Alpine Linux 是一个面向安全应用的轻量级 Linux 发行版。它采用了musl libc和busybox以减小系统的体积和运行时资源消耗，同时还提供了自己的包管理工具apk。Alpine Linux的内核都打了grsecurity/PaX补丁，并且所有的程序都编译为Position Independent Executables (PIE) 以增强系统的安全性。

### Alpine Linux小试

我们可以通过虚拟机来体验一下完整的Alpine Linux。从alpinelinux.org下载iso（当前是v3.3.3版本，大小为78MB），然后就可以通过Virtual Box或者VMWare创建虚拟机了。默认情况下，启动的虚拟机是diskless模式，重启虚拟机会丢掉所有的变更。因而，建议通过`setup-alpine`来修改安装模式，同时也对系统进行一些配置的初始化。

Alpine社区提供了Docker包，可以方便的安装Docker：

```
echo “http://nl.alpinelinux.org/alpine/v3.3/community” >> /etc/apk/repositories
apk update
apk add docker
rc-update add docker boot
service docker start
```

### Alpine Docker镜像

Docker官方还维护了一个Alpine Linux镜像，大小只有4.7MB，比起大家常用的Ubuntu要小的多。现在有很多镜像都已经用这个镜像来代替了以前的Ubuntu/Debian了，比如常用的haproxy、nginx等。

Alpine Linux的官方网站为[http://alpinelinux.org]，从[http://wiki.alpinelinux.org]可以找到更多的使用指南。
