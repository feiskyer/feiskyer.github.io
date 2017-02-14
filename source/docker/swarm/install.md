## 安装

最新版本的docker已经内置了`swarm`和`node`命令来管理swarm集群。

初始化master

```
docker swarm init
```

加入节点：

```
docker swarm join --token $token $master_ip:2377
```

### 在OSX上创建swarm集群

在OS X系统上，由于Docker for Mac只能创建一台虚拟机，所以要创建多节点swarm集群的话，就需要额外启动其他的虚拟机，并手动安装和配置docker。不过借助dind (docker in docker)，不需要创建额外的虚拟机也可以启动一个swarm集群。

```sh
docker swarm init
SWARM_TOKEN=$(docker swarm join-token -q worker)
NUM_WORKERS=3 

for i in $(seq "${NUM_WORKERS}"); do
    docker run -d --privileged --name worker-${i} --hostname=worker-${i} --restart=always -p ${i}2375:2375 docker:1.12-dind
    docker --host=localhost:${i}2375 swarm join --token ${SWARM_TOKEN} ${SWARM_MASTER}:2377
done

```

这时，查询系统的node列表为:

```sh
$ docker node ls
ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
82rg1gpkhm5fajnexre6p0v34 *  moby      Ready   Active        Leader
a0hhwgtqsxosx9gg6h6wqmx68    worker-3  Ready   Active
bn93fte7yflatee3y88qq7ff0    worker-1  Ready   Active
emy5y7qr2y26hk3dtqgkvnak3    worker-2  Ready   Active
```

当然，也可以启动一个由Mano Marks创建的swarm集群可视化容器，更直观的查看集群的状态：

```
docker run -it -d -p 8000:8080 -v /var/run/docker.sock:/var/run/docker.sock manomarks/visualizer
```

![](/images/docker_visualizer.png)

### docker v1.11-

对于docker v1.11以及以下的版本，可以借助swarm镜像来创建swarm集群：

安装swarm的最简单的方式是使用Docker官方的swarm镜像

> $ sudo docker pull swarm 

可以使用下面的命令来查看swarm是否成功安装。
 > $ sudo docker run --rm swarm -v
 
 输出下面的形式则表示成功安装(具体输出根据swarm的版本变化)
> swarm version 0.2.0 (48fd993)



参考文档<http://blog.terranillius.com/post/swarm_dind/>。
