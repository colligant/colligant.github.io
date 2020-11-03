---
layout: post
published: false
img: /assets/post-images/mountains.jpg
---
### Update:
All of the problems described below could most likely be solved by a network that
actually considers time. The U-Net w/o explicit temporal dependence was chosen
b/c it's good for semantic segmentation. I didn't pivot NN architectures because 
using a convolutional recurrent neural network took way too much time and memory to train
and evaluate. I needed a NN that could evaluate over a large spatial region quickly, and
the LSTM-CNN that I tried was way too slow. This was before I realized that incorporating
an attention mechanism would be probably the best way forward. That's for another project/paper.

Oh yeah, the problems described below were solved by incorporating much more data, downloaded
with the help of Google Earth Engine. I don't know why I didn't investigate GEE as an option
earlier. For any remote sensing application, you should probably use GEE.

# Out-of-time domain prediction

At the end of [this post]({% post_url 2020-04-19-training-data-differences %}) I
mentioned that the extraction of the training data for 2015 had some bugs. I fixed those bugs and
re-evaluated the model. The original f1 score of 0.02 jumped to 0.5 overall. The f1 score reported
is the aggregation of all of the predictions over the test data, which occurs over 19 LSAT
path/rows. Investigating the behavoir of the model over the different path/rows will give some
insight into where the model is failing and why.

Recall this figure that outlines the different sampling dates for the different years in which we
have data:

![](/assets/img/2013vs2015.png)

Black represents sampling dates for 2013 and cyan sampling dates for 2015 (2013 is shifted by two
years so the two time series are overlaid).

The code block below will show the best precision/recall dicts for each path rows. By comparing
these with the plot above, we can get a grasp on how sampling dates change model performance.
```
# 34/27
p = {0: 0.3925269645608629, 1: 0.9906956126976513, 2: 0.002487157434741173}
r = {0: 0.27047113470471135, 1: 0.9121665184636042, 2: 0.22526315789473683}

# 39/26
No irrigated pixels.

# 35/27
p = {0: 0.3236202238517947, 1: 0.8748457110368135, 2: 0.06506364922206506}
r = {0: 0.4930902675683623, 1: 0.9850239162753579, 2: 0.006124840221559438}

# 39/27
p = {0: 0.6134531342088583, 1: 0.9820809914831141, 2: 0.5296232089413723}
r = {0: 0.8080089052933767, 1: 0.9162726426505028, 2: 0.8479433629693653}

# 36/26
p = {0: 0.7469135802469136, 1: 0.8770997643389391, 2: 0.8804796228296841}
r = {0: 0.676450034940601, 1: 0.9984108359352775, 2: 0.0727234263227164}

# 39/28
p = {0: 0.7766771184917417, 1: 0.6631823522191242, 2: 0.9855370176656513}
r = {0: 0.9607678434666601, 1: 0.9473155556000862, 2: 0.8506005061934927}

#36/27
p = {0: 0.9616480162767039, 1: 0.6820634936901745, 2: 0.9200302362469784}
r = {0: 0.5037033089998402, 1: 0.9735215647980462, 2: 0.4059343310856665}

# 40/27
p = {0: 0.7384279475982533, 1: 0.7885054442105924, 2: 0.9525328369769717}
r = {0: 0.41582559979472267, 1: 0.8972833830999626, 2: 0.8992791729790622}

# 36/28
p = {0: 0.053937229844014285, 1: 0.6960198532280917, 2: 0.7253728374058475}
p = {0: 0.09111111111111111, 1: 0.8263348583857902, 2: 0.5551177795393815}

# 40/28
p = {0: 0.8201498751040799, 1: 0.030939102828207134, 2: 0.9989633236896757}
r = {0: 0.9015193117334798, 1: 0.7908751291630236, 2: 0.8767873009546112}

# 37/26
p = {0: 0.3860392967942089, 1: 0.6630553208017307, 2: 0.8704578127547316}
r = {0: 0.25056213712789877, 1: 0.9457020903515667, 2: 0.420749337345082}

# 41/27

p = {0: 0.885130231432949, 1: 0.20578511201423139, 2: 0.9950364384563047}
r = {0: 0.8930518265397446, 1: 0.7663876590289672, 2: 0.9441502913044707}

# 37/28
p = {0: 0.7136681500317864, 1: 0.9531156265545754, 2: 0.9407785320875429}
r = {0: 0.8150137941048352, 1: 0.9756467444624163, 2: 0.8882304669123618}

# 41/28
No irrigated pixels.

# 38/27
p = {0: 0.6215097144070496, 1: 0.8612286286196551, 2: 0.23150914015305288}
r = {0: 0.38304833362414936, 1: 0.9065063493167873, 2: 0.16452250108993438}

# 42/27 	  
No irrigated pixels.

# 38/27
p = {0: 0.19284991409541294, 1: 0.9532582146382159, 2: 0.9175719154345171}
r = {0: 0.7746265834751371, 1: 0.9570711813861941, 2: 0.8958911202848496}

# 38/28
p = {0: 0.2857907412362858, 1: 0.9615231460462531, 2: 0.9149192715464026}
r = {0: 0.33034333436436747, 1: 0.9199828911793351, 2: 0.9593757831360198}
```

