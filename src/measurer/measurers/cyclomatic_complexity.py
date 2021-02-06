from typing import Optional, List

import lizard

from src.measurer.abst_measurer import AbstractMeasurer
from src.type.argument import Argument
from src.type.big_file_property import PartialBigFileProperty


class CyclomaticComplexityMeasurer(AbstractMeasurer):
    def measure(self, full_path: str, argument: Argument) -> Optional[PartialBigFileProperty]:
        analyze_result: lizard.FileInformation = lizard.analyze_file(full_path)
        function_list: List[lizard.FunctionInfo] = analyze_result.function_list

        if len(function_list) == 0:
            return None

        avg_cyclocplx = sum([x.cyclomatic_complexity for x in function_list]) / len(function_list)

        if avg_cyclocplx > argument.min_cyclomatic_complexity:
            return PartialBigFileProperty("循環的複雑度 (平均)", str(avg_cyclocplx))
        return None
