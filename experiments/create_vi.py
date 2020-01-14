import functools
from typing import Any
from typing import Mapping

import bayesbench
from .constants import output_dir
from .constants import posterior_db_location
from .posteriors import posteriors
from .try_8schools import get_gold_standard_names


def create_run(
    posterior_name: str, method_name: str, method_specific_arguments
) -> Mapping[str, Any]:
    run = {
        "posterior_name": posterior_name,
        "posterior_db_location": posterior_db_location,
        "output_dir": output_dir,
        "inference_engine": f"bayesbench_stan.{method_name}",
        "diagnostics": [],
        "method_specific_arguments": method_specific_arguments,
    }
    return run


def main():
    wanted_posteriors = get_gold_standard_names()
    runs = []
    for method_name in ["fullrank_advi", "meanfield_advi"]:
        for tol in [0.01, 0.001]:
            args = {"tol_rel_obj": tol}
            new_runs = map(
                functools.partial(
                    create_run, method_name=method_name, method_specific_arguments=args
                ),
                wanted_posteriors,
            )
            runs += list(new_runs)
    outputs = []
    for r in runs:
        # TODO check if same exact run has been completed already
        posterior_name = r["posterior_name"]
        if "lda" in posterior_name:
            continue
        print(f"Starting {posterior_name}")
        try:
            output = bayesbench.run.run(**r)
        except RuntimeError:
            print(f"Error with {posterior_name}")
            continue
        print(f"""Finished {posterior_name}""")
    outputs.append(output)
    print(len(outputs))


if __name__ == "__main__":
    main()
