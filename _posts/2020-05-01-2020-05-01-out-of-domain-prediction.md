---
layout: post
published: true
---
# Out-of-time domain prediction

At the end of [this post]({% post_url 2020-04-19-2020-04-19-training-data-differences %}) I
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

Let's zoom in on two path/rows, 38/27 and 36/27. The resulting time series looks like this:

![](/assets/img/2013vs2015two_path_rows.png)
*Github pages is terrible for hosting images (or I don't know enough about web development).
Anyways, zoom in on the image to see it better.*

Notice the differences in the sampling dates over the two path/rows? 36/27 has a large gap in
sampling dates during 2013 while 38/27 has a much smaller gap. The model was trained on the cyan
sampling dates, and is evaluated on the black dates. What I hope to see happen (by evaluating the
precision and recall of the models on the 2015 test data) is that the 38/27 has higher precision and
recall because of the more regular sampling dates.
```python
# path/row 36/37 has maximum f1 of .65 for the irrigated class:
precision = {0: 0.9616480162767039, 1: 0.6820634936901745, 2: 0.9200302362469784}
recall =    {0: 0.5037033089998402, 1: 0.9735215647980462, 2: 0.4059343310856665}
```
The values here are really all over the place and pretty unacceptable. You never want a model with
98% recall and 68% precision - this indicates way too many false positives. The converse is also
bad: a model that barely predicts anything to be irrigated but is right almost 100% of the times is
also useless.

Even though the model does well when there are regular sampling dates, we can't always be assured
that that data will be available (well, we actually might be able to be assured. I might just not be
able to download it!). An alternative solution to stacking images by date and hoping the network
implicitly learns some date dependence is to ingest a date feature into the model. That's what I'm
going to try next.

The date feature is just going to be a raster of floats that encodes the days since January 1st.
Since I'll give the model this information, hopefully it will learn to deal with irregular sampling
dates, and rely less on temporal signals. I'll also randomly shuffle the order in which images are
fed into the model, since with that date information, the model could feasibly learn to re arrange
the input rasters in a way that is helpful for making decisions. I also might feed the network less
than 14 images - maybe 8 randomly chosen from the time range? This will hopefully make it learn some
robustness to random sampling dates.

Another problem with stacking images by date is that you have to choose a start date. For 2015 (in
the first figure) what image should I first ingest into the model for optimal results? The image
from May or April? It would seem clear cut but when your training set has such variation in sampling
dates (again, the cyan dots in the figures above), what is the right thing to choose? If we force
the model to learn a relatively time-invariant representation of irrigation, this problem is no
longer.

It also important to note that if LSAT 8 wasn't launched in 2013 and only sporadically captured
images during that year that this project would most likely be done, without any consideration of
sampling dates or temporal offsets. The reason why I say this is because the model performs well on
out-of-time domain data when sampling dates are similarly spaced to the training set (I mean, duh).

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
- Feb 2 2019: I added on the capability to extract tiles onto David's project, and added a simple conv-net
  architecture. This architecture consisted of a few conv. layers and a final linear layer to do the
  predictions. As such, it again took ~5 hrs to evaluate a LANDSAT tile.
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
  - Experimented with different sampling techniques.
  This problem was resolved by random majority undersampling.
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
  ![](/assets/img/zach_presentation-1.png)
  The image on the bottom right really didn't make sense to me - the irrigated diversions probably
  didn't change by 3x between years. The large white spots on the images are where I masked out
  clouds.

- I then presented the results of this model at AGU - like Dec 9, 2019 or something.
- Over the break, I worked on the fish-net problem for MPG ranch, so I wasn't able to do much on the
  irrigation project. 
- January 2020: Started downloading all surface reflectance data available (like 7.3 Tb!) in order
  to solve the sampling date issue.
- Feb 2020: Worked on making new models perform well.
- Today: Read the last few blog posts to see where I'm at.
