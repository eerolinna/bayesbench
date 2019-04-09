import yaml
import os
import bayesbench
import json
from bayesbench.compare_means import compare_means


posterior_names = ["8_schools_noncentered"]
methods = ["bayesbench_stan.nuts"]

runs = []

for posterior_name in posterior_names:
    for method in methods:
        runs.append(
            {
                "posterior_name": posterior_name,
                "inference_engine": method,
                "posterior_db_location": "/home/eero/default_posterior_db",
                "diagnostics": ["psis_khat"],
                "output_dir": "8schools_nuts_out",
                "method_specific_arguments": {},
            }
        )


outputs = bayesbench.run.run_many(runs)

print(len(outputs))
