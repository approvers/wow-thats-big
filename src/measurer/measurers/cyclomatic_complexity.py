from typing import Optional, List

import lizard

from src.measurer.abst_measurer import AbstractMeasurer
from src.type.argument import Argument
from src.type.big_file_property import PartialBigFileProperty


class CyclomaticComplexityMeasurer(AbstractMeasurer):
    def measure(self, full_path: str, argument: Argument) -> Optional[PartialBigFileProperty]:
        analyze_result = lizard.analyze_files(full_path)
        function_list: List[lizard.FunctionInfo] = analyze_result["function_list"]
        return sum([x
