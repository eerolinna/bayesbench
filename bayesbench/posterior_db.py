from dataclasses import dataclass
from os.path import join


@dataclass
class PosteriorDatabase:
    location: str

    def get_model_path(self, *, model_name, framework, file_extension):
        return join(
            self.location, join("models", join(framework, model_name + file_extension))
        )

    def get_dataset_path(self, dataset_name):
        return join(self.location, join("datasets", dataset_name + ".json"))
