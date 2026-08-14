---
layout: post
title: "Python __file__ not defined problem"
description: "解决 Python 交互式命令行中 __file__ 未定义的问题，给出借助 inspect 模块获取当前脚本路径的通用变通写法。"
category: 
tags: [python]
---

__file__仅在文件中运行的时候才正常，而在交互式命令行中则需要使用变通的方法：

```
import os
import inspect
import sys
if not hasattr(sys.modules[__name__], '__file__'):
    __file__ = inspect.getfile(inspect.currentframe())

print os.path.dirname(os.path.abspath(__file__))

```


