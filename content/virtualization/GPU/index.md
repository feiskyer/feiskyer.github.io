---
title: GPU虚拟化
date: 2016-10-15 17:19:19
type: page
---

# GPU虚拟化

GPU（图形处理器单元）一开始的时候GPU 主要用于 3D 游戏的渲染，但是现在GPU已经广泛用于加速计算性负载，比如深度学习、VR等。GPU是由几百个核组成，因此可以并发处理数千个线程。尽管 GPU 的内核数目远远超过 CPU，但是它的每个核的处理能力远小于CPU的核，而且不具有现代操作系统的所需要的一些特性，GPU 并不合适用于处理普通的计算，它们更多地用于计算消耗性操作。

NVIDIA、AMD和intel相继推出自己的基于硬件的虚拟化解决方案。

## AMD GPU虚拟化

AMD GPU虚拟化解决方案是完全基于业界标准的SR-IOV(单根输入输出虚拟化)。这是由PCI SIG组织开发的一种规范，为设备的硬件虚拟化应用提供了标准化方法。其能够允许多达15个虚拟化桌面共享同一个图形处理器，其最终用户就能够同等地访问GPU，无论他们是何种工作负载，而且不会有任何性能上的损失。

SR-IOV标准允许一个GPU给多个虚拟机共享使用，因此为每一个用户都提供了虚拟化的性能进行设计、创造并且执行他们的工作负载，而没有一个用户会占据整个GPU。由于硬件的复杂性，目前支持的GPU厂商只有AMD。

## NVIDIA

NVIDIA没有像AMD那样使用的基于硬件的GPU虚拟化技术。其虚拟化方案是称为Grid桌面虚拟化技术，该技术是基于它最新的Tesla GPUs的。NVIDIA的虚拟化方案比较有意思的一个特色是可以虚拟出几种不同model的虚拟显卡。 FloridaAtlantic University基于NVIDIA GPU 虚拟化方案的VDI已经有几年历史了，他们称，可以使用8-12个虚拟化桌面同时共享一个GPU 板卡。NVIDIA目前还不支持KVM，而是支持Citrix、Hyper-V、VMWare等。

![nvidia-vGPU](/images/nvidia-vGPU.png)

![nvidia-2](/images/nvidia-2.png)


## Intel

![](/images/14765250655065.jpg)

Intel支持三种GPU虚拟化方法：

- API转发（GVT-S）：将openGL或者DirectX的API转发给host上的Graphics Driver上。优点是可以共享。缺点是性能差、功能滞后。
- 直通设备（GVT-d）：利用VT-d将显卡直通给虚拟机。优点：性能佳、功能完备。缺点：不能共享。
- 完全GPU虚拟化(GVT-g)：性能佳、功能完备、可以共享。

**API转发**

![](/images/14765251831216.jpg)

远程API 方法分为前端和后端两个部分。前端以动态库的形式被虚拟机中的CUDA程序加载，后端则是运行在宿主机中的一个程序。在这种机制下，首先由前端将虚拟机中的CUDA API重写，将API的名称和相应参数传递给后端。然后后端为前端每个CUDA应用程序创建一个进程，在该进程中转 换来自前端重写后的API，获得API的名称和参数，接着使用宿主机上真实的GPU硬件设备执行相应的API，最后将 API执行结果返回给前端。

这种方法需要进行大量虚拟机与宿主机之间的数据传输，导致GPU虚拟化的性能严重下降。在CUDA程序规模较小时，这些GPU虚拟化框架的性能下降并不太明显。但在进行实际应用中的高性能计算时性能下降非常明显。

**GVT-d**

![](/images/14765252266526.jpg)

利用VT-d将显卡直通给虚拟机，虚拟机完全独享该设备，不支持共享。

**GVT-g**

![](/images/14765252637092.jpg)

通过GPU全虚拟化在多个虚拟机之间共享物理GPU，目前已经在XenGT和KVMGT中支持。

### Intel KVMGT

KVMGT 是Intel® 完全GPU虚拟化（GraphicsVirtualization Technology GVT-g) 的KVM实现，是VGT-g的纯软件方案。其mediatedpass-through相当于软件实现的GPU分时复用，不同于SR-IOV。

