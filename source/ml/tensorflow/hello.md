
# TensorFlow基本操作

```python
import tensorflow as tf
```

## 简单示例

![](/images/14798939270478.jpg)

```python
import tensorflow as tf

a = tf.constant(5, name="input_a")
b = tf.constant(3, name="input_b")
c = tf.mul(a, b, name="mul_c")
d = tf.add(a, b, name="add_d")
e = tf.add(c, d, name="add_e")

with tf.Session() as sess:
    print sess.run(e) # output => 23
    writer = tf.train.SummaryWriter("./hello_graph", sess.graph)
```

接着，可以启动tensorboard来查看这个Graph（在jupyter notebookt中可以执行`!tensorboard --logdir="hello_graph"`）：

```sh
tensorboard --logdir="hello_graph"
```

打开网页<http://localhost:6006>并切换到GRAPHS标签，可以看到生成的Graph：

![](/images/14798950663351.jpg)

## Tensor简单示例

再来看一个输入向量的例子:

![](/images/14798951652137.jpg)

```python
import tensorflow as tf

a = tf.constant([5,3], name="input_a")
b = tf.reduce_prod(a, name="prod_b")
c = tf.reduce_sum(a, name="sum_c")
d = tf.add(c, b, name="add_d")

with tf.Session() as sess:
    print sess.run(d) # => 23
```

## 基本类型

常量：

```python
# Constant

a = tf.constant(2)
b = tf.constant(3)

with tf.Session() as sess:
    print sess.run(a+b)  # => 5
```

变量在计算过程中是可变的，并且在训练过程中会自动更新或优化。如果只想在tf外手动更新变量，那需要声明变量是不可训练的，比如`not_trainable = tf.Variable(0, trainable=False)`。

```python
# Variable
# Variables maintain state across executions of the 
# graph. The following example shows a variable serving
# as a simple counter.

v1 = tf.Variable(10)
v2 = tf.Variable(5)

with tf.Session() as sess:
    # variables must be initialized first.
    tf.initialize_all_variables().run(session=sess)
    print sess.run(v1+v2) # => 15
```

```python
# Placeholder and feed
# Placeholder is used as Graph input when running session
# A feed temporarily replaces the output of an operation
# with a tensor value. You supply feed data as an argument
# to a run() call. The feed is only used for the run call 
# to which it is passed. The most common use case involves
# designating specific operations to be "feed" operations
# by using tf.placeholder() to create them

a = tf.placeholder(tf.int16)
b = tf.placeholder(tf.int16)

# Define some operations
add = tf.add(a, b)
mul = tf.mul(a, b)

with tf.Session() as sess:
    print sess.run(add, feed_dict={a: 2, b: 3})  # ==> 5
    print sess.run(mul, feed_dict={a: 2, b: 3})  # ==> 6
```

```python
# Matrix

# Create a Constant op that produces a 1x2 matrix.  The op is
# added as a node to the default graph.
#
# The value returned by the constructor represents the output
# of the Constant op.
matrix1 = tf.constant([[3., 3.]])

# Create another Constant that produces a 2x1 matrix.
matrix2 = tf.constant([[2.],[2.]])

# Create a Matmul op that takes 'matrix1' and 'matrix2' as inputs.
# The returned value, 'product', represents the result of the matrix
# multiplication.
product = tf.matmul(matrix1, matrix2)
with tf.Session() as sess:
    print product.eval() # => 12
```

## [数据类型](https://www.tensorflow.org/versions/master/resources/dims_types.html#tensor-ranks-shapes-and-types)

Tensorflow有着丰富的数据类型，比如tf.int32, tf.float64等，这些类型跟numpy是一致的。

```python
import tensorflow as tf
import numpy as np

a = np.array([2, 3], dtype=np.int32)
b = np.array([4, 5], dtype=np.int32)
# Use `tf.add()` to initialize an "add" Operation
c = tf.add(a, b)

with tf.Session() as sess:
    print sess.run(c) # ==> [6 8]
```

## 数学计算

TF内置了很多的数学计算操作，包括常见的各种数值计算、矩阵运算以及优化算法。

更多见<https://www.tensorflow.org/versions/master/api_docs/python/math_ops.html>.

## [Rank与Shape](https://www.tensorflow.org/versions/master/resources/dims_types.html#tensor-ranks-shapes-and-types)

Rank | Shape              | Dimension number | Example                                
---- | ------------------ | ---------------- | ---------------------------------------
0    | []                 | 0-D              | A 0-D tensor.  A scalar.               
1    | [D0]               | 1-D              | A 1-D tensor with shape [5].           
2    | [D0, D1]           | 2-D              | A 2-D tensor with shape [3, 4].        
3    | [D0, D1, D2]       | 3-D              | A 3-D tensor with shape [1, 4, 3].     
n    | [D0, D1, ... Dn-1] | n-D              | A tensor with shape [D0, D1, ... Dn-1].

## 图和会话

