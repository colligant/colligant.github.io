---
title: ""
layout: "about"
---

*year in review  / yir in rəˈvyo͞o / • Granular account of accomplishments*

# **FY 2025**

 - Used the CHELSA meterology dataset to drive LPJ - 3600x increase in resolution, 10s of Tbs of data, 50 CPU _years_ of compute, lots of engineering. Grist for the ML mill (?) (more soon!)
 - Contributed to a [paper](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=dnRnHswAAAAJ&sortby=pubdate&citation_for_view=dnRnHswAAAAJ:dhFuZR0502QC) on best practices in geoscientific model software development
 - Recalibrated the LPJ-EOSIM model, read a bunch of literature, and began writing a manuscript detailing the improvements to LPJ
 - Presented a poster on low latency biospheric carbon modeling at AGU 2024. ![agu2025](/AGU_2024_poster.png)*The aforementioned poster. I was more interested in the whole biogeosciences part of the conference but submitted to a computational section. Next year, I'll submit to biogeosciences.*
  
   I learned quite a bit from AGU and as always came away with many interesting ideas.
 - [Global Carbon Budget 2024](https://essd.copernicus.org/preprints/essd-2024-519/) was published (currently in preprint). Fossil fuel emissions continue to rise through 2023 and the land sink declined. 
 - Implemented global parameter perturbation runs (many many many cores)
 - Fixed an uninitialized memory bug in LPJ-EOSIM that led to non-deterministic results
on some systems


# **FY 2024**

Every year, UMD Earth System Science Interdisciplinary Center (ESSIC) asks us to
submit a formal review, which includes listing the achievements over the
past (fiscal) year. I wrote a lot of code this year (11k+ lines, tested),
published data on LPDAAC, and ended up traveling for work quite a bit. I became 
_much_ more familiar with the LPJ-EOSIM ecosystem, got on a few grants, 
and am going to be an author on at least two papers. It felt like a somewhat auspicious year [^2].
[Despite it being a productive year, I still identified blockers that slow down my workflows.](/review-fy-2024)

That being said, let's recap, starting at coolest.

- Submitted LPJ-EOSIM simulations to TRENDYv13, the most recent version of 
  the Global Carbon Budget's land surface ensemble (and will be a coauthor!)
- Presented a plenary (keynote) presentation at [ICOS 2024](https://www.icos-cp.eu/news-and-events/science-conference/icos2024sc/plenary-speakers#:~:text=to%20these%20regions.-,Thomas%20Colligan,-Thomas%20Colligan%20is), on our work to do near real-time carbon flux 
  anomaly detection. ![icos2024](/icos.PNG)*Me, presenting "A Near Real 
  Time Framework for the Detection and Attribution of Carbon Flux Anomalies" at 
  ICOS 2024 (in 
  Versailles. Cool experience).*
- Was interviewed for the NPR podcast [The Pulse](https://www.npr.org/2024/03/29/1200586692/the-pulse-03-29-2024)
  about my experience during the 2019 solar eclipse in Chile. 
- Significantly improved the LPJ model - meaning LPJ was sped up ~100x in some 
  cases! This timing is inaccurate since I wasn't able to finish a 
  full non-sped-up LPJ run and had to do an estimate based on 1/5 of the 
  runtime.
  I refactored the I/O 
  access patterns to allow better integration with the GPFS filesystem on 
  NCCS Discover. Meaning I/O overhead (which previously was ~90% of the 
  runtime (depending on number of threads of course)) was significantly reduced.
- Wrote a python package to format and upload LPJ-EOSIM data products to 
  LPDAAC. I also read John Ousterhout's _A Philosophy of Software Design_ and 
  carefully implemented his suggestions into my code.
- Set up the AWS infrastructure to push data to LPDAAC. This required quite 
  a bit of interdisciplinary collaboration. 
- Ported LPJ to an AWS ParallelCluster which allowed two international PhD 
  students to run LPJ in the cloud. I was also tech support for them.
- Entirely rewrote the infrastructure for distributing LPJ. There were 
  no tests and many of the R source files used outdated libraries, so I 
  modernized and modularized it with Python.


[^1]: I wonder who will actually find this website. Sometimes I find myself in 
the bowels of the internet looking at random personal pages, which is either 
inspiring (wow! they are so consistent about cataloguing their thoughts!) or 
sort of depressing (huh. they only posted once, a "hello world" sort of 
thing. What happened?).

[^2]: That is, if my funding doesn't run out.
