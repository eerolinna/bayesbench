import json
from typing import Any
from typing import Dict
from typing import Mapping
from typing import Optional
from typing import Sequence

from .posterior_db import PosteriorDatabase
from .run import run

"""
def sbc(
    *,
    posterior_db_location: str,
    inference_engine: str,
    posterior_name: str,
    method_specific_arguments: Mapping[str, Any],
    diagnostics: Sequence[str],
    output_dir: str,
    seed: int = None,
) -> None:
    posterior_db = PosteriorDatabase(posterior_db_location)

    dataset_path = posterior_db.get_dataset_path(posterior_name=posterior_name)
    model_name = posterior_db.get_model_name(posterior_name)

    with open(dataset_path) as json_f:
        original_data = json.load(json_f)
    # Generate prior and prior predictive samples

    # call inference engine's `generate_prior_predictive`

    # After we have prior and prior predictive samples we can just call run with new data and postprocess the results to obtain ranks
    all_ranks = []

    prior: Any = []
    prior_predictive: Any = []
    compute_ranks = lambda x: x
    for prior_draw, prior_predictive_draw in zip(prior, prior_predictive):
        # with model 2 this overwrites `y` from data with `y` from prior predictive draw
        new_data = merge(original_data, prior_predictive_draw)

        # Need to make version of run that accepts model name and data (data is different than usually here)
        # Maybe just _run that takes more explicit arguments
        output = run(
            posterior_name=posterior_name,
            inference_engine=inference_engine,
            output_dir=output_dir,
            posterior_db_location=posterior_db_location,
            method_specific_arguments=method_specific_arguments,
            diagnostics=diagnostics,
        )

        ranks = compute_ranks(output, prior_draw)
        all_ranks.append(ranks)

    # do something with all_ranks


def merge(original_data, new_data):
    return {**original_data, **new_data}

"""
