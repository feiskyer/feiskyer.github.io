# OVN libvirt

```sh
ifaceid=$(ovs-vsctl get interface vnet0 external_ids:iface-id)
ovn-nbctl lsp-add <switch name> $IFACE_ID
ovs-vsctl get interface <name> external_ids:attached-mac
MAC_ADDR=$(ovs-vsctl get interface vnet0 external_ids:attached-mac | sed s/\"//g)
ovn-nbctl lsp-set-addresses $IFACE_ID $MAC_ADDR
```

libvirt.xml

```xml
<interface type='bridge'>
  <mac address='52:54:00:93:05:25'/>
  <source network='ovs' bridge='br-int'/>
  <virtualport type='openvswitch'>
    <parameters interfaceid='668033d2-06a4-4aaa-aca5-30cde245e477'/>
  </virtualport>
  <target dev='vnet0'/>
  <model type='virtio'/>
  <alias name='net0'/>
  <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
</interface>
```

参考[Using OVN with KVM and Libvirt](http://blog.scottlowe.org/2016/12/09/using-ovn-with-kvm-libvirt/)


