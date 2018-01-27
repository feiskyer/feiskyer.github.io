---
title: Troubleshooting Windows Containers
date: 2018-01-27 20:11:07
layout: "post"
---

This chapter is about Windows containers troubleshooting.

### Windows Pod stuck in ContainerCreating

Besides reasons introduced in [Troubleshooting Pod](pod.html), there are also other causes including:

* the pause image is misconfigured
* the container image is not [compatible with Windows](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility). Note that containers on Windows Server 1709 should use images with 1709 tags, e.g.
  * `microsoft/aspnet:4.7.1-windowsservercore-1709`
  * `microsoft/windowsservercore:1709`
  * `microsoft/iis:windowsservercore-1709`

### Windows Pod failed to resolve DNS

This is a [known issue](https://github.com/Azure/acs-engine/issues/2027). A workaround is configure kube-dns Pod's IP address to normal Pods, e.g.

```powershell
$adapter=Get-NetAdapter
Set-DnsClientServerAddress -InterfaceIndex $adapter.ifIndex -ServerAddresses 10.244.0.2,10.244.0.3
Set-DnsClient -InterfaceIndex $adapter.ifIndex -ConnectionSpecificSuffix "default.svc.cluster.local"
```

### Windows Pod failed to get ServiceAccount Secret

This is also a [known issue](https://github.com/moby/moby/issues/28401). There is no workaround for current windows yet, but its fix has been released in Windows 10 Insider and Windows Server Insider builds 17074+.

### Windows Pod failed to access Kubernetes API

If you are using a Hyper-V virtual machine, ensure that MAC spoofing is enabled on the network adapter(s).

### Windows node cannot access services clusterIP

This is a known limitation of the current networking stack on Windows. Only pods can refer to the service IP.

## References

* [Troubleshooting Kubernetes](https://docs.microsoft.com/en-us/virtualization/windowscontainers/kubernetes/common-problems)
