import unittest

from src.measure import measure
from src.type.argument import Argument


class CoreTest(unittest.TestCase):

    def test_measure(self):
        arg = Argument(
            directory="testcase",
            min_line=100,
            min_file_size_kb=512,
            min_cyclomatic_complexity=15
        )
        big_files = measure(arg)
        self.assertEqual(len(big_files), 4)
        for file in big_files:
            self.assertTrue("not_big" not in file.path and file.path.endswith("big"))
