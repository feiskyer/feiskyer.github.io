---
title: 10 things to avoid in docker containers
date: 2016-03-01 16:33:16
tags: [docker]
---

Redhat发布的[10 things to avoid in docker containers](https://developerblog.redhat.com/2016/02/24/10-things-to-avoid-in-docker-containers/)对于构建基于Container的服务非常有意义。摘录如下：

> 1) Don’t store data in containers – A container can be stopped, destroyed, or replaced. An application version 1.0 running in container should be easily replaced by the version 1.1 without any impact or loss of data. For that reason, if you need to store data, store it in a volume, but take care if two containers write data on the same volume because it could cause corruption.  Make sure your applications are designed to write to shared data stores.

需要持久化的数据存在volume中，这个是共识了。

> 2) Don’t ship your application in two pieces – As some people see containers as a virtual machine. Most of them tend to think that they should deploy their application in existing running containers. That can be true during the development phase where you need to deploy and debug continuously; but for a continuous deployment (cd) pipeline in QA and production, your application should be part of the image. Remember: Containers should be immutable.

无论Container出了啥状况（挂了、要升级了等等），直接干掉并起一个新的。Kubernetes的Replication Controller已经把这个更新过程自动化了。

> 3) Don’t create large images – A large image will only make it hard to distribute. Make sure that you have only the required files and libraries to run your application/process. Don’t install unnecessary packages or run “updates” (yum update) during builds.

镜像尽量做小，分发更为方便。

> 4) Don’t use a single layer image – To have a more rational use of the layered filesystem, always create your own base image layer for your OS, another layer for the security and user definition, another layer for the lib installation, another layer for the configuration, and finally another layer for the application. It will be easy to recreate  and manage an image, and easy to distribute.

镜像分层，更容易维护。如果只有一个layer的话，就没法知道镜像的更新历史了。

> 5) Don’t create images from running containers – In other terms, don’t use “docker commit” to create an image. This way to build an image is not reproducible and it’s not versionable, and should be completely avoided. Always use a Dockerfile or any other S2I (source-to-image) approach that is totally reproducible.

做镜像，Dockerfile是最好的选择。

> 6) Don’t use only the “latest” tag – The latest tag is just like the “SNAPSHOT” for Maven users. Tags are encouraged to be used specially when you have a layered filesytem. You don’t want to have surprises when you build your image 2 months later and figure out that your application can’t run because a top layer was replaced by a new version that it’s not backward compatible or because a wrong “latest” version is in the build cache. The latest should also be avoided when deploying containers in production.

版本问题，时间长了，用latest会出现各种不一致。用固定版本，需要的时候可以升级版本。

> 7) Don’t run more than one process in a single container – Containers are perfect to run a single process (http daemon, application server, database), but if you have more than a single process, you will have troubles to manage, get logs, and update them individually.

为了便于管理、更新和查询日至，每个Container只跑一个进程。

> 8) Don’t store credentials in the image. Use environment variables – You don’t want to hardcode any username/password in you image. Use the environment variables to get that information from outside the container. A great example for it is the postgres image.

敏感数据不要直接放到image中，最好放到环境变量或者volume中。

> 9) Run processes with a non-root user – “By default docker containers run as root. (…) As docker matures, more secure default options may become available. For now, requiring root is dangerous for others and may not be available in all environments. Your image should use the USER instruction to specify a non-root user for containers to run as”. (From Guidance for Docker Image Authors)

安全期间，还是老实用普通用户来允许container吧。最新发布的docker已经支持user namespace了。

> 10) Don’t rely on IP addresses – Each container have their own internal IP address and it could change if you start and stop it. If your application or microservices needs to communicate to another container, use any names and/or environment variables to pass the proper information from one container to another.

Container每次重启，其IP地址都会变化。所以，不要直接依赖IP地址来通信，使用环境变量或者DNS。
