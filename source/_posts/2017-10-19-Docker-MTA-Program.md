---
layout: post
title: Docker MTA Program
date: 2017-10-19 18:10:18
tags: docker
---

在容器化和云原生的大潮下，很多公司都已经开始了容器化的进程。然而，将已有应用转化为容器和云原生架构并不容易，并且这些遗留应用的维护可能会花费80%的精力。如果能够自动的将这些应用转化为容器应用，显然会是一个巨大的市场。Docker也看到了这个市场，并在 DockerCon EU (2017) 上发布了[Modernize Traditional Applications (MTA) program](https://goto.docker.com/MTAkit.html)，它由 咨询服务、Docker EE以及合作伙伴提供的混合云基础架构组成。首批MTA的合作伙伴包括Avanade, Booz Allen, Cisco, HPE 和 Microsoft 等。

![](/images/15084061914987.jpg)

![](/images/15084061314764.jpg)

![](/images/15084061439253.jpg)

## POC

Docker也提供了两个POC（Proof of Concept）项目

- [Image2Docker](https://github.com/docker/communitytools-image2docker-win)：将已有的Windows应用转换为Docker容器
- [v2c](https://github.com/docker/communitytools-image2docker-linux)：Image2Docker的Linux版本

## 参考文档

- [INTRODUCING THE MODERNIZE TRADITIONAL APPS PROGRAM](https://blog.docker.com/2017/04/modernizing-traditional-apps-with-docker/)
- [THE DOCKER MODERNIZE TRADITIONAL APPS (MTA) PROGRAM ADDS MICROSOFT AZURE STACK](https://blog.docker.com/2017/09/docker-modernize-traditional-apps-mta-program-adds-microsoft-azure-stack/)
- [Docker MTA program](https://goto.docker.com/MTAkit.html)

