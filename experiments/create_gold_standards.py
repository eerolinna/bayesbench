# Import names of all posteriors (put it in a different file so other files can import it too)

# Check which have not been created already, print number of them

# run_many on the resulting jobs

# Print number of run jobs

from typing import Any, Mapping

import bayesbench

from .constants import output_dir, posterior_db_location
from .posteriors import posteriors


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
    for r in runs:
        # TODO check if same exact run has been completed already
        posterior_name = r["posterior_name"]
        if "lda" in posterior_name:
            continue
        print(f"Starting {posterior_name}")
        output = bayesbench.run.run(**r)
        print(f"""Finished {posterior_name}""")
    outputs.append(output)
    print(len(outputs))


if __name__ == "__main__":
    pass
    # main()
