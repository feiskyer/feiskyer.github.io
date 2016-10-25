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
