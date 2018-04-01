---
title: screen tips
---

### 简介 {#_1}

Screen是一个可以在多个进程之间多路复用一个物理终端的窗口管理器。Screen中有会话的概念，用户可以在一个screen会话中创建多个screen窗口，在每一个screen窗口中就像操作一个真实的telnet/SSH连接窗口那样。

### 启动screen {#screen}

    screen
    screen bash
    screen vi test
    screen -ls # 列出所有screen窗口

### 常用快捷键 {#_2}

-   Ctrl+a ? 显示所有快捷键
-   Ctrl+a \"/w 显示窗口列表
-   Ctrl+a n/p 切换到下一个/前一个窗口
-   Ctrl+a 0..9 切换到窗口0..9
-   Ctrl+a d 暂时断开连接 （通过screen -r重新连接）
-   Ctrl+a k 关闭当前窗口
-   Ctrl+a H 记录当前窗口到日志screenlog.n

其他命令列表见<http://www.gnu.org/software/screen/manual/screen.html>.

::: {#disqus_thread}
:::

Please enable JavaScript to view the [comments powered by
Disqus.](http://disqus.com/?ref_noscript)

[comments powered by
[Disqus]{.logo-disqus}](http://disqus.com){.dsq-brlink}
