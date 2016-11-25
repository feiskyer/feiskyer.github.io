---
title: Machine Learning
date: 2016-10-24 22:16:07
---

# Machine Learning

- [基本](basic/)
- [监督学习概览](supervised-learning.html)
- [线性回归](regression/linear.html)
- [逻辑回归](regression/logistic.html)
- [RNN](rnn/)
- [CNN](cnn/)
- [可视化](visualization/)

## [TensorFlow](tensorflow/)

```
docker run -itd -p 8888:8888 -p 6006:6006 tensorflow/tensorflow
```

With GPU

```
$ export CUDA_SO=$(\ls /usr/lib/x86_64-linux-gnu/libcuda* | xargs -I{} echo '-v {}:{}')
$ export DEVICES=$(\ls /dev/nvidia* | xargs -I{} echo '--device {}:{}')
$ docker run -it -p 8888:8888 $CUDA_SO $DEVICES tensorflow/tensorflow-devel-gpu
```

## [Machine Learning Cheet Sheet](cheatsheet.html)

![](/images/14781583352915.png)

There is also a good diagram from Dlib:

![ml_guide](/images/ml_guide.png)


## Readings

1.  [Deep Learning](http://www.iro.umontreal.ca/~bengioy/dlbook/) by Yoshua Bengio, Ian Goodfellow and Aaron Courville
2.  [Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/) by  Michael Nielsen
3.  [Deep Learning](http://research.microsoft.com/pubs/209355/DeepLearning-NowPublishing-Vol7-SIG-039.pdf) by Microsoft Research
4.  [Deep Learning Tutorial](http://deeplearning.net/tutorial/deeplearning.pdf) by LISA lab, University of Montreal

## DataSets

- [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/)
- [MNIST Database of handwritten digits](http://yann.lecun.com/exdb/mnist/)
- [The street View House Numbers](http://ufldl.stanford.edu/housenumbers/)
- [CIFAR-10 and CIFAR-100 tiny images](http://www.cs.toronto.edu/~kriz/cifar.html)
- [IMAGENET](http://www.image-net.org/)
- [Visual Dictionary tiny images](http://www.image-net.org/)
- [Flickr images](https://yahooresearch.tumblr.com/)
- [The Berkeley Segmentation Dataset](https://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/)

##  Landscape of machine intelligence

![](/images/14797924028207.jpg)


**References:**

- <http://scikit-learn.org/stable/tutorial/machine_learning_map/>
- <http://dlib.net/ml_guide.svg>
- <http://www.shivonzilis.com/>

