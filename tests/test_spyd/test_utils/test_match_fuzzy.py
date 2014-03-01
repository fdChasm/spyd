import unittest

from spyd.utils.match_fuzzy import match_fuzzy


class TestMatchFuzzy(unittest.TestCase):
    def test_case_sensitive(self):
        self.assertEqual(match_fuzzy('foo', ['fool', 'food', 'floor'], allow_ci_check=False), 'fool')

    def test_case_insensitive(self):
        self.assertEqual(match_fuzzy('foo', ['FOOL', 'FOOD', 'FLOOR'], allow_ci_check=True), 'FOOL')

    def test_no_match_case_sensitive(self):
        self.assertEqual(match_fuzzy('zzz', ['FOOL', 'FOOD', 'FLOOR'], allow_ci_check=False), None)

    def test_no_match_case_insensitive(self):
        self.assertEqual(match_fuzzy('zzz', ['FOOL', 'FOOD', 'FLOOR'], allow_ci_check=True), None)
