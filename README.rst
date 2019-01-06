=====================================
General Morphological Analysis
=====================================

About
-------
This simple package implements `Morphological analysis <https://en.wikipedia.org/wiki/Morphological_analysis_%28problem-solving%29>`_.
Morphological analysis is the elimination of contradictory statements from a large space of possibilities by systematic search. This allows a clear view on the important effects.

A good introduction is `this video <https://www.youtube.com/watch?v=x4zAniSP0FY>`_.

Difference to their software are that this package allows specification of more complex exclusion criteria rather than just two mutually exclusive values. 

Web implementation
-------------------

https://johannesbuchner.github.io/zwicky-morphological-analysis/

Source code in gh-pages branch.

Pull requests are welcome.

Python implementation
----------------------

This package is written in Python. It has no GUI.

The code is a simple depth-first search with early truncation.

Source code in master branch.

Usage
----------
See zebra.py for an example. There, the `Zebra puzzle <https://en.wikipedia.org/wiki/Zebra_Puzzle>`_ is implemented and solved.


