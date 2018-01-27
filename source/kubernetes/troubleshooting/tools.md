---
title: Troubleshooting Tools for Kubernetes
date: 2018-01-27 20:11:07
layout: "post"
---

This chapter is about tools for troubleshooting kubernetes.

### Essential tools

* kubectl: for interacting with kubernetes cluster
* journalctl：for viewing logs
* iptables：for debugging service problems
* tcpdump：for debugging network problems

### sysdig

[sysdig](https://www.sysdig.org/) is a container troubleshooting tools, which provides both opensource and commercial products. For regular troubleshooting, I believe opensourced version is enough.

On top of sysdig, you can also use csysdig and [sysdig-inspect](https://github.com/draios/sysdig-inspect) as command line interface and GUI.

#### Setup

```sh
# on Linux
curl -s https://s3.amazonaws.com/download.draios.com/stable/install-sysdig | sudo bash

# on MacOS
brew install sysdig
```

#### Examples

```sh
# Refer https://www.sysdig.org/wiki/sysdig-examples/.
# View the top network connections for a single container
sysdig -pc -c topconns

# Show the network data exchanged with the host 192.168.0.1
sysdig -s2000 -A -c echo_fds fd.cip=192.168.0.1

# List all the incoming connections that are not served by apache.
sysdig -p"%proc.name %fd.name" "evt.type=accept and proc.name!=httpd"

# View the CPU/Network/IO usage of the processes running inside the container.
sysdig -pc -c topprocs_cpu container.id=2e854c4525b8
sysdig -pc -c topprocs_net container.id=2e854c4525b8
sysdig -pc -c topfiles_bytes container.id=2e854c4525b8

# See the files where apache spends the most time doing I/O
sysdig -c topfiles_time proc.name=httpd

# Show all the interactive commands executed inside a given container.
sysdig -pc -c spy_users

# Show every time a file is opened under /etc.
sysdig evt.type=open and fd.name
```

### References

- [Overview of kubectl](https://kubernetes.io/docs/reference/kubectl/overview/)
- [Monitoring Kuberietes with sysdig](https://sysdig.com/blog/kubernetes-service-discovery-docker/)
