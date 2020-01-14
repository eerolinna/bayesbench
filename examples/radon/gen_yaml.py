import os

import yaml

posterior_names = """radon_hiearchical_intercept2_hoprior
radon_mn_hiearchical_intercept2_hoprior
radon_partial_pooling2_hoprior
radon_mn_partial_pooling2_hoprior
radon_variable_intercept_slope2_hoprior
radon_mn_variable_intercept_slope2_hoprior
radon_hiearchical_intercept2
radon_mn_hiearchical_intercept2
radon_partial_pooling2
radon_mn_partial_pooling2
radon_variable_intercept_slope2
radon_mn_variable_intercept_slope2""".split(
    "\n"
)

methods = [
    "bayesbench_stan.meanfield_vi",
    "bayesbench_stan.fullrank_vi",
    "bayesbench_stan.laplace",
]

runs = []

tolerances = [0.1, 0.01, 0.001]

n_iterations_list = [100, 1000, 10000]

for posterior_name in posterior_names:
    for method in methods:
        for tolerance in tolerances:
            for n_iterations in n_iterations_list:
                runs.append(
                    {
                        "posterior_name": posterior_name,
                        "inference_engine": method,
                        "posterior_db_location": "db_loc",
                        "diagnostics": ["psis_khat"],
                        "method_specific_arguments": {
                            "tolerance": tolerance,
                            "n_iterations": n_iterations,
                        },
                    }
                )

yaml_contents = yaml.dump(runs)

output_dir = os.path.dirname(os.path.abspath(__file__))

output_path = os.path.join(output_dir, "config.yaml")

with open(output_path, "w") as f:
    f.write(yaml_contents)

print(yaml.dump(runs))
