---
title: ""
layout: "about"
---

# **blockers from fiscal year 2024, plans for next**

*non-exhaustive and mutable list*

The cluster is down today, so I'm working on this in the meantime (as time 
spent reflecting can lead to massive workflow speedups).

- The LPJ pipeline is starting to become a beast. It's swelling and feels a bit unwieldy at times. I would like to transition to a _true_ workflow
  management library to keep everything in pure Python.
- I've noticed that when I need to write code fast the quality really deteriorates, and requires refactoring later.
  This tendency was mentioned in *A Philosophy of Software 
  Design*, and I'd like to remind myself to develop a little slower in the future.
- Attention to detail: iPhone recently let me know that I was receiving around 300 emails per week. I found myself losing the thread
  on some of them this year. My goal this year is to categorize important emails (this has already helped with organization).
- I'm getting so used to Slack messaging that sometimes I send emails with less 
  editing than I should - I should re-read every email before sending it
- LPJ-EOSIM reproducibility: I probably spent two weeks in total chasing a 
  memory allocation bug that caused stochastic behavior in the model.
  This is just a huge signal that I need to write a Docker/Singularity image 
  for this, and transition all the data publication code to the Docker image.
- Quality checking and examining new simulations is cumbersome. Specifically, 
  re-running plotting code each time I need to change y or x limits
  involves a back-and-forth that's wasting time. Investing some time in a 
  non-static website to display line plots could be worth its effort. In 
  addition, plotting COGs interactively (postGIS?) would really speed things up.
- Protecting my time: I enjoy helping others ...and working remotely can be isolating. 
  However, I need to find a balance between helping them and hindering myself.
- When ssh'ing onto Discover I need to set up a .bash_profile 
  that brings me to the same node each time I log in (or... just do it from 
  my ssh alias so if the node is down I don't get rejected?)
- Develop a data management plan for production LPJ simulations. Right now, everything is sitting in a directory on the cluster with timestamps. I'd
  like to formalize the process of running production simulations.
- I looked back at a timeline that I created in February of this year. It was quite ambitious and as a result some things _didn't even get touched_.
For example, I was certain that I could do GCP, ML based downscaling and deployment, on demand NBP and CH4 simulations, and write a website for a methane newsletter. Of course, 
my taskload varied with ICOS, VICC, writing a paper, and the fact that some of my work depended on outside timelines. Still, my goal for this year is to write more realistic timelines.
- I often do exploratory data analysis and so far have been copy-pasting code from one library/jupyter notebook to another, resulting in slower workflows and cluttered EDA scripts.
I'm going to make a Python library to hold my workhorse functions (`nc_tools`?)
 

*Aspirations*

I have a few goals for the upcoming year. Really, there are a ton of low
hanging ML fruits in this field, so I'd like to be involved in one or two of
those projects. I'd like to hone my writing skills so that
publications don't become such a burden. Technically, I'm still making
strides: learning AWS, unit testing, even investing time into pedestrian things
like IDE setup. One specific thing that I'd like to achieve is pushing our entire analysis
pipeline to AWS and codifying a release structure so that future users can
update LPJ and downstream products with minimal effort.

Finally, I'd like to connect with a mentor at NASA to help me with software
development and career growth generally.