---
layout: "post"
---

# System

从docker v1.13开始，新增的`docker system`命令可以用来查看或管理系统资源，比如

* `docker system df` 当前docker容器、数据卷和镜像所使用的资源情况
* `docker system proune` 回收未使用的镜像、volume和网络，并删除停止的容器，当然也可以对每种对象单独回收
    * `docker container prune`
    * `docker image prune`
    * `docker volume prune`
    * `docker network prune`

## docker system命令

```sh
# To show docker disk usage
docker system df
# To get real time events from the server
docker system events
# To display system-wide information
docker system info
# To remove unused data
docker system prune
```