A TensorFlow graph is a description of computations. To compute anything, a graph must be launched in a Session. A Session places the graph ops onto Devices, such as CPUs or GPUs, and provides methods to execute them. These methods return tensors produced by ops as numpy ndarray objects in Python, and as `tensorflow::Tensor` instances in C and C++.

如果不指定图，tensorflow会自动创建一个，可以通过`tf.get_default_graph()`来获取这个默认图。

```python
graph = tf.Graph()
with graph.as_default():
    value1 = tf.constant([1., 2.])
    value2 = tf.Variable([3., 4.])
    result = value1*value2
with tf.Session(graph=graph) as sess:
    tf.initialize_all_variables().run()
    print sess.run(result)
    print result.eval()

# result =>
#    [ 3.  8.]
#    [ 3.  8.]
```

在指定GPU上计算:

```python
with tf.Session() as sess:
  with tf.device("/gpu:1"):
    matrix1 = tf.constant([[3., 3.]])
    matrix2 = tf.constant([[2.],[2.]])
    product = tf.matmul(matrix1, matrix2)
    ...
```

在IPython中可以使用InteractiveSession来简化Session操作：

```python
sess = tf.InteractiveSession()

x = tf.Variable([1.0, 2.0])
a = tf.constant([3.0, 3.0])

# Initialize 'x' using the run() method of its initializer op.
x.initializer.run()

# Add an op to subtract 'a' from 'x'.  Run it and print the result
sub = tf.sub(x, a)
print(sub.eval())  # ==> [-2. -1.]

# Close the Session when we're done.
sess.close()
```

## Name Scope

Name scopes可以把复杂操作分成小的命名块，方便组织复杂的图，并方便在TensorBoard展示。

```python
import tensorflow as tf

with tf.name_scope("Scope_A"):
    a = tf.add(1, 2, name="A_add")
    b = tf.mul(a, 3, name="A_mul")

with tf.name_scope("Scope_B"):
    c = tf.add(4, 5, name="B_add")
    d = tf.mul(c, 6, name="B_mul")

e = tf.add(b, d, name="output")
writer = tf.train.SummaryWriter('./name_scope_1', graph=tf.get_default_graph())
writer.close()
```

![](/images/14799079221189.jpg)


## 一个完整示例

```python
import tensorflow as tf

# Define a new Graph
graph = tf.Graph()

with graph.as_default():

    with tf.name_scope("variables"):
        # Variable to keep track of how many times the graph has been run
        global_step = tf.Variable(0, dtype=tf.int32, trainable=False, name="global_step")

        # Variable that keeps track of the sum of all output values over time:
        total_output = tf.Variable(0.0, dtype=tf.float32, trainable=False, name="total_output")

    # Primary transformation Operations
    with tf.name_scope("transformation"):
        # Separate input layer
        with tf.name_scope("input"):
            # Create input placeholder- takes in a Vector
            a = tf.placeholder(tf.float32, shape=[None], name="input_placeholder_a")

        # Separate middle layer
        with tf.name_scope("intermediate_layer"):
            b = tf.reduce_prod(a, name="product_b")
            c = tf.reduce_sum(a, name="sum_c")

        # Separate output layer
        with tf.name_scope("output"):
            output = tf.add(b, c, name="output")

    with tf.name_scope("update"):
        # Increments the total_output Variable by the latest output
        update_total = total_output.assign_add(output)

        # Increments the above `global_step` Variable, should be run whenever the graph is run
        increment_step = global_step.assign_add(1)

    # Summary Operations
    with tf.name_scope("summaries"):
        avg = tf.div(update_total, tf.cast(increment_step, tf.float32), name="average")

        # Creates summaries for output node
        tf.scalar_summary(b'Output', output, name="output_summary")
        tf.scalar_summary(b'Sum of outputs over time', update_total, name="total_summary")
        tf.scalar_summary(b'Average of outputs over time', avg, name="average_summary")

    # Global Variables and Operations
    with tf.name_scope("global_ops"):
        # Initialization Op
        init = tf.initialize_all_variables()
        # Merge all summaries into one Operation
        merged_summaries = tf.merge_all_summaries()

# Start a Session, using the explicitly created Graph
sess = tf.Session(graph=graph)

# Open a SummaryWriter to save summaries
writer = tf.train.SummaryWriter('./improved_graph', graph)

# Initialize Variables
sess.run(init)


def run_graph(input_tensor):
    """
    Helper function; runs the graph with given input tensor and saves summaries
    """
    feed_dict = {a: input_tensor}
    _, step, summary = sess.run([output, increment_step, merged_summaries],
                                  feed_dict=feed_dict)
    writer.add_summary(summary, global_step=step)

# run graph with some inputs
run_graph([2,8])
run_graph([3,1,3,3])
run_graph([8])
run_graph([1,2,3])
run_graph([11,4])
run_graph([4,1])
run_graph([7,3,1])
run_graph([6,3])
run_graph([0,2])
run_graph([4,5,6])

# flush summeries to disk
writer.flush()

# close writer and session
writer.close()
sess.close()
```

Tensorboard图：

![](/images/14799088837355.jpg)

Tensorboard事件：

![](/images/14799089956982.jpg)

