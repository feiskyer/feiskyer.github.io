# Install OVN On Ubuntu

## From apt-get

```sh
apt-get install -y openvswitch-switch
apt-get install ovn-central ovn-common ovn-controller-vtep ovn-docker ovn-host

export CENTRAL_IP=10.140.0.2
export LOCAL_IP=10.140.0.2
export ENCAP_TYPE=vxlan
ovs-vsctl set Open_vSwitch . external_ids:ovn-remote="tcp:$CENTRAL_IP:6642" external_ids:ovn-nb="tcp:$CENTRAL_IP:6641" external_ids:ovn-encap-ip=$LOCAL_IP external_ids:ovn-encap-type="$ENCAP_TYPE"
```

## From Source

Update & install dependencies

```
apt-get update
apt-get -y install build-essential fakeroot
```

Install Build-Depends from debian/control file

```
apt-get -y install graphviz autoconf automake bzip2 debhelper dh-autoreconf libssl-dev libtool openssl
apt-get -y install procps python-all python-twisted-conch python-zopeinterface python-six
```

Check the working directory & build

```
cd openvswitch-2.6.0

# if everything is ok then this should return no output
dpkg-checkbuilddeps

`DEB_BUILD_OPTIONS='parallel=8 nocheck' fakeroot debian/rules binary`
```

The .deb files for ovs will be built and placed in the parent directory (ie. in …/). The next step is to
build the kernel modules.

Install datapath sources

```
cd ..
apt-get -y install module-assistant
dpkg -i openvswitch-datapath-source_2.6.0-1_all.deb
```

Build kernel modules using module-assistant

```
m-a prepare
m-a build openvswitch-datapath
```

Copy the resulting deb package. Note that your version may differ slightly depending on your specific kernel version.

```
cp /usr/src/openvswitch-datapath-module-*.deb ./
apt-get update
apt-get -y install python-six python2.7
dpkg -i openvswitch-datapath-module-*.deb
dpkg -i openvswitch-common_2.6.0-1_amd64.deb openvswitch-switch_2.6.0-1_amd64.deb
dpkg -i ovn-common_2.6.0-1_amd64.deb ovn-central_2.6.0-1_amd64.deb ovn-host_2.6.0-1_amd64.deb
```

```
/usr/share/openvswitch/scripts/ovs-ctl start --system-id=random
/usr/share/openvswitch/scripts/ovn-ctl start_northd
/usr/share/openvswitch/scripts/ovn-ctl start_controller
/usr/share/openvswitch/scripts/ovn-ctl start_controller_vtep
export CENTRAL_IP=10.140.0.2
export LOCAL_IP=10.140.0.2
export ENCAP_TYPE=vxlan
ovs-vsctl set Open_vSwitch . external_ids:ovn-remote="tcp:$CENTRAL_IP:6642" external_ids:ovn-nb="tcp:$CENTRAL_IP:6641" external_ids:ovn-encap-ip=$LOCAL_IP external_ids:ovn-encap-type="$ENCAP_TYPE"
```
