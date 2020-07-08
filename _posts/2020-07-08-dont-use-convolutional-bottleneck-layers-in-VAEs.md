---
layout: post
published: true
---

I ran into this problem when creating a VAE to recreate satellite images.
I originally wanted the VAE to work on any sized image, and proceeded to build
a FCNN-VAE. I was pretty stumped when I tried to sample from the latent space
of the model.
Code and explanantion are below. First of all, a VAE is a type of generative
model that aims to make sampling from the data distribution easy. It does this by
constraining the latent space of the model to be a unit gaussian distribution 
(an n-dimensional normal distribution with unit variance and 0 mean). To sample
from the model, all we need to do is generate a random normal vector and feed it 
into the decoding part of the model, and we'll get some pretty good looking fake
data. The fact that we can do things like this at all is pretty amazing, and VAEs 
are just one slice of the entire generative modeling spectrum.

## The problem

As stated above, I wanted to make a FCNN-VAE to work on any size image.
I created the model (code here[]), and trained it. One note about prototyping:
MNIST is your friend. The small amount of data and relatively easy problem lets
you test ideas quickly. 
When I sampled from its latent space, I was getting bizarre results. I scratched my head,
and started debugging the code. Maybe I had the reparameterization trick wrong? Maybe
the generation of random normal numbers wasn't working correctly? I validated the data on 
MNIST test data - it wasn't overfitting on the training set, so I knew I should be able to
sample from the latent space. Whatever I tried, the samples ended up looking like the image
on the right:

FCNN-VAE samples             | FC-VAE samples
:-------------------------:|:-------------------------:
![](/assets/img/fcnn_vae.png) | ![](/assets/img/fc_vae.png)

For some contrast, "real" samples from a working VAE look like the left hand image.

The first image is pretty bad for a VAE. This is more what I'd expect when sampling
from a regular autoencoder because of the poorly-behaved latent space.
I finally realized that the likely reason (and I'll investigate this more!) is the 
spatial dependence that the fully convolutional model relies on. The bottleneck layer
in a FCNN-VAE is not a vector, but a convolutional block. That means that each encoded
representation actually encodes spatial information present in the input image. I would
think that generating samples from this latent space would be really hard, as they most likely
encode some spatial features of the input image. To actually test this, I'm examining
the latent space representations of MNIST digits, and seeing if they have any spatial
patterns which correspond to the input. I'm first making the latent space only 1 channel deep.
I can't see any patterns that indicate that spatial correlation in the latent space is playing a
large role. I think this may be due to the fact that I can't really see anything in a 7x7 image.
Removing one of the downsampling (and corresponding upsampling steps) might reveal something, but
interpreting a 14x14 image is kind of hard. 

The 7x7 image             |  14x14          | 28x28
:-------------------------:|:-------------------------:|:-------------------------:
![](/assets/img/fcnn_vae_embedding2downsample.png) | ![](/assets/img/fcnn_vae_embedding_1_downsample.png) | ![](/assets/img/fcnn_vae_embedding_no_downsample.png) |

The images of the latent space embedded of different digits is shown above, along with
their respective resolutions. Maybe if I squint I can see digits in the 14x14 image,
but I'm not sure. You can definitely see digits in the 28x28 image but because
the latent space is the same dimension as the data space, I don't think this means too much.
Sampling from these models is still impossible, though. The next thing to try is to make
a FC-VAE with a latent space of size 28 by 28, and reshape those latent encodings into images,
and see if there is clear spatial patterns present in them. There probably will be.

## The... solution?

After doing those experiments, I'm not convinced that my original explanation applies. 
I thought I couldn't generate samples from a FCNN-VAE because of the spatial autocorrelation
in the latent space, but looking at the latent spaces of various digits doesn't really reveal
spatial structure, except in the case where the latent space is the same size as the input image.
Maybe I just wrote some buggy code (I don't think so, but) that was somehow fixed by the addition
of fully-connected layers. I might revisit this and see if I can come up with a more convincing 
explanation.












