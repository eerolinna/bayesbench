from dataclasses import dataclass, asdict
from typing import Any, List, Mapping, Tuple, Sequence


ModelName = str
DiagnosticName = str
MethodName = str
DataName = str
FilePath = str
FrameworkName = str


@dataclass
class KnowledgeBase:
    model_attributes: Mapping[ModelName, Mapping[str, Any]]
    model_codes: Mapping[ModelName, Mapping[FrameworkName, FilePath]]
    diagnostic_attributes: Mapping[DiagnosticName, Mapping[str, Any]]
    method_attributes: Mapping[MethodName, Mapping[str, Any]]
    data_attributes: Mapping[DataName, Mapping[str, Any]]
    compatible: Sequence[Tuple[MethodName, DiagnosticName]]
    model_use_data: Mapping[ModelName, List[DataName]]

    # Can contain for example
    # - number of parameters
    # - is the parameterization for model X recommended for dataset Y?
    model_data_attributes: Sequence[Tuple[ModelName, DataName, Any]]

    skip: Sequence[Tuple[MethodName, ModelName]]

    relations: Any

    # verified output: don't load outputs automatically but rather store filename to load

    def to_dict(self):
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, dct):
        return cls(**dct)


# Diagnostic output needs to be JSON serializable
# Extra_fitting_args also need to be JSON serializable
