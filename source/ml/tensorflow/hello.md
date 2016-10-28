
# TensorFlow Basic Operations

TensorFlow is a programming system in which you represent computations as graphs. Nodes in the graph are called ops (short for operations). An op takes zero or more Tensors, performs some computation, and produces zero or more Tensors. A Tensor is a typed multi-dimensional array. For example, you can represent a mini-batch of images as a 4-D array of floating point numbers with dimensions [batch, height, width, channels].

TensorFlow programs use a tensor data structure to represent all data -- only tensors are passed between operations in the computation graph. You can think of a TensorFlow tensor as an n-dimensional array or list. A tensor has a static type, a rank, and a shape.


```python
import tensorflow as tf
```

## Basic type


```python
# Constant

a = tf.constant(2)
b = tf.constant(3)

with tf.Session() as sess:
    print sess.run(a+b)
```

    5



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
    print sess.run(v1+v2)
```

    15



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
    print sess.run(add, feed_dict={a: 2, b: 3})
    print sess.run(mul, feed_dict={a: 2, b: 3})
```

    5
    6



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
    print product.eval()
```

    [[ 12.]]


## Graph and session

A TensorFlow graph is a description of computations. To compute anything, a graph must be launched in a Session. A Session places the graph ops onto Devices, such as CPUs or GPUs, and provides methods to execute them. These methods return tensors produced by ops as numpy ndarray objects in Python, and as tensorflow::Tensor instances in C and C++.


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
```

    [ 3.  8.]
    [ 3.  8.]


For ease of use in interactive Python environments, such as IPython you can instead use the InteractiveSession class, and the Tensor.eval() and Operation.run() methods. This avoids having to keep a variable holding the session.


```python
sess = tf.InteractiveSession()

x = tf.Variable([1.0, 2.0])
a = tf.constant([3.0, 3.0])

# Initialize 'x' using the run() method of its initializer op.
x.initializer.run()

# Add an op to subtract 'a' from 'x'.  Run it and print the result
sub = tf.sub(x, a)
print(sub.eval())
# ==> [-2. -1.]

# Close the Session when we're done.
sess.close()
```

    [-2. -1.]


## Complete demo


```python
#!/usr/bin/env python
import tensorflow as tf

# Create a Constant op
# The op is added as a node to the default graph.
#
# The value returned by the constructor represents the output
# of the Constant op.
hello = tf.constant('Hello, TensorFlow!')
x = tf.placeholder("float", 3)
a = tf.placeholder("float", shape=[None, 3])

y = x*2
b = a*2

# Start tf session
sess = tf.Session()
sess.run(tf.initialize_all_tables())

print sess.run(hello)
print sess.run(y, feed_dict={x:[1,2,3]})
print sess.run(b, feed_dict={a:[[1,2,3], [4,5,6]]})

sess.close()
```

    Hello, TensorFlow!
    [ 2.  4.  6.]
    [[  2.   4.   6.]
     [  8.  10.  12.]]



```python

```
