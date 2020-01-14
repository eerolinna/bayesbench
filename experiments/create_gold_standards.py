# Import names of all posteriors (put it in a different file so other files can import it too)
# Check which have not been created already, print number of them
# run_many on the resulting jobs
# Print number of run jobs
import json
import os
from typing import Any
from typing import Mapping

import bayesbench
from .constants import bayesbench_dir
from .constants import output_dir
from .constants import posterior_db_location
from .posteriors import posteriors

posteriors_ran_path = os.path.join(bayesbench_dir, "ran.json")


def create_run(posterior_name: str) -> Mapping[str, Any]:
    run = {
        "posterior_name": posterior_name,
        "posterior_db_location": posterior_db_location,
        "output_dir": output_dir,
        "inference_engine": "bayesbench_stan.nuts",
        "diagnostics": [],
        "method_specific_arguments": {},
    }
    return run


def main():
    runs = map(create_run, posteriors)
    outputs = []
    with open(posteriors_ran_path) as f:
        existing_posteriors = json.load(f)
    for r in runs:
        # TODO check if same exact run has been completed already
        posterior_name = r["posterior_name"]
        if posterior_name in existing_posteriors:
            continue
        if "lda" in posterior_name:
            continue

        if "radon" in posterior_name:
            continue
        with open(posteriors_ran_path, "w") as f:
            existing_posteriors = existing_posteriors + [posterior_name]
            json.dump(existing_posteriors, f)
        print(f"Starting {posterior_name}")
        output = bayesbench.run.run(**r)
        print(f"""Finished {posterior_name}""")
    outputs.append(output)
    print(len(outputs))


if __name__ == "__main__":
    pass
    # main()
