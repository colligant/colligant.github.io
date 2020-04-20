---
layout: post
published: true
updated: Mon April 20
---
Sun Apr 19 10:21:20 MDT 2020

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


