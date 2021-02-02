import unittest

from src.measurer.measurers.filesize import FileSizeMeasurer
from src.type.argument import Argument


class FileSizeMeasurerTest(unittest.TestCase):

    def test_no_big(self):
        measurer = FileSizeMeasurer()
        result = measurer.measure("testcase/not_big", Argument(directory="", min_file_size_kb=512, min_line=-1))
        self.assertIsNone(result)

    def test_big(self):
        measurer = FileSizeMeasurer()
        result = measurer.measure("testcase/big", Argument(directory="", min_file_size_kb=512, min_line=-1))
        self.assertIsNotNone(result)
        self.assertEqual(result.caption, "ファイルサイズ")
        self.assertEqual(result.info, "1.0 MB")
