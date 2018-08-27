# python mnist_NNcomponent.py mnist.yaml
import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data
from NNcomponent import NNcomponent
from config import cfg

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs})
    correct_prediction = tf.equal(tf.argmax(y_pre,1), tf.argmax(v_ys,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys})
    return result

# define placeholder for inputs to network
xs = tf.placeholder(tf.float32, [None, 784], name='xs') # 28x28
ys = tf.placeholder(tf.float32, [None, 10], name='ys')
x_image = tf.reshape(xs, [-1, 28, 28, 1], name='x_image')

# model
prediction = NNcomponent(cfg['NN'], x_image)

cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),
                                              reduction_indices=[1]))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
for i in range(5001):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys})
    if i % 50 == 0:
        print('batch: %4d, accuraty: %5.2f%%' % (i, compute_accuracy(mnist.test.images, mnist.test.labels) *100.0 )   )