---
layout: "post"
---


# Docker 容器

容器是 Docker 又一核心概念。

简单的说，容器是独立运行的一个或一组应用，以及它们的运行态环境。对应的，虚拟机可以理解为模拟运行的一整套操作系统（提供了运行态环境和其他系统环境）和跑在上面的应用。

本章将具体介绍如何来管理一个容器，包括创建、启动和停止等。

* [启动](run.html)
* [守护态运行](daemon.html)
* [终止](stop.html)
* [进入容器](enter.html)
* [导出和导入](import_export.html)
* [删除](rm.html)

## docker v.13+

从Docker v1.13开始，之前常用的容器管理命令都放到了`docker container`的子命令里面，比如

```
Commands:
  attach      Attach to a running container
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes on a container's filesystem
  exec        Run a command in a running container
  export      Export a container's filesystem as a tar archive
  inspect     Display detailed information on one or more containers
  kill        Kill one or more running containers
  logs        Fetch the logs of a container
  ls          List containers
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  prune       Remove all stopped containers
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  run         Run a command in a new container
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  wait        Block until one or more containers stop, then print their exit codes
```

使用示例

```sh
# To create a new container
docker container create --name test busybox
# To run a container
docker container run --name busybox -itd busybox
# To attach to a running container
docker container attach busybox

# To create a image from a container’s changes
docker container commit busybox busybox:v2

# To copy files/folders from the host to a container or vice-versa.
docker container cp file busybox:/file
docker container cp busybox:/file newfile

# To inspect changes on a container’s filesystem
docker container diff busybox
# To run a command in a running container

docker container exec busybox ip addr
# To export a container’s filesystem as a tar archive

docker container export busybox -o busybox.tar
# To display low-level information of a container

docker container inspect busybox
# To kill a running container
docker container kill busybox

# To fetch the logs of a container
docker container logs busybox

# To list containers
docker container ls|list|ps
# To pause all processes within a container
docker container pause busybox
# To unpause all processes within a container
docker container unpause busybox

# To list port mappings for the container
docker container port busybox

# To remove all stopped containers
docker container prune --force

# To rename a container
docker container rename test test2
# To restart a container
docker container restart busybox
# To stop a container
docker container stop busybox
# To start a stopped container
docker container start busybox

# To remove a container
docker container rm test2

# To display a live stream of container(s) resource usage statistics
docker container stats

# To display the running processes of a container
docker container top busybox

# To update configuration of a container
docker container update <OPTIONS> busybox

# To block until a container stops and then print their exit codes
docker container wait busybox
```
