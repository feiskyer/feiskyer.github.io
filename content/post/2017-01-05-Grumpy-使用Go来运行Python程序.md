---
title: 'Grumpy: 使用Go来运行Python程序'
date: 2017-01-05 17:11:09
tags: [Go]
---

Grumpy是Google近期开源（[https://github.com/google/grumpy](https://github.com/google/grumpy)）的把Python程序编译成Go程序的工具，主要是为了解决Python GIL（Global Interpreter Lock）锁的问题，把Python中的多线程转换成goroutine来避免锁的问题。注意它跟PyPy不一样，PyPy是一个Python解释器，而Grumpy不是，它只是把Python程序翻译成了Go程序，然后再编译运行。

Grumpy还在开发中，也还没有在Google的生产环境中使用，很多系统库还没有完成翻译，并且也不支持各种外部库和C扩展。虽然如此，Grumpy仍然是一个值得关注的有趣项目（Github已经有2700+的star）。

## 简单使用

```sh
$ git clone https://github.com/google/grumpy.git
$ cd grumpy
$ echo "print 'hello, world'" | make run
hello, world
```

当然，也可以把程序翻译成Go再运行:

```sh
echo 'print "hello, world"' > hello.py
make
export GOPATH=$PWD/build
export PYTHONPATH=$PWD/build/lib/python2.7/site-packages

tools/grumpc hello.py > hello.go
go build -o hello hello.go
./hello
```
