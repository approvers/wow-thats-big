import unittest

from src.measurer.measurers.filesize import FileSizeMeasurer
from src.type.argument import Argument


class FileSizeMeasurerTest(unittest.TestCase):

    def test_big(self):
        measurer = FileSizeMeasurer()
        result = measurer.measure("testcase", Argument(directory="", min_file_size_kb=512, min_line=-1))
        self.assertIsNotNone(result)
        self.assertEqual(result.caption, "循環的複雑度")
        self.assertEqual(result.info, "1.0 MB")
