import unittest

from spyd.game.server_message_formatter import clientnum_wrapper, \
    room_title_wrapper


class TestServerMessageFormatter(unittest.TestCase):
    def setUp(self):
        pass

    def test_clientnum_wrapper(self):
        self.assertEqual(clientnum_wrapper(5), "\fs\f5(5)\fr")

    def test_room_title_wrapper(self):
        self.assertEqual(room_title_wrapper('Room Name'), '\f1Room Name\f7')
