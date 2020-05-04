---
layout: post
title: First post and AGU
img: /img/agu-poster.png
---

I'm writing this post on the flight back from AGU. 
The lighting overview is that the method we presented does fairly well mapping irrigation, with an overall accuracy of ```97%``` and an f1-score for the irrigated class of ```91%```. The statistics reported aren't modified in any way. Other methods either report different statistics or mask their irrigation maps to a different product like the crop data layer. 

![]({{ site.baseurl }}/img/agu-poster.png)

Above is one of the posters I presented. I got a bunch of good feedback,
from datasets to use to techinques to try. One thing I haven't been doing in my research is split the dataset into test, train, and validation splits. I've only been doing test/train splits, but this means I'm just optimizing for (and reporting) the best test accuracy. That was another valuable insight gained from AGU, one that I'll implement over the break. I was too busy during my poster session to really see what other people are doing related to mapping irrigation, but I'll keep that in mind for next time.
