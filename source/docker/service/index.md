---
layout: "post"
---

# Service

从docker v1.12开始，service可以用来更方便的管理容器服务，一个service就是一组相同功能的容器，并且docker内置了服务发现和基于lvs的负载均衡。

```sh
# To create a new service
docker service create --name nginx nginx

# To display detailed information of a service
docker service inspect nginx

# To list services
docker service ls

# To list the tasks of a service
docker service ps nginx

# To scale one or multiple replicated services
docker service scale nginx=3
# To update a service
docker service update --publish-add=80 nginx

# To view logs of this service
docker service logs -f nginx

# To remove a service
docker service rm nginx
```