Probably need to do something more with examples. At least a concrete radon example

Add PyMC inference engine, then we'll get better idea of what to do with the models

Write example code for all use cases


PyMC3 SBC
https://github.com/ColCarroll/simulation_based_calibration


Diagnostic API

SBC

New sample format

Writing thesis

Probably best to move `bayesbench_stan` and `bayesbench_pymc` under
`bayesbench`, no need to have have separate packages. This means that the
releases will be locked but that's fine, it's better than requiring the user to
install many perhaps unnecessary packages. However if someone uses just stan and
not pymc then we either have to have both as a dependency (not ideal) or we need
((to write error checking code that tells the user to install pymc if they try to))
run code that requires pymc
