---
title: "gPRC"
layout: "post"
---

gPRC是基于HTTP/2的开源高性能PRC框架，它基于Protocol Buffer序列化协议，并支持Java、Go、C++、Python、Node.js、Ruby、PHP等主流编程语言。

gPRC使用非常简单，它根据用户提供的proto文件自动生成服务器端和客户端框架，而用户只需要实现框架的部分接口即可。一个简单的proto示例为

```proto
syntax = "proto3";

message HelloRequest {
    string greeting = 1;
}

message HelloResponse {
    string reply = 1;
}

service HelloService {
rpc SayHello(HelloRequest) returns (HelloResponse);
}
```

## 示例

```sh
# install protobuf and grpc
git clone https://github.com/google/protobuf
cd protobuf
./autogen.sh
./configure
make
make install

# install protoc plugin
go get -u google.golang.org/grpc
go get -u github.com/golang/protobuf/{proto,protoc-gen-go}

# generate go files
cd $GOPATH/src/google.golang.org/grpc/examples/helloworld/helloworld
protoc --go_out=plugins=grpc:. helloworld.proto

# run hello demo
cd GOPATH/src/google.golang.org/grpc/examples/helloworld
go run greeter_server/main.go &
go run greeter_client/main.go
```

## 参考文档

- <https://grpc.io/>
