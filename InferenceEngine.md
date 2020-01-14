# Inference engine

This document describes the input and output boundaries for python inference engines. R inference engines will probably be similar but they don't have to be exactly the same

## Description

Inference engine is a python module that contains functions that comform to the required input and output boundaries.

Inference engines can be distributed as pip installable packages. They can also be just python files locally in the filesystem

Inference engines are essentially wrappers over existing frameworks and thus can be easily added for new probabilistic programming frameworks. The base bayesbench package doesn't need to be modified.

NOTE: Supporting models of different frameworks is an open question

## Input boundary

- Model code or object (object for custom inference methods)
- Dataset as python dict (essentially loaded json)
- List of diagnostics to run along with diagnostic names
- (Method name)
- Extra arguments for the method

## Output boundary

- diagnostic outputs, dict of diagnostic name, output value
- posterior samples
- probably nothing else needed (bayesbench can record the config used and execution speed etc, inference engine doesn't have to do that)

## Considerations

If using a locally defined inference engine in a distributed setting we need to make sure that the remote nodes also have the inference engine available. Or well this applies with pip installed inference engines too.

Inference engines could also have a JSON schema for extra fitting arguments. Then extra fitting arguments can be validated before running the actual inferences (so on one machine instead of in a distributed setting). There is however no way of making sure if the included schema is actually valid for the library. This is probably going to be only a minor nuisance (the problem is analogous to mypy typechecker, which while unsound is still often useful).

We might want to have standard names for fitting arguments. Then inference engines perform the translation from standard names to the library-specific names. A problem is that we might not know all possible parameters.

## Todo

Seems pretty clear right now
Loading diagnostic functions is a bit of an open question but inference engines don't need to be concerned with that
Schema for diagnostic functions: probably functions of one argument (inference output), output is something that is json serializable

SBC
