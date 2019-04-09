import yaml
import os


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
yaml_contents = yaml.dump(runs)

output_dir = os.path.dirname(os.path.abspath(__file__))

output_path = os.path.join(output_dir, "config.yaml")

with open(output_path, "w") as f:
    f.write(yaml_contents)

print(yaml.dump(runs))
