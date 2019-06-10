"""TODO docstring"""
import glob
import json
import os
from os.path import join
from typing import Optional

import yaml

from .output import Output

class PosteriorDatabase:
    def __init__(self, location):
        self.location = location
        self.posteriors = get_posteriors(location)

    def get_model_path(self, *, model_name, framework, file_extension) -> Optional[str]:
        model_dir = join(self.location, "models")
        paths = glob.glob(
            model_dir + f"/**/{model_name}{file_extension}", recursive=True
        )
        n_found = len(paths)
        assert n_found <= 1, f"There were multiple models named {model_name}"
        if n_found == 0:
            return None
        else:
            return paths[0]

    def get_model_name(self, posterior_name):
        model_name = self.posteriors[posterior_name]["model_name"]
        return model_name

    def get_dataset_path(self, *, posterior_name):
        dataset_name = self.posteriors[posterior_name]["dataset_name"]
        dataset_dir = join(self.location, "datasets")
        paths = glob.glob(dataset_dir + f"/**/{dataset_name}.json", recursive=True)
        assert len(paths) == 1, f"There were multiple datasets named {dataset_name}"
        return paths[0]

    def print_posteriors(self):
        posteriors_dir = join(self.location, "posteriors")
        paths = glob.glob(posteriors_dir + "/**/*.yaml", recursive=True)
        for path in paths:
            with open(path) as f:
                posteriors = yaml.safe_load(f)
                for posterior in posteriors:
                    print(posterior["posterior_name"])

    def load_gold_standard(self, posterior_name: str) -> Output:
        gold_standards_dir = join(self.location, "gold_standards")
        paths = glob.glob(
            gold_standards_dir + f"/**/{posterior_name}.json", recursive=True
        )
        num_found = len(paths)
        assert num_found in [
            0,
            1,
        ], f"There were {num_found} gold standards for the posterior {posterior_name}"

        if num_found == 0:
            return None
        gold_standard_path = paths[0]
        with open(gold_standard_path) as f:
            output_dict = json.load(f)

        output = Output.from_dict(output_dict)
        return output


def get_posteriors(location):
    posteriors_dir = join(location, "posteriors")
    paths = glob.glob(posteriors_dir + "/**/*.yaml", recursive=True)
    all_posteriors = {}
    for path in paths:
        with open(path) as f:
            posteriors = yaml.safe_load(f)
            for posterior in posteriors:
                posterior_name = posterior["posterior_name"]
                all_posteriors[posterior_name] = posterior

    return all_posteriors
