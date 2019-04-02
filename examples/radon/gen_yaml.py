import yaml
import os

model_names = """radon_hiearchical_intercept2_hoprior
radon_partial_pooling2_hoprior
radon_variable_intercept_slope2_hoprior
radon_hiearchical_intercept2
radon_partial_pooling2
radon_variable_intercept_slope2""".split(
    "\n"
)

for m in model_names:
    print(m)
dataset_names = ["radon", "radon_mn"]
methods = [
    "bayesbench_stan.meanfield_vi",
    "bayesbench_stan.fullrank_vi",
    "bayesbench_stan.laplace",
]

runs = []

tolerances = [0.1, 0.01, 0.001]

n_iterations_list = [100, 1000, 10000]

for model_name in model_names:
    for dataset_name in dataset_names:
        for method in methods:
            for tolerance in tolerances:
                for n_iterations in n_iterations_list:
                    runs.append(
                        {
                            "model_name": model_name,
                            "dataset_name": dataset_name,
                            "inference_engine": method,
                            "posterior_db_location": "db_loc",
                            "diagnostics": ["psis_khat"],
                            "extra_fitting_arguments": {
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
