# systemtap

SystemTap是DTrace的Linux实现，它把用户提供的脚本转换为内核模块来执行，用来监测和跟踪内核事件。

## 安装

注意，较新的内核不支持systemtap。

### Ubuntu

    sudo apt-get install -y systemtap-runtime systemtap

    echo "deb http://ddebs.ubuntu.com $(lsb_release -cs) main restricted universe multiverse" | \
    sudo tee -a /etc/apt/sources.list.d/ddebs.list
    echo "deb http://ddebs.ubuntu.com $(lsb_release -cs)-updates main restricted universe multiverse
    deb http://ddebs.ubuntu.com $(lsb_release -cs)-security main restricted universe multiverse
    deb http://ddebs.ubuntu.com $(lsb_release -cs)-proposed main restricted universe multiverse" | \
    sudo tee -a /etc/apt/sources.list.d/ddebs.list

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 428D7C01
    sudo apt-get update
    sudo apt-get install linux-image-$(uname -r)-dbgsym -y

### CentOS

    yum install systemtap kernel-devel debuginfo-install kernel

## 参考文档

- Documentation: https://sourceware.org/systemtap/documentation.html
- Examples: https://sourceware.org/systemtap/wiki
- https://taozj.org/201703/systemtap-intro.html

