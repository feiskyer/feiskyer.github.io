---
title: "Neutron rest API"
---

安装依赖工具

```
yum install jq
```

获取token

```
token=$(curl -d '{"auth":{"tenantName": "demo", "passwordCredentials":{"username":"demo", "password":"demo"}}}' -H "Content-Type: application/json" http://192.168.0.10:5001/v2.0/tokens | jq -r .access.token.id)
```

create network

```
curl -i -X POST  -d '{"network":{"name":"net1","admin_state_up":true}}' http://192.168.0.10:9696/v2.0/networks -H "X-Auth-Token:$token" -H "Content-type:application/json"
```

list networks

```
curl -s -X GET http://192.168.0.10:9696/v2.0/networks -H "X-Auth-Token:$token" -H "Content-type:application/json"
```

show network

```
curl -X GET "http://192.168.0.10:9696/v2.0/networks.json?fields=id&name=net1" -H "User-Agent: python-neutronclient" -H "Accept: application/json" -H "X-Auth-Token: $token"

curl -X GET http://192.168.0.10:9696/v2.0/networks/c9784629-e897-4771-ba0c-84dc457c7af3 -H "X-Auth-Token: $token" -H "Content-type: application/json"
```

update network

```
curl -X PUT -d '{"network":{"name":"test-11-v"}}' http://192.168.0.10:9696/v2.0/networks/3c88bce8-3d36-4509-8300-445cfd936841 -H "X-Auth-Token: $token" -H "Content-type: application/json" | jq
```

delete network

```
curl -X DELETE http://192.168.0.10:9696/v2.0/networks/c9784629-e897-4771-ba0c-84dc457c7af3 -H "X-Auth-Token: $token" -H "Content-type: application/json"
```
