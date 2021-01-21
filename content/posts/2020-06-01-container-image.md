---
title: "镜像构建的正确姿势"
date: 2020-06-01
tags: [CloudNative, Kubernetes]
draft: false
---

## Dockerfile

什么是 Dockerfile ？Dockerfile 是一个用来描述镜像构建指令的文本文件。构建系统可以按照这些指令一步步地执行构建出容器镜像。

比如，下面是一个最简单的 Dockerfile：

```
FROM busybox
ENTRYPOINT ["echo", "Hello world, Dockerfile!"]
```

这个 Dockerfile 只包括两条指令：

- FROM 指定 busybox 作为基础镜像，后续所有的指令都在 busybox 镜像基础上进行；
- ENTRYPOINT 设置容器的启动命令。容器创建时，如果没有指定启动命令，这条命令就会执行。

有了 Dockerfile 之后，你就可以用 *docker build* 来构建一个镜像。比如，执行下面的命令构建一个镜像：

```
$ docker build -t feisky/hello .
Sending build context to Docker daemon  2.048kB
Step 1/2 : FROM busybox
latest: Pulling from library/busybox
bdbbaa22dec6: Pull complete
Digest: sha256:6915be4043561d64e0ab0f8f098dc2ac48e077fe23f488ac24b665166898115a
Status: Downloaded newer image for busybox:latest
 ---> 6d5fcfe5ff17
Step 2/2 : ENTRYPOINT ["echo", "Hello world, Dockerfile!"]
 ---> Running in 8647d01c193e
Removing intermediate container 8647d01c193e
 ---> 0eebd98120f4
Successfully built 0eebd98120f4
Successfully tagged feisky/hello:latest
```

这样，我们就成功构建了第一个镜像，它的各层如下图所示。其中，最下面的两层来自基础镜像 busybox，而最上面的一层来自 ENTRYPOINT 指令：

![图片](640-20210121132330027.png)

接下来也就可以使用刚创建的镜像来运行容器：

```
# --rm 表示容器停止后自动删除
$ docker run --rm feisky/hello
Hello world, Dockerfile!
```

可以看到，容器成功输出了 *Hello world, Dockerfile!*。

刚才的示例很简单，只涉及了两条指令 FROM 和 ENTRYPOINT。而实际的应用通常都要复杂得多，只通过 Dockerfile 的指令真的可以给各种各样的应用创建镜像吗？我们再来进一步看看 Dockerfile 到底是如何解决这个问题的：

第一，通过 RUN 支持运行任何 SHELL 或者 POWERSHELL 命令，这样你就可以运行任意指令，灵活定制镜像的内容。

第二，通过 ADD 和 COPY 支持将文件和目录复制到镜像中，这样就可以给镜像添加任意文件。

第三，通过 FROM 从基础镜像开始，而不是一切从零开始。任何已有镜像都可以作为新镜像的基础，这样运行环境类似的应用就都可以复用相同的基础镜像，简化了新镜像的构建过程。

通过这三个特性，你就可以为大部分应用准备好它们的运行环境。当然，只有这些是不够的。实际上，Dockerfile 还支持十多个指令，以便你可以更灵活地定制镜像。

|  **指令**  |         **说明**          |      **示例**       |
| :--------: | :-----------------------: | :-----------------: |
|    FROM    |       设置基础镜像        |     FROM alpine     |
|   LABEL    |       设置镜像标签        | LABEL version="1.0" |
|    RUN     | 运行SHELL或POWERSHELL命令 |  RUN apk add curl   |
| ADD或COPY  |     复制文件到镜像中      |    ADD app /app     |
|    USER    |      设置用户名或UID      |      USER 1001      |
|    ENV     |       设置环境变量        |   ENV GOPATH /go    |
|   EXPOSE   |       暴露指定端口        |      EXPOSE 80      |
| ENTRYPOINT |       设置默认命令        | ENTRYPOINT ["/app"] |
|    CMD     |    设置ENTRYPOINT参数     |   CMD ["--help"]    |
|  WORKDIR   |       设置工作目录        |    WORKDIR /path    |

这些指令中，有两组需要你特别留心。

第一组是复制文件的两个指令，**COPY 和 ADD**。COPY 可以从本地复制文件或者目录到镜像中，而 ADD 则是 COPY 的超集，除了可以复制文件或者目录外，还可以远程下载文件并解压压缩包。由于 ADD 的功能比较复杂，我推荐你优先使用 COPY 指令。需要从远程下载文件时，可以使用 RUN 把所有需要下载的文件以及清理步骤放到一个指令中。

第二组是设置容器命令的两个指令，**ENTRYPOINT 和 CMD**。这两个指令都支持 exec 和 shell 两种模式：

- exec 模式是把应用程序进程作为容器的 1 号进程。比如，*ENTRYPOINT ["top", "-b"]* 就是以 top 命令作为 1 号进程。
- shell 模式则是通过 SHELL命令启动应用。比如，*ENTRYPOINT top -b* 就是以 */bin/sh -c top -b* 启动容器，即 */bin/sh* 是容器的 1 号进程。使用 SHELL 作为 1 号进程时，很容易导致应用无法在容器停止时优雅地关闭，所以一般需要你结合 *exec* ，将应用进程取代 SHELL 作为 1 号进程，比如  *ENTRYPOINT exec top -b*。

