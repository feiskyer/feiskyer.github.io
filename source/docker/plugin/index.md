---
layout: "post"
---

# Plugin


```sh
# To install a plugin
docker plugin install vieux/sshfs
# Use the plugin
docker volume create \
  -d vieux/sshfs \
  --name sshvolume \
  -o sshcmd=user@1.2.3.4:/remote
docker run -v sshvolume:/data busybox ls /data

# To create a plugin from a rootfs and configuration. Plugin data directory must
# contain config.json and rootfs directory.
docker plugin create <plugin-name> <plugin-data-dir>
# To disable a plugin
docker plugin disable <plugin-name>
# To enable a plugin
docker plugin enable <plugin-name>
# To display detailed information of a plugin
docker plugin inspect <plugin-name>

# To list plugins
docker plugin ls|list
# To push a plugin to a registry
docker plugin push <plugin-name:tag>
# To remove a plugin
docker plugin rm <plugin-name>
# To change settings for a plugin
docker plugin set <plugin-name> KEY=VALUE
```
