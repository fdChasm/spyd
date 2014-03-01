import unittest

from spyd.utils.truncate import truncate


class TestTruncate(unittest.TestCase):
    def test_shorter(self):
        self.assertEqual(truncate("abc", 5), "abc")

    def test_longer(self):
        self.assertEqual(truncate("abc", 1), "a")
