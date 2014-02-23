import unittest
from spyd.authentication.master_client_service_factory import MasterClientServiceFactory
from spyd.authentication import master_client_service_factory
from mock import Mock
from spyd.config_loader import ConfigurationError


class TestMasterClientServiceFactory(unittest.TestCase):
    def setUp(self):
        self.punitive_model = Mock()
        self.RegistryManager = Mock()
        master_client_service_factory.RegistryManager = self.RegistryManager

    def test_construction(self):
        self.RegistryManager.get_registrations = Mock(return_value=[])
        MasterClientServiceFactory(self.punitive_model)
        self.RegistryManager.get_registrations.assert_called_once_with('master_client_service')

    def test_build_master_client_service_no_type_config_value(self):
        self.RegistryManager.get_registrations = Mock(return_value=[])
        mcsf = MasterClientServiceFactory(self.punitive_model)

        config = Mock()
        config.get = Mock(return_value=None)

        self.assertRaises(ConfigurationError, mcsf.build_master_client_service, config)

        config.get.called_once_with('type', None)

    def test_build_master_client_service_no_implementations(self):
        self.RegistryManager.get_registrations = Mock(return_value=[])
        mcsf = MasterClientServiceFactory(self.punitive_model)

        config = Mock()
        config.get = Mock(return_value='vanilla')

        self.assertRaises(ConfigurationError, mcsf.build_master_client_service, config)

        config.get.called_once_with('type', None)

    def test_build_master_client_service_matching_implementation(self):
        service_type_registration = Mock()
        service_type_registration.args = ['vanilla']

        master_client_service = Mock()

        vanilla_service_type = Mock()
        vanilla_service_type.build = Mock(return_value=master_client_service)
        
        service_type_registration.registered_object = vanilla_service_type

        self.RegistryManager.get_registrations = Mock(return_value=[service_type_registration])
        mcsf = MasterClientServiceFactory(self.punitive_model)

        config = Mock()
        config.get = Mock(return_value='vanilla')

        built_master_client_service = mcsf.build_master_client_service(config)

        config.get.assert_called_once_with('type', None)

        vanilla_service_type.build.assert_called_once_with(self.punitive_model, config)

        self.assertEqual(built_master_client_service, master_client_service)
