import bayesbench

posterior_names = ["8_schools|noncentered"]
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
                        "diagnostics": [],
                        "posterior_db_location": "/home/eero/posterior_db",
                        "output_dir": "temp_out",
                        "method_specific_arguments": {
                            "tol_rel_obj": tolerance,
                            "iter": n_iterations,
                        },
                    }
                )


outputs = bayesbench.run.run_many(runs)

# result = bayesbench.benchmark(outputs)

# print(result)
