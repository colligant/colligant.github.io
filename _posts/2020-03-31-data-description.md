---
layout: post
published: false
updated: Wed April 8, 2020
img: /assets/post-images/leaves.jpg
---
# Tue Mar 31 13:16:06 MDT 2020

Currently I'm using LANDSAT 8 surface reflectance data, stacked along the channel axis.
Since I only have training data from 2013, I only am training/testing on LANDSAT data from the same
year. However, LANDSAT 8 started taking images over Montana in March/April in 2013, so the year of
2013 is defined as ~March-December for my purposes.

The revisit frequency of LANDSAT 8 is ~16 days, so best case scenario I have around 17 images to
work with. However, some LANDSAT surface reflectance scenes aren't available, so some path/rows only
have a few scenes available. I set the arbitrary threshold of scenes to be 13. This corresponds to a
time period of a few months. I'll try to describe the data setup graphically below.

---
## All surface reflectance images from the year 2013 over MT

![](/assets/img/data-comparison/all_sampling_dates.png)
The x-axis is the LANDSAT path/row over which the images were taken (sparsely labeled). The black
dots on the blue line represent the date at which a LANDSAT image was taken. The blue line only
serves as a visual guide; it's hard to get meaning out of just the black dots. 

It's evident from the above figure that 

- Most path/rows have a different number of images taken of them in 2013.
- Some are sporadically sampled, like the one left of 34_25.
- Some path/rows don't have many images available.
- Ingesting images into the model requires some decision about what time span to focus on.

Since the channel axis of a 2-d convolutional network has to be fixed during training and inference,
I had to make a decision about what time range of images to use. I chose two arbitrary ranges: from
the first sample date (the lowest black point in the above image), and images from mid April to mid
October.

These are shown graphcally in the next two figures.


![](/assets/img/data-comparison/from_beginning_13_images.png)
![](/assets/img/data-comparison/april_to_october.png)

The red line in the plots above indicate the images that I ingest into the model. For the full-year
time range, I chose to use the first 13 images. If a given path/row didn't have 13 images for the
year, I excluded it from the analysis. The exclusions are shown as blue lines w/o a red line
overlaid.  The same method was applied to the images from mid April to mid October, except I chose
the first 9 images. The two numbers (9 and 13) were chosen because most of the path rows had at
least that many images. One thing I could do to increase the amount of data used to train the
network is to randomly sample the start date if it's within the date range (date range can be the
full year or from April to October). I'm going to experiment with doing this.

For reference, the "names" of the two sampling methods are just full-year and partial-year in
another [post]({% post_url 2020-03-31-model-comparison-table %}). They're used to
describe the data in the model comparison table.

# Using all bands
I decided to use all the surface reflectance bands available to me in order to better constrain the
problem. Using RGB images achieved a f1-score of around 80 and 85 for a non-recurrent and recurrent
model, respectively. However, without bands like near infrared, the neural networks don't have
access to things like NDVI and other vegetation indices that are important for determining whether
or not a field is irrigated. The plot that shows the path/rows and associated sampling dates is
below.
![](/assets/img/data-comparison/sampling_dates_all_bands.png)

There are two path/rows included in the RGB data set that are not in the 7-band dataset:
34/29 and 39/29. I need to download the images (or find out where they are) for those path/rows.
Hopefully this dataset will increase the ability of the models to correctly segment irrigated
land.