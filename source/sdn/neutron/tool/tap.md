# 手动创建虚拟机网络

假设：_使用ml2+openvswitch插件_。

首先，创建一个neutron port:

```
neutron port-create net-name
```

然后创建qvb/qvo，并连接到br-int:

```
port_id=5042f4b6-004e-41d4-a184-c3b1f841f9fa
mac=fa:16:3e:bf:88:6d
suffix=$(echo $port_id|cut -c1-11)
ip link add qvb$suffix type veth peer name qvo$suffix
ovs-vsctl -- --may-exist add-port br-int qvo$suffix -- set Interface qvo$suffix external-ids:iface-id=$port_id external-ids:iface-status=active external-ids:attached-mac=$mac external-ids:vm-uuid=$(uuidgen)
neutron port-update $port_id --binding:host_id=$(hostname)
```

这时候查看neutron port，发现已经是ACTIVE状态了：

```
neutron port-show $port_id
```

最后，创建虚拟机所用的qbr网桥：

```
brctl addbr qbr$suffix
ip link set qvb$suffix up
ip link set qvb$suffix promisc on
ip link set qvo$suffix up
ip link set qvo$suffix promisc on
ip link set qbr$suffix up
brctl addif qbr$suffix qvb$suffix
```

最后，就可以把`qbr$suffix`和`tap$suffix`配置到vm的配置文件里面了：

```xml
    <interface type="bridge">
      <mac address="fa:16:33:78:0b:a9"/>
      <model type="virtio"/>
      <source bridge="qbrxxxxxx"/>
      <target dev="tapxxxxxx"/>
      <address slot="0x03" bus="0x00" domain="0x0000" type="pci" function="0x0"/>
    </interface>
```
