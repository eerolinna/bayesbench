"""
See the test function for desciption of what this module does
"""

import glob
import json
from pathlib import Path


def get_file_name(path):
    """Given a full file path return just the filename without extension """
    p = Path(path)

    # with_suffix is needed in case the file has multiple extensions
    return p.with_suffix("").stem


def convert(posterior_info):
    """Converts old style posterior descriptions to new style. See the test
    function for description

    """
    data_name = get_file_name(posterior_info["data"])
    data_path = posterior_info["data"]

    model_name = get_file_name(posterior_info["model"]["stan"])
    model_code_dict = posterior_info["model"]

    data_info = {"data_file": data_path, "name": data_name}

    model_info = {"model_code": model_code_dict, "name": model_name}

    new_posterior_info = {**posterior_info, "data": data_name, "model": model_name}

    # Maybe would need to return file locations too? Where these should be saved
    return data_info, data_name, model_info, model_name, new_posterior_info


def test_convert():
    """Tests convert function"""
    # The convert function should transform
    original = {
        "data": "content/data/prideprejustice_chapter.json",
        "model": {"stan": "content/models/latent_dirichlet_allocation/lda.stan"},
        "gold_standard": None,
    }
    # Into
    # 1. new posterior description
    expected_new_posterior = {
        "data": "prideprejustice_chapter",
        "model": "lda",
        "gold_standard": None,
    }
    # 2. data description
    expected_data_info = {
        "name": "prideprejustice_chapter",
        "data_file": "content/data/prideprejustice_chapter.json",
    }
    # 3. model description
    expected_model_info = {
        "model_code": {"stan": "content/models/latent_dirichlet_allocation/lda.stan"},
        "name": "lda",
    }

    # Check that it actually does
    actual_data_info, _, actual_model_info, _, actual_new_posterior = convert(original)

    assert actual_data_info == expected_data_info
    assert actual_model_info == expected_model_info
    assert actual_new_posterior == expected_new_posterior


def get_new_files():
    base_dir = "/home/eero/posterior_database"

    posterior_dir = base_dir + "/posteriors"
    json_files = glob.glob(posterior_dir + "/*.json")

    new_files = {}

    for filepath in json_files:
        with open(filepath) as f:
            contents = json.load(f)
        data_info, data_name, model_info, model_name, new_posterior = convert(contents)

        data_info_path = base_dir + "/data/" + data_name + ".json"
        model_info_path = base_dir + "/models/" + model_name + ".json"

        posterior_name = get_file_name(filepath)
        new_posterior_path = base_dir + "/posteriors/" + posterior_name + ".json"

        new_files[new_posterior_path] = new_posterior
        new_files[data_info_path] = data_info
        new_files[model_info_path] = model_info
    return new_files


def write_new_files():
    new_files = get_new_files()

    for path in new_files:
        contents = new_files[path]
        with open(path, "w") as f:
            json.dump(contents, f, indent=2)


def test_multiple_extensions():
    """Tests that multiple extensions are removed"""
    path = "content/data/prideprejustice_chapter.json.zip"
    expected = "prideprejustice_chapter"
    actual = get_file_name(path)

    assert actual == expected
