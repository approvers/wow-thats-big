import unittest

from src.measurer.measurers.filesize import FileSizeMeasurer


class FileSizeMeasurerTest(unittest.TestCase):

    def test_no_big(self):
        measurer = FileSizeMeasurer()
        result = measurer.measure(
            "testcase/not_big",
            {FileSizeMeasurer.MIN_FILE_SIZE_KB: 512}
        )
        self.assertIsNone(result)

    def test_big(self):
        measurer = FileSizeMeasurer()
        result = measurer.measure(
            "testcase/big",
            {FileSizeMeasurer.MIN_FILE_SIZE_KB: 512}
        )
        self.assertIsNotNone(result)
        self.assertEqual(result.caption, "ファイルサイズ")
        self.assertEqual(result.info, "1.0 MB")
