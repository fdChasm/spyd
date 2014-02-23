import unittest

from mock import Mock
from spyd.authentication import auth_world_view_factory
from test_utils.mocking import constructorMock


class TestAuthWorldViewFactory(unittest.TestCase):
    def setUp(self):
        self.no_op_auth_service = Mock()
        auth_world_view_factory.NoOpMasterClientService = Mock(return_value=self.no_op_auth_service)
        auth_world_view_factory.AuthWorldView = constructorMock("AuthWorldView")
        self.awvf = auth_world_view_factory.AuthWorldViewFactory()

    def test_build_auth_world_view_no_registered_auth_services(self):
        self.awvf.build_auth_world_view(port=1234)
        Mock.assert_called_with(auth_world_view_factory.AuthWorldView, [self.no_op_auth_service])

    def test_build_auth_world_view_with_registered_general_auth_services(self):
        auth_service = Mock()
        self.awvf.register_auth_service(auth_service)
        self.awvf.build_auth_world_view(port=1234)
        Mock.assert_called_with(auth_world_view_factory.AuthWorldView, [auth_service, self.no_op_auth_service])

    def test_build_auth_world_view_with_registered_specific_auth_services(self):
        auth_service = Mock()
        self.awvf.register_auth_service(auth_service, 1234)
        self.awvf.build_auth_world_view(port=1234)
        Mock.assert_called_with(auth_world_view_factory.AuthWorldView, [auth_service, self.no_op_auth_service])
