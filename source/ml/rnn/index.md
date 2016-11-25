---
title: 递归神经网络
date: 2016-11-11 22:22:22
---

# 递归神经网络（Recurrent Neural Networks，RNN）

递归神经网络（RNN）是两种人工神经网络的总称：时间递归神经网络（recurrent neural network）和结构递归神经网络（recursive neural network）。时间递归神经网络的神经元间连接构成有向图，而结构递归神经网络利用相似的神经网络结构递归构造更为复杂的深度网络。RNN一般指代时间递归神经网络。单纯递归神经网络因为无法处理随着递归，权重指数级爆炸或消失的问题（Vanishing gradient problem），难以捕捉长期时间关联；而结合不同的LSTM可以很好解决这个问题。时间递归神经网络可以描述动态时间行为，因为和前馈神经网络（feedforward neural network）接受较特定结构的输入不同，RNN将状态在自身网络中循环传递，因此可以接受更广泛的时间序列结构输入。

![](/images/14800610249665.png)


## 序列数据

RNN主要解决序列数据的处理，比如文本、语音、视频等等。这类数据的样本间存在顺序关系，每个样本和它之前的样本存在关联。比如说，在文本中，一个词和它前面的词是有关联的；在气象数据中，一天的气温和前几天的气温是有关联的。一组观察数据定义为一个序列，从分布中可以观察出多个序列。

一个序列$X\{x_1, x_2, \ldots, x_N\}$的最简单模型为 

$$P(X)=\prod_{i=1}^N{P(x_i|x_1,\ldots,x_{i-1})}$$

也就是说，序列里的每一个元素都和排在它前面的所有元素直接相关。

当然，这个模型存在致命的问题：它的复杂度会爆炸性增长，$O(N!)$。隐马尔科夫模型（HMM）定义每个元素只和离它最近的$k$个元素相关，解决了复杂度暴增的问题，模型为

$$P(X)=\prod_{i=1}^N{P(x_i|x_{i-1},\ldots,x_{i-(k-1)})}$$

当$k=1$时，模型变为$P(X)=\prod_{i=1}^N{P(x_i|x_{i-1})}$。

只考虑观察值$X$的模型有时表现力不足，因此需要加入隐变量，将观察值建模成由隐变量所生成。隐变量的好处在于，它的数量可以比观察值多，取值范围可以比观察值更广，能够更好的表达有限的观察值背后的复杂分布。加入了隐变量$h$的马尔科夫模型称为隐马尔科夫模型。

$$P(x_1, \ldots, x_T, h_1, \ldots, h_T, \theta) = P(h_1) \prod^T_{t=2}{P(h_t|h_{t-1})} \prod^T_{t=1}{(x_t|h_t)}$$

隐马尔科夫模型实际上建模的是观察值X，隐变量h和模型参数θ的联合分布,HMM的模型长度T是事先固定的，模型参数不共享，其复杂度为$O(T)$。

## RNN

![](/images/14800603666370.png)

把序列视作时间序列，隐含层$h$的自连接边实际上是和上一时刻的$h$相连（上面左图）。在每一个时刻$t$，$h_t$的取值是当前时刻的输入$x_t$，和上一时刻的隐含层值$h_{t-1}$的一个函数：

$$h_t = F_{\theta}(h_{t-1}, x_t)$$

将$h$层的自连接展开，就成为了上图右边的样子，看上去和HMM很像。两者最大的区别在于，RNN的参数是跨时刻共享的。也就是说，对任意时刻$t$，$h_{t-1}$到$h_t$以及$x_t$到$h_t$的网络参数都是相同的。

共享参数的思想和和卷积神经网络（CNN）是相通的，CNN在二维数据的空间位置之间共享卷积核参数，而RNN则是在序列数据的时刻之间共享参数。共享参数使得模型的复杂度大大减少，并使RNN可以适应任意长度的序列，带来了更好的可推广性。

