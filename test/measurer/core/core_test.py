import unittest

from src.measure import measure


class CoreTest(unittest.TestCase):

    def test_measure(self):
        big_files = measure()
        self.assertEqual(len(big_files), 4)
        for file in big_files:
            self.assertTrue("not_big" not in file.path and "big" in file.path)
