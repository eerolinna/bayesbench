import yaml
import os
import bayesbench
import json
from bayesbench.compare_means import compare_means


posterior_names = ["8_schools_noncentered"]
methods = ["bayesbench_stan.meanfield_advi", "bayesbench_stan.fullrank_advi"]

runs = []

tolerances = [0.01]

n_iterations_list = [1000]

for posterior_name in posterior_names:
    for method in methods:
        for tolerance in tolerances:
            for n_iterations in n_iterations_list:
                runs.append(
                    {
                        "posterior_name": posterior_name,
                        "inference_engine": method,
                        "posterior_db_location": "/home/eero/default_posterior_db",
                        "diagnostics": ["psis_khat"],
                        "method_specific_arguments": {
                            "tol_rel_obj": tolerance,
                            "iter": n_iterations,
                        },
                        "output_dir": "out",
                    }
                )


outputs = bayesbench.run.run_many(runs)

print(len(outputs))

result = compare_means(outputs, posterior_db_location="/home/eero/default_posterior_db")

print(result)

output_dir = os.path.dirname(os.path.abspath(__file__))

output_path = os.path.join(output_dir, "result.json")


with open(output_path, "w") as f:
    json.dump(result, f, indent=2, cls=bayesbench.run.NumpyEncoder)
