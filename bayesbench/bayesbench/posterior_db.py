from os.path import join
import yaml
import glob


class PosteriorDatabase:
    def __init__(self, location):
        self.location = location
        self.posteriors = get_posteriors(location)

    def get_model_path(self, *, model_name, framework, file_extension):
        model_dir = join(self.location, "models")
        paths = glob.glob(
            model_dir + f"/**/{model_name}{file_extension}", recursive=True
        )
        assert len(paths) == 1, f"There were multiple models named {model_name}"
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