## RNN变种

**双向RNN**

单向RNN的问题在于$t$时刻进行分类的时候只能利用$t$时刻之前的信息， 但是在$t$时刻进行分类的时候可能也需要利用未来时刻的信息。双向RNN（bi-directional RNN）模型正是为了解决这个问题， 双向RNN在任意时刻$t$都保持两个隐藏层，一个隐藏层用于从左往右的信息传播记作， 另一个隐藏层用于从右往左的信息传播记作。

![](/images/14800674189366.jpg)


**Deep RNN**

Deep(Bidirectional)RNNs与Bidirectional RNNs相似，只是对于每一步的输入有多层网络。这样，该网络便有更强大的表达与学习能力，但是复杂性也提高了，同时需要更多的训练数据。

![](/images/14800617168946.jpg)

## Vanishing and Exploding Gradients

![](/images/14800646899102.jpg)

> The reason why it is difficult for an RNN to learn such long-term dependencies lies in how errors are propagated trough the network during optimization. Remember that we propagate the errors through the unfolded RNN in order to compute the gradients. For long sequences, the unfolded network gets very deep and has many layers. At each layer, backpropagation scales the error from above in the network by the local derivatives.
> 
> If most of local derivatives are much smaller than the value of one, the gradient gets scaled down at every layer causing it to shrink exponentially and eventually, vanish. Analogously, many local derivatives being greater than one cause the gradient to explode.

This problem actually exists in any deep networks, not just recurrent ones. However, in RNNs the connections between time steps are tied each. Therefore, local derivatives of such weights are either all lesser or all greater than one and the gradient is alawys scaled in the same direction for each weight in the original (not unfolded) RNN. Therefore, the problem of vanishing and exploding gradients is more prominent in RNNs than in forward networks.


## LSTM

LSTM 全称叫 Long Short Term Memory networks，它和传统 RNN 唯一的不同就在与其中的神经元（感知机）的构造不同。传统的 RNN 每个神经元和一般神经网络的感知机没啥区别，但在 LSTM 中，每个神经元是一个“记忆细胞”（have an internal state that helps to remember errors over many time steps. this internal state has a self-connection with a fixed weight of one and a linear activation function, so that its local derivative is always one），细胞里面有一个“输入门”（input gate）, 一个“遗忘门”（forget gate）， 一个“输出门”（output gate）：

![](/images/14800648468281.jpg)
![](/images/14800650119222.jpg)

这个设计的用意在于，能够使得 LSTM 维持两条线，两条线互相呼应，互相纠缠:

1. 一条明线: 当前时刻的数据流（包括其他细胞的输入和来自数据的输入）
2. 一条暗线: 这个细胞本身的记忆流

典型的工作流为：在“输入门”中，根据当前的数据流来控制接受细胞记忆的影响；接着，在 “遗忘门”里，更新这个细胞的记忆和数据流；然后在“输出门”里产生输出更新后的记忆和数据流。LSTM 模型的关键之一就在于这个“遗忘门”， 它能够控制训练时候梯度在这里的收敛性（从而避免了 RNN 中的梯度 vanishing/exploding 问题），同时也能够保持长期的记忆性。

目前 LSTM 模型在实践中取得了非常好的效果， 只需要训练一个两三层的LSTM, 它就可以

- 模仿保罗·格雷厄姆进行[写作](https://github.com/karpathy/char-rnn)
- 生成维基百科的 markdown 页面
- 手写[识别](https://github.com/szcom/rnnlib)
- 帮你写[代码](http://cs.stanford.edu/people/karpathy/char-rnn/)

![](/images/14800610955452.png)


**参考文档**

- [从HMM到RNN](http://rayz0620.github.io/2015/05/14/rnn_note_1/)
- [Understanding LSTM Networks](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- [深度循环神经网络与LSTM 模型](https://www.15yan.com/story/huxAyyeuYAj/)


