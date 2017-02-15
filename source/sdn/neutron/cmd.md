# Neutron常用命令

```sh
# 创建外网网络
neutron net-create --router:external=True br-ex
# 添加一个外网子网
neutron subnet-create --name demo-ex-subnet br-ex 169.169.169.0/24

# 创建路由器
neutron router-create demo-router
# 创建网络和子网
neutron net-create demo-net
neutron subnet-create --name demo-subnet demo-net 10.10.10.0/24
# 将子网连接到路由器
neutron router-interface-add demo-router demo-subnet

# 为路由器设置外网网关
neutron router-gateway-set demo-router br-ex
neutron router-show demo-router

# 创建一个port
neutron port-create --name demo-port demo-net
# 创建一个公网IP
neutron floatingip-create br-ex
# 绑定该公网IP到Port
neutron floatingip-associate 9964459f-0726-4795-bb80-932834ec1720 888d9397-9447-41ec-8259-74c4a92bb3ac

# 最后清理资源
neutron port-delete demo-port
neutron floatingip-delete 9964459f-0726-4795-bb80-932834ec1720
neutron router-interface-delete demo-router demo-subnet
neutron router-gateway-clear demo-router
neutron router-delete demo-router
neutron net-delete demo-net
neutron subnet-delete demo-ex-subnet
```
