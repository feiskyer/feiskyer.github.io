# ovn-docker

There is [OVN integration with Docker networking](https://github.com/openvswitch/ovs/blob/master/INSTALL.Docker.md), as well.  This currently resides in the main OVS repo, though it could be split out into its own repository in the future, similar to ovn-kubernetes.

* http://docs.openvswitch.org/en/latest/howto/docker/
* http://dockone.io/article/1200

```sh
# start docker
docker daemon --cluster-store=consul://127.0.0.1:8500 \
    --cluster-advertise=$HOST_IP:0

# start north
/usr/share/openvswitch/scripts/ovn-ctl start_northd
ovn-nbctl set-connection ptcp:6641
ovn-sbctl set-connection ptcp:6642

# start south
ovs-vsctl set Open_vSwitch . \
    external_ids:ovn-remote="tcp:$CENTRAL_IP:6642" \
    external_ids:ovn-nb="tcp:$CENTRAL_IP:6641" \
    external_ids:ovn-encap-ip=$LOCAL_IP \
    external_ids:ovn-encap-type="$ENCAP_TYPE"
/usr/share/openvswitch/scripts/ovn-ctl start_controller

# start openvswitch plugin
pip install Flask
PYTHONPATH=$OVS_PYTHON_LIBS_PATH ovn-docker-overlay-driver --detach

# create docker network
docker network create -d openvswitch --subnet=192.168.1.0/24 foo
```

