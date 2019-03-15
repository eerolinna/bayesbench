# command line arguments
# - path to stan file
# - path to json dataset
# - method to use: nuts / hmc / vi-fullrank / vi-meanfield
# - output directory

# compile model with stan_utility
# run inference
# save output file

# Saving output file
# - figure out filename. we take hash of model code (file contents) + method name

# Write some code for loading also
# - load all outputs from directory to list
# - or load some specified output (give model file and give method name, or list of these)
# Then user can do whatever they want with the results
# Should be able to load edward/pymc results too


# Edward & pymc
# - I guess easiest to have model file and dataset separately, then can reuse datasets
# - Load model module with importlib, need to have standardized function name
# - Should be pretty straightforward to adapt from stan code

import json
from typing import Dict, Any, Mapping
from .output import Output
from . import stan_utility
import pystan
import functools
import numpy
from hashlib import md5
import os
import time
import importlib
import pymc3 as pm


def run(
    *,
    model_code_path: str,
    method_name: str,
    lib_name: str,
    dataset_path: str,
    output_dir: str,
) -> None:
    if lib_name == "stan":
        run_stan(
            model_code_path=model_code_path,
            dataset_path=dataset_path,
            output_dir=output_dir,
            method_name=method_name,
        )
    else:
        raise NotImplementedError()


def stan_method(*, stan_model, method_name):
    "method names should not contain dashes (-)"
    stan_methods: Mapping[str, Any] = {
        "stan_nuts": stan_model.sampling,
        "stan_vb_fullrank": functools.partial(stan_model.vb, algorithm="fullrank"),
        "stan_vb_meanfield": functools.partial(stan_model.vb, algorithm="meanfield"),
    }
    return stan_methods[method_name]


def run_stan(
    *, model_code_path: str, dataset_path: str, output_dir: str, method_name: str
) -> None:
    """
    Run inference and save output
    """
    with open(dataset_path) as json_f:
        dataset = json.load(json_f)

    model_code = open(model_code_path).read()

    # compile stan model
    # give it dataset
    stan_model = stan_utility.compile_model(model_code_path)

    start = time.time()

    # check if method X should be skipped for model Y
    method = stan_method(stan_model=stan_model, method_name=method_name)

    # load extra args for model X and method Y
    extra_args: Dict[str, Any] = {}

    stan_fit = method(data=dataset, **extra_args)

    # run diagnostics
    # check that diagnostic and method are compatible

    end = time.time()
    output = stan_result_to_output(
        stan_fit=stan_fit,
        creation_time=start,
        execution_time=end - start,
        model_name=model_code_path,
        dataset_path=dataset_path,
        method_name=method_name,
    )
    # TODO file for extra_fitting_args

    save_output(
        output=output,
        output_dir=output_dir,
        model_code=model_code,
        method_name=method_name,
        dataset_path=dataset_path,
    )


def stan_result_to_output(
    *, stan_fit, creation_time, execution_time, model_name, dataset_path, method_name
):
    """
    Extract samples
    Not sure if this needs to be a function
    """
    samples = stan_fit.extract(permuted=True)

    output = Output(
        samples=samples,
        diagnostics=[],
        creation_time=creation_time,
        execution_time=execution_time,
        model_name=model_name,
        lang="python",
        framework="stan",
        dataset_name=dataset_path,
        extra_fitting_args={},
        method_name=method_name,
    )
    return output


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def save_output(
    *,
    output: Output,
    output_dir: str,
    model_code: str,
    method_name: str,
    dataset_path: str,
) -> None:
    code_hash = md5(model_code.encode("ascii")).hexdigest()

    dataset_hash = md5(dataset_path.encode("ascii")).hexdigest()

    filename = f"{method_name}-{code_hash}-{dataset_hash}.json"

    full_filename = os.path.join(output_dir, filename)

    with open(full_filename, "w") as f:
        json.dump(output.to_dict(), f, cls=NumpyEncoder)


"""

import pymc3 as pm

X, y = linear_training_data()
with pm.Model() as linear_model:
    weights = pm.Normal('weights', mu=0, sd=1)
    noise = pm.Gamma('noise', alpha=2, beta=1)
    y_observed = pm.Normal('y_observed',
                mu=X.dot(weights),
                sd=noise,
                observed=y)

    prior = pm.sample_prior_predictive()
    posterior = pm.sample()
    posterior_pred = pm.sample_posterior_predictive(posterior)


pymc_model_path

"""


def run_pymc(
    *, model_code_path: str, dataset_path: str, output_dir: str, method_name: str
) -> None:
    model_module = importlib.import_module(
        model_code_path
    )  # TODO might need to process path
    model = model_module.model  # type: ignore

    with open(dataset_path) as json_f:
        dataset = json.load(json_f)

    model_with_data = model(**dataset)

    result = pm.sample(model=model_with_data)

    # can also use pm.ADVI(model=model_with_data)
    # or pm.FullRankADVI(model=model_with_data)
    # these need pm.fit() also
    ...


if __name__ == "__main__":
    model_code_path = "8_schools.stan"
    method_name = "stan_vb_fullrank"
    lib_name = "stan"
    dataset_path = "8_schools_data.json"
    output_dir = "out"
    run(
        model_code_path=model_code_path,
        method_name=method_name,
        lib_name=lib_name,
        dataset_path=dataset_path,
        output_dir=output_dir,
    )
    print("Done")
