---
layout: post
published: true
---
After trying to solve the problem of model out-of-time domain prediction in a few different ways
(taking cloud-free images, taking images only in june, using all available images, randomly sampling
a subset of ordered images, random permuting a subset of images, ingesting a time feature), I
realized that the only way forward seemed to be to constrain the problem with more data. I had been
using only training data from 2013, and evaluating on data from 2015. The final iteration of the
model did alright on the 2015 test set, reaching up to 90% f1 on certain path rows, but having an
overall f1 score of 54% (4% increase after ingesting randomly sampled scenes with a time attribute).
The reason I had only been focusing on 2013/2015 is because of the amount of time and resources
required to download satellite imagery. If I wanted to go pre-2013, I'd have to download L7 data and
figure out how to process it and whatnot. The sheer amount of data required (and I didn't want to
throw any out after I'd used it, because what if I made an error and had to redownload it?) was just
too much to play around with incorporating data from a greater temporal range.

So finally I made the decision to move to Google Earth Engine, something that I had not really
pursued in the past because I thought LANDSAT images had to be downloaded in their entirety. It
turns out that GEE makes extracting tiles from data quite easy, and means that I don't have to
download terabytes of image data to expand the temporal or spatial scale of the project.

The preliminary experiment that I did was training on data from 2008-2013, and evaluating on data
from 2015. This reached an overall f1 score of 95% for the irrigated class, a huge step up from
the last method where I was only concerned with data from 2013. To incorporate both L7 and L8, I
took the mean of images captured in 32-day spans, starting from May 1st of the year.

However, the way I sampled tiles meant that there were many repeated labeled pixels. The workflow
that I followed to extract training/test data was to create an "image stack", where the bands
corresponded to LANDSAT features and raster masks of shapefiles. I then iterated over all of the
polygons in the training/test shapefiles, and extracted a tile centered at a random point within
each polygon. This means that if two polygons were within ~4000m of each other, their labels were
sampled twice. I'm afraid that this sampling bias was partly responsible for the 95% f1 score, but
we'll see what happens when I re-extract the data in a different scheme.

To do a raster scan over the data (making sure each labeled pixel is only sampled once), I generated
a grid of points over the test data (spaced according to 30m * 256), and I'm sampling a 256X256 tile from those points. 

