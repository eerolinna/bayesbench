# Provide methods that take Stan model and data and extra fitting arguments as input and run inference
# Take diagnostics to run as input
# return Output object, so essentially extract samples from chains or q or whatever. Return diagnostic values too.

# Most of the metadata (execution time, method name, dataset name etc) could be filled by bayesbench, then it doesn't need to be repeated in the inference method packages


# Bayesbench can handle turning command line arguments into a list of diagnostic functions to call, so this package doesn't need to worry about that

# Advanced stuff: can we validate that the diagnostics actually work for the intermediate output that the inference method produces? We could sort of do this with some test cases probably

from typing import Mapping, Any, Tuple, Callable, Optional
import pystan
from . import stan_utility
from bayesbench.output import Samples
import pandas as pd
import numpy as np
import json


def nuts(
    *,
    model_name: str,
    data: Mapping[str, Any],
    diagnostics: Any,
    get_model_path: Callable,
    seed: Optional[int],
    method_specific_arguments: Mapping[str, Any],
) -> Tuple[Samples, Mapping[str, Any], Mapping[str, Any]]:

    stan_model = get_compiled_model(model_name, get_model_path)

    # load extra args for model X and method Y
    stan_fit = stan_model.sampling(data=data, **method_specific_arguments)

    samples = stan_fit.extract()

    diagnostic_values: Mapping[str, Any] = {}  # TODO

    explicit_args = method_specific_arguments  # TODO

    # maybe add included diagnostics here
    # So essentially every inference engine can provide built-in diagnostics and then there can be extra diagnostics also
    # More diagnostics is unlikely to be worse than less diagnostics

    return samples, diagnostic_values, explicit_args


def fullrank_advi(
    *,
    model_name: str,
    data: Mapping[str, Any],
    diagnostics: Any,
    get_model_path: Callable,
    seed: Optional[int],
    method_specific_arguments: Mapping[str, Any],
) -> Tuple[Samples, Mapping[str, Any], Mapping[str, Any]]:

    return base_advi(
        model_name=model_name,
        data=data,
        diagnostics=diagnostics,
        get_model_path=get_model_path,
        seed=seed,
        method_specific_arguments=method_specific_arguments,
        algorithm="fullrank",
    )


def meanfield_advi(
    *,
    model_name: str,
    data: Mapping[str, Any],
    diagnostics: Any,
    get_model_path: Callable,
    seed: Optional[int],
    method_specific_arguments: Mapping[str, Any],
) -> Tuple[Samples, Mapping[str, Any], Mapping[str, Any]]:
    return base_advi(
        model_name=model_name,
        data=data,
        diagnostics=diagnostics,
        get_model_path=get_model_path,
        seed=seed,
        method_specific_arguments=method_specific_arguments,
        algorithm="meanfield",
    )


def base_advi(
    *,
    model_name: str,
    data: Mapping[str, Any],
    diagnostics: Any,
    get_model_path: Callable,
    seed: Optional[int],
    method_specific_arguments: Mapping[str, Any],
    algorithm: str,
) -> Tuple[Samples, Mapping[str, Any], Mapping[str, Any]]:

    stan_model = get_compiled_model(model_name, get_model_path)

    result = stan_model.vb(data=data, algorithm=algorithm, **method_specific_arguments)

    sample_file = result["args"]["sample_file"].decode("utf-8")
    df = pd.read_csv(sample_file, comment="#")

    samples = df.to_dict(orient="list")

    # TODO: Right now arrays get individual keys (arr[1], arr[2] etc)
    # Need to change that so MCMC and VI are compatible with each other
    new_samples = {k: np.array(v) for (k, v) in samples.items()}
    # here I should convert samples to the slots formation
    # Need to define the slots
    # Then in order to convert I need information from from {model}-info.json
    # We can use arviz to convert but then I have to map that back to whatever format we choose to use
    # Later we should remove arviz because that lets us avoid a dependency, but for now arviz is a good thing to save time

    # Hmm arviz might not work because it seems to expect MCMC result. Then I probably need to write the logic myself

    model_info = get_model_info(model_name, get_model_path)

    diagnostic_values: Mapping[str, Any] = {}  # TODO

    explicit_args = method_specific_arguments  # TODO

    return new_samples, diagnostic_values, explicit_args


# Stan 2 and 3 can have different packages, or at least different versions

# This will be deleted, unnecessary soon
def stan_method(*, stan_model, method_name):
    "method names should not contain dashes (-)"
    stan_methods: Mapping[str, Any] = {
        "stan_nuts": stan_model.sampling,
        "stan_vb_fullrank": functools.partial(stan_model.vb, algorithm="fullrank"),
        "stan_vb_meanfield": functools.partial(stan_model.vb, algorithm="meanfield"),
    }
    return stan_methods[method_name]


def get_compiled_model(model_name: str, get_model_path: Callable):

    framework = "stan"
    file_extension = ".stan"
    model_code_path = get_model_path(
        framework=framework, file_extension=file_extension, model_name=model_name
    )

    stan_model = stan_utility.compile_model(model_code_path)
    return stan_model


def get_model_info(model_name: str, get_model_path: Callable) -> Mapping[str, Any]:
    framework = "stan"
    file_extension = ".json"
    info_path = get_model_path(
        framework=framework,
        file_extension=file_extension,
        model_name=f"{model_name}-info",
    )
    with open(info_path) as f:
        info = json.load(f)

    return info


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
