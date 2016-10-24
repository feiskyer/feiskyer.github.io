# systemtap

Useful systemtap scripts.

- Documentation: https://sourceware.org/systemtap/documentation.html
- Examples: https://sourceware.org/systemtap/wiki

setup for ubuntu:

    1.install systemtap

    $sudo apt-get install systemtap
    $sudo apt-get install systemtap-runtime

    2.install kernel-debug-info

    echo "deb http://ddebs.ubuntu.com $(lsb_release -cs) main restricted universe multiverse" | \
    sudo tee -a /etc/apt/sources.list.d/ddebs.list
    echo "deb http://ddebs.ubuntu.com $(lsb_release -cs)-updates main restricted universe multiverse
    deb http://ddebs.ubuntu.com $(lsb_release -cs)-security main restricted universe multiverse
    deb http://ddebs.ubuntu.com $(lsb_release -cs)-proposed main restricted universe multiverse" | \
    sudo tee -a /etc/apt/sources.list.d/ddebs.list

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 428D7C01
    sudo apt-get update
    sudo apt-get install linux-image-$(uname -r)-dbgsym

setup for fedora:

    yum install systemtap kernel-devel debuginfo-install kernel
