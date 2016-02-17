---
layout: post
title: "Using cAdvisor to monitor docker"
description: ""
category: Docker
tags: [docker]
---

cAdvisor (Container Advisor) provides container users an understanding of the resource usage and performance characteristics of their running containers. It is a running daemon that collects, aggregates, processes, and exports information about running containers. Specifically, for each container it keeps resource isolation parameters, historical resource usage, histograms of complete historical resource usage and network statistics. This data is exported by container and machine-wide.

cAdvisor has native support for Docker containers and should support just about any other container type out of the box. We strive for support accross the board so feel free to open an issue if that is not the case. cAdvisor's container abstraction is based on lmctfy's so containers are inherently nested hierarchically.

To quickly tryout cAdvisor on your machine with Docker, we have a Docker image that includes everything you need to get started. Simply run:

```
sudo docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:rw \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  --detach=true \
  --name=cadvisor \
  google/cadvisor:latest
```

cAdvisor is now running (in the background) on `http://localhost:8080`. The setup includes directories with Docker state cAdvisor needs to observe

![](/images/cadvisor.png)

See more at <https://github.com/google/cadvisor>.

