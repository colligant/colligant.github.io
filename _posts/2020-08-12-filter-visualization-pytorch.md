---
layout: post
published: true
---
# Filter Visualization in Pytorch

The easiest way to see what a given convolutional filter
is looking for in a neural network is to optimize the response
of an activation produced by said filter. This requires
doing gradient descent on the input image of the network. However,
as noted in [distill.pub], doing this naively can result in 
somewhat adversarial examples, dominated by high-frequency noise.

There are a few tricks that make the generated images look better,
which I'll iteratively add to the optimization problem.

## Naive gradient descent.

