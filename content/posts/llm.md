+++
title = "What an LLM taught me about my (innie) self"
date = 2025-04-10T14:40:43Z
draft = false
+++

![alt text](/innie.png)*Me, staring down the barrel of yet another segfault*

I keep an extensive work journal, recording my ideas, problems, and solutions daily.
Since starting my current role ~1.5 years ago I've written 16895 lines of notes.
At 36 lines per page this comes to 469 pages, indicating that I've written about a third of _War and Peace_ [^1].

The notes contain code snippets, rambling thoughts, and TODO lists, but also concise ideas and solutions to problems. While re-reading my notebook myself may be a useful exercise (and I do 
reference old notes often), I figured I could use an LLM to summarize my "notes novel" for me: What are my main blockers? Achievements? Where can I optimize workflows or patterns of thought to become 
a better engineer and scientist?

### Wetware self-reflection

Here are my perceived blockers before using an LLM:

- Having to re-run global simulations due to bugs in LPJ
- A working but relatively scratchy-feeling pipeline
- Constant HPC issues: I/O overload on GPFS, OS updates, ephemeral SLURM bugs
- Configuration of the software ecosystem (no overlaying orchestrator, because SLURM & HPC constraints)

Ideally, I'd like to build a more resilient pipeline to distribute LPJ, refactor the output scheme (LPJ writes _on each timestep_), and cleverly split inputs. That being said, we're at a point that was unthinkable a year ago:
fast, easily configured, and QA'd simulations that automatically estimate uncertainty and incorporate multiple drivers.

### Hardware (i.e, ChatGPT) reflection
I'm using ChatGPT 4o to reason over my notes file [^2] with the prompt derived from the first two paragraphs of this post. It came back with:
> - Abstract your preprocessing, QA, and merge routines into reusable modules (i.e., your own internal “LPJ-utils” lib). Too many time sinks are due to ad-hoc code.
> - Build simulation validation routines that catch common config or flag issues pre-submit.
> - Invest in config/schema linting and pipeline dry-run logic—this would prevent bugs like unturned-on flags or missing variables.
> - Consider formalizing regression tests for scientific outputs (e.g., NBP bounds, GPP sanity checks, driver conformity).

Some of these are useful, and some suffer from incomplete knowledge. For example, I've abstracted all preprocessing/merging into reusable modules (and created a new library - `nc_tools` for custom reused analyses),
and created prebaked protocols for simulations to reduce configuration load. However, I _like_ the idea of better simulation validation routines & I would love to write bit-wise regression tests for LPJ (but I'm already oversubscribed!).
All in all, the suggestions that ChatGPT gave me aren't too surprising: reuse code (which I do, and it can't see that because it doesn't have access to my github), formalize tests, and protect my time.

I asked it to go deeper, and got some more interesting results:

> - Design for your future self at scale
> - Codify your debugging instincts into tooling:
>   You debug like a surgeon — slicing right to the problem. But you do this manually, every time.
>   Build a reusable debugging harness that can test key outputs for scientific sanity (e.g., “Is GPP plausible given input radiation?”). Logics like this can become property-based tests or assertions.
> - Shift from tactical iteration to system refinement:
>   Every 2 weeks, step back and ask: “What would make this entire class of problem impossible?” Write the answer down, even if you can’t implement it yet.
> - Shift into mentorship mode (even if solo):
>   You’re reaching a level where writing code is no longer your most valuable contribution. Designing reusable systems and mentoring others (or your future self) is.
>   Even if there’s no one else today. Make README files, “how this works” diagrams, or short Loom videos. Build infrastructure that’s teachable.
> - Build interrupt-resilient flow:
>   Cluster downtime, flaky tools, or long I/O waits derail deep work.
>   Instead of waiting, queue up fallback tasks like writing inline docstrings, reviewing last week’s commits, or writing one-shot unit tests. This keeps momentum even when infrastructure doesn’t cooperate.

These are all good suggestions. I particularly like the 2-week review where I ask how I can make the class of problem impossible. However, once I read these ideas, my thought processes changed, and concrete
ideas started to develop:

> - The reason why tests are _so hard_ to implement successfully is because of the scale of the data. Instead of throwing more compute at it (which is a bad idea because
> of I/O latency on the cluster), why not reduce the amount of data? It'll require some LPJ engineering and pipeline engineering but could greatly reduce cognitive load.
> - Re-prioritize tasks for future me: do automated bitwise CI/CD, Dockerize the model, rewrite the way LPJ is configured. Just do it.
> - Systemic issues in the LPJ model (like excessive I/O, uninitialized memory errors, and conditional compilation bugs) have been caused by a lack of institutional knowledge around C development on HPC systems [^3]. 
>   The solution? Writing a best practices document and employing bitwise regression tests.
> - Standardize the debugging harness. Start recording when/why simulations failed (e.g., outputs failed to write to disk, out of netcdf bounds) and _code_ meta-solutions to them.
 

### Conclusion
ChatGPT came up with some good ideas - write tests, codify institutional knowledge, and protect my time. The refracted image that ChatGPT gave me of my past
few years helped me carve a path forward to improve my workflow. My self-perceived blockers were technical, and ChatGPT gave me 
different suggestions on how to think about the classes of problems that arise (through my own prompting to "think deeply about meta-blockers"). Overall, this was a useful
exercise, and I've already begun thinking about how to implement some of these co-creations.

Doing this reflective exercise at points during the past ~1.5 years led to significant improvements of the workflow [^4]. I'm excited to see where the next year takes me with these insights!

[^1] I make no assertion that the quality of my notes is even mildly literary.

[^2] Context length, byte-pair-encoding, and the way ChatGPT processes large files means this is fine.

[^3] New LPJ developers are given the github, HPC credentials, and then told to dive in. Many folks have just worked in R and have no experience with C (pointers, allocating memory, function pointers, datatypes!)

[^4] Running 100s of global simulations, increasing LPJ resolution, reading literature, writing papers, contributing to papers, pushing data to LPDAAC, formalizing new
processes in LPJ, etc, etc, etc
