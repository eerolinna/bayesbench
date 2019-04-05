import yaml
import os
import bayesbench
from IPython import embed

# For this simple example only run a small number of posteriors
posterior_names = """radon_partial_pooling2
radon_mn_partial_pooling2
""".split(
    "\n"
)

methods = ["bayesbench_stan.meanfield_vi", "bayesbench_stan.fullrank_vi"]

runs = []

tolerances = [0.1]

n_iterations_list = [1000]

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
                        "extra_fitting_arguments": {
                            "tolerance": tolerance,
                            "n_iterations": n_iterations,
                        },
                    }
                )


outputs = bayesbench.run.run_many(runs)

print(len(outputs))
embed()

# result = compare_means(outputs)

# print(result)
