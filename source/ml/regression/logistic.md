# Logistic Regression

Softmax function:
![](/images/14799623866417.jpg)

![](/images/14799624626532.jpg)

## 逻辑回归示例

```python
import os
import tensorflow as tf

# initialize variables/model parameters
W = tf.Variable(tf.zeros([5, 1]), name="weights")
b = tf.Variable(0., name="bias")

def read_csv(batch_size, file_name, record_defaults):
    filename_queue = tf.train.string_input_producer(
        [os.path.dirname(__file__) + "/" + file_name])

    reader = tf.TextLineReader(skip_header_lines=1)
    key, value = reader.read(filename_queue)

    # decode_csv will convert a Tensor from type string (the text line) in
    # a tuple of tensor columns with the specified defaults, which also
    # sets the data type for each column
    decoded = tf.decode_csv(value, record_defaults=record_defaults)

    # batch actually reads the file and loads "batch_size" rows in a single
    # tensor
    return tf.train.shuffle_batch(decoded,
                                  batch_size=batch_size,
                                  capacity=batch_size * 50,
                                  min_after_dequeue=batch_size)

def inference(X):
    # compute inference model over data X and return the result
    return tf.sigmoid(tf.matmul(X, W) + b)

def loss(X, Y):
    # compute loss over training data X and expected outputs Y
    return tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
        tf.matmul(X, W) + b, Y))

def inputs():
    # data is downloaded from https://www.kaggle.com/c/titanic/data.
    passenger_id, survived, pclass, name, sex, age, sibsp, parch, ticket, fare,\
        cabin, embarked = read_csv(100,
                                   "train.csv",
                                   [[0.0], [0.0], [0], [""],
                                    [""], [0.0], [0.0], [0.0],
                                    [""], [0.0], [""], [""]])

    # convert categorical data
    is_first_class = tf.to_float(tf.equal(pclass, [1]))
    is_second_class = tf.to_float(tf.equal(pclass, [2]))
    is_third_class = tf.to_float(tf.equal(pclass, [3]))
    gender = tf.to_float(tf.equal(sex, ["female"]))

    # Finally we pack all the features in a single matrix;
    # We then transpose to have a matrix with one example per row and one
    # feature per column.
    features = tf.transpose(
        tf.pack([is_first_class,
                 is_second_class,
                 is_third_class,
                 gender,
                 age]))
    survived = tf.reshape(survived, [100, 1])

    return features, survived


def train(total_loss):
    # train / adjust model parameters according to computed total loss
    learning_rate = 0.01
    return tf.train.GradientDescentOptimizer(learning_rate).minimize(
        total_loss)


def evaluate(sess, X, Y):
    # evaluate the resulting trained model
    predicted = tf.cast(inference(X) > 0.5, tf.float32)

    print sess.run(tf.reduce_mean(tf.cast(tf.equal(predicted, Y), tf.float32)))

# Create a saver.
# saver = tf.train.Saver()

# Launch the graph in a session, setup boilerplate
with tf.Session() as sess:
    tf.initialize_all_variables().run()

    X, Y = inputs()

    total_loss = loss(X, Y)
    train_op = train(total_loss)

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    # actual training loop
    training_steps = 1000
    for step in range(training_steps):
        sess.run([train_op])
        # for debugging and learning purposes, see how the loss gets decremented
        # through training steps
        if step % 100 == 0:
            print "loss at step ", step, ":", sess.run([total_loss])
        # save training checkpoints in case loosing them
        # if step % 1000 == 0:
        #     saver.save(sess, 'my-model', global_step=step)

    evaluate(sess, X, Y)
    coord.request_stop()
    coord.join(threads)
    # saver.save(sess, 'my-model', global_step=training_steps)
```

```
loss at step  0 : [1.0275139]
loss at step  100 : [1.389969]
loss at step  200 : [1.4667224]
loss at step  300 : [0.67178178]
loss at step  400 : [0.568793]
loss at step  500 : [0.48835525]
loss at step  600 : [1.0899736]
loss at step  700 : [0.84278578]
loss at step  800 : [1.0500686]
loss at step  900 : [0.89417559]
0.72
```

## minst示例

```python
import tensorflow as tf
import numpy as np
import input_data

# Import MINST data
mnist = input_data.read_data_sets("../MNIST_data/", one_hot=True)
```

    Extracting ../MNIST_data/train-images-idx3-ubyte.gz
    Extracting ../MNIST_data/train-labels-idx1-ubyte.gz
    Extracting ../MNIST_data/t10k-images-idx3-ubyte.gz
    Extracting ../MNIST_data/t10k-labels-idx1-ubyte.gz


```python
# Parameters
learning_rate = 0.01
training_epochs = 25
batch_size = 100
display_step = 1

# tf Graph Input
x = tf.placeholder("float", [None, 784]) # mnist data image of shape 28*28=784
y = tf.placeholder("float", [None, 10]) # 0-9 digits recognition => 10 classes

# Create model
def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))

def model(X, w):
    return tf.matmul(X, w)

# like in linear regression, we need a shared variable weight matrix
# for logistic regression
w = init_weights([784, 10]) 

# Construct model
# compute mean cross entropy (softmax is applied internally)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(model(x, w), y)) 
train_op = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost) # construct optimizer
predict_op = tf.argmax(model(x, w), 1) # at predict time, evaluate the argmax of the logistic regression

# Launch the graph
with tf.Session() as sess:
    tf.initialize_all_variables().run()

    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = int(mnist.train.num_examples/batch_size)
        # Loop over all batches
        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            # Fit training using batch data
            sess.run(train_op, feed_dict={x: batch_xs, y: batch_ys})
            # Compute average loss
            avg_cost += sess.run(cost, feed_dict={x: batch_xs, y: batch_ys})/total_batch
        # Display logs per epoch step
        if epoch % display_step == 0:
            print "Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost)

    print "Optimization Finished!"

    # Test model
    correct_prediction = tf.equal(predict_op, tf.argmax(y, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print "Accuracy:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels})
```

    Epoch: 0001 cost= 1.181141054
    Epoch: 0002 cost= 0.664358092
    Epoch: 0003 cost= 0.553026987
    Epoch: 0004 cost= 0.499294951
    Epoch: 0005 cost= 0.466518660
    Epoch: 0006 cost= 0.443856266
    Epoch: 0007 cost= 0.427351894
    Epoch: 0008 cost= 0.414347254
    Epoch: 0009 cost= 0.403219846
    Epoch: 0010 cost= 0.394844531
    Epoch: 0011 cost= 0.387121435
    Epoch: 0012 cost= 0.380693078
    Epoch: 0013 cost= 0.375634897
    Epoch: 0014 cost= 0.369904718
    Epoch: 0015 cost= 0.365776612
    Epoch: 0016 cost= 0.361626607
    Epoch: 0017 cost= 0.358361928
    Epoch: 0018 cost= 0.354674878
    Epoch: 0019 cost= 0.351685582
    Epoch: 0020 cost= 0.349124772
    Epoch: 0021 cost= 0.346287186
    Epoch: 0022 cost= 0.344134942
    Epoch: 0023 cost= 0.341778976
    Epoch: 0024 cost= 0.340130984
    Epoch: 0025 cost= 0.337454195
    Optimization Finished!
    Accuracy: 0.9122

