---
title: ""
layout: "about"
---

*year in review  / yir in rəˈvyo͞o / • Granular account of accomplishments*

# **FY 2025 (Oct '24 - Oct '25)**

It's that time of year again - let's look back on what I've accomplished. This year was less focused on greenfield software development and more on
maintaining and updating the existing tooling around LPJ - I read a few books on programming and refactored almost the entire project while adhering to best practices. There are now three Python modules comprising ~12k LOC (oof). 
One of my tasks involved writing a thorough treatment of the LPJ model (now at ~44 pages, few figures), after which I can confidently say I understand the way LPJ models ecosystems<small>[^1]</small>. This was partly
to support a new data push effort where we're getting streaming land CO2 products on LPDAAC. I also started learning `terraform` and AWS more in depth. 

Overall, I had an OK year: learned a lot about writing better code, redesigned and developed large parts of the software ecosystem around LPJ, learned about AWS and conventional HPC, contributed data to various scientific papers, and wrote quite a bit of a technical manuscript on how LPJ works.

 - Used `terraform` to provision AWS resources for 1) running LPJ on Batch and 2) accomplishing the LPDAAC data pushes. IaC is cool.
 - Was made PI on a couple of computational projects on NCCS
 - Collaborated on a couple of ML projects - one with a paper under review and marketable product, another under development<small>[^2]</small>. When in doubt, pretrain.
 - Implemented a proof of concept autodoc system for LPJ, which will use the process descriptions mentioned below 
 - Described every single process in LPJ-EOSIM that leads to CO2 estimates, which will be published as the ATBD with LPJ CO2 on LPDAAC. This is coupled with a manuscript in prep that's 44 pages describing the state of LPJ-EOSIM (i.e., every process, how they interact, and updates we've made since the original model recap paper).
 - Contributed our NRT ERA5 LPJ products to a [low latency carbon budgeting analysis](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=dnRnHswAAAAJ&sortby=pubdate&citation_for_view=dnRnHswAAAAJ:_kc_bZDykSQC)
 - Rewrote some key parts of the workflow in Prefect and Dask (which required a bit of encouragement to get to work on our SLURM-managed HPC). I learned a _ton_ about GPFS and HPC strategies in this process. Overall I'm super impressed by Dask/Prefect/SLURM integrations.
 - Got awarded a grant on which I'm a Co-PI
 - Refactored much of the tooling around LPJ to reduce complexity and add maintainable features (following DRY etc). Big update: using the pipeline as an actual API and abstracting away the heavy compute. Previously it was primarily a command line interface. Now simulations have nice abstractions that makes dealing with them much less complex.
 - Submitted LPJ-EOSIM simulations to TRENDYv14 (land sink neutral or slightly negative compared to last year)<small>[^3]</small>. I also took the time to script the bespoke unit conversions and formatting requirements for TRENDY, which will make subsequent year submissions really easy.
 - Attended the Warming-Induced Emissions Model Intercomparison Project (WIE-MIP) meeting in Bern, CH, where I briefly presented on the pros and cons of a cloud-based MIP analysis platform
 - Used the [CHELSA meterology](https://tcolligan.org/posts/high-res-dgvm/) dataset to drive LPJ - 3600x increase in resolution, 10s of Tbs of data, 50 CPU _years_ of compute, lots of engineering. Grist for the ML mill (?) (more soon!). 
 - Contributed to a [paper](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=dnRnHswAAAAJ&sortby=pubdate&citation_for_view=dnRnHswAAAAJ:dhFuZR0502QC) on best practices in geoscientific model software development
 - Presented a poster on low latency biospheric carbon modeling at AGU 2024. ![agu2025](/AGU_2024_poster.png)*The aforementioned poster. I was more interested in the whole biogeosciences part of the conference but submitted to a computational section. Next year, I'll submit to biogeosciences.*
   I learned quite a bit from AGU and as always came away with many interesting ideas.
 - [Global Carbon Budget 2024](https://essd.copernicus.org/preprints/essd-2024-519/) was published (currently in preprint). Fossil fuel emissions continue to rise through 2023 and the land sink declined. 
 - Implemented global parameter perturbation runs (many many many cores)
 - Fixed an uninitialized memory bug in LPJ-EOSIM that led to non-deterministic results
on some systems

On the side, I vibe-coded an app that uses an LLM as a backend to do your budget for you, and wrote some code for my Garmin watch to enable
a custom "pickleball" activity. I also crystallized my thoughts about using LLMs: don't offload your cognitive tasks to them. Use them for enabling web search and providing scaffolds for day zero coding, but otherwise
they just aren't good enough yet to effectively make design/code/research decisions for me. Plus there's no opportunity to learn if you're just asking some RLVR algorithm to think for you. 


# **FY 2024**

Every year, UMD Earth System Science Interdisciplinary Center (ESSIC) asks us to
submit a formal review, which includes listing the achievements over the
past (fiscal) year. I wrote a lot of code this year (11k+ lines, tested),
published data on LPDAAC, and ended up traveling for work quite a bit. I became 
_much_ more familiar with the LPJ-EOSIM ecosystem, got on a few grants, 
and am going to be an author on at least two papers. It felt like a somewhat auspicious year<small>[^4]</small>.
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

[^1]: I'm looking at this like technical documentation which will eventually be incorporated into the LPJ codebase and pushed to a docs site with some autodoc tool
[^2]: My suggestions led to nice increases in performance, which feels good. 
[^3]: We integrated a new temperature response function which helps reanalysis drivers estimate reasonable levels of land CO2 sink, but decreases respiration enough to make LPJ miss the
O2/N2 constraint... and as such is excluded from estimates of the land sink in TRENDY this year. However, this isn't a big deal, as we have another model configuration that is well within the constraint.
[^4]: That is, if my funding doesn't run out.
