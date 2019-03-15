# Benchmarking a new method

- Define inference method as function that accepts a Stan model (and a dataset) and possibly method-specific extra arguments. Register the function with the framework.
- Get list of jobs that run the new method with different models and datasets. Outputs of comparison methods would ideally be cached and not need to be rerun.
- Run jobs
- View results. The library provides list of output objects and the user does whatever they want with them.

## Misc

It should be possible to use other models than Stan models too

SBC is missing