![](/images/14765253042303.jpg)

KVMGT从intel的broadwell处理器开始支持。

其性能：

* 3D性能可以达到host的80%以上。
* 2D性能可以达到host的70%以上。
* Media解码能力可以到host的90%以上。
* Media转码能力可以到host的80%以上。

KVMGT支持的Features

* 可以运行native的driver。
* DirectX*11.1
* OpenGL*4.2
* OpenCL*1.2
* MediaSDK16.2
* DirectX*12

开源：

- Kernel: https://github.com/01org/igvtg-kernel
- Qemu: https://github.com/01org/igvtg-qemu

## GPU虚拟化使用示例

**PCI pass-through**

```
# Boot kernel with 'intel_iommu=on'

# Unbind driver from the device and bind 'pci-stub' to it
echo "168c 0030" > /sys/bus/pci/drivers/pci-stub/new_id
echo 0000:0b:00.0 > /sys/bus/pci/devices/0000:0b:00.0/driver/unbind
echo 0000:0b:00.0 > /sys/bus/pci/drivers/pci-stub/bind

# Then just run
sudo qemu-system-i386 -m 1024 \
    -device pci-assign,host=0b:00.0,rombar=0 \
    -enable-kvm \
    -kernel $KERNEL \
    -hda $DISK \
    -boot c \
    -append "root=/dev/sda rw"
```

**VFIO**

VFIO 在 Linux kernel3.6/qemu1.4 以后支持，目前只支持 PCI 设备。VFIO 是一套用户态驱动框架，提供两种基本服务：向用户态提供设备访问接口 和 向用户态提供配置IOMMU 接口。 它第一次向用户态开放了 IOMMU 接口，能完全在用户态配置 IOMMU，将 DMA 地址空间映射进而限制在进程虚拟地址空间之内。

VFIO 可以用于实现高效的用户态驱动。在虚拟化场景可以用于 PCI 设备透传。通过用户态配置IOMMU接口，可以将DMA地址空间映射限制在进程虚拟空间中，这对高性能驱动和虚拟化场景device passthrough尤其重要。相对于传统方式，VFIO对UEFI支持更好。VFIO 技术实现了用户空间直接访问设备。无须root特权，更安全，功能更多。

```
modprobe vfio
modprobe vfio-pci

# unbind first
echo <vf_BDF> > /sys/bus/pci/device/<vf_BDF>/driver/unbind
lspci -s <vf_BDF> -n //to get its number
echo 8086 1520 > /sys/bus/pci/drivers/vfio-pci/new_id
```

qemu:

```
qemu-kvm -m 16G -smp 8 -net none -device vfio-pci,host=81:10.0 -drive file=/var/lib/libvirt/images/rhel7.1.img,if=virtio -nographic
```

libvirt:

```sh
$ cat net2.xml
<hostdev mode='subsystem' type='pci'managed='yes'>
     <driver name='vfio'/>
     <source>
       <address type='pci' domain='0x0000' bus='0x0b' slot='0x00'function='0x0'/>
     </source>
</hostdev>

$ virsh attach-device vfio_test net2.xml --config
```

**参考文档**

- [GPU虚拟化](http://mp.weixin.qq.com/s?src=3&timestamp=1476523033&ver=1&signature=ifj0PRCsXKHVPiVcl-dNxhSlKKKcX6hwO1rz-hbipIp2Dy5LLw5PW2PB5095130d0UBFiuLPYuYr4SebXgDOoW2LP1ldzHh1XNPVH7NF3py5VVmdpxMlL2Lp2G6LdAlCe82FUzmemhMt682-i82I4i9mhggmee6oE4KjuVtLljM=)
- [GPU-Accelerated Applications](http://www.nvidia.com/content/gpu-applications/PDF/GPU-apps-catalog-mar2015.pdf)
- [NVIDIA Grid vGPU User Guide](http://images.nvidia.com/content/pdf/grid/guides/GRID-vGPU-User-Guide.pdf)
- [OpenStack 企业私有云的若干需求（1）：Nova 虚机支持 GPU](http://www.cnblogs.com/sammyliu/p/5179414.html)
