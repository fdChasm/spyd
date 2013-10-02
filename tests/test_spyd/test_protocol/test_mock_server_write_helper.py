import unittest
from spyd.protocol import swh
from testing_utils.protocol.mock_server_write_helper import mock_server_write_helper
from testing_utils.protocol import server_write_helper

class Test(unittest.TestCase):
    """Unit tests for ScheduledCallbackWrapper."""
    def setUp(self):
        pass
        
    def test_mocking(self):
        self.assertNotEqual(server_write_helper.put_servinfo, swh.put_servinfo)
        with mock_server_write_helper():
            self.assertEqual(server_write_helper.put_servinfo, swh.put_servinfo)
        self.assertNotEqual(server_write_helper.put_servinfo, swh.put_servinfo)
