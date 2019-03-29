# Provide methods that take Stan model and data and extra fitting arguments as input and run inference
# Take diagnostics to run as input
# return Output object, so essentially extract samples from chains or q or whatever. Return diagnostic values too.

# Most of the metadata (execution time, method name, dataset name etc) could be filled by bayesbench, then it doesn't need to be repeated in the inference method packages


# Bayesbench can handle turning command line arguments into a list of diagnostic functions to call, so this package doesn't need to worry about that

# Advanced stuff: can we validate that the diagnostics actually work for the intermediate output that the inference method produces? We could sort of do this with some test cases probably


def stan_nuts(model, data, diagnostics, seed, extra_fitting_args):
    pass


def stan_fullrank_vi(model, data, diagnostics, seed, extra_fitting_args):
    pass


# Meanfield also
# Should meanfield/fullrank just be extra fitting args? I guess they should be considered as separate methods


def alternative(method, model, data, diagnostics, seed, extra_fitting_args):
    if method == "stan_nuts":
        return stan_nuts(model, data, diagnostics, seed, extra_fitting_args)
    elif method == "stan_fullrank_vi":
        pass


# Stan 2 and 3 can have different packages, or at least different versions
