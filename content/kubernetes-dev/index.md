---
title: Kubernetes Development
date: 2016-10-21 16:11:07
type: page
---

# Tips for kubernetes development

## Setup development virtual machine

```sh
apt-get install -y gcc make socat git

# install docker
curl -fsSL https://get.docker.com/ | sh

# install etcd
curl -L https://github.com/coreos/etcd/releases/download/v3.0.10/etcd-v3.0.10-linux-amd64.tar.gz -o etcd-v3.0.10-linux-amd64.tar.gz && tar xzvf etcd-v3.0.10-linux-amd64.tar.gz && /bin/cp -f etcd-v3.0.10-linux-amd64/{etcd,etcdctl} /usr/bin && rm -rf etcd-v3.0.10-linux-amd64*

# install golang
curl -sL https://storage.googleapis.com/golang/go1.8.linux-amd64.tar.gz | tar -C /usr/local -zxf -
export GOPATH=/gopath
export PATH=$PATH:$GOPATH/bin:/usr/local/bin:/usr/local/go/bin/

# Get kubernetes code
mkdir -p $GOPATH/src/k8s.io
git clone https://github.com/kubernetes/kubernetes $GOPATH/src/k8s.io/kubernetes
cd $GOPATH/src/k8s.io/kubernetes

# Start a local cluster
export KUBERNETES_PROVIDER=local
hack/local-up-cluster.sh
```

Setup kubectl in another shell:

```sh
export KUBERNETES_PROVIDER=local
cluster/kubectl.sh config set-cluster local --server=http://127.0.0.1:8080 --insecure-skip-tls-verify=true
cluster/kubectl.sh config set-context local --cluster=local
cluster/kubectl.sh config use-context local
```

## Kubelet dockershim mode

```
kubelet --experimental-dockershim --v=3 --logtostderr
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

go test with ginkgo focus

```
go test -v -ginkgo.focus='Test streaming in container'
```

## Running node e2e locally

```sh
# running a node e2e with frakti runtime
export KUBERNETES_PROVIDER=local
make test-e2e-node PARALLELISM=2 CONTAINER_RUNTIME_ENDPOINT=/var/run/frakti.sock RUNTIME=remote FOCUS="\[Conformance\]"
```

## Bot commands

- Run all tests: `@k8s-bot test this`
- Allow PR author to test: `@k8s-bot ok to test`
- Jenkins Bazel Build `@k8s-bot bazel test this`
- Jenkins unit/integration `@k8s-bot unit test this`
- Jenkins GKE smoke e2e `@k8s-bot cvm gke e2e test this`
- Jenkins non-CRI GCE Node e2e `@k8s-bot non-cri node e2e test this`
- Jenkins kops AWS e2e `@k8s-bot kops aws e2e test this`
- Jenkins GCE etcd3 e2e `@k8s-bot gce etcd3 e2e test this`
- Jenkins GCI GKE smoke e2e `@k8s-bot gci gke e2e test this`
- Jenkins GCI GCE e2e `@k8s-bot gci gce e2e test this`
- Jenkins GCE e2e    `@k8s-bot cvm gce e2e test this`
- Jenkins non-CRI GCE  `@k8s-bot non-cri e2e test this`
- Jenkins GCE Node e2e `@k8s-bot node e2e test this`
- Jenkins Kubemark GCE e2e `@k8s-bot kubemark e2e test this`
- See more commands at <https://github.com/kubernetes/test-infra/blob/master/prow/jobs.yaml>

**Auto LGTM (only applied if you are one of assignees):**

- `/lgtm` and `/lgtm cancel`
- `/assign @userA @userB` and `/unassign`
- `/close`
- `/release-note`
- `/release-note-none`

Check more commands at [kubernetes test-infra](https://github.com/kubernetes/test-infra/blob/master/prow/commands.md).

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
    - v1.5.1
    - v1.4.3
    ...

# http proxy is required in China
$ minikube start --docker-env HTTP_PROXY=http://proxy-ip:port --docker-env HTTPS_PROXY=http://proxy-ip:port --vm-driver=xhyve
```
