"""
See the test function for desciption of what this module does
"""

import glob
import json
import os
import zipfile
from pathlib import Path

import yaml


def get_file_name(path):
    """Given a full file path return just the filename without extension """
    p = Path(path)

    # with_suffix is needed in case the file has multiple extensions
    return p.with_suffix("").stem


def convert(posterior_info, posterior_name):
    """Converts old style posterior descriptions to new style. See the test
    function for description

    """
    data_name = get_file_name(posterior_info["data"])
    data_path = posterior_info["data"]

    model_path = posterior_info["model"]["stan"]
    model_name = get_file_name(model_path)

    new_posterior_info = {
        "posterior_name": posterior_name,
        "dataset_name": data_name,
        "model_name": model_name,
    }

    # Maybe would need to return file locations too? Where these should be saved
    return data_path, model_path, new_posterior_info


def test_convert():
    """Tests convert function"""
    # The convert function should transform
    original = {
        "data": "content/data/prideprejustice_chapter.json",
        "model": {"stan": "content/models/latent_dirichlet_allocation/lda.stan"},
        "gold_standard": None,
    }
    posterior_name = "wow"
    # Into
    # 1. new posterior description
    expected_new_posterior = {
        "dataset_name": "prideprejustice_chapter",
        "model_name": "lda",
        "posterior_name": "wow",
    }

    # Check that it actually does
    _, _, actual_new_posterior = convert(original, posterior_name)

    assert actual_new_posterior == expected_new_posterior


def get_new_files():
    base_dir = "/home/eero/old_posterior_database"

    new_base_dir = "/home/eero/posterior_db"
    posterior_dir = base_dir + "/posteriors"
    json_files = glob.glob(posterior_dir + "/*.json")

    new_files = {}

    for filepath in json_files:
        with open(filepath) as f:
            contents = json.load(f)
        posterior_name = get_file_name(filepath)
        data_path, model_path, new_posterior = convert(contents, posterior_name)

        new_posterior_path = new_base_dir + "/posteriors/" + posterior_name + ".yaml"

        new_files[new_posterior_path] = yaml.dump([new_posterior])

        data_path = os.path.join(base_dir, data_path)
        model_path = os.path.join(base_dir, model_path)

        data_name = get_file_name(data_path)
        model_name = get_file_name(model_path)

        zfile = zipfile.ZipFile(data_path + ".zip")
        files = zfile.infolist()
        assert len(files) == 1
        with zfile.open(files[0], "r") as f:
            data_contents = f.read().decode("utf-8")

        with open(model_path) as f:
            model_contents = f.read()

        new_model_path = new_base_dir + "/models/stan/" + model_name + ".stan"
        new_data_path = new_base_dir + "/datasets/" + data_name + ".json"

        new_files[new_data_path] = data_contents
        new_files[new_model_path] = model_contents
    return new_files


def write_new_files():
    new_files = get_new_files()

    for path in new_files:
        contents = new_files[path]
        with open(path, "w") as f:
            f.write(contents)


def test_multiple_extensions():
    """Tests that multiple extensions are removed"""
    path = "content/data/prideprejustice_chapter.json.zip"
    expected = "prideprejustice_chapter"
    actual = get_file_name(path)

    assert actual == expected
