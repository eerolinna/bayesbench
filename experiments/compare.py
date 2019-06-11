from collections import defaultdict


def recursive_defaultdict():
    return defaultdict(recursive_defaultdict)


def defaultdict_to_dict(d):
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = defaultdict_to_dict(v)
    return dict(d)


def compare(posterior_outputs, gold_standards, comparisons):
    result = recursive_defaultdict()

    for posterior_name in posterior_outputs:
        gold_standard = gold_standards[posterior_name]
        for (method_name, output) in posterior_outputs[posterior_name].items():
            samples, gold_samples, parameter_names = make_matrixes(
                output, gold_standard
            )

            for (comparison_name, comparison_function) in comparisons.items():
                for parameter_name in parameter_names:
                    r = comparison_function(
                        samples[parameter_name], gold_samples[parameter_name]
                    )
                    if isinstance(r, list):
                        for i, val in enumerate(r):
                            new_parameter_name = f"{parameter_name}[{i}]"
                            result[posterior_name][comparison_name][method_name][
                                new_parameter_name
                            ] = val
                    else:
                        result[posterior_name][comparison_name][method_name][
                            parameter_name
                        ] = r

    return defaultdict_to_dict(result)


# Quantiles might not fit in this comparison framework. It would probably work
# easier with obtaining result for each parameter. However if some parameters
# are lists then it would produce a list of tests for that parameter


def make_matrixes(output, gold_standard):
    # Take union of parameter names
    # Make matrix so that the column order is the same
    samples = output.samples
    gold_samples = gold_standard.samples

    raw_param_names = set(samples.keys()) & set(gold_samples.keys())
    parameter_names = [name for name in raw_param_names if "__" not in name]

    return samples, gold_samples, parameter_names
