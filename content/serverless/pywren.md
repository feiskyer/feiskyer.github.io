---
title: PyWren
type: page
---

[PyWren](https://github.com/ericmjonas/pywren)是一个基于AWS Lambda的Python计算框架，模拟了[Python futures](http://pythonhosted.org/futures/)包的map/reduce功能，非常适用于机器学习参数调优（parameter tuning）等科学计算任务。

> Behind the scenes, PyWren serializes the function with the data, using Python’s Pickle serialization function and a bit of technology borrowed from the PySpark project. PyWren places serialized data and function into S3, then evokes Lambda, along with a slimmed-down version of Anaconda, a packaged version of Python and supporting tools offered by Continuum IO. The results are delivered back to S3, then unpickled, and returned to the user.


## 示例

### Hello world

```python
import pywren
import numpy as np

def addone(x):
    return x + 1

    wrenexec = pywren.default_executor()
    xlist = np.arange(10)
    futures = wrenexec.map(addone, xlist)

    print [f.result() for f in futures]
```

### FLOPS

```python
loopcnt = 10

def big_flops(std_dev):
    running_sum = 0
    for i in loopcnt:
        A = np.random.normal(0, std_dev, (4096, 4096))
        B = np.random.normal(0, std_dev, (4096, 4096))
        c = np.dot(A, B)
        running_sum += np.sum(c)
    return running_sum

wrenexec = pywren.default_executor()
std_devs = np.linspace(1, 10, 1600)
futures = wrenexec.map(big_flops, std_devs)
pywren.wait(futures)
```

## 链接

- [PyWren Github](https://github.com/ericmjonas/pywren)
- [PyWren examples](https://github.com/ericmjonas/pywren/tree/master/examples)
- [With PyWren, AWS Lambda Finds an Unexpected Market in Scientific Computing](https://thenewstack.io/aws-lambda-finds-unexpected-market-scientific-computing/)
