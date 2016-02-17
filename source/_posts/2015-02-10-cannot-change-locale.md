---
layout: post
title: "cannot change locale"
description: ""
category: linux
tags: [Linux]
---

运行locale命令<span id="more-912"></span>  
LANG=  
LANGUAGE=  
LC_CTYPE="POSIX"  
LC_NUMERIC="POSIX"  
LC_TIME="POSIX"  
LC_COLLATE="POSIX"  
LC_MONETARY="POSIX"  
LC_MESSAGES="POSIX"  
LC_PAPER="POSIX"  
LC_NAME="POSIX"  
LC_ADDRESS="POSIX"  
LC_TELEPHONE="POSIX"  
LC_MEASUREMENT="POSIX"  
LC_IDENTIFICATION="POSIX"  
LC_ALL=  

修改profile

vi /etc/profile

添加如下内容

export LC_ALL=en_US.UTF-8

source /etc/profile

得到错误 setlocale: LC_ALL: cannot change locale (en_US.UTF-8): No such file or directory  
&nbsp;运行 dpkg-reconfigure locales

得到错误

perl: warning: Setting locale failed.  
perl: warning: Please check that your locale settings:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; LANGUAGE = (unset),  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; LC_ALL = "en_US.UTF-8",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; LANG = "en_US.UTF-8"  
&nbsp;&nbsp;&nbsp; are supported and installed on your system.  
perl: warning: Falling back to the standard locale ("C").  
locale: Cannot set LC_CTYPE to default locale: No such file or directory  
locale: Cannot set LC_MESSAGES to default locale: No such file or directory  
locale: Cannot set LC_ALL to default locale: No such file or directory  
/bin/bash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)  

解决办法

apt-get purge locales

apt-get autoclean

apt-get install locales

cd /usr/share/locales

./install-language-pack en_US.UTF-8

dpkg-reconfigure locales

修复完成

运行locale

LANG=en_US.UTF-8  
LANGUAGE=  
LC_CTYPE="en_US.UTF-8"  
LC_NUMERIC="en_US.UTF-8"  
LC_TIME="en_US.UTF-8"  
LC_COLLATE="en_US.UTF-8"  
LC_MONETARY="en_US.UTF-8"  
LC_MESSAGES="en_US.UTF-8"  
LC_PAPER="en_US.UTF-8"  
LC_NAME="en_US.UTF-8"  
LC_ADDRESS="en_US.UTF-8"  
LC_TELEPHONE="en_US.UTF-8"  
LC_MEASUREMENT="en_US.UTF-8"  
LC_IDENTIFICATION="en_US.UTF-8"  
LC_ALL=en_US.UTF-8
