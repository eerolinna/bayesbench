import importlib
import json
from typing import Any
from typing import Callable
from typing import Mapping
from typing import Optional
from typing import Tuple

import pymc3 as pm

from bayesbench import Samples

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


def nuts(
    *,
    model_name: str,
    data: Mapping[str, Any],
    diagnostics: Any,
    get_model_path: Callable,
    seed: Optional[int],
    method_specific_arguments: Mapping[str, Any],
) -> Tuple[Samples, Mapping[str, Any], Mapping[str, Any]]:

    model = get_model(model_name=model_name, data=data, get_model_path=get_model_path)

    chains = 1  # TODO
    draws = 1000  # TODO
    with model:
        trace = pm.sample(draws, chains)  # TODO use method_specific_arguments
        prior = pm.sample_prior_predictive()
        posterior_predictive = pm.sample_posterior_predictive(trace, 500, model)

    # Here I could probably use arviz for now. Might be good to check though how much work implementing this without arviz would be because we want that at some point anyway

    # Also need to check how prior and prior predictive differ from each other. I guess `prior` contains both in here.
    raise Exception("Not finished yet")

    # For VI can also use pm.ADVI(model=model_with_data)
    # or pm.FullRankADVI(model=model_with_data)
    # these need pm.fit() also


def generate_prior_predictive(model_name, data, get_model_path):
    # This shouldn't really depend on data but not sure if it is possible to do without
    # Or well it might depend on part of the data but not full data
    model = get_model(model_name=model_name, data=data, get_model_path=get_model_path)

    with model:
        prior = pm.sample_prior_predictive()

    raise Exception("Not finished yet")


def get_model(*, model_name: str, data, get_model_path):
    framework = "pymc3"
    file_extension = ".py"

    model_code_path = get_model_path(
        framework=framework, file_extension=file_extension, model_name=model_name
    )

    model_module = importlib.import_module(model_code_path)

    # we assume the model function is named model
    model = model_module.model  # type: ignore

    model_with_data = model(data)
    return model_with_data
