from abc import ABCMeta, abstractmethod
from typing import Optional

from src.type.argument import Argument
from src.type.big_file_property import PartialBigFileProperty


class AbstractMeasurer(metaclass=ABCMeta):
    @abstractmethod
    def measure(self, full_path: str, argument: Argument) -> Optional[PartialBigFileProperty]:
        pass
