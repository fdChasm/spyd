import unittest
from spyd.utils.filtertext import filtertext


class TestFilterText(unittest.TestCase):
    def test_truncates(self):
        self.assertEqual(filtertext('abc', True, 2), 'ab')

    def test_removes_whitespace(self):
        self.assertEqual(filtertext('a b c', False, 30), 'abc')

    def test_removes_cube_format_chars(self):
        self.assertEqual(filtertext('\fs\f3a \f2b c\fr', True, 30), 'a b c')
