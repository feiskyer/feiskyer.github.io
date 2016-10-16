---
title: cri-o (ocid)
date: 2016-10-16 15:58:21
---

# cri-o

cri-o基于Kubelet容器运行时接口（CRI）为Kubernetes带来了原生的OCI运行时(目前仅支持runc)。cri-o还在紧张有序的开发中，预计与Kubernetes v1.5一起发布第一个alpha版本。

## 编译安装

```sh
# Ubuntu 16.04 LTS Xenial
apt-get install -y linux-headers-$(uname -r) build-essential golang libglib2.0-dev
apt-get install -y runc

# install docker
echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" > /etc/apt/sources.list.d/docker.list
apt-get install -y apt-transport-https ca-certificates
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
apt-get update && apt-get install -y docker-engine

# get and build cri-o
export GOPATH=/gopath
export PATH=$GOPATH/bin:$PATH
mkdir -p $GOPATH
go get -d github.com/kubernetes-incubator/cri-o
cd $GOPATH/src/github.com/kubernetes-incubator/cri-o
make install.tools
make binaries
make docs
make install
```

## cri-o单独使用

```sh
# Start ocid
ocid --runtime $(which runc) --debug

# Play with ocid
ocic pod create --config test/testdata/sandbox_config.json
ocic pod list
ocic ctr create --pod 31885791dfa4c112ef1a61bad89b347aa37a7d35177578451c5c512c19b6396a --config test/testdata/container_redis.json
ocic ctr start --id e28b037b26690075456f4e51318314544d6e226a85c103080e5dd818e936341a
```

启动一个redis容器后的进程关系：

```
      ├─13009 ocid --runtime /usr/sbin/runc --debug
      ├─13049 /usr/libexec/ocid/conmon -c default-podsandbox1-0-infra -r /usr/sbin/runc
      ├─16081 /usr/libexec/ocid/conmon -c default-podsandbox1-0-podsandbox1-redis-0 -r /usr/sbin/runc
      ├─podsandbox1.slice:container:infra
      │ └─13058 /pause
      └─default-podsandbox1-0-podsandbox1-redis-0
        └─16090 redis-server *:6379
```

## Kubernetes cri-o

*to be continued*


