---
layout: post
published: true
---
# Satellite data, machine learning, and mapping irrigation

## Why map irrigation?

Worldwide, irrigation accounts for 70% of water use. In water-scarce regions like the arid Western
United States, it can account for an even larger percentage. The ability to irrigate crops has
helped spur development in many areas of the world, and crops grown on irrigated land comprise
almost 40% of global crop yield. Despite the fact that irrigation is so important for food
production, knowing exactly how much land is irrigated has historically been a difficult task.
We decided to try and map irrigation using modern machine learning techiques that have been proven
to surpass human perfomance on similar tasks. Maps of irrigation help provide upper and lower bounds
on water usage, and understanding where and when we irrigate will help inform sustainable decisions
about where to apply water in the future. Maps of irrigated extent can also be ingested into models
that predict everything from groundwater availibility to the decisions farmers will make when
planting crops. In essence, understanding more about how we produce food with irrigation will
provide much needed data to plan for the future.

![](/assets/img/irrigation.png)
*Image from Dieter, C.A., Maupin, M.A., Caldwell, R.R., Harris, M.A., Ivahnenko, T.I., Lovelace, J.K., Barber, N.L., and Linsey, K.S., 2018, Estimated use of water in the United States in 2015: U.S. Geological Survey Circular 1441, 65 p., https://doi.org/10.3133/cir1441.*

The figure above shows water withdrawals for irrigation, in millions of gallons per day. The big
thing to notice about this graphic is that the western United States relies much more heavily on
irrigation to grow crops. We're focusing only on the western US, along the same division as in the
figure above.


Central to mapping irrigation is the availibility of free satellite data. We use data collected by
NASA's LANDSAT satellites, which collect images over a given spot on the Earth every two weeks.
These images go back to the 1970s and continue until today, and will continue to be taken into the
foreseeable future. The pie-in-the-sky goal of this project is to produce a machine learning
algorithm that maps irrigation that can be used for any year available in the LANDSAT record.
We decided to use LANDSAT satellite data because it spans such a long time period. 

At its heart, the problem of mapping irrigation is the same as semantic segmentation. If you're not
familiar with semantic segmentation, it was discussed in depth in the [previous post]({% post_url 2020-04-22-conv-nets-and-gradient-descent %}).

The thing about these algorithms is that they need a lot of labeled data to make good predictions,
so labelling enough data is often a difficult task. Companies like [Google or
Microsoft](https://www.forbes.com/sites/korihale/2019/05/28/google-microsoft-banking-on-africas-ai-labeling-workforce/#42b36bd541c4)
outsource this very tedious task to workers in other countries. Thankfully we didn't have to pay for
our data as it was donated by David Ketchum, another BRIDGES trainee. 
Our irrigation semantic segmentation predictions look like this:
![](/assets/img/satellite-vs-predictions.png)

The image on the left is the raw satellite data that is ingested into the model, and the image on
the right is the predictions produced by the neural network. Red means that the neural network has
labeled the pixel in the input image as irrigated, green means pixel is labeled as unirrigated, and
blue means uncultivated land like forest, wetlands, or scrublands. The models that we have are
actually performing very well for regions where we have data - other irrigated maps don't achieve
nearly the same precision as our method. The neural network architecture (i.e. how the weights are
arranged) that we use was pretty much exactly copied from [this
paper](https://arxiv.org/pdf/1505.04597.pdf). It was published in 2015 and already has 13,000
citations! It's called a U-Net, and consists of successive downsampling steps and upsampling steps.

![](/assets/img/u-net-architecture.png)
*Image credit [Ronneberger et al].*

In the figure above, an image is ingested into the model on the left. It then passes the image
through some weight layers and then downsamples it. Downsampling is a common technique in
machine learning / computer vision, and it basically crunches an image down. By crunching the image
down, the neural network can incorporate more visual context into its decisions. The authors of the
UNet paper start with an image that's size 572x572 and end up downsampling it until it's only 32
pixels on each side! We do basically the same thing when mapping irrigation. Interestingly, the
original UNet was used to segment cells in biomedical images. It does really well at mapping
irrigation, which means that the two tasks (segmenting cells and mapping irrigation) are really
similar, at least in the high-dimensional data space in which the neural network resides.

All in all, mapping and monitoring irrigation in a way that is comprehensive, consistent, and
timely is what we aspire to do. This will help create actionable information to help inform
decisions at the FEW nexus. Our group tries to do this by using modern machine learning (UNet) and
satellite data to map irrigation.
