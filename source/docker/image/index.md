---
layout: "post"
---


# Docker 镜像

在之前的介绍中，我们知道镜像是 Docker 的三大组件之一。

Docker 运行容器前需要本地存在对应的镜像，如果镜像不存在本地，Docker 会从镜像仓库下载（默认是 Docker Hub 公共注册服务器中的仓库）。

本章将介绍更多关于镜像的内容，包括：

* 从仓库获取镜像；
* 管理本地主机上的镜像；
* 介绍镜像实现的基本原理。

**目录**

* [获取镜像](pull.html)
* [列出](list.html)
* [创建](create.html)
* [存出和载入](save_load.html)
* [移除](rmi.html)
* [实现原理](internal.html)

## v1.13+

从docker v1.13开始，镜像相关的操作都被放到了`docker image`的子命令里。

```sh
cat >Dockerfile <<EOF
FROM alpine
RUN apk update && apk add curl && rm -rf /var/cache/apk/*
ENTRYPOINT ["sh"]
EOF

# To build an image from a Dockerfile
docker image build -t curl .
# To show the history of an image
docker image history curl

# To import the contents from a tarball to create a filesystem image
docker image import <file-name> <image-name>
# To display low-level information of a image
docker image inspect curl

# To load an image from a tar archive or STDIN
docker image load -i <file-name>

#To list images
docker image ls|list|images

# To remove unused images
docker image prune --force

# To pull an image from a registry
docker image pull <image-name:tag>

# To push an image to a registry
docker image push <image-name:tag>

# To remove a image
docker image rm <image-id/name>

# To save an image to a tar archive
docker image save <image-name>

# To create a tag for a image
docker image tag <old-image-name> <new-image-name>
```