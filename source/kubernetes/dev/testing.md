---
layout: "post"
---

# Kubernetes测试

## 单元测试

单元测试直接运行`go test`命令即可，比如

```sh
go test -v k8s.io/kubernetes/pkg/kubelet
```

## End to end (e2e)测试

e2e测试相对麻烦些，本地e2e测试的方法为：

```sh
make WHAT='test/e2e/e2e.test'
make ginkgo
export KUBERNETES_PROVIDER=local

# 只测试某个case
go run hack/e2e.go -v -test --test_args='--ginkgo.focus=Kubectl\sclient\s\[k8s\.io\]\sKubectl\srolling\-update\sshould\ssupport\srolling\-update\sto\ssame\simage\s\[Conformance\]$'
```

## Node e2e测试

```sh
export KUBERNETES_PROVIDER=local
make test-e2e-node FOCUS="InitContainer"
```

## 辅助工具

有时可以借助kubectl的模版来获取想要的数据，比如查询某个container的镜像的方法为

```sh
kubectl get pods nginx-4263166205-ggst4 -o template '--template={{if (exists . "status" "containerStatuses")}}{{range .status.containerStatuses}}{{if eq .name "nginx"}}{{.image}}{{end}}{{end}}{{end}}'
```
