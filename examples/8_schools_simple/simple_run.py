import bayesbench


def main():
    posterior_names = ["8_schools-8_schools_noncentered"]
    methods = ["fullrank", "meanfield"]

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
                            "inference_engine": "bayesbench_stan.vb",
                            "diagnostics": [],
                            "posterior_db_location": "/home/eero/posterior_database",
                            "output_dir": "temp_out",
                            "method_specific_arguments": {
                                "tol_rel_obj": tolerance,
                                "iter": n_iterations,
                                "algorithm": method,
                            },
                        }
                    )


    outputs = bayesbench.run.run_many(runs, parallel=False)

    # result = bayesbench.benchmark(outputs)

    # print(result)