The precision/recall dictionaries above (unformatted, I know) represent the highest values over that
LANDSAT path row. There are different values of precision/recall because the chosen start date can
vary.  Examine path/row 37/28. The model did the best across all classes, and the sampling dates between
the two years are pretty regular. In contrast, the model did poorly on path/row 36/28, which has
pretty regular sampling dates after the second image was taken. However, there are no regular images
between April/June! Basically, this is out-of-domain prediction. 

Even though the model does well when there are regular sampling dates, we can't always be assured
that that data will be available (well, we actually might be able to be assured. I might just not be
able to download it!). 

## Reworking assumptions (and input data!)

The working assumption for this project is that a neural network is a complicated enough function to
take a stack of images (implicitly organized by date captured), and learn a representation of
irrigation abstract enough to correctly identify irrigated pixels. This assumption is definitely
false, as the networks readily reach high accuracy on irrigated test sets. However, neural networks
are good at learning distributions of data and generalizing within that distribution, but they have
almost no generalization power *outside* of that distribution. 

With out-of-time-domain prediction we assume that changing the year where
we want to have irrigated predictions won't be out-of-distribution. 
There are a couple of reasons why this is reasonable:
- The sensors on the satellites don't change from year to year, meaning the same EM wave powers are
  recorded year to year
- Irrigated land doesn't change in phenology or shape from year to year (center pivots, flood
  irrigation are here to stay)

However, the factor I didn't consider is the difference in available sampling dates from year to
year. Changing these significantly makes the problem suddenly out-of-distribution, and the neural
networks do poorly. This is the problem that I've been describing and battling with for a few
months. The solution is to relax the assumptions that are baked into the NN. The assumption that it
learns is that it will recieve a stack of images organized in a somewhat meaningful manner. Since
the stack of images can't always be organized in a meaningful way, I'm going to throw this
assumption out of the window and add a little more information to the model.

The thing I'm going to try is adding a date raster on to the feature stack, and randomly shuffling
the input rasters. In this way, it should learn to combine features based on their corresponding
date and hopefully rely less on a static set of input dates. 

There are two options (and I'm not convinced that they're actually different)
- Encode date as days since January, or something like that
- Encode date as a categorical feature

I've written code to encode date as a "days since January" raster and we'll see how that works out.
So far, the training statistics indicate the model is training a lot slower with random input
dates and maybe has already converged around 85% train f1 and 78% train accuracy... (compared to
like 97, 98 in both of those categories for the other input data). I'll update this after a few
days.
It's kind of hard to verify results visually, so I'll post the code that I'm using to split the
raster stack and shufflei it. 
```python
# image_stack.shape (112, 7760, 7760) 
# I add the date rasters onto the end of the image stack, so a image stack
# of 14 7-band images becomes 14*(7+1) = 112 bands.
n_images = image_stack.shape[0] // 8
n_bands = 7

# Make multidimensional array of shape (n_images, n_bands).
# Each row contains the indices of the image at that row index
# Alternatively, each row is a list of numbers that corresponds to where
# an image is in the original image stack, where an image is 7 contiguous bands
# taken at the same date
indices = np.asarray([np.arange(i, i+n_bands) for i in range(0, n_images*n_bands, n_bands)])
# min_images is a hyperparameter that chooses the number of images fed into the model
# choose dates randomly, no replacement, randomly ordered through time
image_index = np.random.choice(indices.shape[0], size=min_images, 
	replace=False)
# now add on the date raster on the end - the date raster is appended to the 
# end of the original image.
indices = indices[image_index, :].ravel()
# n_images*n_bands + image_index says grab the bands starting
# from n_images*n_bands that are in image_index
image_indices = np.hstack((indices, n_images*n_bands + image_index))
# np hstack stacks them horizontally, basically concatenation in this case.
return image_stack[image_indices]
```


