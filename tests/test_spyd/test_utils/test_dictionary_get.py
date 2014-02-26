import unittest
from spyd.utils.dictionary_get import dictget


class TestDictionaryGet(unittest.TestCase):
    def test_simple(self):
        self.assertEqual([1, 2, 3], dictget({'a': 1, 'b': 2, 'c': 3}, 'a', 'b', 'c'))
