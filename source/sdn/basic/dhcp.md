# DHCP与DNS

## DHCP

DHCP（Dynamic Host Configuration Protocol）是一个用于主机动态获取IP地址的配置解析，使用UDP报文传送，端口号为67何68。

DHCP使用了租约的概念，或称为计算机IP地址的有效期。租用时间是不定的，主要取决于用户在某地连接Internet需要多久，这对于教育行业和其它用户频繁改变的环境是很实用的。通过较短的租期，DHCP能够在一个计算机比可用IP地址多的环境中动态地重新配置网络。DHCP支持为计算机分配静态地址，如需要永久性IP地址的Web服务器。

![](https://upload.wikimedia.org/wikipedia/commons/2/28/DHCP_session_en.svg)

## DNS

DNS（Domain Name System）是一个解析域名和IP地址对应关系的服务，它以递归的方式运行：首先访问最近的DNS服务器，如果查询到域名对应的IP地址则直接返回，否则的话再向上一级查询。DNS通常以UDP报文来传送，并使用端口号53。

## FAQ

### dnsmasq bad DHCP host name 问题

这个问题是由于hostname是数字前缀，并且dnsmasq对版本低于2.67，这个问题在[2.67版本中修复](http://www.thekelleys.org.uk/dnsmasq/CHANGELOG):

>   Allow hostnames to start with a number, as allowed in
>   RFC-1123. Thanks to Kyle Mestery for the patch. 