One thing I'd also like to include is a simple timeline of work on this project, which is below.

## Timeline, progress, setbacks...

This project would also have moved forward a lot faster if I had investigated out-of-domain
accuracy sooner. This is basically the timeline of the project and the various steps I took to get
to where I am now:

- Began working in earnest on the project in December of 2018. The input data here was the three
  images taken between May and November that had the least cloud cover, as well as ET, slope,
  aspect, and elevation.
- Got David's codebase off the ground and running on path/row 39/27 (resulting in predictions given
  during a lab meeting on Dec 4, 2018). David's project used 1-d features (single pixel stack) and
  ingested those into a two-layer MLP. Pretty simple, and it took ~5 hours to get predictions for a
  single image. Test statistics (precision, recall) weren't reported.
- Feb 2 2019: I added on the capability to extract tiles onto David's project, and added a simple
  conv-net architecture. This architecture consisted of a few conv. layers and a final linear layer
  to do the predictions. As such, it again took ~5 hrs to evaluate a LANDSAT tile.
- Feb 19, 2019: Changed the model to a FCNN (can't remember the exact architecture), so that
  evaluation of images took minutes instead of hours. I also added some climate features into the
  data that the model ingested (precip, et).
- It's  worth noting that in all of the bullet points above I was masking out cloud-covered data
  from the training set, so the model couldn't handle clouds.
- I worked on this project for a while after February, trying to deal with imbalanced data in the
  training set. I had noticed that the number of pixels that we had for each class were imbalanced,
  sometimes by a factor of 100 to 1. Some things I did to remedy this:
  - Tried offline hard negative/positive mining.
  - Implemented binary and multiclass focal loss.
  - Implemented dice loss for the binary case.
  - Experimented with different sampling techniques.  This problem was resolved by random majority
    undersampling.
- Work on this problem continued until the end of school, at which point I worked on eclipse stuff
  for the whole summer (May through August). This was pretty bad for research productivity (as in I
  didn't work on irrigation stuff at all).
- Around October of 2019, I started evaluating models that I had trained with random majority
  undersampling and focal loss ($\gamma = 0.5$). On Halloween, I presented a model that had reached
  71% precision and 90% recall on the irrigated class.
- Probably a few weeks later I reached 90/92 percent precision and recall on the irrigated class. I
  considered this good enough and evaluated images over Montana from 2013-2018.
- Then I participated in the NASA EPSCOR technical review for Marco's project - I presented the
  model and the results. During this talk, Zach Lauffenburger gave a presentation that used my
  products to look at irrigation in Ravalli county. The predictions from years other than 2013
  looked bizarre and the irrigated acreage predicted by my model varied wildly. This is when I first
  realized that there was a problem with the data ingested. Remember that I used the three least
  cloudy images from a growing season? Well, these images could really be taken any time between May
  and October! The problem that I was describing above with the different sampling dates was
  exacerbated. However, I didn't do any formal evaluation of how the model was doing because there
  wasn't ground truth data available to me at the time. This is the figure that piqued my interest:
  ![](/assets/img/zach_presentation-1.png) The image on the bottom right really didn't make sense to
  me - the irrigated diversions probably didn't change by 3x between years. The large white spots on
  the images are where I masked out clouds.
- I then presented the results of this model at AGU - like Dec 9, 2019 or something.
- Over the break, I worked on the fish-net problem for MPG ranch, so I wasn't able to do much on the
  irrigation project. 
- January 2020: Started downloading all surface reflectance data available (like 7.3 Tb!) in order
  to solve the sampling date issue.
- Feb 2020: Worked on making new models perform well.
- Today: Read the last few blog posts to see where I'm at.
