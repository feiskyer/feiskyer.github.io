# 快速搭建基于 Docker 的隔离开发环境

使用 `Dockerfile` 文件指定你的应用环境，让它能在任意地方复制使用：

```Dockerfile
FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
```

在 fig.yml 文件中指定应用使用的不同服务，让它们能够在一个独立的环境中一起运行：

**注意不需要再额外安装 Postgres 了！**

接着执行命令 `fig up` ，然后 Fig 就会启动并运行你的应用了。

![Docker](../images/fig-example-large.png)

为你的项目创建一个目录

```sh
$ mkdir figtest
$ cd figtest
```

进入目录，创建 `app.py`，这是一个能够让 Redis 上的一个值自增的简单 web 应用，基于 Flask 框架。

```python
from flask import Flask
from redis import Redis
import os
app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello()
    redis.incr('hits')
    return 'Hello World! I have been seen %s times.' % redis.get('hits')

if __name__ == "__main__"
    app.run(host="0.0.0.0", debug=True)
```

在 `requirements.txt` 文件中指定应用的 Python 依赖包。

```sh
flask
redis
```

下一步我们要创建一个包含应用所有依赖的 Docker 镜像，这里将阐述怎么通过 `Dockerfile` 文件来创建。

```Dockerfile
FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
```

以上的内容首先告诉 Docker 在容器里面安装 Python ，代码的路径还有Python 依赖包。关于 Dockerfile 的更多信息可以查看 [镜像创建](../image/create.md#利用 Dockerfile 来创建镜像) 和 [Dockerfile 使用](../dockerfile/README.md)

接着我们通过 `fig.yml` 文件指定一系列的服务.

这里指定了两个服务：

* web 服务，通过当前目录的 `Dockerfile` 创建。并且说明了在容器里面执行`python app.py ` 命令 ，转发在容器里开放的 5000 端口到本地主机的 5000 端口，连接 Redis 服务，并且挂载当前目录到容器里面，这样我们就可以不用重建镜像也能直接使用代码。
* redis 服务，我们使用公用镜像 [redis](https://registry.hub.docker.com/_/redis/)。

现在如果执行 `fig up` 命令 ，它就会拉取 redis 镜像，启动所有的服务。

    $ fig up
    Pulling image redis...
    Building web...
    Starting figtest_redis_1...
    Starting figtest_web_1...
    redis_1 | [8] 02 Jan 18:43:35.576 # Server started, Redis version 2.8.3

`fig run` 指令可以帮你向服务发送命令。例如：查看 web 服务可以获取到的环境变量:

```sh
fig run web env
```

执行帮助命令 `fig --help` 查看其它可用的参数。

假设你使用了 `fig up -d` 启动 Fig，可以通过以下命令停止你的服务：

```sh
fig stop
```

以上内容或多或少的讲述了如何使用Fig 。通过查看下面的引用章节可以了解到关于命令、配置和环境变量的更多细节。如果你有任何想法或建议，[可以在 GitHub 上提出](https://github.com/docker/fig)。
