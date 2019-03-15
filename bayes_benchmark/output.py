from dataclasses import dataclass, asdict
from typing import Any, List, Mapping, Tuple, Optional

Samples = Mapping[str, List[float]]


@dataclass
class Output:
    samples: Samples
    diagnostics: List[
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
    framework: str
    dataset_name: str
    extra_fitting_args: Mapping[
        str, Mapping[str, Any]
    ]  # method and model name as keys. Value type depends on method

    def to_dict(self):
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)


# Diagnostic output needs to be JSON serializable
# Extra_fitting_args also need to be JSON serializable

# seed
