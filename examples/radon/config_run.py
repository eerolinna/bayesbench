# Run by loading a config file
import yaml
import os


current_dir = os.path.dirname(os.path.abspath(__file__))

path = os.path.join(current_dir, "config.yaml")

with open(path) as f:
    runs = yaml.safe_load(f)

outputs = bayesbench.run_many(runs)

result = compare_means(outputs)

print(result)
