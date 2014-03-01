import unittest
from spyd.utils.ping_buffer import PingBuffer


class Test(unittest.TestCase):
    def setUp(self):
        self.ping_buffer = PingBuffer()

    def test_add_one(self):
        self.ping_buffer.add(5)
        self.assertEqual(self.ping_buffer.pings, [5])

    def test_add_two(self):
        self.ping_buffer.add(1)
        self.ping_buffer.add(3)
        self.assertEqual(self.ping_buffer.pings, [1, 3])

    def test_add_gt_n(self):
        self.ping_buffer.BUFFERSIZE = 2
        self.ping_buffer.add(10)
        self.ping_buffer.add(1)
        self.ping_buffer.add(3)
        self.assertEqual(self.ping_buffer.pings, [1, 3])

    def test_avg_one(self):
        self.ping_buffer.add(5)
        self.assertEqual(self.ping_buffer.avg(), 5)

    def test_avg_two(self):
        self.ping_buffer.add(1)
        self.ping_buffer.add(3)
        self.assertEqual(self.ping_buffer.avg(), 2)

    def test_avg_last_n(self):
        self.ping_buffer.BUFFERSIZE = 2
        self.ping_buffer.add(10)
        self.ping_buffer.add(1)
        self.ping_buffer.add(3)
        self.assertEqual(self.ping_buffer.avg(), 2)
