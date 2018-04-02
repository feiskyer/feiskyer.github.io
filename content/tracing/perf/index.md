---
title: "perf"
type: page
---

## perf简介

perf是Linux内核自带的性能分析工具。通过它，应用程序可以利用 PMU，tracepoint 和内核中的特殊计数器来进行性能统计。它不但可以分析指定应用程序的性能问题 (per thread)，也可以用来分析内核的性能问题，当然也可以同时分析应用代码和内核，从而全面理解应用程序中的性能瓶颈。

       Performance counters for Linux are a new kernel-based subsystem that provide a framework for all things performance analysis. It covers hardware
       level (CPU/PMU, Performance Monitoring Unit) features and software features (software counters, tracepoints) as well.

## perf list

`perf list` 查询perf所支持的事件，在其他命令中可以使用`-e`指定事件

## perf top

`perf top` 显示指定事件（默认是CPU周期）消耗最多的函数或指令，其格式为

```
Samples: 5K of event 'cpu-clock', Event count (approx.): 1191156157
Overhead  Shared Object            Symbol
   6.27%  hyperkube                [.] runtime.scanobject
   5.59%  hyperkube                [.] runtime.memmove
   5.01%  hyperkube                [.] runtime.mallocgc
   4.94%  [kernel]                 [k] 0x00007fff8183e045
```

* 第一列 事件发生的比例
* 第二列 应用程序、模块或内核
* 第三列 `[.]`表示应用程序, `[k]`表示内核
* 第四列 符号名，无符号时显示为地址

## perf stat

## perf record/report/annotate

## 参考文档

* https://perf.wiki.kernel.org/index.php/Tutorial
* https://www.ibm.com/developerworks/cn/linux/l-cn-perf1/
