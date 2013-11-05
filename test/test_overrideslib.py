# -*- coding: utf-8 -*-
from fixture import SubManFixture
from subscription_manager.overrides import OverrideLib, Override
from subscription_manager.injection import require, CP_PROVIDER


class OverrideTests(SubManFixture):

    def setUp(self):
        SubManFixture.setUp(self)
        self.cp = require(CP_PROVIDER).consumer_auth_cp
        self.override_lib = OverrideLib(self.cp)

    def test_add_function(self):
        repos = ['x', 'y']
        override_props = {'a': 'b', 'c': 'd'}
        overrides = [Override(repo, name, value) for repo in repos for name, value in override_props.items()]
        expected = [
            {'contentLabel': 'x', 'name': 'a', 'value': 'b'},
            {'contentLabel': 'x', 'name': 'c', 'value': 'd'},
            {'contentLabel': 'y', 'name': 'a', 'value': 'b'},
            {'contentLabel': 'y', 'name': 'c', 'value': 'd'},
        ]
        result = self.override_lib._add(overrides)
        self.assertTrue(self.assert_items_equals(expected, result))

    def test_remove_function(self):
        repos = ['x', 'y']
        props_to_remove = ['a', 'b']
        removes = [Override(repo, name) for repo in repos for name in props_to_remove]
        expected = [
            {'contentLabel': 'x', 'name': 'a'},
            {'contentLabel': 'x', 'name': 'b'},
            {'contentLabel': 'y', 'name': 'a'},
            {'contentLabel': 'y', 'name': 'b'},
        ]
        result = self.override_lib._remove(removes)
        self.assertTrue(self.assert_items_equals(expected, result))

    def test_remove_all(self):
        repos = ['x', 'y']
        expected = [
            {'contentLabel': 'x'},
            {'contentLabel': 'y'},
        ]
        result = self.override_lib._remove_all(repos)
        self.assertTrue(self.assert_items_equals(expected, result))

    def test_remove_all_with_no_repos_given(self):
        repos = []
        result = self.override_lib._remove_all(repos)
        self.assertEquals(None, result)
