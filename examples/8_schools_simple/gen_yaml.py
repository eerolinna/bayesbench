import yaml
import os

model_names = ["8_schools_noncentered"]
dataset_names = ["8_schools"]
methods = ["bayesbench_stan.nuts", "bayesbench_stan.fullrank_vi"]

runs = []

for model_name in model_names:
    for dataset_name in dataset_names:
        for method in methods:
            runs.append(
                {
                    "model_name": model_name,
                    "dataset_name": dataset_name,
                    "inference_engine": method,
                    "posterior_db_location": "/home/eero/default_posterior_db",
                }
            )

yaml_contents = yaml.dump(runs)

output_dir = os.path.dirname(os.path.abspath(__file__))

output_path = os.path.join(output_dir, "config.yaml")

with open(output_path, "w") as f:
    f.write(yaml_contents)

print(yaml.dump(runs))
