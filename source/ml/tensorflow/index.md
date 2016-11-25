# Tensorflow tutorials

![](/images/14798901858154.jpg)

Tensorflow是谷歌在2015年11月开源的机器学习框架，来源于Google内部的深度学习框架DistBelief。由于其良好的架构、分布式架构支持以及简单易用，自开源以来得到广泛的关注。主要特点包括：

- 良好的架构，使用数据流图来进行数值计算
- 简单易用，并且社区还有很多的模型封装（比如keras和skflow等）
- 灵活高效，既可以使用CPU，也可以使用GPU
- 开放活跃的社区

## Tensorflow架构

Tensorflow官方定义为：

> Tensorflow是一个使用数据流图(data flow graphs)技术来进行数值计算的开源软件库。

![](/images/14798908006236.gif)


数据流图是是一个有向图，使用结点（一般用圆形或者方形描述，表示一个数学操作或者数据输入的起点和数据输出的终点）和线（表示数字、矩阵或者Tensor张量）来描述数学计算。数据流图可以方便的将各个节点分配到不同的计算设备上完成异步并行计算，非常适合大规模的机器学习应用。

![](/images/14798912403951.jpg)

## 应用场景

- 机器学习相关的开发研究
- 开发与部署一体化的架构
- 大规模分布式模型
- 嵌入式或移动设备模型

## 链接

- 官方网站: <https://www.tensorflow.org/>
- Github: <https://github.com/tensorflow/tensorflow>
- Tensorflow models: <https://github.com/tensorflow/models>
- Tensorflow ecosystem: <https://github.com/tensorflow/ecosystem>


