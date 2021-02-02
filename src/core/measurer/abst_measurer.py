from abc import ABCMeta, abstractmethod
from typing import Union, TextIO, BinaryIO, Optional

from src.core.type.argument import Argument
from src.core.type.big_file_property import PartialBigFileProperty


class AbstractMeasurer(metaclass=ABCMeta):
    @abstractmethod
    def measure(self, full_path: str, argument: Argument) -> Optional[PartialBigFileProperty]:
        pass
