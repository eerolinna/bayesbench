# command line arguments
# - path to stan file
# - path to json dataset
# - method to use: nuts / hmc / vi-fullrank / vi-meanfield
# - output directory

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
from typing import Dict, Any, Mapping, Sequence, Optional
from .output import Output, RunConfig
from .posterior_db import PosteriorDatabase
import functools
import numpy
from hashlib import md5
import os
import time
import importlib
import argparse


def run(
    *,
    posterior_db_location: str,
    inference_engine: str,
    posterior_name: str,
    method_specific_arguments: Mapping[str, Any],
    diagnostics: Sequence[str],
    output_dir: str,
    seed: int = None,
    save=True,
) -> None:

    # load model from posterior DB
    # - Stan: load model as text
    # - PyMC: Use importlib to import the python module
    # Maybe both of these should happen in inference engine

    # load dataset from posterior DB

    # load inference engine

    # load diagnostics with importlib

    # run inference engine with model and dataset and extra fitting args
    # inference engine returns samples and diagnostic values
    # Create output
    #

    posterior_db = PosteriorDatabase(posterior_db_location)

    dataset_path = posterior_db.get_dataset_path(posterior_name=posterior_name)
    model_name = posterior_db.get_model_name(posterior_name)

    inference_engine_name, method_name = inference_engine.rsplit(".", 1)

    with open(dataset_path) as json_f:
        dataset = json.load(json_f)

    inference_engine_module = importlib.import_module(inference_engine_name)

    method = getattr(inference_engine_module, method_name)

    start = time.time()

    samples, diagnostic_values, explicit_args = method(
        model_name=model_name,
        data=dataset,
        diagnostics=diagnostics,
        get_model_path=posterior_db.get_model_path,
        seed=seed,
        method_specific_arguments=method_specific_arguments,
    )

    end = time.time()
    output = result_to_output(
        samples=samples,
        diagnostics=diagnostic_values,
        inference_engine_name=inference_engine_name,
        creation_time=start,
        execution_time=end - start,
        posterior_name=posterior_name,
        method_name=method_name,
        method_specific_arguments=explicit_args,
        seed=seed,
    )
    if save:
        save_output(output=output, output_dir=output_dir)
    return output


def run_many(runs):
    results = []
    for run_data in runs:
        results.append(run(**run_data))

    return results


def result_to_output(
    *,
    samples,
    diagnostics,
    creation_time,
    execution_time,
    posterior_name,
    method_name,
    inference_engine_name: str,
    method_specific_arguments,
    seed: Optional[int],
):
    run_config = RunConfig(
        seed=seed,
        lang="python",
        posterior_name=posterior_name,
        inference_engine=inference_engine_name,
        method_name=method_name,
        method_specific_arguments=method_specific_arguments,
    )

    output = Output(
        samples=samples,
        diagnostics=diagnostics,
        creation_time=creation_time,
        execution_time=execution_time,
        run_config=run_config,
    )
    return output


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def get_hash(to_hash: str) -> str:
    return md5(to_hash.encode("ascii")).hexdigest()


def save_output(*, output: Output, output_dir: str) -> None:

    # This hashing is from https://stackoverflow.com/questions/5884066/hashing-a-dictionary
    # NOTE: This might not be stable across machines and python versions.
    # That is not a huge problem, but we can later look into if there is a better way to generate unique file names
    config_hash = get_hash(
        json.dumps(
            output.run_config.to_dict(),
            sort_keys=True,
            ensure_ascii=True,
            separators=(",", ":"),
        )
    )

    filename = f"{config_hash}.json"

    full_filename = os.path.join(output_dir, filename)

    with open(full_filename, "w") as f:
        json.dump(output.to_dict(), f, cls=NumpyEncoder)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run inference")
    parser.add_argument("--json", required=True, help="Arguments as json string")
    parser.add_argument("--output-dir", required=True, help="Output directory")

    args = parser.parse_args()

    data = json.loads(args.json)

    posterior_name = data["posterior_name"]
    inference_engine = data["inference_engine"]
    output_dir = args.output_dir
    posterior_db_location = data["posterior_db_location"]
    method_specific_arguments = data.get("method_specific_arguments", {})
    diagnostics = data.get("diagnostics", [])

    run(
        posterior_name=posterior_name,
        inference_engine=inference_engine,
        output_dir=output_dir,
        posterior_db_location=posterior_db_location,
        method_specific_arguments=method_specific_arguments,
        diagnostics=diagnostics,
    )


def test_main():
    # load command line arguments here and pass to run
    model_name = "8_schools_noncentered"
    inference_engine = "bayesbench_stan.meanfield_advi"
    dataset_name = "8_schools"
    output_dir = "out"
    posterior_db_location = "/home/eero/default_posterior_db"
    extra_fitting_args: Mapping[str, Any] = {}
    diagnostics: Sequence[str] = []
    run(
        model_name=model_name,
        inference_engine=inference_engine,
        dataset_name=dataset_name,
        output_dir=output_dir,
        posterior_db_location=posterior_db_location,
        extra_fitting_args=extra_fitting_args,
        diagnostics=diagnostics,
    )
    print("Done")


if __name__ == "__main__":
    main()
