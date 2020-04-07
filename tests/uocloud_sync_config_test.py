from uocloud_sync.uocloud_sync_config import UOCloudSyncConfig, APP_NAME
from unittest import mock


class TestUOCloudSyncConfig:
    def test_missing_client_id(self):
        config = UOCloudSyncConfig()
        with mock.patch.dict(config._config, {APP_NAME: {'test_key': 'test_value'}}):
            assert config.get_client_id() == ''

    def test_missing_client_secret(self):
        config = UOCloudSyncConfig()
        with mock.patch.dict(config._config, {APP_NAME: {'test_key': 'test_value'}}):
            assert config.get_client_secret() == ''

    def test_missing_app_name_section(self):
        config = UOCloudSyncConfig()
        with mock.patch.dict(config._config, {'test_section': {'test_key': 'test_value'}}, clear=True):
            assert config.get_client_secret() == ''

    def test_client_id(self):
        config = UOCloudSyncConfig()
        with mock.patch.dict(config._config, {APP_NAME: {'client_id': 'test_value'}}):
            assert config.get_client_id() == 'test_value'

    def test_client_secret(self):
        config = UOCloudSyncConfig()
        with mock.patch.dict(config._config, {APP_NAME: {'client_secret': 'test_value'}}):
            assert config.get_client_secret() == 'test_value'
