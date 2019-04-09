from dataclasses import dataclass, asdict
from typing import Any, Sequence, Mapping, Tuple, Optional
import numpy as np

Samples = Mapping[str, Sequence[float]]

# Maybe better to change output format into a zipfile that contains 1 file for metadata and 1 file for samples.
# Then we can quickly load the metadata file without having to load the sample file


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
        output = cls(**dct)

        new_samples = {k: np.array(v) for (k, v) in output.samples.items()}
        output.samples = new_samples
        return output


# Diagnostic output needs to be JSON serializable
# Extra_fitting_args also need to be JSON serializable
