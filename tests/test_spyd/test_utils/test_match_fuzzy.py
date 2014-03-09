import time
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

    def test_timing(self):
        start = time.clock()
        match_fuzzy('zzz', [chr(c) * 4 for c in xrange(ord('a'), ord('z'))] * 400)
        end = time.clock()
        execution_time = end - start
        times_per_second = 1.0 / execution_time
        print times_per_second
