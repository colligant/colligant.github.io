---
layout: post
published: false
---

tf/keras provides a model.fit() method that takes care
of the training loop for your model. You can customize the
behavoir of the model by providing custom callbacks and metrics.
The model fit method is flexible and useful, as it hides all the guts of the training step
and allows you to keep your code clean.
There are a few different ways to feed data to your model when using
the model.fit() method: a custom python generator, a subclass 
of the keras.Sequence class, or through a tf.data.Dataset. Using
any one of these methods requires you to define the size
of your dataset. If you subclass the keras.Sequence class, this is
taken care of in a custom __len__() method, but for the other two
methods (custom generator or tf.data.Dataset), you have to pass
in the number of steps per epoch to the model.fit() method.

The satellite machine learning problem I work on uses Google Earth
Engine to download all of the training data. Handily, GEE exports 
satellite data and associated rasterized labels as TFRecords,
meaning using a tf.data.Dataset is the most reasonable choice
for feeding data into my models. My problem is extremely imbalanced,
meaning that there are thousands of times more training examples from
the majority classes than from the minority (target) class. To overcome
the imbalance in the dataset, I've found that simple random majority
undersampling works best. This is oversampling the minority class
until the number of training examples from each class per mini-batch is the same.
However, this means the definition of an *epoch* becomes a little hazier.

Usually, an epoch is defined as when the model has seen each example in
the training set exactly once. When classes are imbalanced (and you want
to implement random majority undersampling in each mini-batch), it's not
possible to see every example from each class exactly once - there has
to be some repeats.


![](/assets/img/imbalanced_data.png)


You can either define the epoch to be where the red block ends,
(this would mean repeating each example in the minority class 5 times),
or where one of the green blocks end (meaning only 1/5 of the majority class
would be seen). I usually use the latter definition, and define the
steps per epoch as the number of training examples in the minority class.
I still want to see every example in the majority class, but just not all
in one epoch. When the number of examples in the majority class is extreme (think
tens or hundreds of thousands), and the number of examples in the minority class
is small (think hundreds to thousands), iterating over the entire dataset takes
a long time and makes it difficult to keep an eye on the "pulse" of the model - how
well it's doing after a few hundred steps of gradient descent. It also makes
scheduling a learning rate decay a little more difficult. As I'm writing this,
it seems to me like I could probably fix the problem I'm about to
describe by using the former definition of an epoch.

When using the second definition of an epoch (hereafter called "minority epoch"),
training is cut off before the tf.data.Dataset has fully exhausted all of the
examples in its queue. I'm not convinced that it begins where it left of
at the beginning of the next epoch. This means that only a subset of the majority
class is ever presented to the model.

## Jupyter notebook showing the behavoir of a tf.data.Dataset over epoch



```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1' # make GPU invisible.
import tensorflow as tf
import tensorflow_datasets as tfds
```


```python
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data(path='mnist.npz')
```

Now we'll use the mnist dataset to investigate model.fit(), and
make sure that training resumes where it left off. First, we'll make
a dummy model.


```python
def model_fn():
    
    inp = tf.keras.layers.Input(shape=(28,28,1))
    x = tf.keras.layers.Conv2D(10, kernel_size=3, activation='relu')(inp)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Conv2D(10, kernel_size=3, activation='relu')(x)
    x = tf.keras.layers.MaxPooling2D()(x)
    x = tf.keras.layers.Conv2D(10, kernel_size=3, activation='relu')(x)
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    return tf.keras.models.Model(inputs=[inp], outputs=[x])
```


