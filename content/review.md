---
title: ""
layout: "about"
---

*personal review /ˌäptəməˈzāSH(ə)n/ • the process of examining your workflow to resolve blockers*

Some years ago, I noticed that my deep learning workflows all had one thing in common: It was near impossible to
reproduce every experiment I ran without a lot of work. I kept good notes but sometimes what you really need is the
exact code of your experiment, plus a description. Ideally, you'd track everything on Git, but paths change, data
loaders evolve, and minor tweaks like adjusting n_layers from 10 to 12 don't always fit neatly into version control.

To solve this, I wrote a templating library for DL projects that kept track of every experiment automatically. 
This saved me hours of time and significantly improved reproducibility [^1].

I noticed this pain point while I was doing a periodic review of my workflows, something I started in grad school. I
find that it's pretty easy to examine common work patterns and find bottlenecks. Sometimes these bottlenecks are
technical (e.g., how can I automatically sync files to a cluster), or mental (e.g., consistently getting stuck in a
particular phase of a project).

Technical ones are easier to find and solve, mental ones less so. My rule of thumb is to spend a few hours doing this
every month or so. It almost always leads to greater efficiency, exposure to new tools, and a fresh perspective on old 
problems.

[^1] There are many solutions to this problem. It's often not necessary to roll your own solution. Part of a successful
review process is finding relevant software to apply to your blockers.