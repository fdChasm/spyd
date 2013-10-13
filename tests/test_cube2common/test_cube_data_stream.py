import unittest

from cube2common.cube_data_stream import CubeDataStream


class TestCubeDataStreams(unittest.TestCase):

    def setUp(self):
        pass

    def test_bytes(self):
        cds = CubeDataStream("")
        for i in range(0, 256):
            cds.putbyte(i)
            self.assertEqual(cds.getbyte(), i)

    def test_integers(self):
        cds = CubeDataStream("")
        for i in range(-10000, 10000, 7):
            cds.putint(i)
            self.assertEqual(cds.getint(), i)

    def test_unsigned_integers(self):
        cds = CubeDataStream("")
        for i in range(0, 20000, 7):
            cds.putuint(i)
            self.assertEqual(cds.getuint(), i)

    def test_strings(self):
        cds = CubeDataStream("")
        animals = ["cat", "dog", "rabbit", "hamster", "frog"]

        order = []

        for animal in animals:
            cds.putstring(animal)
            order.append(animal)

        while len(order) > 0:
            animal = cds.getstring()
            self.assertEqual(animal, order.pop(0))

    def test_floats(self):
        cds = CubeDataStream("")

        # Not all floats will encode to IEEE 754 and back and be equal
        floats = [-355.3233947753906, 352332.09375, 323333.90625]

        order = []

        for f in map(float, floats):
            cds.putfloat(f)
            order.append(f)

        while len(order) > 0:
            f = cds.getfloat()
            self.assertEqual(f, order.pop(0))
