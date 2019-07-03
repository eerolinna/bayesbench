import functools
import glob
import json
from collections import OrderedDict, defaultdict

import numpy as np
import pandas as pd
from scipy.stats import kruskal, ks_2samp, levene, mood, ranksums, ttest_ind

from bayesbench.output import Output

from .compare import compare
from .constants import output_dir

wanted_posterior = "8_schools|noncentered"


def diagnostics_good(output):
    name = output.run_config.posterior_name

    return all(output.diagnostics.values())


def get_gold_standard_names():
    gold_standards = {}
    files = glob.glob(output_dir + "/*.json")
    for filepath in files:
        output = get_output(filepath)
        run_config = output.run_config
        posterior_name = run_config.posterior_name
        if run_config.method_name == "nuts":
            if diagnostics_good(output):
                gold_standards[posterior_name] = output
        # check if posterior is 8 schools

    return gold_standards.keys()


def get_all():
    gold_standards = {}
    method_outputs = defaultdict(dict)
    files = glob.glob(output_dir + "/*.json")
    for filepath in files:
        output = get_output(filepath)
        run_config = output.run_config
        posterior_name = run_config.posterior_name
        if run_config.method_name == "nuts":
            if diagnostics_good(output):
                gold_standards[posterior_name] = output
        else:
            tolerance = run_config.method_specific_arguments.get("tol_rel_obj", 0.01)
            method_name = f"{run_config.method_name} tol={tolerance}"
            method_outputs[posterior_name][method_name] = output
        # check if posterior is 8 schools
    gold_standard_names = gold_standards.keys()
    final_method_outputs = {}
    for name in gold_standard_names:
        final_method_outputs[name] = method_outputs[name]
    return final_method_outputs, gold_standards


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
            p_str = f"p = {p:.2f}"
        return f"{p_str} ({s:.2f})"

    s, p = f(x, y)
    threshold = 0.01
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
    outputs, gold_standards = get_all()
    mean_wrapper = functools.partial(
        scipy_wrapper, f=functools.partial(ttest_ind, equal_var=False)
    )
    ks_wrapper = functools.partial(scipy_wrapper, f=ks_2samp)
    moods_wrapper = functools.partial(scipy_wrapper, f=mood)
    kruskal_wrapper = functools.partial(scipy_wrapper, f=kruskal)
    ranksums_wrapper = functools.partial(scipy_wrapper, f=ranksums)
    levene_wrapper = functools.partial(scipy_wrapper, f=levene)
    comparisons = {"Mean (T-test)": mean_wrapper, "Mood's median test": moods_wrapper}
    r = compare(outputs, gold_standards, comparisons)
    return r


def to_dataframe():
    r = try_stuff()
    frames = {}
    for posterior_name, posterior_comparisons in r.items():
        temp_df = {}
        for comparison_name, comparison_values in posterior_comparisons.items():
            sorted_items = sorted(comparison_values.items(), key=lambda x: x[0])
            new_comparison_values = OrderedDict(sorted_items)
            temp_df[comparison_name] = pd.DataFrame.from_dict(new_comparison_values)
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
  <link rel="stylesheet" href="https://cdn.jupyter.org/notebook/5.1.0/style/style.min.css">
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
