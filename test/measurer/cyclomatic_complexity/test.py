import unittest

from src.measurer.measurers.filesize import FileSizeMeasurer
from src.type.argument import Argument


class FileSizeMeasurerTest(unittest.TestCase):

    def test_not_big(self):
        measurer = FileSizeMeasurer()
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
        measurer = FileSizeMeasurer()
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
