---
title: Kubernetes Development
date: 2016-10-21 16:11:07
---

# Tips for kubernetes development

## Dev in container

```
docker pull feisky/kubernetes-dev
```

## Setup development virtual machine

```sh
apt-get install -y gcc make socat git

# install docker
curl -fsSL https://get.docker.com/ | sh

# install etcd
curl -L https://github.com/coreos/etcd/releases/download/v3.0.10/etcd-v3.0.10-linux-amd64.tar.gz -o etcd-v3.0.10-linux-amd64.tar.gz && tar xzvf etcd-v3.0.10-linux-amd64.tar.gz && /bin/cp -f etcd-v3.0.10-linux-amd64/{etcd,etcdctl} /usr/bin && rm -rf etcd-v3.0.10-linux-amd64*

# install golang
curl -sL https://storage.googleapis.com/golang/go1.7.1.linux-amd64.tar.gz | tar -C /usr/local -zxf -
export GOPATH=/gopath
export PATH=$PATH:$GOPATH/bin:/usr/local/bin:/usr/local/go/bin/

# Get essential tools for building kubernetes
go get -u github.com/jteeuwen/go-bindata/go-bindata

# Get kubernetes code
mkdir -p $GOPATH/src/k8s.io
git clone https://github.com/kubernetes/kubernetes $GOPATH/src/k8s.io/kubernetes
cd $GOPATH/src/k8s.io/kubernetes

# Start a local cluster
# set dockerd --selinux-enabled
export KUBERNETES_PROVIDER=local
export ALLOW_SECURITY_CONTEXT=yes
export EXPERIMENTAL_RUNTIME_INTEGRATION_TYPE=cri
# export NET_PLUGIN=kubenet
hack/local-up-cluster.sh
```

Setup kubectl in another shell:

```sh
export KUBERNETES_PROVIDER=local
cluster/kubectl.sh config set-cluster local --server=http://127.0.0.1:8080 --insecure-skip-tls-verify=true
cluster/kubectl.sh config set-context local --cluster=local
cluster/kubectl.sh config use-context local
```

## Unit tests

```sh
# unit test a special package
go test -v k8s.io/kubernetes/pkg/kubelet/kuberuntime
```

## Running e2e test locally

```sh
make WHAT='test/e2e/e2e.test'
make ginkgo

export KUBERNETES_PROVIDER=local
go run hack/e2e.go -v -test --test_args='--ginkgo.focus=Port\sforwarding'
go run hack/e2e.go -v -test --test_args='--ginkgo.focus=Feature:SecurityContext'
```

## Running node e2e locally

```sh
export KUBERNETES_PROVIDER=local
make test-e2e-node FOCUS="InitContainer" TEST_ARGS="--runtime-integration-type=cri"
```

## Bot commands

- Jenkins verification: `@k8s-bot verify test this`
- GCE E2E: `@k8s-bot cvm gce e2e test this`
- Test all: `@k8s-bot test this please, issue #IGNORE`
- CRI test: `@k8s-bot cri test this.`
- Verity test: `@k8s-bot verify test this`
- See more commands at <https://github.com/kubernetes/test-infra/blob/master/prow/jobs.yaml>

**Auto LGTM (only applied if you are one of assignees):**

- `/lgtm`
- `/lgtm cancel`

## Tips for git

Fetch a pull request to local:

```sh
git fetch upstream pull/324/head:branch
git fetch upstream pull/365/merge:branch
```

Or add following config to `.git/config` and run `git fetch` for all pull requests:

```
    fetch = +refs/pull/*:refs/remotes/origin/pull/*
```

## Start a VM on GCE via docker-machine

```sh
docker-machine create --driver google --google-project xxxx --google-machine-type n1-standard-2 --google-disk-size 30 kubernetes
```

## Minikube for starting local cluster

```sh
$ minikube get-k8s-versions
The following Kubernetes versions are available:
    - v1.5.0-alpha.0
    - v1.4.3
    - v1.4.2
    - v1.4.1
    - v1.4.0
    - v1.3.7
    - v1.3.6
    - v1.3.5
    - v1.3.4
    - v1.3.3
    - v1.3.0

# http proxy is required in China
$ minikube start --docker-env HTTP_PROXY=http://proxy-ip:port --docker-env HTTPS_PROXY=http://proxy-ip:port --vm-driver=xhyve --kubernetes-version="v1.4.3"
```
