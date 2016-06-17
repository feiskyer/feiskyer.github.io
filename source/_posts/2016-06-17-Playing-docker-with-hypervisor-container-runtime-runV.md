---
title: Playing docker with hypervisor container runtime runV
date: 2016-06-17 17:12:38
tags: [docker, runV]
---

The latest master branch of [runV](https://github.com/hyperhq/runv) has already supported running as an runtime in docker. Since v1.11, docker introduced OCI contain runtime (runc) integration via containerd. Since runc and runV are both [recommended implementation of OCI](https://github.com/opencontainers/runtime-spec/blob/master/implementations.md), it is natural to make runV working with containerd. 

Now let's have a try.

### Install runv and docker

Docker could be installed via <https://docs.docker.com/engine/installation/>.

Since only master branch of runV supports running integrated with docker, we should compile runV by source.

```sh
sudo apt-get install -y autoconf automake pkg-config libdevmapper-dev libsqlite3-dev libvirt-dev qemu libvirt-bin
mkdir -p $GOPATH/src/github.com/hyperhq
cd $GOPATH/src/github.com/hyperhq
git clone https://github.com/hyperhq/runv
cd runv
./autogen.sh
./configure
make
make install
```

### Start docker with runV runtime

Stop docker first since it is running with runc by default.

```sh
systemctl stop docker
```

Now start docker with runV:

```sh
# start containerd
systemd-run --unit=containerd-runv docker-containerd --debug -l /var/run/docker/libcontainerd/docker-containerd.sock --runtime /usr/local/bin/runv --runtime-args --debug --runtime-args --driver=libvirt --runtime-args --kernel=/var/lib/hyper/kernel --runtime-args --initrd=/var/lib/hyper/hyper-initrd.img --start-timeout 2m

# start docker
systemd-run --unit=docker-runv docker daemon -D -l debug --containerd=/var/run/docker/libcontainerd/docker-containerd.sock

# check status
[root@linux ~]# systemctl status containerd-runv
● containerd-runv.service - /usr/bin/docker-containerd --debug -l /var/run/docker/libcontainerd/docker-containerd.sock --runtime /usr/local/bin/runv --runtime-args --debug --runtime-args --driver=libvirt --runtime-args --kernel=/var/lib/hyper/kernel --runtime-args --initrd=/var/lib/hyper/hyper-initrd.img --start-timeout 2m
   Loaded: loaded (/run/systemd/system/containerd-runv.service; static; vendor preset: disabled)
  Drop-In: /run/systemd/system/containerd-runv.service.d
           └─50-Description.conf, 50-ExecStart.conf
   Active: active (running) since 五 2016-06-17 09:47:57 UTC; 10s ago
 Main PID: 12650 (docker-containe)
   Memory: 1.8M
   CGroup: /system.slice/containerd-runv.service
           └─12650 /usr/bin/docker-containerd --debug -l /var/run/docker/libcontainerd/docker-containerd.sock --run...

6月 17 09:47:57 linux systemd[1]: Started /usr/bin/docker-containerd --debug -l /var/run/docker/libcontainerd/docker...
6月 17 09:47:57 linux systemd[1]: Starting /usr/bin/docker-containerd --debug -l /var/run/docker/libcontainerd/docke...
6月 17 09:47:57 linux docker-containerd[12650]: time="2016-06-17T09:47:57Z" level=warning msg="containerd: low ...=4096
6月 17 09:47:57 linux docker-containerd[12650]: time="2016-06-17T09:47:57Z" level=debug msg="containerd: read p...unt=0
6月 17 09:47:57 linux docker-containerd[12650]: time="2016-06-17T09:47:57Z" level=debug msg="containerd: superv...nerd"
6月 17 09:47:57 linux docker-containerd[12650]: time="2016-06-17T09:47:57Z" level=debug msg="containerd: grpc a...sock"
Hint: Some lines were ellipsized, use -l to show in full.

[root@linux ~]# systemctl status docker-runv
● docker-runv.service - /usr/bin/docker daemon -D -l debug --containerd=/var/run/docker/libcontainerd/docker-containerd.sock
   Loaded: loaded (/run/systemd/system/docker-runv.service; static; vendor preset: disabled)
  Drop-In: /run/systemd/system/docker-runv.service.d
           └─50-Description.conf, 50-ExecStart.conf
   Active: active (running) since 五 2016-06-17 09:34:11 UTC; 25s ago
 Main PID: 11120 (docker)
   Memory: 20.8M
   CGroup: /system.slice/docker-runv.service
           └─11120 /usr/bin/docker daemon -D -l debug --containerd=/var/run/docker/libcontainerd/docker-containerd.sock

6月 17 09:34:13 linux docker[11120]: time="2016-06-17T09:34:13.019309548Z" level=debug msg="Registering POST, /volumes/create"
6月 17 09:34:13 linux docker[11120]: time="2016-06-17T09:34:13.019448115Z" level=debug msg="Registering DELETE, /volumes/{name:.*}"
6月 17 09:34:13 linux docker[11120]: time="2016-06-17T09:34:13.019551244Z" level=debug msg="Registering POST, /build"
6月 17 09:34:13 linux docker[11120]: time="2016-06-17T09:34:13.019607895Z" level=debug msg="Registering GET, /networks"
6月 17 09:34:13 linux docker[11120]: time="2016-06-17T09:34:13.019675700Z" level=debug msg="Registering GET, /networks/{id:.*}"
6月 17 09:34:13 linux docker[11120]: time="2016-06-17T09:34:13.019771551Z" level=debug msg="Registering POST, /networks/create"
6月 17 09:34:13 linux docker[11120]: time="2016-06-17T09:34:13.020256142Z" level=debug msg="Registering POST, /networks/{id:.*}/connect"
6月 17 09:34:13 linux docker[11120]: time="2016-06-17T09:34:13.020369131Z" level=debug msg="Registering POST, /networks/{id:.*}/disconnect"
6月 17 09:34:13 linux docker[11120]: time="2016-06-17T09:34:13.020463042Z" level=debug msg="Registering DELETE, /networks/{id:.*}"
6月 17 09:34:13 linux docker[11120]: time="2016-06-17T09:34:13.021491071Z" level=info msg="API listen on /var/run/docker.sock"
```

### Create container 

Let's create a nginx container.

```sh
[root@linux ~]# docker run -i -d  nginx
6a34a0513ebbdb2c57d828bf4e814773c8a5cf6af8c35e4376f2028769a7c35c
[root@linux ~]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
6a34a0513ebb        nginx               "nginx -g 'daemon off"   9 seconds ago       Up 3 seconds        80/tcp, 443/tcp     berserk_mcnulty

# Is it working
[root@linux ~]# docker inspect --format '{{ .NetworkSettings.IPAddress }}' 6a34a0513ebb
172.17.0.2
[root@linux ~]# curl -I 172.17.0.2
HTTP/1.1 200 OK
Server: nginx/1.11.1
Date: Fri, 17 Jun 2016 09:52:37 GMT
Content-Type: text/html
Content-Length: 612
Last-Modified: Tue, 31 May 2016 14:40:22 GMT
Connection: keep-alive
ETag: "574da256-264"
Accept-Ranges: bytes
```

Is the container really running in runV with hypervisor?

```sh
root@linux ~]# runv list
ID                                                                 PID         STATUS      BUNDLE                                                                                           CREATED
6a34a0513ebbdb2c57d828bf4e814773c8a5cf6af8c35e4376f2028769a7c35c   12756       running     /var/run/docker/libcontainerd/6a34a0513ebbdb2c57d828bf4e814773c8a5cf6af8c35e4376f2028769a7c35c   2016-06-17T09:48:38.324839156Z

[root@linux ~]# runv state 6a34a0513ebbdb2c57d828bf4e814773c8a5cf6af8c35e4376f2028769a7c35c
{
  "ociVersion": "0.6.0-dev",
  "id": "6a34a0513ebbdb2c57d828bf4e814773c8a5cf6af8c35e4376f2028769a7c35c",
  "pid": 12756,
  "bundlePath": "/var/run/docker/libcontainerd/6a34a0513ebbdb2c57d828bf4e814773c8a5cf6af8c35e4376f2028769a7c35c",
  "rootfsPath": "/var/run/docker/libcontainerd/6a34a0513ebbdb2c57d828bf4e814773c8a5cf6af8c35e4376f2028769a7c35c/rootfs",
  "status": "running",
  "created": "2016-06-17T09:48:38.324839156Z"
}

[root@linux ~]# virsh list
 Id    名称                         状态
----------------------------------------------------
 919   vm-CeaKLvbPEg                  running

[root@linux ~]# ps -ef | grep vm-CeaKLvbPEg | grep -v grep
root     12743     1  1 09:48 ?        00:00:06 /usr/bin/qemu-system-x86_64 -name vm-CeaKLvbPEg -S -machine pc-i440fx-2.0,accel=tcg,usb=off -cpu Haswell-noTSX,+abm,+hypervisor,+rdrand,+f16c,+osxsave,+ht,+vme -m 128 -realtime mlock=off -smp 1,sockets=1,cores=1,threads=1 -uuid 4f158103-bd5e-4fd1-a62f-9e18093ceaf4 -nographic -no-user-config -nodefaults -chardev socket,id=charmonitor,path=/var/lib/libvirt/qemu/domain-vm-CeaKLvbPEg/monitor.sock,server,nowait -mon chardev=charmonitor,id=monitor,mode=control -rtc base=utc -no-reboot -boot strict=on -kernel /var/lib/hyper/kernel -initrd /var/lib/hyper/hyper-initrd.img -append console=ttyS0 panic=1 no_timer_check -device virtio-scsi-pci,id=scsi0,bus=pci.0,addr=0x3 -device virtio-serial-pci,id=virtio-serial0,bus=pci.0,addr=0x2 -fsdev local,security_model=none,id=fsdev-fs0,path=/var/run/hyper/vm-CeaKLvbPEg/share_dir -device virtio-9p-pci,id=fs0,fsdev=fsdev-fs0,mount_tag=share_dir,bus=pci.0,addr=0x4 -chardev socket,id=charserial0,path=/var/run/hyper/vm-CeaKLvbPEg/console.sock,server,nowait -device isa-serial,chardev=charserial0,id=serial0 -chardev socket,id=charchannel0,path=/var/run/hyper/vm-CeaKLvbPEg/hyper.sock,server,nowait -device virtserialport,bus=virtio-serial0.0,nr=1,chardev=charchannel0,id=channel0,name=sh.hyper.channel.0 -chardev socket,id=charchannel1,path=/var/run/hyper/vm-CeaKLvbPEg/tty.sock,server,nowait -device virtserialport,bus=virtio-serial0.0,nr=2,chardev=charchannel1,id=channel1,name=sh.hyper.channel.1 -device virtio-balloon-pci,id=balloon0,bus=pci.0,addr=0x5 -msg timestamp=on
```

### Is it stable?

Of course not, runV is still under quick development and features are not complete now. For example, there are a lot of commands not supported now:

- `docker stop`
- `docker stats`
- `docker exec`

Although there are still problems, I'm exited by what runV has done. Looking forward to its release.

