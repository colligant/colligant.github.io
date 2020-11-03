---
layout: post
published: false
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
# EarthEngine Arrays.sample() method.
This is a method that samples random points within bounds from an array. The array can be composed
of columns of pixels or 2-d arrays of pixels. Points that are masked in the array are not sampled
(this makes sense, right?). The point where this gets frustrating is when you don't want to sample
randomly from the interior of a polygon.  There's no functionality in EE to sample from an arbitrary
grid of points over an array, with easily interpretable spacing (there is sampleRegions, but I
haven't really pursued using this because you have to specify the point spacing by a "scale"
parameter, which is sensitive to projections. I think explicitly specifying a projection in EE is
frowned upon). This means that sampling at points requires doing some geospatial analysis to
generate a grid of points over the ROI, and then sampling at those points. However, if the 
data has masked pixels at any of those points, those samples will be thrown out (this is intended
functionality, and makes sense, except for my use case). 

# Training with AI platform: Code and example commands

AI platform is Google's service for training machine learning models. It's hosted in the cloud and
has customizable machines that you can run your models on. AI platform uses Google Cloud Storage
(GCS) to access your training/evaluation data. This is great for my use case, as EarthEngine can
export labeled data tiles directly to GCS. 
Submitting a training job to AIP is also pretty easy: you just wrap all of your code into a python
module and off you go. The gcloud command is used to submit jobs to AIP, and you can also test all
of your code before submitting it with a few flags. To test your code locally, run this command: 
```shell
gcloud ai-platform local train \
--package-path ai-platform-module \
--module-name ai-platform-module.train_model \
--job-dir local-train-output
```
All of the arguments after the -- flags are the names that the user provides. For example, I
wrapped all of my training code in a directory named ai-platform-module (imaginative, I know), and
within that the model training happens within train_model.py (--module-name
ai-platform-module.train_model). The interesting thing about this command (and useful!) is that if
you have all of your data stored in GCS, you can still test your code on your local machine. When
the gcloud service is started, it interprets paths prefixed with "gs://" as GCS buckets, and
actually downloads and locally caches the required data. This was useful for me as I had an
incorrect feature spec for deserializing TFRecord files, and I was able to fix it before submitting
the job to the cloud.
