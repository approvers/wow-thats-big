import unittest

from src.measurer.measurers.cyclomatic_complexity import CyclomaticComplexityMeasurer
from src.type.argument import Argument


class CyclomaticComplexityMeasurerTest(unittest.TestCase):
    def test_not_big(self):
        measurer = CyclomaticComplexityMeasurer()
        result = measurer.measure(
            "testcase/not_big.py",
            Argument(
                directory="",
                min_file_size_kb=512,
                min_line=-1,
                min_cyclomatic_complexity=15
            )
        )
        self.assertIsNone(result)

    def test_big(self):
        measurer = CyclomaticComplexityMeasurer()
        result = measurer.measure(
            "testcase/musical_typer_main.py",
            Argument(
                directory="",
                min_file_size_kb=512,
                min_line=-1,
                min_cyclomatic_complexity=15
            )
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.caption, "循環的複雑度(平均)")
        self.assertEqual(float(result.info), 18)
