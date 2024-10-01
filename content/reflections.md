---
title: ""
layout: "about"
---

*reflections*  / rəˈflekSH(ə)ns / • A log of achievements and 
thoughts on work

Non-binding contract with myself to keep this updated [^1]

# **2024**

Every year, UMD Earth System Science Interdisciplinary Center (ESSIC) asks us to
submit a formal review, which includes listing the achievements over the
last year. I wrote a lot of code this year (11k+ lines, tested),
published data on LPDAAC, and ended up traveling for work quite a bit. I became 
_much_ more familiar with the LPJ-EOSIM ecosystem, got on a few grants, 
and am going to be an author on at least two papers. If everything continues 
as is, it was a somewhat auspicious year [^2].

I have a few goals for the upcoming year. Really, there are a ton of low 
hanging ML fruits in this field, so I'd like to be involved in one or two of 
those projects. Additionally, I'd like to hone my writing skills so that 
publications don't become such a burden. Technically, I'm still making
strides: learning AWS, unit testing, even things like IDE setup. One 
specific thing that I'd like to achieve is pushing the entire 
pipeline to AWS and codifying a release structure so that future users can 
update LPJ and products with minimal effort.
Concretely, I'd like to connect with a mentor at NASA to help me with software 
development and attend a conference on scientific software dev.

So, let's recap, starting at most recent.

- Submitted LPJ-EOSIM simulations to TRENDYv13, the most recent version of 
  the Global Carbon Budget's land surface ensemble (and will be a coauthor!)
- Presented a plenary (read: keynote) presentation at [ICOS 2024](https://www.icos-cp.eu/news-and-events/science-conference/icos2024sc/plenary-speakers#:~:text=to%20these%20regions.-,Thomas%20Colligan,-Thomas%20Colligan%20is), on our work to do near real time carbon flux 
  anomaly detection. ![icos2024](/icos.PNG)*Me, presenting work at ICOS (in 
  Versailles. Cool experience).*
- Did a ton of model improvement - meaning LPJ was sped up 100x in some 
  cases! This timing is sort of inaccurate since it takes _a ton of time_ 
  for LPJ to run in the non-sped-up mode. Basically I refactored the I/O 
  access patterns to allow better integration with the GPFS filesystem on 
  NCCS Discover. Meaning I/O overhead (which previously was like 90% of the 
  runtime (depending on number of threads of course)) was significantly reduced.
- Wrote a python package to format and upload LPJ-EOSIM data products to 
  LPDAAC. I also read John Osterhout's _A Philosophy of Software Design_ and 
  thought _really_ hard about how to implement his axioms into my code.
- Set up the AWS infrastructure to push data to LPDAAC. This required quite 
  a bit of interdisciplinary collaboration which was so rewarding to see 
  through to the end.
- Ported LPJ to an AWS ParallelCluster which allowed two international PhD 
  students to run LPJ in the cloud. I was also tech support for them.
- Entirely rewrote the infrastructure for distributing LPJ. There weren't
  any tests and many of the R source files used old libraries. This looked like 
  writing a bunch of tested Python.


[^1] I wonder who actually finds this website. Sometimes I find myself in 
the bowels of the internet looking at random personal pages, which is either 
inspiring (wow! they are so consistent about cataloguing their thoughts!) or 
sort of depressing (huh. they only posted once, a "hello world" sort of 
thing. What happened?).

[^2] That is, if my funding doesn't run out.