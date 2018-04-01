---
layout: post
title: "Perform Consistent Snapshots with qemu guest agent"
description: ""
category: 
tags: []
---

A while back, I [wrote an article](http://www.sebastien-han.fr/blog/2012/12/10/openstack-perform-consistent-snapshots/) about taking consistent snapshots of your virtual machines in your OpenStack environment.
    However this method was really intrusive since it required to be inside the virtual machine and to manually summon a filesystem freeze.
    In this article, I will use a different approach to achieve the same goal without the need to be inside the virtual machine.
 
The only requirement is to have a virtual machine running the qemu-guest-agent.


# OpenStack Nova and QEMU guest agent

The QEMU guest support landed in Nova during the Havana cycle, so basically we are two release ahead.
This functionality is based on Glance properties.

But how does that work?

The principle is quite easy. A virtual machine boots with a new virtio device attached pointing to unix socket on the hypervisor. Inside the virtual machine this socket will appear as a new character device, commonly under `/dev/virtio-ports/`.

A picture is always better:

![](/assets/qemu-agent-freeze-thaw.png)


# Configure the QEMU agent

For Ubuntu, you need to apply this fix since AppArmor will not allow the creation of the socket:

```
$ sudo echo "/var/lib/libvirt/qemu/*.sock rw," | sudo tee -a /etc/apparmor.d/abstractions/libvirt-qemu
$ sudo service libvirt-bin restart
$ sudo service nova-compute restart
$ sudo service apparmor reload
```

Configure your Glance image:

```
$ glance image-create --name cirros \
--disk-format raw \
--container-format bare \
--file cirros-0.3.3-x86_64-disk.raw \
--is-public True \
--property hw_qemu_guest_agent=yes \
--progress
```

Boot your virtual machine: `nova boot ....`

Verify that the agent is in the virtual machine:

```
ubuntu@agent:~$ file /dev/virtio-ports/org.qemu.guest_agent.0
/dev/virtio-ports/org.qemu.guest_agent.0: symbolic link to ../vport2p1
```

Install the QEMU agent inside your VM:

```
ubuntu@agent:~$ sudo apt-get install -y qemu-guest-agent
ubuntu@agent:~$ sudo mkdir /var/log/qemu-agent
ubuntu@agent:~$ sudo tee /etc/default/qemu-guest-agent > /dev/null <<EOF
DAEMON\_ARGS="--logfile /var/log/qemu-agent/org.qemu.guest_agent.0.log --fsfreeze-hook --verbose"
EOF
ubuntu@agent:~$ sudo service qemu-guest-agent restart
 * Restarting QEMU Guest Agent qemu-qa
 *    ...done
 *    ubuntu@agent:~$ sudo ls /var/log/qemu-agent/
 *    org.qemu.guest_agent.0.log
```

Now go back on the hypervisor and check that the socket file is present (it must here since we have the character device inside the virtual machine):

```
$ sudo bash -c  "ls /var/lib/libvirt/qemu/*.sock"
/var/lib/libvirt/qemu/capabilities.monitor.sock  /var/lib/libvirt/qemu/org.qemu.guest_agent.0.instance-00000007.sock

$ sudo file /var/lib/libvirt/qemu/org.qemu.guest_agent.0.instance-00000007.sock
/var/lib/libvirt/qemu/org.qemu.guest_agent.0.instance-00000007.sock: socket
```

Test if the QEMU agent responds:

```
$ sudo virsh qemu-agent-command instance-00000007 '{"execute":"guest-ping"}'
{"return":{}}
```

Setup the fsfreeze hook mechanism, on Red Hat systems the file already exists:

```
buntu@agent:~$ sudo wget -O /etc/qemu/fsfreeze-hook https://raw.githubusercontent.com/qemu/qemu/master/scripts/qemu-guest-agent/fsfreeze-hook
ubuntu@agent:~$ sudo chmod +x /etc/qemu/fsfreeze-hook
```

Configure a basic hook, it will be executed either during the freeze or thaw operation:

```
ubuntu@agent:~$ sudo mkdir /etc/qemu/fsfreeze-hook.d
ubuntu@agent:~$ sudo tee > /etc/qemu/fsfreeze-hook.d/foo.sh > /dev/null <<EOF
#!/bin/bash

case "$1" in
    freeze)
        echo "I'm frozen" > /tmp/freeze
        ;;
    thaw)
        echo "I'm thawed" >> /tmp/freeze
        ;;
    *)
        exit 1
        ;;
esac
EOF
ubuntu@agent:~$ sudo chmod +x /etc/qemu/fsfreeze-hook.d/foo.sh
```

Now let’s freeze ad thaw the filesystem:

```
$ sudo virsh qemu-agent-command instance-00000008 '{"execute":"guest-fsfreeze-freeze"}'
$ sudo virsh qemu-agent-command instance-00000008 '{"execute":"guest-fsfreeze-thaw"}'
```

Did the hook work as expected? Yes!

```
ubuntu@agent:~$ sudo cat /tmp/freeze
I'm frozen
I'm thawed
```

# OpenStack Nova and Snapshots

Several patches have been submitted to quiesce the filesystem prior to run the snapshot.

The initial work to support fs-freeze while performing a snapshot of an instance was introduced in Juno with a [spec](https://review.openstack.org/#/c/99780/).

However the commit only got [merged](https://review.openstack.org/#/c/72038/9) in December…
This will be available in Kilo.
Another effort to support this feature while booting from a volume is currently under review.

The original blueprint can be found [here](https://blueprints.launchpad.net/nova/+spec/quiesced-image-snapshots-with-qemu-guest-agent).
Ultimately this option will be available via a Glance property:

`$ glance image-update 53bd9dbe-23db-412b-81d5-9743aabdfeb5 --property os_require_quiesce=yes`

When this option will be set and the virtual machine running the QEMU guest agent, when a user will snapshot an instance, the filesystem will get frozen and thawed after the operation.  

    > I’m really looking forward to the Kilo release now! What about you?
