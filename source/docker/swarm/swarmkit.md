---
title: SwarmKit使用方法
date: 2016-10-13 22:47:27
---

swarm命令格式

```sh
# To initialize a swarm
docker swarm init <OPTIONS>
# To join a swarm as a node and/or manager
docker swarm join <OPTIONS> <HOST>:<PORT>
# To manage join tokens
docker swarm join-token <OPTIONS> worker/manager
# To update the swarm
docker swarm update <OPTIONS>
# To leave the swarm
docker swarm leave
```

## 建立swarm集群

初始化swarm master

```
docker swarm init
```

其他节点加入该集群

```
SWARM_TOKEN=$(docker swarm join-token -q worker)
SWARM_MASTER_ID=$(docker node ls | grep Leader | awk '{print $1}')
SWARM_MASTER=$(docker node inspect $SWARM_MASTER_ID -f {{.ManagerStatus.Addr}})
swarm join --token ${SWARM_TOKEN} ${SWARM_MASTER}
```

## 服务管理

创建服务

```
docker service create --replicas 2 -p 80:80/tcp --name nginx nginx
```

扩展服务

```
docker service scale nginx=3
```

## 网络管理

MacVlan网络

```
docker network create -d macvlan --subnet=192.168.0.0/16 --ip-range=192.168.41.0/24 --aux-address="favoriate_ip_ever=192.168.41.2" --gateway=192.168.41.1 -o parent=eth0.41 macnet41
docker run --net=macnet41 -it --rm alpine /bin/sh
```

overlay网络

```
docker network create -d overlay mynet
docker service create –name frontend –replicas 5 -p 80:80/tcp –network mynet mywebapp
docker service create –name redis –network mynet redis:latest
```

## 节点管理

```sh
# To list nodes in the swarm
docker node ls

# To demote a node from manager in the swarm
docker node demote node2
# To promote one or more nodes to manager in the swarm
docker node promote node2

# To display detailed information on a node
docker node inspect node1

# To list tasks running on one or more nodes.
docker node ps self|node1

# To remove one or more nodes from the swarm
docker node rm node1

# To update a node
docker node update [OPTIONS] node2
```

## 加密

从docker v1.13开始，docker将raft日志加密存储，也更好的支持secret功能。这个加密的key默认是存在磁盘上的，可以通过`autolock`功能禁止保存该key到磁盘上，但要注意禁止后docker重启时需要人工unlock swarm。

```
# Initialize a swarm with autolocking enabled
docker swarm init --autolock
# restart docker
service docker restart
# To unlock swarm
docker swarm unlock

# To view the current unlock key
docker swarm unlock-key

# To enable autolock on an existing swarm
docker swarm update --autolock=true

# You should rotate the locked swarm’s unlock key on a regular schedule.
docker swarm unlock-key --rotate
```