import functools
import glob
import json
from collections import defaultdict

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, mood, ttest_ind
from universal_divergence import estimate

from bayesbench.output import Output

from .compare import compare
from .constants import output_dir

wanted_posterior = "8_schools|noncentered"


def get_8_schools():
    gold_standards = {}
    method_outputs = defaultdict(dict)
    files = glob.glob(output_dir + "/*.json")
    for filepath in files:
        output = get_output(filepath)
        run_config = output.run_config
        posterior_name = run_config.posterior_name
        if posterior_name == wanted_posterior:
            if run_config.method_name == "nuts":
                gold_standards[posterior_name] = output
            else:
                method_outputs[posterior_name][run_config.method_name] = output
        # check if posterior is 8 schools

    if not gold_standards.get(wanted_posterior):
        raise ValueError("Directory is missing gold standard")
    return method_outputs, gold_standards


def get_output(filepath):
    with open(filepath) as f:
        dct = json.load(f)
    output = Output.from_dict(dct)
    return output


def scipy_wrapper(x, y, f):
    def format_s_p(s, p):
        if p < threshold:
            p_str = f"p < {threshold}"
        else:
            p_str = f"p = {p:.4f}"
        return f"{p_str} ({s:.2f})"

    s, p = f(x, y)
    threshold = 0.005
    if isinstance(s, float):
        return format_s_p(s, p)
    if isinstance(s, np.ndarray):
        result = []
        for (statistic, pvalue) in zip(s, p):
            r = format_s_p(statistic, pvalue)
            result.append(r)
        return result
    return (s, p)


def try_stuff():
    outputs, gold_standards = get_8_schools()
    mean_wrapper = functools.partial(
        scipy_wrapper, f=functools.partial(ttest_ind, equal_var=False)
    )
    ks_wrapper = functools.partial(scipy_wrapper, f=ks_2samp)
    moods_wrapper = functools.partial(scipy_wrapper, f=mood)
    comparisons = {"mean": mean_wrapper, "mood": moods_wrapper}
    r = compare(outputs, gold_standards, comparisons)
    return r


def to_dataframe():
    r = try_stuff()
    frames = {}
    for posterior_name, posterior_comparisons in r.items():
        temp_df = {}
        for comparison_name, comparison_values in posterior_comparisons.items():
            temp_df[comparison_name] = pd.DataFrame.from_dict(comparison_values)
        frames[posterior_name] = pd.concat(temp_df, axis=1)

    return frames


def frames_to_html():
    frames = to_dataframe()

    html = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Experiments</title>
</head>
<body>
    """
    for posterior_name, frame in frames.items():
        html += f"""<h3>{posterior_name}</h3>"""
        html += frame.to_html()

    html += """
    </body>
    </html>
    """

    with open("test.html", "w") as f:
        f.write(html)
