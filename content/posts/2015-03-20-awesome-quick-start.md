---
layout: post
title: "awesome quick start"
description: ""
category: Linux
tags: [Linux]
---

awesome是Linux平台出色的窗口管理器，具有速度快、界面简捷等优点。其安装也比较简单：

```
sudo apt-get install -y awesome awesome-extra gnome-settings-daemon nautilus
sudo apt-get install -y --no-install-recommends gnome-session
mkdir -p ~/.config/awesome
```

常用快捷键整理：

    切换程序
    切换到下一个程序：Mod4 + j
    切换到上一个程序：Mod4 + k
    切换到主窗口中的第一个程序：Mod4 + Ctrl + Return

    切换tag
    切换到上一个选择的tag：Mod4 + Esc
    切换到某个指定的tag：Mod4 + 1-9
    切换到前一个tag：Mod4 + Left
    切换到下一个tag：Mod4 + Right

    程序窗口状态修改
    最大化/非最大化：Mod4 + m
    浮动/平铺：Mod4 + Ctrl + Space
    最小化：Mod4 + n
    从最小化中恢复：Mod4 + Ctrl + n
    关闭程序：Mod4 + Shift + C

    程序窗口的转移和显示
    转移到某个tag：Mod4 + Shift + 1-9（或在某个tag名上按Mod4+鼠标左键）
    增加到某些tag：Mod4 + Shift + Ctrl + 1-9
    转移到下一个窗口中的位置：Mod4 + Shift + j
    转移到上一个窗口中的位置：Mod4 + Shift + k

    布局修改
    当前程序窗口宽度增加5％：Mod4 + Shift + h
    当前程序窗口宽度减少5％：Mod4 + Shift + l
    切换到下一种布局方式：Mod4 + Space
    切换到上一种布局方式：Mod4 + Ctrl + Space

    窗口管理
    重启awesome：Mod4 + Ctrl + r
    退出awesome：Mod4 + Shift + q
    运行某个命令：Mod4 + r
    打开awesome菜单：Mod4 + w

    多显示器下的操作
    切换到下一个屏幕：Mod4 + Ctrl + j
    切换到上一个屏幕：Mod4 + Ctrl + k
    将程序发送到下一个屏幕：Mod4 + o
