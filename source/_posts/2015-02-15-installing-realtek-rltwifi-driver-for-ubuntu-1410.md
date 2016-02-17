---
layout: post
title: "Installing Realtek rltwifi driver for Ubuntu 14.10"
description: ""
category: Linux
tags: [Linux]
---

### 安装方法

Ubuntu 14默认内核版本没有带RTL8192ee的网卡驱动，因而就无法通过无线网络联网，并且Reltek官方网站也没有提供合适的驱动。而最新的Linux内核已经带了相应驱动，所以一般建议修复的方法就是升级内核版本到最新。但如果不想内核升级咋办呢？幸好Github上已经有人将这个驱动写好了，直接安装即可：

```
git clone git@github.com:lwfinger/rtlwifi_new.git
cd rtlwifi_new
make
sudo make install
```

### 无线网卡管理

* 打卡无线网卡电源 `iwconfig wlan0 txpower on`
* 扫描无线网络     `iwlist wlan0 scan`
* 连接到无线网络   `iwconfig wlan0 essid 'wifi' key '123456'`
* 查看无线网卡状态 `iwconfig wlan0`
* 通过DHCP为网卡分配IP `dhclient wlan0`

注意，iwconfig不支持为WPA/WPA2类型的无线网络配置密码，对于WPA类型的网络，可通过下面的方法配置：

```
#/etc/network/interfaces
iface wlan1 inet dhcp
wpa-driver wext
wpa-ssid TP-LINK_043A
wpa-psk bda9a9d988e666a78889089a098c8689a

其中wpa-psk是由wpa-passphrase [ssid] [passphrase] 产生的

修改完后重启网络 sudo /etc/init.d/networking restart
```

附注：对应wep类型的网络配置为

```
#/etc/network/interfaces
auto wlan0
iface wlan0 inet static
wireless-essid TP08129
wireless_keymode restricted
wireless-key 0812992180
address 192.168.1.60
netmask 255.255.255.0
gateway 192.168.1.1
broadcast 192.168.1.255
```

