import json
from collections import defaultdict
from typing import Any
from typing import List
from typing import Mapping
from typing import Sequence

import numpy as np

from bayesbench.output import Output
from posterior_db import PosteriorDatabase


def compare_means(outputs: Sequence[Output], posterior_db_location=None):
    result: Mapping[str, List[Any]] = defaultdict(list)
    for output in outputs:
        posterior_name = output.run_config.posterior_name

        means = get_mean(output)

        result[posterior_name].append(
            {
                "method": output.run_config.method_name,
                "inference_engine": output.run_config.inference_engine,
                "means": means,
                "gold_standard": False,
            }
        )

    if posterior_db_location:
        for posterior_name in result:
            posterior_db = PosteriorDatabase(posterior_db_location)

            gold_standard = posterior_db.load_gold_standard(posterior_name)

            if gold_standard:
                posterior_name = gold_standard.run_config.posterior_name
                means = get_mean(gold_standard)
                result[posterior_name].append(
                    {
                        "method": gold_standard.run_config.method_name,
                        "inference_engine": gold_standard.run_config.inference_engine,
                        "means": means,
                        "gold_standard": True,
                    }
                )
    return result


def get_mean(output: np.ndarray):
    result = {}
    for key in output.samples:
        values = output.samples[key]
        result[key] = values.mean(axis=0)

    return result
