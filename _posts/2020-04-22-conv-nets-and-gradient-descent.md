---
layout: post
published: true
---

# Gradient Descent

They key idea behind neural networks (and what people mean when they say NNs "learn") is gradient
descent. This is an idea from calculus that's been around since the 1600s, and is pretty intuitive.

Say you're training for a running race and you want to see what your average pace is. You collect a
bunch of measurements, and plot them on the following graph:
![](/assets/img/basic-nn/fake-data.png)
The x-axis is time, and the y-axis is distance (in bizarre units, but you get the idea). There's
clearly a relationship between the two variables - the longer you run, the further you go. What's
more, the relationship seems to be really linear! This bodes well if you want to run even longer
distances, as you can assume your pace will stay the same over time. By just looking at this graph,
you can get a general idea of how far you run per unit time (~0.2 units distance every 10 units
time?), but the best way to figure out your pace would be to fit a line to the data and look at the
slope. Fitting a line to the data is where gradient descent comes in, which I'll talk about in a
second.

To fit a line, we need to describe it mathematically. The function that describes a line is
$f(x) = w_0 * x + w_1$, where $w_0, w_1$ are the slope and intercept (called "weights" in
machine learning). To fit a line to the data, we could guess at a bunch of $w_0, w_1$, look at
the resulting line, and make a judgment call on whether or not that line fits well. That process
would look something like the below figure.
![](/assets/img/basic-nn/guessing.gif)

These guesses are all pretty bad - maybe the second frame of the gif does the best? To actually
formalize the notion of "good" or "bad" fits, we need what's called a loss function. Loss functions
are equations that take the output of your model (in our case, the predictions from $f(x) = w_0 * x + w_1$), and compares it to the actual ground truth data (in this example, the distance we ran).
A handy way to do this for linear regression is to evaluate your function at a measured x-point, get
the value of f(x) that results, and compare the value of f(x) to the actual measured value, y.

Let's grab the best parameters that resulted from our random guesses above and see what this looks
like for a real data point.

![](/assets/img/basic-nn/misfit.png)

We evaluate our guess function $f(x) = 0.838x + 0.065$ at x=10 and get a result of 0.236. The real
value at x = 10 (how far we ran after 10 time units) is 0.303. To quantify the difference between
our predictions and the real data, typically what we do is take what's called the $L_2$ norm.
"Taking the $L_2$ norm" means computing the squared difference between the predictions and the real
data. For the guess in the above picture, that looks like this:

$$ L_2 \text{norm} = (y_{predicted} - y_{true})^2 = (0.236 - 0.303)^2 = 0.005 $$. 

The error in the prediction for this data point is 0.005. Big error values mean our guess was really
bad, and small values mean that the guess was pretty good. To incorporate all of the data into our
loss calculation, we repeat this process for every point in the dataset and take the average, like
so:

$$L_2 = \frac{1}{n} \sum_{i=1} ^{n} (y_{predicted} - y_{true} )^2 $$. 

This is also called mean-squared-error (MSE) loss. By applying this equation to the dataset above,
we can get the average misfit of our guess function compared to the true data. Remembering that
$y_{predicted} = f(x) = w_0x + w_1$, the equation for MSE loss can be rewritten like this:

$$L_2 = \frac{1}{n} \sum_{i=1} ^{n} ( w_0x + w_1 - y_{true} )^2 $$. 

This makes it explicit: We get the misfit of our function f(x) by passing its results into another
function, $L_2$. The $L_2$ loss is then a function of $w_0$ and $w_1$, and by tuning the two
parameters we can minimize the value of the $L_2$ loss. It's handy to think of $w_0$ and
$w_1$ as the x and y-axes on a 3-d graph, and the value of $L_2$ as the function value at a given
point.
 ![Loss surface.](/assets/img/basic-nn/loss-surface.png)
 ![Loss surface, in 3d.](/assets/img/basic-nn/loss-surface-3d.png)

*The loss surface for our problem. The axes correspond to guesses of parameter values, and the color
of the image indicates how good our guess was, when using $L_2$ loss.*

