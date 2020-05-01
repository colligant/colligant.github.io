---
layout: post
published: true
updated: Wed April 22
---

Since I presented at AGU, I've changed the data that the model ingests.
It used to ingest 3 LANDSAT 8 TOA scenes (11 bands, corresponding to the 3 landsat scenes over a
path/row that had the least cloud cover), DEM, and climate data from GridMet. The training data
also didn't include any clouds: I masked the clouds out before extracting training data.
Now, I am used LSAT 8 surface reflectance data (7 bands per image) for all possible dates during
the year. This corresponds to ~14 images. However, the path/rows for each data set (3 scene LSAT TOA
and n-scene LSAT surface reflectance) aren't the exact same. I couldn't download some surface
reflectance path rows (namely p/r 39 29) that I could for the TOA data.

However, the two test sets don't differ appreciably in the amount of pixels for each class.
Below are the statistics for the models that performed the best (so far) on the two datasets.
It's worth noting that exactly the same labeled polygons make up the test sets - I haven't changed
that since the beginning. The training sets aren't the same, though. For the surface reflectance
scenes I extract data with a raster scan and I perform off-line oversampling by extracting data
tiles over the centroids of each labeled polygon. For the TOA data, I just extracted data by a
raster scan. The labels extracted by a raster scan for each method are the exact same.


### TOA data:

```python
# TOA data confusion matrix:
# class 0: irrigated
# class 1: unirrigated (includes wetlands)
# class 2: uncultivated
# class 3: fallow

# The model that produced this confusion matrix
# was trained with focal loss ($\gamma$ = 0.5).

cmat = np.array([[ 104992,	5944,	 1855, 	  788],
                  [5366,	8613056, 189310,  457],
                  [3596,	97431,	 5243977, 257],
                  [2375,	9165,	 2689,	  3048]])

# And corresponding pixels per class, plus percentage that are given class 
# This is sum over columns
pixels_per_class =  array([ 113579, 8808189, 5345261, 17277])

# sum (pixels_per_class)
14284306


# And percentages:
array([0.00795131, 0.61663402, 0.37420516, 0.00120951])
```

### Surface reflectance:
```python
# Surface reflectance:

#class 0: irrigated
#class 1: unirrigated (wetlands, fallow included in this class)
#class 2: uncultivated (forest, etc)

cmat = [[    95217,     7006,     1289],
	 [    9364, 10038087,    73292],
	 [    1196,  290288,   5061238]]

# And corresponding pixels per class, plus percentage that are given class
# This is sum over columns
pixels_per_class =  array([  103512, 10120743,  5352722])

# sum (pixels_per_class)
15576977

# And percentages:
array([0.00664519, 0.64972446, 0.34363035])

```

Two things to notice:

The percentage of pixels in each class are roughly the same, despite the fact that there 
are ~1.3 million pixels more in the surface reflectance dataset.

There are ~10k more irrigated pixels in the original test set than the surface reflectance test set
(due to the exclusion of path/row 39/29). 


### Evaluating on the year 2015.
I downloaded surface reflectance images for the year 2015 in areas where we have labeled irrigated
data. Since the model reached ~91 f1 on the 2013 data, I figured it would be a good idea to evaluate
the performance of the 2013 model on 2015 data. So I extracted data for 2015. The subletly here with
evalutation / validation lies in choosing the start date of the image stack to ingest into the
model. For 2015, the whole years' worth of images is available (from Jan 1 to Dec 31), and for 2013
only images from March through Dec are available. I thought that starting the validation for 2015
around March or April would produce good results, but recall was ~0.01. This means that the model is
only noticing 1% of the pixels that are irrigated. So right now I'm experimenting with different
start dates. I'm starting at the first image we have for 2015 (January), and stepping through one
image at a time. So far (with start dates in the first 5 or so images of 2015), the model is failing
miserably, reporting really bad f1 scores. This is frustrating, but before I nail down the
following I won't report results:
- I'm extracting 2015 data on a remote machine (where I have a branch of the project that
  isn't always up-to-date with master b/c of path differences and use differences). This makes it
  impossible to tell if the extraction is working correctly. I'm going to copy some data over to
  this machine and make sure it's correct.
- The model overfit on the training/test set for 2013. The accuracy of the model (even though I
  trained it for 4 days) never started decreasing. This indicates that the train/test datasets
  either 
  - Are too correlated, and it's impossible to overfit
  - The training set is too large for the model to fit entirely (I mean, it's precisely 555,414,828
  pixels and the network has only ~5m params. The pixel count of 555m definitely has repeats). I
  also choose a random start date for the image stack that is fed into the model at train time. That
  means the dataset to fit is around a factor of 5 larger than the number of labeled tiles (50k).

I don't know how to test either of these hypotheses. 
To actually investigate whether or not the images from 2013 and 2015 had similar spacing in
time/absolute values of dates during the year at which they were taken, I produced the following
figure:
![](/assets/img/2013vs2015.png)

The black dots indicate sampling dates for 2015 images, and the cyan dots indicate the same for
2013.
The x-axis is the path/row over which the stream of images was taken. Two things to notice:
 - The images from 2013 and 2015 are offset by a few days (around 5 or 6 ) when there are
   images. This is to be expected, and sampling dates from the 2013 training dataset are all over
   the map as well.
 - There are gaps in the data, especially for 2013. The irregular sampling dates for the two years
   may be troublesome for the model.

I hope that the method works for out-of-time domain data. If it didn't, it wouldn't be worth
much. I'm going to manually investigate the data, and hope that there's something wrong with 
the data extraction or the start date for evaluation. So far, with start indices from 0-7, the model
fails miserably. The precision and recall for all of the classes (uncultivated, irrigated,
unirrigated) hover around the same values:

```python
# p: precision, r:recall
# 0: irrigated, 1: uncultivated, 2: unirrigated
start idx 5
p:{0: 0.9613971388584199, 1: 0.2637492017861905, 2: 0.15763485105628156}
r:{0: 0.019837333995067673, 1: 0.9365013412690851, 2: 0.7966828662035332}
---------------
start idx 6
 p:{0: 0.9612048179842079, 1: 0.2821509774239669, 2: 0.1553397497541973}
 r:{0: 0.01775879267815372, 1: 0.9431848352355213, 2: 0.8397357248654894}
---------------
start idx 7
 p:{0: 0.9635220145581115, 1: 0.27067814296413256, 2: 0.15140776861381938}
 r:{0: 0.01707038479516491, 1: 0.8873007289751927, 2: 0.8351860293064247}
 ...
 and so on for start idx 8, 9 (and 0, 1, 2, 3, 4).
```

This is really frustrating. I've spent so much time on this project (not doing anything with the ML
algorithm, but mostly messing around with feature preprocessing) with no results.
I'm going to also evaluate images with the 2015 data and see what happens.

If out-of-time-domain prediction is still this terrible, I have to change something significant
about the model (OR THE DATA). One thing I could do would be to add more data - extract data for
unirrigated/uncultivated for years other than 2013. Another thing would be to train a recurrent
model or something like that. Or just accept the fact that prediction for different years is not
feasible.

Honestly, I don't know what else to do. I might just evaluate the model on certain path/rows which
have similar sampling dates and call it. I could preprocess the data so that the sampling dates of
the 2015 data are similar to the 2013 data. This might result in better accuracy.
## UPDATE! 
The extraction of training data was incorrect! Let's see if re-extracting and retesting
results in something better...
[see here for a description of what's going on]({% post_url 2020-05-01-2020-05-01-out-of-domain-prediction %}).

