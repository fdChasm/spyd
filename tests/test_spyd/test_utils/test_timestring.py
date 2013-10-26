import unittest
from spyd.utils.timestring import parseTimeString, simplify

class TestSimplify(unittest.TestCase):
    def test_absolute_hours(self):
        self.assertEqual(simplify(['2h']), ['=2h'])

class TestParseTimeString(unittest.TestCase):
    def test_absolute_hours(self):
        self.assertEqual(parseTimeString('2h'), ('=', 7200))

    def test_absolute_minutes(self):
        self.assertEqual(parseTimeString('2m'), ('=', 120))

    def test_absolute_seconds(self):
        self.assertEqual(parseTimeString('55s'), ('=', 55))

    def test_positive_hours(self):
        self.assertEqual(parseTimeString('+2h'), ('+', 7200))

    def test_positive_minutes(self):
        self.assertEqual(parseTimeString('+2m'), ('+', 120))

    def test_positive_seconds(self):
        self.assertEqual(parseTimeString('+33s'), ('+', 33))

    def test_negative_hours(self):
        self.assertEqual(parseTimeString('-4h'), ('-', 14400))

    def test_negative_minutes(self):
        self.assertEqual(parseTimeString('-12m'), ('-', 720))

    def test_negative_seconds(self):
        self.assertEqual(parseTimeString('-13s'), ('-', 13))

    def test_stacked_signs(self):
        self.assertEqual(parseTimeString('--13s'), ('+', 13))
        self.assertEqual(parseTimeString('---13s'), ('-', 13))
        self.assertEqual(parseTimeString('=+=13s'), ('=', 13))
        self.assertEqual(parseTimeString('-+13s'), ('-', 13))
        self.assertEqual(parseTimeString('-++13s'), ('-', 13))

    def test_white_space(self):
        self.assertEqual(parseTimeString('-    13s'), ('-', 13))
        self.assertEqual(parseTimeString('-   -13s'), ('+', 13))
        self.assertEqual(parseTimeString('  =13  s'), ('=', 13))

    def test_combinations(self):
        self.assertEqual(parseTimeString('+2m5h'), ('=', 18120))
        self.assertEqual(parseTimeString('+5h-3s'), ('+', 17997))
        self.assertEqual(parseTimeString('34m32s'), ('=', 34 * 60 + 32))
        self.assertEqual(parseTimeString('034m032s'), ('=', 34 * 60 + 32))
        self.assertEqual(parseTimeString('034m-032s'), ('=', 34 * 60 - 32))

    def test_no_units(self):
        self.assertEqual(parseTimeString('34'), ('=', 34))
        self.assertEqual(parseTimeString('+34'), ('+', 34))
        self.assertEqual(parseTimeString('-34'), ('-', 34))

    def test_no_sign(self):
        self.assertEqual(parseTimeString('3h'), ('=', 10800))
        self.assertEqual(parseTimeString('3m'), ('=', 180))
        self.assertEqual(parseTimeString('3s'), ('=', 3))

    def test_just_unit(self):
        self.assertEqual(parseTimeString('h'), ('=', 3600))
        self.assertEqual(parseTimeString('m'), ('=', 60))
        self.assertEqual(parseTimeString('s'), ('=', 1))

    def test_signed_unit(self):
        self.assertEqual(parseTimeString('+h'), ('+', 3600))
        self.assertEqual(parseTimeString('+m'), ('+', 60))
        self.assertEqual(parseTimeString('+s'), ('+', 1))
        self.assertEqual(parseTimeString('-h'), ('-', 3600))
        self.assertEqual(parseTimeString('-m'), ('-', 60))
        self.assertEqual(parseTimeString('-s'), ('-', 1))
        self.assertEqual(parseTimeString('=h'), ('=', 3600))
        self.assertEqual(parseTimeString('=m'), ('=', 60))
        self.assertEqual(parseTimeString('=s'), ('=', 1))
