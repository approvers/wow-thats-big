import unittest

from src.measurer.measurers.cyclomatic_complexity import CyclomaticComplexityMeasurer


class CyclomaticComplexityMeasurerTest(unittest.TestCase):
    def test_not_big(self):
        measurer = CyclomaticComplexityMeasurer()
        result = measurer.measure(
            "testcase/not_big.py",
            {CyclomaticComplexityMeasurer.MIN_COMPLEXITY: 15.0}
        )
        self.assertIsNone(result)

    def test_big(self):
        measurer = CyclomaticComplexityMeasurer()
        result = measurer.measure(
            "testcase/musical_typer_main.py",
            {CyclomaticComplexityMeasurer.MIN_COMPLEXITY: 15.0}
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.caption, "循環的複雑度 (平均)")
        self.assertEqual(float(result.info), 18)
