---
title: ""
layout: "about"
---

*clean code /klēn/ /kōd/ • future-proofing your software*  

During my Master's in Computer Science, I focused on applying code as a means to an end. My
work in satellite computer vision involved extensive coursework in math and machine learning, 
but not necessarily software design. However, I quickly realized during one of my [optimization](/optimization) processes
that writing complex code tends to lead to unnecessary mental overhead, increased
development time, and the tendency to curse yourself a few months down the road (_why did I write it like that?_). 


The solution was defining a set of rules for software development, instead of relying on memory or habit. I was
particularly guided by John Ousterhout's _A Philosophy of Software Design_, so some of the following guidelines mirror
his suggestions.

- Design before implementing. Ideally twice but at least once. Using a paper and pen can help ideas flow more easily. Consider future improvements or use cases.
- Modules should be _deep_. Hide complexity behind simple function calls.
- Modules and functions should fulfill a single role. This makes them resilient to internal refactors, as you only need to maintain the interface.
- Write unit and integration tests. Think about edge cases. It's a wonder how many times this will save you from insidious bugs.
- It's ok to refactor code, but realize that every system is imperfect. Good enough is really often good enough.


Writing code is similar to writing essays: ideas have to mesh clearly to deliver a cohesive whole. If you can 
express yourself succinctly in both writing and code your point is communicated more effectively. Complexity is 
inevitable, but your writing (whether code or prose) doesn't have to multiply it. 

The final point is that these are all only guidelines. Trying to apply them perfectly every time just leads to writer's block.