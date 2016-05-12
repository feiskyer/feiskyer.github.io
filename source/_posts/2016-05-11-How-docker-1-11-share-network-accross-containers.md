---
title: How docker 1.11 share network accross containers
date: 2016-05-11 10:25:06
tags: [docker]
---

Docker 1.11 has moved to runc with containerd, I am interested in how it processing shared netns accross containers.

For example, I have already running a container 75599a6f387b7842c6da57efd38f9742b2ca621782f891402f83852c66dbd706. A new container within same netns can be created with cmd:

```sh
docker run -itd --net=container:75599a6f387b alpine sh
```

This will generate a runc `config.json` as follows:

```json
{
    "ociVersion": "0.6.0-dev",
    "platform": {
        "os": "linux",
        "arch": "amd64"
    },
    "process": {
        "terminal": true,
        "user": {
            "additionalGids": [
                0,
                1,
                2,
                3,
                4,
                6,
                10,
                11,
                20,
                26,
                27
            ]
        },
        "args": [
            "sh"
        ],
        "env": [
            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
            "HOSTNAME=75599a6f387b",
            "TERM=xterm"
        ],
        "cwd": "/",
        "capabilities": [
            "CAP_CHOWN",
            "CAP_DAC_OVERRIDE",
            "CAP_FSETID",
            "CAP_FOWNER",
            "CAP_MKNOD",
            "CAP_NET_RAW",
            "CAP_SETGID",
            "CAP_SETUID",
            "CAP_SETFCAP",
            "CAP_SETPCAP",
            "CAP_NET_BIND_SERVICE",
            "CAP_SYS_CHROOT",
            "CAP_KILL",
            "CAP_AUDIT_WRITE"
        ]
    },
    "root": {
        "path": "/var/lib/docker/devicemapper/mnt/d33c7932917e64bde482b437fc3ccaad9a00a04e0cf49e39f9d3be5d71991db6/rootfs",
        "readonly": false
    },
    "hostname": "75599a6f387b",
    "mounts": [
        {
            "destination": "/proc",
            "type": "proc",
            "source": "proc",
            "options": [
                "nosuid",
                "noexec",
                "nodev"
            ]
        },
        {
            "destination": "/dev",
            "type": "tmpfs",
            "source": "tmpfs",
            "options": [
                "nosuid",
                "strictatime",
                "mode=755"
            ]
        },
        {
            "destination": "/dev/pts",
            "type": "devpts",
            "source": "devpts",
            "options": [
                "nosuid",
                "noexec",
                "newinstance",
                "ptmxmode=0666",
                "mode=0620",
                "gid=5"
            ]
        },
        {
            "destination": "/sys",
            "type": "sysfs",
            "source": "sysfs",
            "options": [
                "nosuid",
                "noexec",
                "nodev",
                "ro"
            ]
        },
        {
            "destination": "/sys/fs/cgroup",
            "type": "cgroup",
            "source": "cgroup",
            "options": [
                "ro",
                "nosuid",
                "noexec",
                "nodev"
            ]
        },
        {
            "destination": "/dev/mqueue",
            "type": "mqueue",
            "source": "mqueue",
            "options": [
                "nosuid",
                "noexec",
                "nodev"
            ]
        },
        {
            "destination": "/etc/resolv.conf",
            "type": "bind",
            "source": "/var/lib/docker/containers/75599a6f387b7842c6da57efd38f9742b2ca621782f891402f83852c66dbd706/resolv.conf",
            "options": [
                "rbind",
                "rprivate"
            ]
        },
        {
            "destination": "/etc/hostname",
            "type": "bind",
            "source": "/var/lib/docker/containers/75599a6f387b7842c6da57efd38f9742b2ca621782f891402f83852c66dbd706/hostname",
            "options": [
                "rbind",
                "rprivate"
            ]
        },
        {
            "destination": "/etc/hosts",
            "type": "bind",
            "source": "/var/lib/docker/containers/75599a6f387b7842c6da57efd38f9742b2ca621782f891402f83852c66dbd706/hosts",
            "options": [
                "rbind",
                "rprivate"
            ]
        },
        {
            "destination": "/dev/shm",
            "type": "bind",
            "source": "/var/lib/docker/containers/d8230e57e88d15515a94138ef512a4271e31d03bb6fb257b3d57a847e70b5c68/shm",
            "options": [
                "rbind",
                "rprivate"
            ]
        }
    ],
    "hooks": {},
    "linux": {
        "resources": {
            "devices": [
                {
                    "allow": false,
                    "access": "rwm"
                },
                {
                    "allow": true,
                    "type": "c",
                    "major": 1,
                    "minor": 5,
                    "access": "rwm"
                },
                {
                    "allow": true,
                    "type": "c",
                    "major": 1,
                    "minor": 3,
                    "access": "rwm"
                },
                {
                    "allow": true,
                    "type": "c",
                    "major": 1,
                    "minor": 9,
                    "access": "rwm"
                },
                {
                    "allow": true,
                    "type": "c",
                    "major": 1,
                    "minor": 8,
                    "access": "rwm"
                },
                {
                    "allow": true,
                    "type": "c",
                    "major": 5,
                    "minor": 0,
                    "access": "rwm"
                },
                {
                    "allow": true,
                    "type": "c",
                    "major": 5,
                    "minor": 1,
                    "access": "rwm"
                },
                {
                    "allow": false,
                    "type": "c",
                    "major": 10,
                    "minor": 229,
                    "access": "rwm"
                }
            ],
            "disableOOMKiller": false,
            "oomScoreAdj": 0,
            "memory": {
                "kernelTCP": null,
                "swappiness": 18446744073709551615
            },
            "cpu": {},
            "pids": {
                "limit": 0
            },
            "blockIO": {
                "blkioWeight": 0
            }
        },
        "cgroupsPath": "/docker/d8230e57e88d15515a94138ef512a4271e31d03bb6fb257b3d57a847e70b5c68",
        "namespaces": [
            {
                "type": "mount"
            },
            {
                "type": "network",
                "path": "/proc/14702/ns/net"
            },
            {
                "type": "uts"
            },
            {
                "type": "pid"
            },
            {
                "type": "ipc"
            }
        ],
        "devices": [
            {
                "path": "/dev/zero",
                "type": "c",
                "major": 1,
                "minor": 5,
                "fileMode": 438,
                "uid": 0,
                "gid": 0
            },
            {
                "path": "/dev/null",
                "type": "c",
                "major": 1,
                "minor": 3,
                "fileMode": 438,
                "uid": 0,
                "gid": 0
            },
            {
                "path": "/dev/urandom",
                "type": "c",
                "major": 1,
                "minor": 9,
                "fileMode": 438,
                "uid": 0,
                "gid": 0
            },
            {
                "path": "/dev/random",
                "type": "c",
                "major": 1,
                "minor": 8,
                "fileMode": 438,
                "uid": 0,
                "gid": 0
            },
            {
                "path": "/dev/fuse",
                "type": "c",
                "major": 10,
                "minor": 229,
                "fileMode": 438,
                "uid": 0,
                "gid": 0
            }
        ],
        "maskedPaths": [
            "/proc/kcore",
            "/proc/latency_stats",
            "/proc/timer_stats",
            "/proc/sched_debug"
        ],
        "readonlyPaths": [
            "/proc/asound",
            "/proc/bus",
            "/proc/fs",
            "/proc/irq",
            "/proc/sys",
            "/proc/sysrq-trigger"
        ]
    }
}
```

So, it is very clear how it works:

- New container mounts same network namespace `/proc/14702/ns/net`
- New container mounts same network related configs, such as `/etc/resolv.conf`, `/etc/hosts` and `/etc/hostname`

There is still a little problem when first container is deleted: it could be deleted without any warning, but after delete operation, the second container will become not functional:

```sh
[~]# docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
d8230e57e88d        alpine              "sh"                14 minutes ago      Up 14 minutes                           focused_spence
[~]# docker exec d8230e57e88d echo aaa
rpc error: code = 2 desc = "oci runtime error: exec failed: lstat /proc/14702/ns/net: no such file or directory"
```

