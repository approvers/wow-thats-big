import unittest

from src.core.measure import measure
from src.core.type.argument import Argument


class CoreTest(unittest.TestCase):

    def test_measure(self):
        arg = Argument(
            directory="testcase",
            min_line=100,
            min_file_size_kb=512
        )
        big_files = measure(arg)
        self.assertEqual(len(big_files), 3)
        for file in big_files:
            self.assertTrue("not_big" not in file.path and file.path.endswith("big"))
