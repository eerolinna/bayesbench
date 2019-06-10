from dataclasses import dataclass, asdict, fields
from typing import Any, Sequence, Mapping, Tuple, Optional
import numpy as np
from zipfile import ZipFile
import json

Samples = Mapping[str, Sequence[float]]

# Maybe better to change output format into a zipfile that contains 1 file for metadata and 1 file for samples.
# Then we can quickly load the metadata file without having to load the sample file

"""
@dataclass
class Samples:
    posterior: Mapping[str, Sequence[float]]
    posterior_predictive: Mapping[str, Sequence[float]]
    log_likelihood: Sequence[float]
"""


@dataclass
class RunConfig:
    posterior_name: str
    inference_engine: str
    method_name: str
    method_specific_arguments: Mapping[str, Any]
    seed: Optional[int]
    lang: str

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)

    @classmethod
    def from_zip(cls, filename: str):
        with ZipFile(filename) as zip:
            with zip.open("config.json") as config_f:
                run_config_dict = json.load(config_f)

        return cls.from_dict(run_config_dict)


@dataclass
class Output:
    # TODO: Right now `samples` includes not just posterior but also prior predictive and posterior predictive samples too.
    # This is the Stan approach. However PyMC and Pyro have a bit different approach that might be better.
    samples: Samples
    diagnostics: Sequence[
        Tuple[str, Any]
    ]  # list of diagnostic names and outputs, output type depends on name

    # these time things should be optional and have default value None
    creation_time: Optional[float]  # unix time
    execution_time: Optional[float]
    # Seed is also optional

    run_config: RunConfig

    def to_dict(self):
        # maybe not needed?
        # self.run_details = asdict(self.run_details)
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, dct):
        dct["run_config"] = RunConfig.from_dict(dct["run_config"])

        """
        Equivalent to
        output = Output(
            run_config=dct["run_config"],
            samples=dct["samples"],
            creation_time=dct["creation_time"],
            ...
        )
        """
        output = cls(**dct)

        new_samples = {k: np.array(v) for (k, v) in output.samples.items()}
        output.samples = new_samples
        return output

    def to_zip(self, filename: str):
        with ZipFile(filename, "w") as zip:
            config = json.dumps(self.run_config)
            zip.writestr("config.json", config)

            field_names = [
                field.name for field in fields(self) if field.name is not "run_config"
            ]
            # This is equivalent to
            # {
            #   "samples": self.samples,
            #   "creation_time": self.creation_time,
            #   ...
            # }
            rest = {field_name: getattr(self, field_name) for field_name in field_names}

            zip.writestr("inference.json", json.dumps(rest))

    @classmethod
    def from_zip(cls, filename: str):
        with ZipFile(filename) as zip:
            with zip.open("config.json") as config_f:
                run_config_dict = json.load(config_f)

            with zip.open("inference.json") as f:
                dct = json.load(f)

        dct["run_config"] = run_config_dict
        return cls.from_dict(dct)


# Diagnostic output needs to be JSON serializable
# Method specific arguments also need to be JSON serializable
