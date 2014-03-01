import unittest

from spyd.utils.net import longToDottedQuad, dottedQuadToLong


class TestNet(unittest.TestCase):
    def test_long_dotted_quad_round_trip(self):
        cases = ['127.0.0.1', '255.255.255.0', '128.0.0.1', '168.192.1.1']
        for case in cases:
            self.assertEqual(longToDottedQuad(dottedQuadToLong(case)), case)
