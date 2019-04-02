import importlib
import pymc3 as pm
import json

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
