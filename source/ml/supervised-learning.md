# 监督学习

![](/images/14799100305456.jpg)

## tensorflow框架

```python
import tensorflow as tf

# initialize variables/model parameters

# define the training loop operations

def inference(X):
    # compute inference model over data X and return the result

def loss(X, Y):
    # compute loss over training data X and expected outputs Y

def inputs():
    # read/generate input training data X and expected outputs Y

def train(total_loss):
    # train / adjust model parameters according to computed total loss

def evaluate(sess, X, Y):
    # evaluate the resulting trained model

# Create a saver.
saver = tf.train.Saver()

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
        if step % 10 == 0:
            print "loss: ", sess.run([total_loss])
        # save training checkpoints in case loosing them
        if step % 1000 == 0:
            saver.save(sess, 'my-model', global_step=step)

    evaluate(sess, X, Y)

    coord.request_stop()
    coord.join(threads)
    saver.save(sess, 'my-model', global_step=training_steps)
```

万一训练过程中断，可以通过下面的方式恢复：

```python
with tf.Session() as sess:
    # model setup....

    initial_step = 0

    # verify if we don't have a checkpoint saved already
    ckpt = tf.train.get_checkpoint_state(os.path.dirname(__file__))
    if ckpt and ckpt.model_checkpoint_path:
        # Restores from checkpoint
        saver.restore(sess, ckpt.model_checkpoint_path)
        initial_step = int(ckpt.model_checkpoint_path.rsplit('-', 1)[1])

    #actual training loop
    for step in range(initial_step, training_steps):
       # run each train step
```


