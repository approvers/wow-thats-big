import dataclasses
from typing import Union, Optional


@dataclasses.dataclass
class ArgumentDefinition:
    name: str
    arg_type: type
    default_value: Optional[Union[int, float, str]]

    def __post_init__(self):
        if self.arg_type not in [int, float, str]:
            raise InvalidDefinitionError(
                self.name,
                f"arg_type ({self.arg_type}) is not supported; 'int', 'float', and 'str' is supported"
            )

        if self.default_value is not None and type(self.default_value) != self.arg_type:
            raise InvalidDefinitionError(
                self.name,
                f"The type of default value and the arg_type does not match"
                f"({type(self.default_value)} != {self.arg_type})"
            )


class InvalidDefinitionError(Exception):
    def __init__(self, arg_name: str, reason: str):
        super().__init__(f"Invalid argument definition for '{arg_name}': {reason}")
