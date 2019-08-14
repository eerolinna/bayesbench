import copy
import glob
import json


def rewrite_path(base_dir, replace_function):
    json_files = glob.glob(f"{base_dir}/*.json")

    new_files = {}
    for path in json_files:
        with open(path) as f:
            contents = json.load(f)

        new_contents = replace_function(contents)

        new_files[path] = new_contents

    import ipdb

    ipdb.set_trace()

    for path in new_files:
        with open(path, "w") as f:
            json.dump(new_files[path], f, indent=2)


def replace_model(contents):
    old_code_path = contents["model_code"]["stan"]
    new_code_path = old_code_path.replace("content/models/", "content/models/stan/")

    new_contents = copy.deepcopy(contents)
    new_contents["model_code"]["stan"] = new_code_path

    return new_contents


def replace_data(contents):
    old_dataset_path = contents["data_file"]
    new_dataset_path = old_dataset_path.replace(
        "content/datasets/", "content/datasets/data/"
    )

    new_contents = copy.deepcopy(contents)
    new_contents["data_file"] = new_dataset_path

    return new_contents


def main():
    base_path = "/home/eero/posterior_database/"
    # rewrite_path(base_path + "content/datasets/info", replace_data)
    rewrite_path(base_path + "content/models/info", replace_model)
