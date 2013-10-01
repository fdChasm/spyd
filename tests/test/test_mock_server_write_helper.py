import unittest
from sauerpyd.protocol import swh
from testutils.protocol.mock_server_write_helper import mock_server_write_helper
import testutils.protocol.server_write_helper

class Test(unittest.TestCase):
    """Unit tests for ScheduledCallbackWrapper."""
    def setUp(self):
        pass
        
    def test_mocking(self):
        self.assertNotEqual(testutils.protocol.server_write_helper.put_servinfo, swh.put_servinfo)
        with mock_server_write_helper():
            self.assertEqual(testutils.protocol.server_write_helper.put_servinfo, swh.put_servinfo)
        self.assertNotEqual(testutils.protocol.server_write_helper.put_servinfo, swh.put_servinfo)
