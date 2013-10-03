import re
import unittest

from spyd.permissions.group import Group

functionality_name = 'test.can.faceplant'
functionality_pattern = re.compile("^test\.can\..*$")

class TestGroup(unittest.TestCase):
    def setUp(self):
        pass

    def test_direct_allows(self):
        group = Group('test.my_group', (), Ellipsis, (functionality_pattern,), ())
        self.assertTrue(group.allowed(functionality_name))

    def test_direct_denies(self):
        group = Group('test.my_group', (), Ellipsis, (), (functionality_pattern,))
        self.assertFalse(group.allowed(functionality_name))
        
    def test_unknown_functionality(self):
        group = Group('test.my_group', (), Ellipsis, (), ())
        self.assertIsNone(group.allowed(functionality_name))

    def test_deny_overrules_allow(self):
        group = Group('test.my_group', (), Ellipsis, (functionality_pattern,), (functionality_pattern,))
        self.assertFalse(group.allowed(functionality_name))
        
    def test_regex_functionality_allows(self):
        group = Group('test.my_group', (), Ellipsis, (functionality_pattern,), ())
        self.assertTrue(group.allowed(functionality_name))
        
    def test_regex_functionality_denies(self):
        group = Group('test.my_group', (), Ellipsis, (), (functionality_pattern,))
        self.assertFalse(group.allowed(functionality_name))

    def test_inheritance_child_allow_supercedes_parent_deny(self):
        parent_group = Group('test.parent_group', (), Ellipsis, (), (functionality_pattern,))
        child_group = Group('test.child_group', (parent_group,), Ellipsis, (functionality_pattern,), ())
        self.assertTrue(child_group.allowed(functionality_name))

    def test_inheritance_child_deny_supercedes_parent_allow(self):
        parent_group = Group('test.parent_group', (), Ellipsis, (functionality_pattern,), ())
        child_group = Group('test.child_group', (parent_group,), Ellipsis, (), (functionality_pattern,))
        self.assertFalse(child_group.allowed(functionality_name))

    def test_inheritance_child_defers_to_parent_allow(self):
        parent_group = Group('test.parent_group', (), Ellipsis, (functionality_pattern,), ())
        child_group = Group('test.child_group', (parent_group,), Ellipsis, (), ())
        self.assertTrue(child_group.allowed(functionality_name))

    def test_inheritance_child_defers_to_parent_deny(self):
        parent_group = Group('test.parent_group', (), Ellipsis, (), (functionality_pattern,))
        child_group = Group('test.child_group', (parent_group,), Ellipsis, (), ())
        self.assertFalse(child_group.allowed(functionality_name))
        
