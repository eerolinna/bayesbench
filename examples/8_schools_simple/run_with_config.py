# Run by loading a config file
import json
import os

import yaml

import bayesbench
from bayesbench.compare_means import compare_means

current_dir = os.path.dirname(os.path.abspath(__file__))

path = os.path.join(current_dir, "config.yaml")

with open(path) as f:
    runs = yaml.safe_load(f)

outputs = bayesbench.run.run_many(runs)

result = compare_means(outputs)

print(result)


output_dir = os.path.dirname(os.path.abspath(__file__))

output_path = os.path.join(output_dir, "result.json")


with open(output_path, "w") as f:
    json.dump(result, f, indent=2)
