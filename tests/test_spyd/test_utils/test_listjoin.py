import unittest
from spyd.utils.listjoin import listjoin


class TestListJoin(unittest.TestCase):
    def test_no_items(self):
        self.assertEqual(listjoin([]), "")

    def test_one_item(self):
        self.assertEqual(listjoin(['A']), "A")

    def test_two_items(self):
        self.assertEqual(listjoin(['A', 'B']), "A, and B")

    def test_three_items(self):
        self.assertEqual(listjoin(['A', 'B', 'C']), "A, B, and C")
