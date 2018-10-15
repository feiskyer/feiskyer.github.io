---
title: docker存储结构解析 - feisky
tags: []
date: 2014-11-19 21:11:00
---

【摘要】由于aufs并未并入内核，故而目前只有Ubuntu系统上能够使用aufs作为docker的存储引擎，而其他系统上使用lvm thin provisioning（overlayfs是一个和aufs类似的union filesystem，未来有可能进入内核，但目前还没有；Lvm snapshot are... [阅读全文](http://www.cnblogs.com/feisky/p/4106212.html)
