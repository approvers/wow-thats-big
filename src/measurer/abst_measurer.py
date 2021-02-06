from abc import ABCMeta, abstractmethod
from typing import Optional, Dict

from src.type.big_file_property import PartialBigFileProperty


class AbstractMeasurer(metaclass=ABCMeta):
    @abstractmethod
    def get_required_argument(self) -> Dict[str, type]:
        pass

    @abstractmethod
    def measure(self, full_path: str, argument: Dict) -> Optional[PartialBigFileProperty]:
        pass
