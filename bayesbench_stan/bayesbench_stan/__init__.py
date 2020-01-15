# Provide methods that take Stan model and data and extra fitting arguments as input and run inference
# Take diagnostics to run as input
# return Output object, so essentially extract samples from chains or q or whatever. Return diagnostic values too.
# Most of the metadata (execution time, method name, dataset name etc) could be filled by bayesbench, then it doesn't need to be repeated in the inference method packages
# Bayesbench can handle turning command line arguments into a list of diagnostic functions to call, so this package doesn't need to worry about that
# Advanced stuff: can we validate that the diagnostics actually work for the intermediate output that the inference method produces? We could sort of do this with some test cases probably
import json
import os
from collections import defaultdict
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple

import numpy as np
import pandas as pd
from pystan.diagnostics import check_hmc_diagnostics

from . import stan_utility
from bayesbench.output import Samples


def nuts(
    *,
    model_name: str,
    data: Mapping[str, Any],
    diagnostics: Any,
    get_model_path: Callable,
    seed: Optional[int],
    method_specific_arguments: Mapping[str, Any],
) -> Tuple[Samples, Mapping[str, Any], Mapping[str, Any]]:

    stan_model = get_compiled_model(get_model_path)

    # load extra args for model X and method Y
    stan_fit = stan_model.sampling(data=data, **method_specific_arguments)

    samples = stan_fit.extract()

    diagnostic_values: Mapping[str, Any] = check_hmc_diagnostics(stan_fit)  # TODO

    explicit_args = method_specific_arguments  # TODO

    # maybe add included diagnostics here
    # So essentially every inference engine can provide built-in diagnostics and then there can be extra diagnostics also
    # More diagnostics is unlikely to be worse than less diagnostics

    return samples, diagnostic_values, explicit_args


def vb(
    *,
    model_name: str,
    data: Mapping[str, Any],
    diagnostics: Any,
    get_model_path: Callable,
    seed: Optional[int],
    method_specific_arguments: Mapping[str, Any],
) -> Tuple[Samples, Mapping[str, Any], Mapping[str, Any]]:

    stan_model = get_compiled_model(get_model_path)

    result = stan_model.vb(data=data, **method_specific_arguments)

    sample_file = result["args"]["sample_file"].decode("utf-8")
    df = pd.read_csv(sample_file, comment="#")

    samples = df.to_dict(orient="list")

    new_samples = transform_samples(samples)
    # here I should convert samples to the slots formation
    # Need to define the slots
    # Then in order to convert I need information from from {model}-info.json
    # We can use arviz to convert but then I have to map that back to whatever format we choose to use
    # Later we should remove arviz because that lets us avoid a dependency, but for now arviz is a good thing to save time

    # Hmm arviz might not work because it seems to expect MCMC result. Then I probably need to write the logic myself

    diagnostic_values: Mapping[str, Any] = {}  # TODO

    explicit_args = method_specific_arguments  # TODO

    return new_samples, diagnostic_values, explicit_args


# Stan 2 and 3 can have different packages, or at least different versions


def generate_prior_predictive(model_name, data, get_model_path):
    model = get_generative_model(model_name=model_name, get_model_path=get_model_path)

    fit = model.sampling(algorithm="Fixed_param")

    samples = fit.extract()

    # This contains both prior and prior predictive samples. Should find a way to extract them separately.
    # For prior predictive there is not a corresponding parameter in the normal model
    # For prior predictive variables there also is a dataset variable with the same name
    # So we can use the data to figure out which are prior and which are prior predictive

    raise Exception("Not finished yet")


def get_generative_model(model_name: str, get_model_path: Callable):
    framework = "stan"
    file_extension = ".stan"

    model_code_path = get_model_path(
        framework=framework,
        file_extension=file_extension,
        model_name="gen_" + model_name,
    )
    stan_model = stan_utility.compile_model(model_code_path)
    return stan_model


def get_compiled_model(get_model_path: Callable):

    framework = "stan"
    model_code_path = get_model_path(framework)

    stan_model = stan_utility.compile_model(model_code_path)
    return stan_model


# There should be a function that can be used to create inference engine with custom inference methods
def create_custom_inference_method(func, dataset, other_args):
    pass
    # Get model code path
    # Compile model

    # Run 1 iteration so we get a fitresult that exposes the gradients etc
    # NOTE this requires dataset, so actually this needs to return a function that takes a dataset and other arguments and then applies them to `func`

    # call func and return result

    # So essentially this does some of the boring plumming
    # Pystan3 I think won't need the 1 iteration


def transform_samples(samples: Mapping[str, List[Any]]):
    """
    Used for transforming samples from Stan's VI output to the format of Stan's MCMC output

    Takes input that is of the form
    {
        ...
        "eta.1": [...],
        "eta.2": [...],
        ...
    }
    and turns it into
    {
        ...
        "eta": [[...], [...]],
        ...
    }
    and then also transposes the lists to match the shape of MCMC output
    and then turns all lists to numpy arrays (which is what MCMC outputs)
    """
    merged_samples: Dict[str, List[Any]] = {}

    lengths: Dict[str, int] = defaultdict(int)

    for key in samples:
        if "." in key:
            actual_key, n_as_str = key.split(".")
            n = int(n_as_str)
            if n > lengths[actual_key]:
                lengths[actual_key] = n

    for actual_key in lengths:
        print(actual_key)
        merged_samples[actual_key] = [0] * lengths[actual_key]

    for key in samples:
        if "." in key:
            actual_key, n_as_str = key.split(".")
            n = int(n_as_str)

            merged_samples[actual_key][n - 1] = samples[key]
        else:
            merged_samples[key] = samples[key]

    new_samples = {k: np.array(v).transpose() for (k, v) in merged_samples.items()}

    return new_samples
