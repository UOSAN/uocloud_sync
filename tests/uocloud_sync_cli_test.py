import pytest
from argparse import ArgumentParser, Namespace, ArgumentError
from uocloud_sync.uocloud_sync_cli import SplitAction


class TestUOCloudSyncCli:
    def test_split_action_with_nargs(self):
        with pytest.raises(ValueError, match='nargs not allowed'):
            SplitAction(option_strings=['--src'], dest='src', nargs='3')

    def test_split_action_with_invalid_format(self):
        with pytest.raises(ArgumentError, match='not in the required format'):
            split_action = SplitAction(option_strings=['--src'], dest='src')
            split_action(ArgumentParser(), Namespace(), 'invalid format test string')

    def test_split_action_no_endpoint(self):
        with pytest.raises(ArgumentError, match='endpoint not specified'):
            split_action = SplitAction(option_strings=['--src'], dest='src')
            split_action(ArgumentParser(), Namespace(), ':path')

    def test_split_action_no_path(self):
        with pytest.raises(ArgumentError, match='path not specified'):
            split_action = SplitAction(option_strings=['--src'], dest='src')
            split_action(ArgumentParser(), Namespace(), 'endpoint:')

    def test_split_action(self):
        namespace = Namespace()
        split_action = SplitAction(option_strings=['--src'], dest='src')
        split_action(ArgumentParser(), namespace, 'endpoint:path')
        assert namespace.src_endpoint == 'endpoint'
        assert namespace.src_path == 'path'
