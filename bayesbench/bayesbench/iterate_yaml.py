import yaml
import json

import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Print yaml file as one json object per line"
    )
    parser.add_argument("yaml_file", help="Yaml file to process")

    args = parser.parse_args()

    with open(args.yaml_file) as f:
        data = yaml.safe_load(f)
        if isinstance(data, list):
            for row in data:
                print(json.dumps(row))
        else:
            print(json.dumps(row))