```python
model = model_fn()
model.summary()
```

    Model: "functional_1"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    input_1 (InputLayer)         [(None, 28, 28, 1)]       0         
    _________________________________________________________________
    conv2d (Conv2D)              (None, 26, 26, 10)        100       
    _________________________________________________________________
    max_pooling2d (MaxPooling2D) (None, 13, 13, 10)        0         
    _________________________________________________________________
    conv2d_1 (Conv2D)            (None, 11, 11, 10)        910       
    _________________________________________________________________
    max_pooling2d_1 (MaxPooling2 (None, 5, 5, 10)          0         
    _________________________________________________________________
    conv2d_2 (Conv2D)            (None, 3, 3, 10)          910       
    _________________________________________________________________
    flatten (Flatten)            (None, 90)                0         
    _________________________________________________________________
    dense (Dense)                (None, 1)                 91        
    =================================================================
    Total params: 2,011
    Trainable params: 2,011
    Non-trainable params: 0
    _________________________________________________________________


Ok, now we have a small model made for binary classification. Let's make an imbalanced data problem by making the NN classify 1s as class 1, and everything else as class 0.


```python
ones = x_train[y_train == 1, :]
everything_else = x_train[y_train != 1, :]
print(ones.shape, everything_else.shape)
```

    (6742, 28, 28) (53258, 28, 28)


Now we have an imbalanced dataset: ~7k records for the minority class, and 53k for the majority class. I'll make
them into tf.data.Datasets, then choose from them uniformly. Notice that I also zip a "count
dataset" into the full dataset that I'm going to feed to the model. The model.fit() method
expects some sort of generator that yields either (features, labels, sample_weights) or (features,
labels). sample_weights weight each class when the loss is calculated. Inserting a tf.range() as a
sample_weight will make our model perform poorly, but that's OK since we're just examining the
behavoir of model.fit() and tf.data.Datasets.


```python

count_dataset = tf.data.Dataset.range(ones.shape[0])
ones_ds = tf.data.Dataset.zip((tf.data.Dataset.from_tensor_slices(ones), 
                               tf.data.Dataset.from_tensor_slices(tf.ones((ones.shape[0]), dtype=tf.uint8)),
                               count_dataset))

count_dataset = tf.data.Dataset.range(everything_else.shape[0])
other_ds = tf.data.Dataset.zip((tf.data.Dataset.from_tensor_slices(everything_else), 
                                tf.data.Dataset.from_tensor_slices(tf.zeros((everything_else.shape[0]), dtype=tf.uint8)),
                                count_dataset))
```
Now we have the datasets for the digits labeled 1, and every other digit. Below we'll batch the
datasets and use tf.data.Dataset.choose_from_datasets to sample examples from each dataset in an
alternating fashion.

```python

# I'm not going to shuffle, as it's unnecessary in this problem
batch_size = 16
ones_ds = ones_ds.repeat() # make them repeat indefinitely
other_ds = other_ds.repeat()
datasets = [ones_ds, other_ds]
choice_dataset = tf.data.Dataset.range(len(datasets)).repeat()
# choose them based on the choice dataset
dataset = tf.data.experimental.choose_from_datasets(datasets,
           choice_dataset).batch(batch_size).repeat()

```

Is this working? Let's look at the labels for a sample batch
and make sure the labels are balanced.


```python
batch = dataset.take(1)
for _, labels, count in batch:
    print(labels)
    print(count)
```

    tf.Tensor([1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0], shape=(16,), dtype=uint8)
    tf.Tensor([0 0 1 1 2 2 3 3 4 4 5 5 6 6 7 7], shape=(16,), dtype=int64)


Looks pretty balanced to me. The counts look correct too. Now, we'll train a model with a custom
metric that prints the index of the batch to a file. The model will not train with the data as we've
set it up, as the sample weights are totally bizarre.


```python
class BatchCounter(tf.keras.metrics.Metric):
    
    def __init__(self, name='bc', **kwargs):
        super(BatchCounter, self).__init__(name=name, **kwargs)
        self.epoch = 0
        self.count = None
        self.count = self.add_weight(name='count', shape=(batch_size,1))
        
    def update_state(self, y_false, y_pred, sample_weight):
        self.count.assign(sample_weight)
        
    def result(self):
        if self.count is not None:
            return self.count[-1]
        return 0

    def reset_states(self):
        self.epoch += 1
        tf.print(self.epoch, output_stream="file://foo.out")
        tf.print(self.count, output_stream="file://foo.out")
        
```
All BatchCounter does is store the count (remember, it's passed in as a sample weight) at each step
and prints the count tensor to a file at the end of each epoch.

```python
bc = BatchCounter()
model.compile(tf.keras.optimizers.Adam(1e-3), loss='binary_crossentropy',
            metrics=['acc'], weighted_metrics=[bc])
```


```python
model.fit(dataset,
         steps_per_epoch=y_test.shape[0] // batch_size,
         epochs=10)
```

    Epoch 1/10
    625/625 [==============================] - 4s 7ms/step - loss: 276.4914 - acc: 0.9601 - bc: 4999.0000
    Epoch 2/10
    625/625 [==============================] - 3s 6ms/step - loss: 155.0134 - acc: 0.9857 - bc: 9999.0000
    Epoch 3/10
    625/625 [==============================] - 4s 7ms/step - loss: 204.1138 - acc: 0.9856 - bc: 14999.0000
    Epoch 4/10
    625/625 [==============================] - 4s 7ms/step - loss: 234.8912 - acc: 0.9896 - bc: 19999.0000
    Epoch 5/10
    625/625 [==============================] - 4s 6ms/step - loss: 180.8350 - acc: 0.9825 - bc: 24999.0000
    Epoch 6/10
    625/625 [==============================] - 4s 7ms/step - loss: 174.9996 - acc: 0.9857 - bc: 29999.0000
    Epoch 7/10
    625/625 [==============================] - 4s 6ms/step - loss: 193.0053 - acc: 0.9864 - bc: 34999.0000
    Epoch 8/10
    625/625 [==============================] - 4s 7ms/step - loss: 226.0220 - acc: 0.9892 - bc: 39999.0000
    Epoch 9/10
    625/625 [==============================] - 4s 6ms/step - loss: 199.9080 - acc: 0.9809 - bc: 44999.0000
    Epoch 10/10
    625/625 [==============================] - 4s 7ms/step - loss: 201.9290 - acc: 0.9807 - bc: 49999.0000

The model definitely trained, and even seems to do OK!

```python
!cat foo.out
```

    1
    [[4992]
     [4992]
     [4993]
     ...
     [4998]
     [4999]
     [4999]]
    2
    [[3250]
     [9992]
     [3251]
     ...
     [9998]
     [3257]
     [9999]]
    3
    [[1508]
     [14992]
     [1509]
     ...
     [14998]
     [1515]
     [14999]]
    4
    [[6508]
     [19992]
     [6509]
     ...
     [19998]
     [6515]
     [19999]]
    5
    [[4766]
     [24992]
     [4767]
     ...
     [24998]
     [4773]
     [24999]]
    6
    [[3024]
     [29992]
     [3025]
     ...
     [29998]
     [3031]
     [29999]]
    7
    [[1282]
     [34992]
     [1283]
     ...
     [34998]
     [1289]
     [34999]]
    8
    [[6282]
     [39992]
     [6283]
     ...
     [39998]
     [6289]
     [39999]]
    9
    [[4540]
     [44992]
     [4541]
     ...
     [44998]
     [4547]
     [44999]]

Cool! It looks like the tf.data.Dataset is resuming where it left off at the end of each epoch. The
numbers above the bracketed numbers are the epoch. The count for the minority class repeats while
the count for the majority class keeps going up! This is exactly the behavoir that is desired, and
it makes sense that the architects of keras/tensorflow constructed it this way. Less complicated
errors have definitely occurred though, so it's always a good idea to check your assumptions about
what's happening behind the scenes. I also delved deep into the source code for model.fit(), and
it says the same thing as what we saw.

As an aside, I generated the markdown for the notebooks using the following command:
```shell
jupyter nbconvert --to markdown my_notebook.ipynb
```