If we have a really small value of the $L_2$ loss, it means that the guess for our parameters is
really good. So we want to minimize the value of the loss, given that the things we can tune are
$w_0$ and $w_1$. "Tuning" $w_0$ and $w_1$ means sliding the red dot in the image around until we get
to the minimum value of the surface. 

Notice that the minumum values of the loss in the 3-d surface above also correspond to very flat
areas in the loss surface. "Very flat" means that the slope of the loss surface is close to 0. This
is a general principle that applies to any optimization problem like this: The area where a loss
function is minimized has a slope of 0. In machine learning lingo, "slope" is called
gradient. If we're far away from a minumum (like in the yellow areas in the surface above), the
gradient will be large. What we want to do is find the location in the loss surface where the
gradient is 0, as this corresponds to a minima in the loss function. Every point on the loss surface
has an associated gradient, and the nice thing about gradients is that they always point in the
direction of greatest slope. So to get to a gradient of 0 (the point that corresponds to a minimum
in our loss function), we just step in the direction of the gradient at a given point on the loss
surface. This is all pretty abstract (and hard to explain without visuals!) so I'll motivate it with
a few animations.

We can think of the loss surface as a mountain that we're on that we want to get to the bottom of.
However, the only information we have is the direction of greatest slope in our immediate vicinity -
we're blindfolded and can only tell which direction is the direction of greatest change. To get to
the bottom of the mountain, we want to take small steps in the direction of greatest change until
the slope is near 0. [This link](https://ml-cheatsheet.readthedocs.io/en/latest/gradient_descent.html) has a good explanation if you're still confused.

The gif below shows the general idea: start at a area of really high gradient and high loss, and
iteratively step towards a minumum by using the local information. You can see in the beginning that
the little red dot takes large steps towards the minimum, but as the loss surface becomes flatter,
it takes smaller steps, basically not moving toward the end.
![](/assets/img/basic-nn/grad-descent.gif)

When the red dot hits the minimum, the parameters correspond to the line of best fit for the data,
shown in the figure below.
![](/assets/img/basic-nn/lobf.png)
*The line of best fit!*

Pretty cool! 

Neural networks generalize this idea by adding more parameters. In the example above, our
loss function had only two independent parameters: $w_0$ and $w_1$. By tuning these parameters
through gradient descent, we arrived at the line of best fit to our problem, corresponding to a
minumum of our loss function. Neural networks have millions of tunable parameters, and by using
gradient descent to tune these parameters we can minimize any loss function. 

# Convolutional Neural Networks

Convolutional neural networks (conv nets) are a class of functions that operate mostly on images and
are optimized by gradient descent. For the purposes of this blog post, a conv net is a function
that takes an image as input and produces an image as output. This image that is produced is then
compared to a desired output image and a loss value is computed. The tunable parameters in the
network are then changed to minimize the value of the loss. The process is exactly the same as in
the example above, but instead of having only one input dimension (x, or time), there can be
hundreds or even millions. An image is technically a single data point with millions of dimensions!

An example of what these networks are used for is semantic segmentation: Take an image as input, and
produce an image as output whose colors correspond to the label of each pixel in the input image.

To make this concrete, here's an example. Say we took a bunch of pictures of bees that were
attracted to a scented container, like the picture below.
![](/assets/img/basic-nn/Day 1 Blank VS Scented006.jpg)
If we wanted to label all the bees in the image, we could sit in front of a computer and label each
pixel that was part of a bee by hand, or we could use a neural network to label each pixel. If we
had some labels like this 
![](/assets/img/basic-nn/Day 1 Blank VS Scented006.png)
where each white pixel corresponded to a bee pixel, we could train a neural network to label bees in
images. This task of labelling each pixel as a bee or not bee is called semantic segmentation. Of
course, if you had the right labels, you could teach the network to label anything.

Here's a gif of the convolutional neural network when it's trying to see where the bees are in an
image for the image/label pair above:

The process of refining the predictions that the neural network makes is called training.

Hopefully this post made neural networks a little more intuitive and clearly explained semantic
segmentation. Next post, I'll talk about how we apply semantic segmentation to satellite images to
recover maps of irrigation.

