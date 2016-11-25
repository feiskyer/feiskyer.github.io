---
title: 卷积
date: 2016-11-11 22:22:22
---

# 卷积（Convolution）

图像的卷积定义为

$$f(x) = act(\sum_{i, j}^n \theta_{(n - i)(n - j)} x_{ij} + b)$$

其计算过程为

![](/images/14799893344613.jpg)

## 示例

```python
import tensorflow as tf
import numpy as np

sess = tf.InteractiveSession()
input_batch = tf.constant([
        [  # First Input
            [[0.0], [1.0]],
            [[2.0], [3.0]]
        ],
        [  # Second Input
            [[2.0], [4.0]],
            [[6.0], [8.0]]
        ]
    ])

kernel = tf.constant([
        [
            [[1.0, 2.0]]
        ]
    ])

conv2d = tf.nn.conv2d(input_batch, kernel, strides=[1, 1, 1, 1], padding='SAME')
print sess.run(conv2d)

lower_right_image_pixel = sess.run(input_batch)[0][1][1]
lower_right_kernel_pixel = sess.run(conv2d)[0][1][1]
print lower_right_image_pixel, lower_right_kernel_pixel
```

output => 

```
[[[[  0.   0.]
   [  1.   2.]]

  [[  2.   4.]
   [  3.   6.]]]


 [[[  2.   4.]
   [  4.   8.]]

  [[  6.  12.]
   [  8.  16.]]]]
[ 3.] [ 3.  6.]
```

## 示例2

```python
import tensorflow as tf
import numpy as np

sess = tf.InteractiveSession()
input_batch = tf.constant([
        [  # First Input (6x6x1)
            [[0.0], [1.0], [2.0], [3.0], [4.0], [5.0]],
            [[0.1], [1.1], [2.1], [3.1], [4.1], [5.1]],
            [[0.2], [1.2], [2.2], [3.2], [4.2], [5.2]],
            [[0.3], [1.3], [2.3], [3.3], [4.3], [5.3]],
            [[0.4], [1.4], [2.4], [3.4], [4.4], [5.4]],
            [[0.5], [1.5], [2.5], [3.5], [4.5], [5.5]],
        ],
    ])

kernel = tf.constant([  # Kernel (3x3x1)
        [[[0.0]], [[0.5]], [[0.0]]],
        [[[0.0]], [[1.0]], [[0.0]]],
        [[[0.0]], [[0.5]], [[0.0]]]
    ])

# NOTE: the change in the size of the strides parameter.
conv2d = tf.nn.conv2d(input_batch, kernel, strides=[1, 3, 3, 1], padding='SAME')
sess.run(conv2d)
```

output =>

```
array([[[[ 2.20000005],
         [ 8.19999981]],

        [[ 2.79999995],
         [ 8.80000019]]]], dtype=float32)
```

## 示例3（图像卷积）

原始图片：

![](/images/14800378635343.jpg)

提取边缘：

```python
%matplotlib inline
import matplotlib as mil
#mil.use('svg')
mil.use("nbagg")

import tensorflow as tf
import numpy as np
from matplotlib import pyplot
sess = tf.InteractiveSession()

image_filename = "n02113023_219.jpg"
filename_queue = tf.train.string_input_producer(
    tf.train.match_filenames_once(image_filename))

image_reader = tf.WholeFileReader()
_, image_file = image_reader.read(filename_queue)
image = tf.image.decode_jpeg(image_file)

sess.run(tf.initialize_all_variables())
coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(coord=coord)

image_batch = tf.image.convert_image_dtype(tf.expand_dims(image, 0), tf.float32, saturate=False)

kernel = tf.constant([
        [
            [[ -1., 0., 0.], [ 0., -1., 0.], [ 0., 0., -1.]],
            [[ -1., 0., 0.], [ 0., -1., 0.], [ 0., 0., -1.]],
            [[ -1., 0., 0.], [ 0., -1., 0.], [ 0., 0., -1.]]
        ],
        [
            [[ -1., 0., 0.], [ 0., -1., 0.], [ 0., 0., -1.]],
            [[ 8., 0., 0.], [ 0., 8., 0.], [ 0., 0., 8.]],
            [[ -1., 0., 0.], [ 0., -1., 0.], [ 0., 0., -1.]]
        ],
        [
            [[ -1., 0., 0.], [ 0., -1., 0.], [ 0., 0., -1.]],
            [[ -1., 0., 0.], [ 0., -1., 0.], [ 0., 0., -1.]],
            [[ -1., 0., 0.], [ 0., -1., 0.], [ 0., 0., -1.]]
        ]
    ])


conv2d = tf.nn.conv2d(image_batch, kernel, [1, 1, 1, 1], padding="SAME")
activation_map = sess.run(tf.minimum(tf.nn.relu(conv2d), 255))

fig = pyplot.gcf() #pyplot.figure()
ax1 = fig.add_subplot(121)
ax1.set_title("original")
ax1.set_xticks([])
ax1.set_yticks([])
ax1.imshow(image_batch[0].eval(), interpolation='nearest')
ax2 = fig.add_subplot(122)
ax2.imshow(activation_map[0], interpolation='nearest')
ax2.set_title("after")
ax2.set_xticks([])
ax2.set_yticks([])
# fig.set_size_inches(4, 4)
# fig.savefig("example-edge-detection.png")
fig.show()

filename_queue.close(cancel_pending_enqueues=True)
coord.request_stop()
coord.join(threads)
```

![](/images/14800377001999.jpg)

还有很多其他的卷积核<https://en.wikipedia.org/wiki/Kernel_(image_processing)>，比如

```python
kernel = tf.constant([
        [
            [[ 0., 0., 0.], [ 0., 0., 0.], [ 0., 0., 0.]],
            [[ -1., 0., 0.], [ 0., -1., 0.], [ 0., 0., -1.]],
            [[ 0., 0., 0.], [ 0., 0., 0.], [ 0., 0., 0.]]
        ],
        [
            [[ -1., 0., 0.], [ 0., -1., 0.], [ 0., 0., -1.]],
            [[ 5., 0., 0.], [ 0., 5., 0.], [ 0., 0., 5.]],
            [[ -1., 0., 0.], [ 0., -1., 0.], [ 0., 0., -1.]]
        ],
        [
            [[ 0., 0., 0.], [ 0., 0., 0.], [ 0., 0., 0.]],
            [[ -1., 0., 0.], [ 0., -1., 0.], [ 0., 0., -1.]],
            [[ 0, 0., 0.], [ 0., 0., 0.], [ 0., 0., 0.]]
        ]
    ])


conv2d = tf.nn.conv2d(image_batch, kernel, [1, 1, 1, 1], padding="SAME")
activation_map = sess.run(tf.minimum(tf.nn.relu(conv2d), 255))

fig = pyplot.gcf() #pyplot.figure()
ax1 = fig.add_subplot(121)
ax1.set_title("original")
ax1.set_xticks([])
ax1.set_yticks([])
ax1.imshow(image_batch[0].eval(), interpolation='nearest')
ax2 = fig.add_subplot(122)
ax2.imshow(activation_map[0], interpolation='nearest')
ax2.set_title("after")
ax2.set_xticks([])
ax2.set_yticks([])
```

![](/images/14800377471467.jpg)

**参考**

- [working with images](https://github.com/backstopmedia/tensorflowbook/blob/master/chapters/05_object_recognition_and_classification/Chapter%205%20-%2004%20Working%20with%20Images.ipynb)

