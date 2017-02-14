---
layout: "post"
---

# Docker 中的网络功能介绍

Docker 允许通过外部访问容器或容器互联的方式来提供网络服务。

* [外部访问容器](port_mapping.html)
* [容器互联](linking.html)
* [Docker 1.12网络](networking.html)

## docker network命令

```sh
# To list networks
docker network ls
# To create a network
docker network create -d overlay --attachable dev

# To connect a container to a network
docker network connect dev busybox
# To disconnect a container from a network
docker network disconnect dev busybox

# To display detailed information of a network
docker network inspect dev

# To remove a network
docker network rm dev

# To remove all unused networks
docker network prune
```
