layout: "post"
title: "Hello world to Docker Mac"
date: "2016-04-15 16:34"
---

终于等到了Docker for Mac。如之前期待的，体验真的很棒：

- 安装简单了，标准的Mac Application
    ![](/images/docker-mac-setting.png)
- VPN无障碍
- 原生的（osxfs）文件系统共享（其实还支持9p方式）
- Docker Application管理 xhyve VM，更改配置后会自动重启
- 速度快，在使用体验上跟在Linux上面已经差别不大
- 可以与docker toolbox共存：Docker for Mac也会像Linux上面一样监听一个`/var/run/docker.sock`，这样客户端默认情况下就会走它的API；但也可以通过环境变量告诉docker CLI调用其他Docker Daemon的API（比如docker-machine管理的vm等）

![](/images/docker-for-mac-and-toolbox.png)


跑一个nginx试试：

```sh
➜  ~ docker version
Client:
 Version:      1.11.0
 API version:  1.23
 Go version:   go1.5.4
 Git commit:   4dc5990
 Built:        Wed Apr 13 19:36:04 2016
 OS/Arch:      darwin/amd64

Server:
 Version:      1.11.0
 API version:  1.23
 Go version:   go1.5.4
 Git commit:   a5315b8
 Built:        Thu Apr 14 10:19:52 2016
 OS/Arch:      linux/amd64
➜  ~
➜  ~ ls /var/run/docker.sock
/var/run/docker.sock
➜  ~ docker run -itd -p 9191:80 nginx
53a8b3d5f1846273e10ff08086c679695d7f0536a9678e49b44990806ce03d54

➜  ~ curl localhost:9191
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

当然了，由于还是Beta版，小问题还是有的。不过感觉目前的状态已经可以替代Linux vm作大部分的开发测试了。

