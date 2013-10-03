import unittest

from spyd.permissions.functionality import Functionality
from spyd.permissions.permission_resolver import PermissionResolver, GroupInheritanceCycle,\
    MissingInheritedGroup


test_permission_dictionary = {
    "local.admin": {
        "allows": ["*"],
        "priority": 10
    },
    "local.ban": {
        "denies": ["server.connect"]
    },
    "local.player": {
        "allows": ["server.connect", "server.chat", "server.play", "server.be_n00b"]
    },
    "local.master": {
        "inherits": ["local.player"],
        "denies": ["server.be_n00b"],
        "allows": ["server.setmap"],
        "priority": 5
    }
}

test_permission_dictionary_with_cycles = {
     "group1": {
         "inherits": ["group2"]
     },
     "group2": {
         "inherits": ["group1"]
     }
}

test_permission_dictionary_with_missing_group = {
     "group1": {
         "inherits": ["group2"]
     }
}


class TestPermissionResolver(unittest.TestCase):
    def setUp(self):
        self.permission_resolver = PermissionResolver.from_dictionary(test_permission_dictionary)

    def test_ban_denies_connect(self):
        server_connect_functionality = Functionality("server.connect")
        self.assertFalse(self.permission_resolver.groups_allow(["local.ban"], server_connect_functionality))

    def test_ban_allows_chat(self):
        server_chat_functionality = Functionality("server.chat")
        self.assertTrue(self.permission_resolver.groups_allow(["local.player", "local.ban"], server_chat_functionality))

    def test_master_overrides_ban_allows_connect(self):
        server_connect_functionality = Functionality("server.connect")
        self.assertTrue(self.permission_resolver.groups_allow(["local.player", "local.master", "local.ban"], server_connect_functionality))

    def test_master_overrides_player_denies_noobishness(self):
        be_a_noob_functionality = Functionality("server.be_n00b")
        self.assertTrue(self.permission_resolver.groups_allow(["local.player"], be_a_noob_functionality))
        self.assertFalse(self.permission_resolver.groups_allow(["local.player", "local.master"], be_a_noob_functionality))

    def test_admin_overrides_master_allows_noobishness(self):
        be_a_noob_functionality = Functionality("server.be_n00b")
        self.assertTrue(self.permission_resolver.groups_allow(["local.player", "local.master", "local.admin"], be_a_noob_functionality))

    def test_master_inherits_from_player(self):
        server_connect_functionality = Functionality("server.connect")
        self.assertTrue(self.permission_resolver.groups_allow(["local.master"], server_connect_functionality))

    def test_cycles_raise_exception(self):
        self.assertRaises(GroupInheritanceCycle, PermissionResolver.from_dictionary, test_permission_dictionary_with_cycles)

    def test_missing_group_raise_exception(self):
        self.assertRaises(MissingInheritedGroup, PermissionResolver.from_dictionary, test_permission_dictionary_with_missing_group)
