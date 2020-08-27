---
layout: post
published: true
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






















