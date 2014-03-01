import unittest
from spyd.utils.constrain import constrain_range, ConstraintViolation


class TestConstrain(unittest.TestCase):
    def test_constrain_range_in_range_returns_none(self):
        for v in xrange(11):
            self.assertEqual(constrain_range(v, 0, 10, '0 to 10'), None)

    def test_constrain_range_less_than(self):
        self.assertRaises(ConstraintViolation, constrain_range, -1, 0, 10, '0 to 10')

    def test_constrain_range_greater_than(self):
        self.assertRaises(ConstraintViolation, constrain_range, 11, 0, 10, '0 to 10')
