---
title: "runV"
type: page
---

[runV](https://github.com/hyperhq/runv) 是[Open Container Initiative (OCI) 标准](https://github.com/opencontainers/runtime-spec) 的一个实现（其他实现包括[runc](runc.html)和[clear container](https://github.com/01org/cc-oci-runtime)等）。与runc不同的是，runV是一个基于虚拟化的OCI引擎，支持kvm、kvmtool、Xen、QEMU等各种虚拟化技术，并通过Xen 4.9+提供的xenpv驱动、KSM、精简内核、无需Guest OS、vhostuser等技术大大提升了虚拟化的性能（所谓的轻量级虚拟化）。此外，runV也支持x86、ARM等多种不同的平台。

## runV安装

```sh
# install dependencies
sudo apt-get install -y autoconf automake pkg-config libdevmapper-dev libvirt-dev libvirt-bin wget libaio1 libpixman-1-0 jq qemu-system-x86 qemu

# install hyperstart
git clone https://github.com/hyperhq/hyperstart.git ${GOPATH}/src/github.com/hyperhq/hyperstart
cd ${GOPATH}/src/github.com/hyperhq/hyperstart
./autogen.sh && ./configure && make
sudo mkdir -p /var/lib/hyper/
sudo cp build/hyper-initrd.img build/kernel /var/lib/hyper

# install runv
git clone https://github.com/hyperhq/runv $GOPATH/src/github.com/hyperhq/runv
cd $GOPATH/src/github.com/hyperhq/runv
./autogen.sh && ./configure --without-xen
make && make install
```

## 容器示例

```sh
# create the top most bundle directory
mkdir /containerbundle
cd /containerbundle

# create the rootfs directory
mkdir rootfs

# export busybox via Docker into the rootfs directory
docker export $(docker create busybox) | tar -C rootfs -xvf -

# generate oci bundle spec
runv spec

# run as root
cd /containerbundle
runv --kernel /var/lib/hyper/kernel --initrd /var/lib/hyper/hyper-initrd.img run mycontainer
# If you used the unmodified `runv spec` template this should give you a `sh` session inside the container.
$ ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1   4352   232 ttyS0    S+   05:54   0:00 /init
root         2  0.0  0.5   4448   632 pts/0    Ss   05:54   0:00 sh
root         4  0.0  1.6  15572  2032 pts/0    R+   05:57   0:00 ps aux
```

## containerd with runV

```sh
mkdir -p /etc/containerd/
containerd config default > /etc/containerd/config.toml

cat >> /etc/containerd/config.toml <<EOF
[plugins.linux]
  shim = "containerd-shim"
  no_shim = false
  runtime = "runv"
  shim_debug = true
EOF

ctr pull docker.io/library/busybox:latest
ctr run --rm -t docker.io/library/busybox:latest foobar sh
```



## docker with runV

```sh
# install docker
curl -sSL https://get.docker.com/ | bash

mkdir -p /etc/docker
cat >/etc/docker/daemon.json <<EOF
{
  "default-runtime": "runv",
  "runtimes": {
    "runv": {
      "path": "runv"
    }
  }
}
EOF

systemctl restart docker
docker info|grep Runtime # should show runv in the list
docker run --rm -it busybox sh
```
