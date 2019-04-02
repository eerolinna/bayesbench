from dataclasses import dataclass, asdict
from typing import Any, Sequence, Mapping, Tuple, Optional

Samples = Mapping[str, Sequence[float]]

# Maybe better to change output format into a zipfile that contains 1 file for metadata and 1 file for samples.
# Then we can quickly load the metadata file without having to load the sample file
# NOTE this assumes that I remember correctly that zipfiles can be unzipped in a streaming fashion where we can only unzip the metadata without having to zip the sample file. Need to check


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
    seed: Optional[int]

    model_name: str
    method_name: str
    lang: str
    inference_engine: str
    dataset_name: str
    extra_fitting_args: Mapping[str, Any]

    def to_dict(self):
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)


# Diagnostic output needs to be JSON serializable
# Extra_fitting_args also need to be JSON serializable

# seed