在 ENTRYPOINT 和 CMD 组合使用时，还有一点需要你注意，即当 ENTRYPOINT 使用 shell 模式时，CMD 设置的任何选项都会被忽略。所以我推荐你在设置 ENTRYPOINT 时，总是使用 exec 模式。

## 构建上下文

在上一节我们讲到，你可以使用 COPY 指令把文件复制到镜像中。不过，要复制的文件从哪里来呢？

在前面的 docker build 示例中，你可能已经注意到了最后的点（.），它正是用来指定构建上下文的，也就是把当前目录作为构建上下文。从前面的示例中你可以看到，构建镜像的第一步就是把构建上下文发送到 Docker daemon：

```
Sending build context to Docker daemon  2.048kB
```

这说明镜像构建是在 Docker daemon 中运行的，并且客户端会把构建上下文先发送给 Docker daemon 之后才可以进行镜像构建。所以，为了减少镜像构建上下文的大小，通常把 Dockerfile 放到一个只包含镜像所需文件的单独目录中。

如果构建目录中还有其他镜像不需要的文件，可以通过 *.dockerignore* 将它们忽略。*.dockerignore* 类似于 *.gitignore*，它基于 Go 语言的 filepath.Match ，匹配每一行设置的表达式，忽略匹配的文件。比如：

```
# 忽略所有的go文件
**/*.go
# 忽略README.md之外的所有markdown文件
*.md
!README.md
```

这个示例忽略了所有的go文件以及除了README.md之外的所有markdown文件。在编写 Dockerfile 时，不要忘记添加一个 .dockerignore 文件，把镜像不需要的文件剔除掉。

## 镜像优化

了解了 Dockerfile 的基本原理之后，在镜像构建时还有没有其他需要注意的地方呢？接下来，我们再一起来看看都有哪些镜像构建的最佳实践。

**第一，为了降低复杂性并减少依赖，你应该尽量避免镜像包含不必要的软件包**。通常，应用程序的镜像中一般不需要安装开发调试软件包。如果真的需要从源码编译构建应用，那就使用多阶段构建。

比如，下面是一个两阶段构建 Go 应用程序的示例，第一阶段使用 golang:1.13 编译出应用二进制文件，第二阶段再把编译的结果复制到最终的镜像中：

```
FROM golang:1.13 AS builder
WORKDIR /go/src/my-app
COPY . .
RUN go build -a -o app .
FROM alpine:latest  
RUN apk --no-cache add ca-certificates
COPY --from=builder /go/src/my-app/app .
CMD ["./app"]
```

**第二，为了方便镜像的维护，并减少镜像的大小，镜像的层数应尽可能少**。 比如，你应该把软件包的安装和缓存清理放到同一个 *RUN* 指令中，避免把不必要的缓存文件提交到镜像中。

以 *centos* 镜像为例，把缓存清理放到单独指令中会让镜像总大小增加约 30MB：

![图片](640-20210121132407454.png)

你可以使用下面的方法把 yum install 和 yum clean 放在同一个 RUN 指令中来减小镜像的大小：

```
FROM centos
RUN yum update --assumeyes && \
    yum install --assumeyes vim && \
    yum clean all
```

**第三，选择最小的基础镜像**。比如，centos 基础镜像的大小已经达到了 220MB，如果换成 alpine 的话，则只有 5MB 的大小。除了可以让镜像体积变小之外，更小的基础镜像因为包含更少的软件包，也降低了意外漏洞的风险。

**第四，以最小权限用户运行应用程序**。默认情况下，容器内的root用户跟宿主机的root用户是同一个，以root用户运行的容器也会有宿主机root用户的特权。根据最小权限原则，你应该尽量限制容器的访问权限，避免以root用户运行应用。比如下面的例子中，使用 USER 指令为镜像设置了一个普通用户 node：

```
FROM node:alpine
WORKDIR /app
USER node
COPY --chown=node:node . .
CMD ["node", "app.js"]
```

**最后，利用缓存加速构建**。docker build 按照 Dockerfile 中指令的顺序逐个执行，并把每个指令的构建结果缓存起来，这样下次构建的时候就可以进行复用，减少构建时间。不过你要注意，只要有一条指令跟缓存不一致，那么其后所有的指令都不会再复用缓存。所以，我推荐你尽量把很少变化的指令放到前面，而经常变化的指令（比如 COPY 和 CMD）放到后面。

## 小结

本文总结了容器镜像的构建方法，并梳理了构建镜像时的注意事项。在构建镜像时，最基本的原则是**小巧安全、适当复用**。选择小的基础镜像、避免安装不必要的软件包、减少镜像层数、最小化容器用户的权限等都是实现这个原则的有效方法。在镜像构建的时候，你还可以利用镜像构建的缓存，加速镜像的构建。


---

欢迎扫描下面的二维码关注**漫谈云原生**公众号，回复**任意关键字**查询更多云原生知识库，或回复**联系**加我微信。

![](/assets/mp.png)