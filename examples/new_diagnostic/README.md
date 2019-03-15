# Benchmarking new diagnostic

- Define diagnostic as a function that accepts output produced by some inference method. Register the diagnostic with the library.
- Get list of jobs that run the new diagnostic with different models and datasets. Comparison results would ideally be cached and not need to be rerun.
- Run jobs
- View results. The library provides list of output objects and the user does whatever they want with them.

## Misc

Nothing right now