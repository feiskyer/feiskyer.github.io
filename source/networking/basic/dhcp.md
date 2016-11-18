# DHCP



# dnsmasq

## bad DHCP host name 问题

这个问题是由于hostname是数字前缀，并且dnsmasq对版本低于2.67，这个问题在[2.67版本中修复](http://www.thekelleys.org.uk/dnsmasq/CHANGELOG):

>   Allow hostnames to start with a number, as allowed in
>   RFC-1123. Thanks to Kyle Mestery for the patch. 

